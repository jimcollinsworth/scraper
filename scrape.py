import cProfile
from bs4 import BeautifulSoup
import pandas as pd

cProfile.run('main()', 'app.profile')
 
# install snakeviz package
# generate report by calling "snakeviz app.profile"

def extract_urls_from_bookmarks(file_path):
    """
    Extracts all URLs from Chrome's exported bookmarks HTML file.
    
    Args:
    - file_path (str): path to the exported bookmarks file
    
    Returns:
    - list of URLs
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file.read(), 'html.parser')
    # Find all anchor tags and extract href values
    urls = [a['href'] for a in soup.find_all('a')]
    return urls

def save_urls_to_csv(urls, csv_path='urls.csv'):
    """
    Saves a list of URLs to a CSV file.
    
    Args:
    - urls (list): list of URLs
    - csv_path (str): path to save the CSV file
    """
    df = pd.DataFrame(urls, columns=['URLs'])
    df.to_csv(csv_path, index=False)

if __name__ == '__main__':
    bookmarks_file_path = input("Enter the path to the bookmarks HTML file: ")
    urls = extract_urls_from_bookmarks(bookmarks_file_path)
    
    output_csv_path = input("Enter the path to save the CSV file (or press enter for 'urls.csv'): ")
    if not output_csv_path:
        output_csv_path = 'urls.csv'
    
    save_urls_to_csv(urls, output_csv_path)
    print(f"URLs saved to {output_csv_path}")
