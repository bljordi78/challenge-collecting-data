import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
import math
from concurrent.futures import ThreadPoolExecutor

def Codes():
    """
    Function to create a dataframe with all Belgian zip codes
    """

    codes = pd.read_csv("utils/code-postaux-belge.csv",sep=";")
    codes = codes[['Code', 'Localite']]
    codes['Localite'] = codes['Localite'].str.replace(' ', '-', regex=False).str.replace("'", "", regex=False)
    
    codes['Key'] = codes['Code'].astype(str) + '-' + codes['Localite']
    
    rootURL = 'https://immovlan.be/fr/immobilier?transactiontypes=a-vendre&propertytypes=maison,appartement&towns='

    codes['rootURL'] = codes['Key'].apply(lambda x: rootURL + x + '&page=')
    
    return codes


def Ads(rootURL):
    """
    Function to retrieve all properties adverts URLs
    It takes the root url including the zip and page number 1
    Open that page and calculates the total number of pages for that particular zip
    Then loop through all pages to retrieve the URLs for each advert
    """

    links = []
    headers = {
        'User-Agent': (
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) '
            'Gecko/20100101 Firefox/115.0'
        ),
        'Accept': (
            'text/html,application/xhtml+xml,application/xml;q=0.9,'
            'image/avif,image/webp,*/*;q=0.8'
        ),
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'TE': 'trailers',
    }
        
    try:
        # First page to find the total pages
        url = rootURL['rootURL'] + '1'
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "lxml")

        total_pages = 1
        pages = soup.find('div', class_='col-12 mb-2')
        if pages:
            text = pages.text.strip()
            text = re.search(r'^\d+', text)
            if text:
                total_results = int(text.group())
                total_pages = math.ceil(total_results / 20) # as there are 20 results per page

        # Loop through all pages
        for p in range(1, total_pages + 1):
            url = rootURL['rootURL'] + str(p)
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, "lxml")

            # only interested in links that include '/detail/'
            for a in soup.find_all('a', href=True):
                if '/detail/' in a['href']:       
                    if a['href'] not in links:
                        links.append(a['href'])

    except Exception as e:
        print(f"Error on {rootURL['Key']}: {e}")

    return list(links)


def Get_adlinks(codes_sliced):
    """
    Multi thread function to speed up the process of retrieving all urls
    """
    with ThreadPoolExecutor(max_workers=8) as executor:
        results = list(executor.map(Ads, [row for i, row in codes_sliced.iterrows()]))

    # flatten all sublists into one list links
    adlinks = [link for sublist in results for link in sublist]
    
    return adlinks
