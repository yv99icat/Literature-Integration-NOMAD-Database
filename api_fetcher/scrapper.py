from traceback import print_tb

from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from tools import extract_domain_name,get_doi_by_title
import re


firefox_options = Options()
firefox_options.add_argument("--headless")
driver = webdriver.Firefox(options=firefox_options)

def find_doi(url):
    domain = extract_domain_name(url)
    driver.get(url)
    doi_url = ""
    if domain == "nature":
        span_elements = driver.find_elements(By.CSS_SELECTOR, 'span.c-bibliographic-information__value')
        doi_url = span_elements[-1].text
    elif domain == "sciencedirect":
        a_tag = driver.find_element(By.CSS_SELECTOR, 'a.anchor.doi.anchor-primary')
        doi_url = a_tag.get_attribute("href")
    elif domain == "arxiv":
        title_element = driver.find_element(By.CSS_SELECTOR, 'h1.title.mathjax')
        title_text = title_element.text
        doi_url = get_doi_by_title(title_text)
    elif domain == "scitation":
        doi_element = driver.find_element(By.CSS_SELECTOR, 'div.citation-doi a')
        doi_url = doi_element.get_attribute("href")

    else:
        raise TypeError("Sorry, Not Supported link")
    return doi_url




