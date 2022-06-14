# CORD-19-Vaccination Dataset
CORD-19-Vaccination dataset

## Download the dataset

Multiple methods are available to access the dataset. 

A) Instructions to download the file:
1. Download the dataset from the GitHub repo
2. Extract to the desired folder

B) Python code to access the dataset
Please use the following Python code to download and extract the dataset.

```Python
# Download the CORD-19-Vaccination dataset and unzip
# Tested on Python 3.9

import requests # if not already installed, please install using 'pip install requests'
import zipfile

url = 'https://github.com/manisha-Singh-UW/CORD-19-Vaccination/raw/main/dataset/cord_19_vaccination_metadata.zip'

# download the file to the local folder
req = requests.get(url)

if req.status_code != 200:
    print(f'[error]HTTP error: {req.url} "Status Code:" {req.status_code}')
else:
    # split URL to get the filename
    filename = url.split('/')[-1]

    # Writing the file to the local file system
    with open(filename,'wb') as fp:
        fp.write(req.content)

    print(f'File {filename} successfully downloaded to local folder')

    with zipfile.ZipFile(filename, 'r') as zip_f:
        zip_f.extractall('.')

    print(f'File {filename} successfully unzipped to local folder')

```

## Example Usage / Reading the Dataset

The following code loads the dataset into a Pandas DataFrame.

```python
# import the pandas library
import pandas as pd

dataset_path = 'cord_19_vaccination_metadata.csv'

dataset_df = pd.read_csv(dataset_path, encoding='utf-8')

print(dataset_df.head())

print(dataset_df.info())
```

## Internal organization of the dataset and data constituents

The dataset consist of the metadata.csv which consists of the fields below. Most of the columns directly come from the CORD-19 dataset, and have the same column description as mentioned in the data statement of CORD-19. The rows in marked 'CORD-19' were  extracted from CORD-19. The rows marked 'Data Augmentation' are from the CORD-19-Vaccination dataset added as part of the data augmentation. 


 
| Column Id  | Column description  | data type  | Data Source | Example values |
| --- | --- | --- | --- | --- |
| cord_uid  |  A str-valued field that assigns a unique identifier to each <sub>CORD-19</sub> paper. This is not necessarily unique per row, which is explained in the FAQs  | `string`  | <sub>CORD-19</sub> | d1pd09zj  |
| sha  | A List[str]-valued field that is the SHA1 of all PDFs associated with the <sub>CORD-19</sub> paper. Most papers will have either zero or one value here (since either have a PDF or we don't), but some papers will have multiple. For example, the main paper might have supplemental information saved in a separate PDF. Or might have two separate PDF copies of the same paper. If multiple PDFs exist, their SHA1 will be semicolon-separated (e.g. '4eb6e165ee705e2ae2 a24ed2d4e67da42831ff4a; d4f0247db5e916c20eae 3f6d772e8572eb828236')  | `string`  | <sub>CORD-19</sub> | 1cee4a0d0e823379ec 34a462a04561bf4cd736a2  |
| source_x  | A List[str]-valued field that is the names of sources from which we received this paper. Also semicolon-separated. For example, 'ArXiv; Elsevier; PMC; WHO'. There should always be at least one source listed  | `string`  | <sub>CORD-19</sub> | PMC  |
| title  | A str-valued field for the paper title  | `string`  | <sub>CORD-19</sub> | Synthetic carbohydrate-based vaccines: challenges and opportunities  |
| doi  | A str-valued field for the paper DOI  | `string`  | <sub>CORD-19</sub> | 10.1186/s12929-019-0591-0  |
| pmcid  | A str-valued field for the paper's ID on PubMed Central. Should begin with PMC followed by an `integer`.  | `string`  | <sub>CORD-19</sub> | PMC6941340  |
| pubmed_id  | An int-valued field for the paper's ID on PubMed.  | `integer`  | <sub>CORD-19</sub> | 31900143  |
| license  | A str-valued field with the most permissive license we've found associated with this paper. Possible values include: 'cc0', 'hybrid-oa', 'els-covid', 'no-cc', 'cc-by-nc-sa', 'cc-by', 'gold-oa', 'biorxiv', 'green-oa', 'bronze-oa', 'cc-by-nc', 'medrxiv', 'cc-by-nd', 'arxiv', 'unk', 'cc-by-sa', 'cc-by-nc-nd'  | `string`  | <sub>CORD-19</sub> | cc-by  |
| abstract  | A str-valued field for the paper's abstract  | `string`  | <sub>CORD-19</sub> | Glycoconjugate vaccines based on bacterial capsular polysaccharides (CPS) have been extremely successful in preventing bacterial infections. The glycan antigens for the preparation of CPS based glycoconjugate vaccines are mainly obtained from bacterial fermentation, the quality and length of glycans are always inconsistent. Such kind of situation make the CMC of glycoconjugate vaccines are difficult to well control. Thanks to the advantage of synthetic methods for carbohydrates syntheses. The well controlled glycan antigens are more easily to obtain, and them are conjugated to carrier protein to from the so-call homogeneous fully synthetic glycoconjugate vaccines. Several fully glycoconjugate vaccines are in different phases of clinical trial for bacteria or cancers. The review will introduce the recent development of fully synthetic glycoconjugate vaccine.  |
| publish_time  | A str-valued field for the published date of the paper. This is in yyyy-mm-dd format. Not always accurate as some publishers will denote unknown dates with future dates like yyyy-12-31  | `string`  | <sub>CORD-19</sub> | 1/3/2020  |
| authors  | A List[str]-valued field for the authors of the paper. Each author name is in Last, First Middle format and semicolon-separated.  | `string`  | <sub>CORD-19</sub> | Mettu, Ravinder; Chen, Chiang-Yun; Wu, Chung-Yi  |
| journal  | A str-valued field for the paper journal. `string`s are not normalized (e.g. BMJ and British Medical Journal can both exist). Empty `string` if unknown.  | `string`  | <sub>CORD-19</sub> | J Biomed Sci  |
| mag_id  | Deprecated, but originally an int-valued field for the paper as represented in the Microsoft Academic Graph.  | `integer`  | <sub>CORD-19</sub> | |
| who_covidence_id  | A str-valued field for the ID assigned by the WHO for this paper. Format looks like #72306.  | `string`  | <sub>CORD-19</sub> | |
| arxiv_id  | A str-valued field for the arXiv ID of this paper.  | `string`  | <sub>CORD-19</sub> | |
| pdf_json_files  | A List[str]-valued field containing paths from the root of the current data dump version to the parses of the paper PDFs into JSON format. Multiple paths are semicolon-separated. Example: document_parses/pdf_json/ 4eb6e165ee705e2ae2a2 4ed2d4e67da42831ff4a.json; document_parses/pdf_json/ d4f0247db5e916c20eae3 f6d772e8572eb828236.json  | `string`  | <sub>CORD-19</sub> | document_parses/pdf_json/ 1cee4a0d0e823379ec3 4a462a04561bf4cd736a2.json  |
| pmc_json_files  | A List[str]-valued field. Same as above, but corresponding to the full text XML files downloaded from PMC, parsed into the same JSON format as above  | `string`  | <sub>CORD-19</sub> | document_parses/pmc_json/PMC6941340.xml.json  |
| url  | A List[str]-valued field containing all URLs associated with this paper. Semicolon-separated.  | `string`  | <sub>CORD-19</sub> | https://www.ncbi.nlm.nih.gov /pmc/articles/PMC6941340/  |
| s2_id  | A str-valued field containing the Semantic Scholar ID for this paper. Can be used with the Semantic Scholar API (e.g. s2_id=9445722 corresponds to http://api.semanticscholar.org /corpusid:9445722  | `string`  | <sub>CORD-19</sub> | |
| lang_id  | Language identifier: The language id for which the fastText model’s confidence is highest becomes the language id for that paper.  | `string`  | <sub>Data Augmentation</sub> | en  |
| lang_id_confidence  | Language id confidence: This is score assigned to the language id by the fastText model.  | `string`   | <sub>Data Augmentation</sub> | 0.9167  |
| lang_id_predictions  | Language id predictions: This column gives the top three scores given by the fastText model.   | `string`  | <sub>Data Augmentation</sub> | en=0.9167, id=0.0055, fr=0.0043  |
| aff_lab_inst  | Affiliation Lab/Institution: This field gives the first author’s Lab/Institution for each paper.  | `string`  | <sub>Data Augmentation</sub> | University of Maryland School of Medicine  |
| Aff_location   | Affiliation location: The location of the lab/institution.   | `string`  | <sub>Data Augmentation</sub> | postCode=21201; region=MD; settlement=Baltimore  |
| Aff_country  | Affiliation country:  The country of the lab/institution.   | `string`  | <sub>Data Augmentation</sub> | USA  |
| Keywords  | Keywords: Extracted from the ‘Title’, ‘Abstract’ and body of the text using Yake. The list contains the top 20 keywords.   | `string`  | <sub>Data Augmentation</sub> | DNA vaccine; archaeosome; DNA; recombinant DNA vaccine; pDNA - surface localized archaeosome ; archaeosome vaccines group; cells; DNA vaccine candidate; localized archaeosome; vaccine; archaeosome vaccines; groups; plasmid DNA; gene DNA vaccine; PBS control groups; recombinant gene; pDNA-encapsulated archaeosomes; gene; mice; control groups  |
| Labelled_abstract  | Labeled Abstract: The Abstract is passed through sequential sentence classification and the result is every sentence of the abstract is labelled with one of the following labels: ‘Background, Objective, Method, Result, Conclusion ’  | `string`  | <sub>Data Augmentation</sub> | BACKGROUND: Glycoconjugate vaccines based on bacterial capsular polysaccharides (CPS) have been extremely successful in preventing bacterial infections. BACKGROUND: The glycan antigens for the preparation of CPS based glycoconjugate vaccines are mainly obtained from bacterial fermentation, the quality and length of glycans are always inconsistent. BACKGROUND: Such kind of situation make the CMC of glycoconjugate vaccines are difficult to well control. CONCLUSIONS: Thanks to the advantage of synthetic methods for carbohydrates syntheses. |
| topic  | Topic: Label for the inferred topic of the paper. The label corresponds to the topic which had the highest probability among the predicted topic distribution.   | `string`  | <sub>Data Augmentation</sub> | Vaccine development; Vaccination side-effects / Treatments  |
| topic_index  | Topic Index: Index associated with the inferred topic for the paper, can take values between 0 and 4.   | `integer`  | <sub>Data Augmentation</sub> | 0; 1; 2; 3; 4  |
| topic_prob  | Topic Probability: Probability of the given paper corresponding to the assigned topic label.   | `float`  | <sub>Data Augmentation</sub> | 0.524614  |
| std_first _auth_country  | Standardized First Author Country: Name of the country affiliated with the first author of the paper, standardized to match the Geopandas ‘'naturalearth_lowres'’ country names.   | `string`  | <sub>Data Augmentation</sub> | Taiwan; United States of America  |



## Metadata

Total number of entries: 29286 entries

Total number of columns: 32

Column Details:

| #  | Column_Name            | Non-Null Values Count | Data_type |
|----|------------------------|-----------------------|-----------|
| 0  | index                  | 29286 non-null        | int64     |
| 1  | cord_uid               | 29286 non-null        | object    |
| 2  | sha                    | 28749 non-null        | object    |
| 3  | source_x               | 29286 non-null        | object    |
| 4  | title                  | 29286 non-null        | object    |
| 5  | doi                    | 28675 non-null        | object    |
| 6  | pmcid                  | 24256 non-null        | object    |
| 7  | pubmed_id              | 23148 non-null        | float64   |
| 8  | license                | 29286 non-null        | object    |
| 9  | abstract               | 29286 non-null        | object    |
| 10 | publish_time           | 29286 non-null        | object    |
| 11 | authors                | 29237 non-null        | object    |
| 12 | journal                | 25696 non-null        | object    |
| 13 | mag_id                 | 0 non-null            | float64   |
| 14 | who_covidence_id       | 0 non-null            | float64   |
| 15 | arxiv_id               | 667 non-null          | float64   |
| 16 | pdf_json_files         | 28749 non-null        | object    |
| 17 | pmc_json_files         | 21942 non-null        | object    |
| 18 | url                    | 29286 non-null        | object    |
| 19 | s2_id                  | 27511 non-null        | float64   |
| 20 | lang_id                | 29286 non-null        | object    |
| 21 | lang_id_confidence     | 29286 non-null        | float64   |
| 22 | lang_id_predictions    | 29286 non-null        | object    |
| 23 | aff_lab_inst           | 28749 non-null        | object    |
| 24 | aff_location           | 19465 non-null        | object    |
| 25 | aff_country            | 18525 non-null        | object    |
| 26 | keywords               | 29286 non-null        | object    |
| 27 | labeled_abstract       | 29286 non-null        | object    |
| 28 | topic                  | 29286 non-null        | object    |
| 29 | topic_index            | 29286 non-null        | int64     |
| 30 | topic_prob             | 29286 non-null        | float64   |
| 31 | std_first_auth_country | 27303 non-null        | object    |

