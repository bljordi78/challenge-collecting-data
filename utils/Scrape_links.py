import pandas as pd
from bs4 import BeautifulSoup
import re
import requests


def Scrape_properties(list):
    """
    Function that receives a list of ad urls and scrape the information for each property
    """
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

    # Create a dataframe to store the results, starting with the ad links
    df = pd.DataFrame(list, columns=["ad_link"])

    # Iterate through all the links 
    for i in range(len(df)):

        url = None
        try:
            url = df.loc[i, "ad_link"]
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, "lxml")     

            # First extracting isolated pieces
            title = soup.find('span', class_="detail__header_title_main")
            title = title.contents[0].strip() if title else ""

            ref = soup.find('span', class_="vlancode")
            ref = ref.text.strip() if ref else ""

            price = soup.find('span', class_="detail__header_price_data")    
            if price:
                price = price.text.strip() 
                price = re.sub(r"[^\d]", "", price)    
            else: ""    

            address_container = soup.find('div', class_='detail__header_address')
            address = ""
            zip = ""
            if address_container:
                inner_div = address_container.find('div', class_='d-lg-block d-none')
                if inner_div:
                    spans = inner_div.find_all('span')
                    address = spans[0].text.strip() if len(spans) > 0 else ""
                    zip = spans[1].text.strip() if len(spans) > 1 else ""
                else:
                    # No inner div, try to find single span with city-line class directly inside address_container
                    span = address_container.find('span', class_='city-line')
                    if span:
                        zip = span.text.strip()

            # Adding the data to the dataframe
            df.loc[i, "Ref"] = ref
            df.loc[i, "Titre"] = title
            df.loc[i, "Prix"] = price
            df.loc[i, "Addresse"] = address
            df.loc[i, "Localite"] = zip    
        
            # then all relevant information is in the class general-info w-100
            # iterating through all div, p, h4 to retrieve the fields
            # keeping the html labels as codes and retriving their values to add to the dataframe
            info_section = soup.find("div", class_="general-info w-100")
            if info_section:
                for data_row in info_section.find_all("div", class_="data-row-wrapper"):
                    for item in data_row.find_all("div"):
                        h4 = item.find("h4")
                        p = item.find("p")
                        if h4 and p:
                            label = h4.get_text(strip=True)
                            value = p.get_text(strip=True)
                            # shorten label or sanitize column name
                            label_clean = re.sub(r"[^\w\s]", "", label).strip().replace(" ", "_")
                            df.loc[i, label_clean] = value
        
        except Exception as e:
            print(f"Error at index {i} — {url if url else 'URL unknown'}\n→ {e}")

    return df