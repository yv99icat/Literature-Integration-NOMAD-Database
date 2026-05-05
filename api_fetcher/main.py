from tools import open_json, save_json,extract_domain_name
import re
from tools import fetch_abstract
from scrapper import find_doi
from api_call import fetch_solar_cell_references
from cleaning_data import clean_and_process_csv

fetch_solar_cell_references()

references_list= open_json("doi_solar_cell.json")

#remove duplicate
cleaned_links = list(dict.fromkeys(references_list))


doi_pattern = r'10\.\d{4,9}/[-._;()/:A-Z0-9]+'


doi_list = [re.search(doi_pattern, url, re.IGNORECASE).group(0) for url in cleaned_links if re.search(doi_pattern, url, re.IGNORECASE)]



doi_list_meta_data = []

for doi in doi_list:
    try:
        result = fetch_abstract(doi)
        if 'error' not in result:  # Check if the result contains an error
            doi_list_meta_data.append(result)  # Add successful results to metadata list
        else:
            print(f"Failed to fetch data for DOI: {doi} - {result['error']}")
    except Exception as e:
        print(f"An error occurred for DOI: {doi} - {str(e)}")  # Catch any unexpected errors
    finally:
        print(f"DOI: {doi}")
        print(f"Result: {result}\n")


print("len meta data ",len(doi_list_meta_data))

save_json(doi_list_meta_data,"doi_list_meta_data.json")

clean_and_process_csv("doi_list_meta_data.json","cleaned_abstracts.csv")