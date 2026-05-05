import json
import csv
import re

# Function to clean the abstracts
def clean_text(text):
    cleaned_text = ' '.join(text.split())
    cleaned_text = re.sub(r'\s*([,.])\s*', r'\1 ', cleaned_text)
    cleaned_text = re.sub(r'<[^>]+>', '', cleaned_text)
    return cleaned_text

def clean_and_process_csv(json_file,csv_file):


    with open(json_file, 'r',encoding='utf-8') as json_file:
        data = json.load(json_file)


    output_csv = csv_file
    with open(output_csv, 'w',encoding="utf-8",newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['abstracts'])


        for entry in data:
            abstract = entry.get('abstract')
            if abstract:  # Check if abstract is not None or empty
                cleaned_abstract = clean_text(abstract)
                if cleaned_abstract.strip():  # Only write non-empty cleaned abstracts
                    writer.writerow([cleaned_abstract])

    print(f'Cleaned abstracts have been written to {output_csv}')
