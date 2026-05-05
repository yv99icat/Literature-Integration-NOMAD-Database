from operator import index
from traceback import print_tb
from pandas.io.sas.sas_constants import dataset_length
from tools import open_json, save_json
import re
from collections import Counter





data = open_json("doi_list_meta_data.json")



all_title = []
all_abstract = []

for i in data:
    all_title.append(i["title"])
    all_abstract.append(i["abstract"])


all_abstract = [x for x in all_abstract if x is not None]

sum = all_title + all_abstract




# Function to clean the titles by removing the tags
def clean_text(text):
    # Remove HTML/XML-like tags
    clean_text = re.sub(r'<.*?>', '', text)
    return clean_text

# Apply cleaning function to all titles
cleaned_titles = [clean_text(title) for title in sum]


# Words to exclude from the count (stop words)
exclude_words = {'the', 'of', 'in', 'on', 'a', 'an', 'and', 'with', 'to', 'by', 'for', 'is', 'as','we',"that","are","this"}

# Function to count single words (unigrams) excluding stop words
def count_words(titles_list):
    word_list = []
    for title in titles_list:
        # Split title into words, remove punctuation, and convert to lowercase
        words = re.findall(r'\b\w+\b', title.lower())
        # Append words excluding the common stop words
        word_list.extend([word for word in words if word not in exclude_words])
    return Counter(word_list)


def count_bigrams(titles_list):
    bigram_list = []
    for title in titles_list:
        # Split title into words, remove punctuation, and convert to lowercase
        words = re.findall(r'\b\w+\b', title.lower())
        # Remove stop words
        filtered_words = [word for word in words if word not in exclude_words]
        # Create bigrams and join them as strings
        bigrams = [' '.join([filtered_words[i], filtered_words[i+1]]) for i in range(len(filtered_words)-1)]
        # Add to the bigram list
        bigram_list.extend(bigrams)
    return Counter(bigram_list)


def sort_dict_by_value(counter_dict):
    return dict(sorted(counter_dict.items(), key=lambda item: item[1], reverse=True))

# Get the frequency of words (unigrams)
frequency_dict = count_words(cleaned_titles)
bigram_frequency = count_bigrams(cleaned_titles)
# Display the results
print("Cleaned Titles: ", cleaned_titles)
print("Word frequency: ", sort_dict_by_value(frequency_dict))
print("bigram_frequency ", sort_dict_by_value(bigram_frequency))

save_json(sort_dict_by_value(frequency_dict),"single_word_frequency.json")
save_json(sort_dict_by_value(bigram_frequency),"bigram_word_frequency.json")