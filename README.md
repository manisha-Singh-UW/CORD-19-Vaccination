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

