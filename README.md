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



