from traceback import print_tb
import re
import requests
import json
import arxiv
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry




def save_json(file, file_name=None): # Remove duplicates
    with open(file_name, 'w',encoding='utf-8') as f:
        json.dump(file, f,ensure_ascii=False)
    return file

def open_json(file):
    with open(file) as f:
        d = json.load(f)
        return d




# Create a session and configure retries
session = requests.Session()
retry = Retry(
    total=5,  # Total number of retries
    read=3,  # Retry on read errors
    connect=3,
    backoff_factor=0.5,
    status_forcelist=[429, 500, 502, 503, 504]
)
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
session.mount('https://', adapter)

def fetch_abstract(doi):
    api_url = f'https://api.crossref.org/works/{doi}'
    try:
        response = session.get(api_url, timeout=10)  # Use session for the request and set a timeout
        print(f"Request to this URL: {api_url}")

        if response.status_code == 200:
            data = response.json()

            # Clean the title
            title = re.sub(r'<sub>(.*?)</sub>|<jats:[^>]+>(.*?)</jats:[^>]+>', r'\1\2', data['message']['title'][0])

            # Check for abstract
            if 'abstract' in data['message']:
                extracted_texts = re.findall(
                    r'<jats:p xml:lang="en">(.*?)</jats:p>|<jats:p>(.*?)</jats:p>|<p>(.*?)</p>|<jats:*>(.*?)</jats:*>|<sub>(.*?)</sub>',
                    data['message']['abstract'],
                    re.DOTALL
                )

                # Flatten and clean the abstract
                flattened_texts = [text for match in extracted_texts for text in match if text]
                abstract = re.sub(r'<sub>(.*?)</sub>|<jats:[^>]+>(.*?)</jats:[^>]+>', r'\1\2', flattened_texts[0])
                return {"doi": doi, "title": title, "abstract": abstract}

            # No abstract found
            return {"doi": doi, "title": title, "abstract": None}

        # Request failed
        return {"doi": doi, "error": f"HTTP error: {response.status_code}"}

    except requests.exceptions.RequestException as e:
        return {"doi": doi, "error": f"Request failed: {str(e)}"}


def extract_domain_name(url):
    if url.startswith('http://'):
        url = url[7:]
    elif url.startswith('https://'):
        url = url[8:]


    if url.startswith('www.'):
        url = url[4:]


    domain_parts = url.split('.')


    return domain_parts[0] if domain_parts else None


def get_doi_by_title(title):

    formatted_title = title.replace(" ", "+")


    url = f"https://api.crossref.org/works?query.bibliographic={formatted_title}"

    try:

        response = requests.get(url)
        response.raise_for_status()


        data = response.json()


        if data['message']['items']:
            # Extract DOI from the first item
            doi = data['message']['items'][0].get('DOI', 'DOI not found')
            return doi
        else:
            return "No DOI found for the given title."

    except requests.exceptions.RequestException as e:
        return f"An error occurred: {e}"



def post_data(url,data):


    headers = {"Content-Type": "application/json"}

    json_data = json.dumps(data)

    response = requests.post(url, data=json_data, headers=headers).json()

    return response