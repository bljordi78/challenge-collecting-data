# COLLECTING DATA CHALLENGE

## Becode project to build a scraper to retrieve data from properties on sale by Immovlan
## Author: Jordi Batlle


## Disclaimer
Due to the lengthy process of setting a list of all properties advertising URLs, the project is divided in 2 parts:
- The scraping part (includes main.py, get_links.py, scrape_links.py)
- A notebook where I clean up the scraping output (cleanData.ipynb)


## The Mission
As you know the real estate company "ImmoEliza" wants to create a Machine Learning model to make price predictions on real estate sales in Belgium.
In that mission your first task is to build a dataset gathering information about at least 10.000 properties all over Belgium. This dataset will be used later as a training set for your prediction model.

### Features
- Data all over Belgium.
- Minimum 10 000 inputs without duplicates
- No empty row. If you are missing information, set the value to `None`.
- The dataset must be clean. Try as much as possible to record only numerical values.

### Guidelines:
This project follows the guidelines from [immo_eliza]( https://github.com/becodeorg/BXL-Bouman-9/blob/main/projects/02-TheHill/immo_eliza/1.immo_eliza_scraping.md).


## Usage
Type on Git Bash or other terminal:

git clone git@github.com:bljordi78/challenge-collecting-data.git

cd challenge-collecting-data

python main.py

Then go through the notebook cleadData.ipynb


## Project challenges
Due to difficulty to access Immoweb, the project uses Immovlan website
First challenge was that when doing a search-all query, the website did not allow to go beyond page 50 (about 2000 results):
-	I downloaded from internet a csv file with all Belgian zip codes
-	Then I had to launch a search for each of these zip codes
Second challenge was to determinate the number of pages for each single search by zip code
-	On the first page of each single search, I read the total number of results
-	Then dividing by 20 (number of results per page) I could determinate the number of pages to iterate through
Other challenges would probably remain on strictly finding the way to retrieve the information on each page, ie. performing webscraping.
Final challenge, my code was very slow at retrieving the data, because I needed to query each zip code but even though there was likely a quicker option.
As there are 2762 zip codes in Belgiun, I am scraping the data in batches of 50 zip codes.
On the deadline day, starting the batches at 9h and until 15h when I am wrapping up, the code could only retrieve data for 600 zip codes.
Then I used a notebook to clean up the data scraped:
-	Remove duplicates
-	Drop all NAs on the price variable as this will be the target variable
-	Drop variables with more than 50% NAs
-	Split some information into 2 variables
-	Recode Oui/Non variables to 0/1
Finally, save the data frame to CSV. Ending up with:
-	16686Records
-	27 variables (although some are not predictive)

