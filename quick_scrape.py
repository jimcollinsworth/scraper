''' quick scrape of a list of URLS

Used to validate,analyze a list of URLS for scraping. Loads a CSV or text file with URLS.
For each URLs, retrieve it, record size, info on robot or terms, classify the result type (csv, html, pdf...)
Show useful realtime status info while scraping.
Save summary of all urls at end in a CSV, save scraped results for each URL in a directory.
'''

import os
import asyncio
import multiprocessing
from concurrent.futures import ProcessPoolExecutor
from time import sleep, time

import httpx


async def scrape(urls):
    """this is our async scraper that scrapes"""
    results = []
    async with httpx.AsyncClient(timeout=httpx.Timeout(30.0)) as client:
        scrape_tasks = [client.get(url.strip()) for url in urls]
        for response_f in asyncio.as_completed(scrape_tasks):
            try:
                response = await response_f
                result = f"{response.url},{response.status_code},{len(response.text)}"
                print(result)
                results.append(result)
            except Exception as e:
                print(f"Error occurred while scraping: {e}")

    return results


def scrape_wrapper(args):
    i, urls = args
    print(f"subprocess {i} started")
    result = asyncio.run(scrape(urls))
    print(f"subprocess {i} ended")
    return result


def multi_process(urls):
    _start = time()

    batches = []
    batch_size = multiprocessing.cpu_count() - 1  # let's keep 1 core for ourselves
    print(f"scraping {len(urls)} urls through {batch_size} processes")
    for i in range(0, len(urls), batch_size):
        batches.append(urls[i : i + batch_size])
    with ProcessPoolExecutor() as executor:
        for result in executor.map(scrape_wrapper, enumerate(batches)):
            print(result)
        print("done")

    print(f"multi-process finished in {time() - _start:.2f}")

def single_process(urls):
    _start = time()
    results = asyncio.run(scrape(urls))
    print(f"single-process finished in {time() - _start:.2f}")


if __name__ == "__main__":
    file_name = input("Enter the path to the CSV file: ")
    while not os.path.exists(file_name):
        print("File does not exist. Please try again.")
        file_name = input("Enter the path to the CSV file: ")
    with open(file_name, "r") as file:
        urls = [line.strip() for line in file]
    multi_process(urls)
    # multi-process finished in 7.22
    single_process(urls)