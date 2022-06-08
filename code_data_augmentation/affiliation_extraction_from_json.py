import logging
from pathlib import Path
import json
from typing import Dict


class Conf:
    # all are class attributes, please update base on your local environment
    pdf_json_path = r'D:\dataset\cord19\document_parses\pdf_json'


def get_aff(pdf_json_text: str) -> Dict:
    '''
    Input: string, 
        for example: 'document_parses/pdf_json/1cee4a0d0e823379ec34a462a04561bf4cd736a2.json'
        for example: 'document_parses/pdf_json/30dbeba55ccec8e99f2154ed35dc28d2d2f39c76.json; document_parses/pdf_json/7563f3897d50bf1fa4ae5df16d91c3c1fa58e474.json'
    Output: Dict
        aff_dict['aff_lab_inst']: <string>
        aff_dict['aff_location']: <string>
        aff_dict['aff_country']: <string>

    '''

    aff_dict = {}
    aff_dict['aff_lab_inst'] = ''
    aff_dict['aff_location'] = ''
    aff_dict['aff_country'] = ''

    alab_set = set()
    aloc_set = set()
    acountry_set = set()

    for pdf_json_str in pdf_json_text.split(sep=';'):  # because there can be multiple semicolon-separated pdfs
        try:
            json_filepath = Conf.pdf_json_path + pdf_json_str.strip().replace(r'document_parses/pdf_json/', '\\')
            json_path_obj = Path(json_filepath)
            if json_path_obj.exists():
                # logging.info(f'Processing: {json_filepath}')
                full_file_dict = json.loads(json_path_obj.read_text(encoding='utf-8'))
                authors = full_file_dict['metadata']['authors']
                # logging.info(f'author len: {len(authors)}')

                for auth in authors:
                    if 'affiliation' in auth:
                        aff = auth['affiliation']
                        if 'laboratory' in aff:
                            if aff['laboratory']:  # only if string is not empty
                                alab_set.add(aff['laboratory'])
                        if 'institution' in aff:
                            if aff['institution']:
                                alab_set.add(aff['institution'])
                        if 'location' in aff:
                            # process all location info
                            loc_dict = aff['location']
                            if 'country' in loc_dict:
                                if loc_dict['country']:
                                    acountry_set.add(loc_dict['country'])
                            loc_strings = [f'{k}={v}' for k, v in loc_dict.items() if (k != 'country' and v != '')]
                            for loc_strings_item in loc_strings:
                                aloc_set.add(loc_strings_item)
            else:
                logging.error(f'Missing json file: {json_filepath}; {pdf_json_str}')

        except Exception as e:
            logging.error(f'{str(e)}')
    # end for

    if len(alab_set) > 0:
        aff_dict['aff_lab_inst'] = '; '.join(sorted(alab_set))
    else:
        aff_dict['aff_lab_inst'] = '_null_'

    if len(acountry_set) > 0:
        aff_dict['aff_country'] = '; '.join(sorted(acountry_set))

    if len(aloc_set) > 0:
        aff_dict['aff_location'] = '; '.join(sorted(aloc_set))

    # escape " symbol for Updating into database
    if '"' in aff_dict['aff_lab_inst']:
        aff_dict['aff_lab_inst'] = aff_dict['aff_lab_inst'].replace('"', '""')
    if '"' in aff_dict['aff_country']:
        aff_dict['aff_country'] = aff_dict['aff_country'].replace('"', '""')
    if '"' in aff_dict['aff_location']:
        aff_dict['aff_location'] = aff_dict['aff_location'].replace('"', '""')

    # logging.info(f'Lab:{alab_set}, Country:{acountry_set}, Loc:{aloc_set}')
    # logging.info(f'aff_dict: {aff_dict}')

    return aff_dict


if __name__ == '__main__':
    input_str = 'document_parses/pdf_json/ffea7ba3e851069566953f62c666856312ef5e10.json'

    print(get_aff(input_str))
    # {'aff_lab_inst': 'University of Maryland School of Medicine', 'aff_location': 'postCode=21201; region=MD; settlement=Baltimore', 'aff_country': 'USA'}
