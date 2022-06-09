import logging
import yake  # https://github.com/LIAAD/yake
import json
from pathlib import Path
from typing import Tuple


class Conf:
    # all are class attributes, please update based on your local environment
    pdf_json_path = r'D:\dataset\cord19\document_parses\pdf_json'


def get_body_text(pdf_json_text: str) -> str:
    '''
    Parse and return the body text of pdf_json file
    Input:
        string, for example: 'document_parses/pdf_json/ffea7ba3e851069566953f62c666856312ef5e10.json'
    Output:
        string, the body text of the paper
    '''
    ret_body_text = ''

    if pdf_json_text == 'None':
        return ''

    body_text_str_list = []
    stopwords = ['Fig.', 'figure', 'Figure', 'Supplementary Fig.', 'Supplementary Table', 'Additional', 'Additional file', 'file']
    for pdf_json_str in pdf_json_text.split(sep=';'):  # because there can be multiple semicolon-separated pdfs
        try:
            json_filepath = Conf.pdf_json_path + pdf_json_str.strip().replace(r'document_parses/pdf_json/', '\\')
            json_path_obj = Path(json_filepath)
            if json_path_obj.exists():
                logging.info(f'Processing: {json_filepath}')
                full_file_dict = json.loads(json_path_obj.read_text(encoding='utf-8'))
                body_text_list = full_file_dict['body_text']
                logging.info(f'body_text len: {len(body_text_list)}')

                for body_text_item in body_text_list:
                    body_text_str = ''
                    if 'text' in body_text_item:
                        body_text_str = str(body_text_item['text'])

                        # additional cleanup of the text
                        if 'cite_spans' in body_text_item:
                            for cite_spans_dict in body_text_item['cite_spans'][::-1]:
                                if 'start' in cite_spans_dict and 'end' in cite_spans_dict:
                                    body_text_str = body_text_str[:cite_spans_dict['start']] + body_text_str[cite_spans_dict['end']:]

                        for s in stopwords:
                            body_text_str = body_text_str.replace(s, '')

                        body_text_str_list.append(body_text_str)
            else:
                logging.error(f'Missing json file: {json_filepath}; {pdf_json_str}')

        except Exception as e:
            logging.error(f'{str(e)}')
    # end for

    ret_body_text = '. '.join(body_text_str_list)
    # logging.info(f'Found body text length: {len(ret_body_text):,} characters')

    return ret_body_text


def get_keywords_yake(extraction_text: str, lang_id: str = 'en') -> str:
    '''
    Use the yake library to process a block of text and return a string of keywords
    '''
    ret_keywords_str = ''

    # max_ngram_size = 3
    # deduplication_thresold = 0.9
    # deduplication_algo = 'seqm'
    # windowSize = 1
    num_of_keywords = 20
    keyw_obj = None

    kw_extractor = yake.KeywordExtractor(lan=lang_id, top=num_of_keywords)
    keyw_obj = kw_extractor.extract_keywords(extraction_text)

    if keyw_obj:
        ret_keywords_str = '; '.join([k for k, v in keyw_obj])

    logging.info(f'Ext_text: {extraction_text}')
    logging.info(f'Keywords: {ret_keywords_str}')

    return ret_keywords_str


def get_keywords_for_full_text(index, title_text, abstract_text, lang_id, pdf_json_text) -> Tuple:
    logging.info(f'{index}, {title_text}, {abstract_text}, {lang_id}, {pdf_json_text}')
    body_text = get_body_text(pdf_json_text)
    text_for_keyword_extraction = title_text + ". " + abstract_text + ". " + body_text
    keywords_str = get_keywords_yake(text_for_keyword_extraction, lang_id)
    return index, keywords_str


if __name__ == '__main__':
    row_iter = 1  # index in the database
    title_text = 'Oral typhoid vaccine Ty21a elicits antigen-specific resident memory CD4(+) T cells in the human terminal ileum lamina propria and epithelial compartments'
    abstract_text = '''
        BACKGROUND: Salmonella enterica serovar Typhi (S. Typhi) is a highly invasive bacterium that infects the human intestinal mucosa and causes ~ 11.9–20.6 million infections and ~ 130,000–223,000 deaths annually worldwide. Oral typhoid vaccine Ty21a confers a moderate level of long-lived protection (5–7 years) in the field. New and improved vaccines against enteric pathogens are needed but their development is hindered by a lack of the immunological correlates of protection especially at the site of infection. Tissue resident memory T (T(RM)) cells provide immediate adaptive effector immune responsiveness at the infection site. However, the mechanism(s) by which S. Typhi induces T(RM) in the intestinal mucosa are unknown. Here, we focus on the induction of S. Typhi-specific CD4+T(RM) subsets by Ty21a in the human terminal ileum lamina propria and epithelial compartments. METHODS: Terminal ileum biopsies were obtained from consenting volunteers undergoing routine colonoscopy who were either immunized orally with 4 doses of Ty21a or not. Isolated lamina propria mononuclear cells (LPMC) and intraepithelial lymphocytes (IEL) CD4+T(RM) immune responses were determined using either S. Typhi-infected or non-infected autologous EBV-B cell lines as stimulator cells. T-CMI was assessed by the production of 4 cytokines [interferon (IFN)γ, interleukin (IL)-2, IL-17A and tumor necrosis factor (TNF)α] in 36 volunteers (18 vaccinees and 18 controls volunteers). RESULTS: Although the frequencies of LPMC CD103+ CD4+T(RM) were significant decreased, both CD103+ and CD103− CD4+T(RM) subsets spontaneously produced significantly higher levels of cytokines (IFNγ and IL-17A) following Ty21a-immunization. Importantly, we observed significant increases in S. Typhi-specific LPMC CD103+ CD4+T(RM) (IFNγ and IL-17A) and CD103− CD4+T(RM) (IL-2 and IL-17A) responses following Ty21a-immunization. Further, differences in S. Typhi-specific responses between these two CD4+T(RM) subsets were observed following multifunctional analysis. In addition, we determined the effect of Ty21a-immunization on IEL and observed significant changes in the frequencies of IEL CD103+ (decrease) and CD103− CD4+T(RM) (increase) following immunization. Finally, we observed that IEL CD103− CD4+T(RM), but not CD103+ CD4+T(RM), produced increased cytokines (IFNγ, TNFα and IL-17A) to S. Typhi-specific stimulation following Ty21a-immunization. CONCLUSIONS: Oral Ty21a-immunization elicits distinct compartment specific immune responses in CD4+T(RM) (CD103+ and CD103−) subsets. This study provides novel insights in the generation of local vaccine-specific responses. Trial registration This study was approved by the Institutional Review Board and registered on ClinicalTrials.gov (identifier NCT03970304, Registered 29 May 2019—Retrospectively registered, http://www.ClinicalTrials.gov/NCT03970304)
    '''
    lang_id = 'en'
    pdf_json_text = 'document_parses/pdf_json/ffea7ba3e851069566953f62c666856312ef5e10.json'

    keywords = get_keywords_for_full_text(row_iter, title_text, abstract_text, lang_id, pdf_json_text)

    print(f'Keywords: {keywords}')
    # Keywords: (1, 'IEL; LPMC; responses; LPMC and IEL; cells; subsets; Typhi; volunteers; unvaccinated volunteers; Oral; significantly; higher levels; observed; unvaccinated; LPMC versus IEL; stimulation; higher; significant; significantly higher levels; Typhi-specific')
