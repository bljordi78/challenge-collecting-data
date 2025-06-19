# Import libraries to run the project as long as functions created in the utils folder
import warnings
warnings.filterwarnings("ignore")
from utils.Get_links import Get_adlinks, Codes
from utils.Scrape_links import Scrape_properties
import pandas as pd
import time


def scrape_slice(codes, start, step):
    """
    Due to slow scraping, I created a function with the tasks to be done
    and I scrape in batches of 50 zip codes
    codes : a slice of 50 zip codes
    start/end : index of the 50 zip codes in the dataframe
    """
    
    end = min(start + step, len(codes))  # prevents index out of range as total number of zip codes is not multiple of 50
    codes_sliced = codes[start:end]

    print(f"\nScraping links from {start} to {end - 1}...")
    start_time = time.time()

    ad_links = Get_adlinks(codes_sliced)
    df = Scrape_properties(ad_links)

    end_time = time.time()
    print(f"Scraped {len(df)} ads in {end_time - start_time:.2f} seconds.")

    # Once I retrieve the data for 50 zip codes, I save it in a csv file
    file_name = f"output/immovlan_properties_{start}_{end}.csv"
    df.to_csv(file_name, index=False, encoding="utf-8-sig")
    print(f"Saved to {file_name}")


if __name__ == "__main__":
    
    codes = Codes()

    # # First run
    # for start in range(0, 50, 10):
    #     scrape_slice(codes, start, step=10)

    # # Second run
    # for start in range(50, 100, 10):
    #     scrape_slice(codes, start, step=10)

    # # Third run
    # for start in range(100, 150, 10):
    #     scrape_slice(codes, start, step=10)

    # # Fourth run
    # for start in range(150, 200, 10):
    #     scrape_slice(codes, start, step=10)

    # # Fifth run
    # for start in range(200, 250, 10):
    #     scrape_slice(codes, start, step=10)

    # Sixth run
    # for start in range(250, 300, 10):
    #     scrape_slice(codes, start, step=10)

    # # Seventh run
    # for start in range(300, 350, 10):
    #     scrape_slice(codes, start, step=10)

    # # Eighth run
    # for start in range(350, 400, 10):
    #     scrape_slice(codes, start, step=10)

    # # Ninth run
    # for start in range(400, 450, 10):
    #     scrape_slice(codes, start, step=10)

    # # Tenth run
    # for start in range(450, 500, 10):
    #     scrape_slice(codes, start, step=10)

    # # Eleventh run
    # for start in range(500, 550, 10):
    #     scrape_slice(codes, start, step=10)

    # # Twelfth run
    # for start in range(550, 600, 10):
    #     scrape_slice(codes, start, step=10)

    # # Thirteenth run
    # for start in range(600, 650, 10):
    #     scrape_slice(codes, start, step=10)

    # # Fourteenth run
    # for start in range(650, 700, 10):
    #     scrape_slice(codes, start, step=10)

    # # Fifteenth run
    # for start in range(700, 750, 10):
    #     scrape_slice(codes, start, step=10)

    # # Sixteenth run
    # for start in range(750, 800, 10):
    #     scrape_slice(codes, start, step=10)