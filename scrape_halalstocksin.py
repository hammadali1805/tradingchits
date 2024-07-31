import pandas as pd
from bs4 import BeautifulSoup
import requests

# URL of the page to scrape
url = "https://halalstock.in/halal-shariah-compliant-shares-list/"

# Headers to mimic a regular browser request
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# Sending a request to fetch the HTML content
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.content, 'html.parser')

# print(soup)
# Extract table data
table = soup.find('table', {'id': 'tablepress-12'})
table_rows = table.find_all('tr')

# Extract column headers
headers = [th.text.strip() for th in table_rows[0].find_all('th')]

# Initialize empty list for data
data = []

# Iterate through rows skipping the header row
for row in table_rows[1:]:
    row_data = []
    for td in row.find_all('td'):
        if td.find('img'):
            row_data.append(td.find('img')['src'].split('-')[2][:-4])
        else:
            row_data.append(td.text.strip())
    data.append(row_data)

# Create DataFrame
df = pd.DataFrame(data, columns=headers)

df.to_csv('compliance_halalstock', index=False)
