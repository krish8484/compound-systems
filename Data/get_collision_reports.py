import requests
import os
from datetime import datetime, timedelta

# Base URL
base_url = 'https://www.dmv.ca.gov/portal/file/'

# Companies to check
companies = ['weride', 'zoox', 'apple', 'ponyai', 'nuro', 'ghostautonomy', 'waymo', 'cruise']

# Date to start checking
year_ = 2018
month_ = 3
day_ = 1

# File to store downloads in
storage_folder_name = 'CA_DMV_AV_COLLISION_REPORTS'

# Create a folder to store the PDFs
os.makedirs(storage_folder_name, exist_ok=True)

# Function to download a PDF file
def download_pdf(pdf_url, folder):
    response = requests.get(pdf_url)
    pdf_name = pdf_url.split('/')[-2] + '.pdf'
    pdf_path = os.path.join(folder, pdf_name)
    with open(pdf_path, 'wb') as file:
        file.write(response.content)

def url_exists(url):
    try:
        # Make a HEAD request to check the existence of the URL
        response = requests.head(url, allow_redirects=True)
        return response.status_code == 200
    except requests.exceptions.RequestException as e:
        print(f"Error checking URL: {e}")
        return False

def generate_pdf_url(base_url, company, date_str):
    # Try the first URL pattern
    pdf_url_1 = f"{base_url}{company}_{date_str}-pdf/"
    if url_exists(pdf_url_1):
        return pdf_url_1

    # Try the second URL pattern
    pdf_url_2 = f"{base_url}{company}{date_str}-pdf/"
    if url_exists(pdf_url_2):
        return pdf_url_2

    # If both URLs fail, return None
    return None

# Generate all possible dates in the given year up to today
today = datetime.today()
start_date = datetime(year_, month_, day_)
dates = [start_date + timedelta(days=x) for x in range((today - start_date).days + 1)]

# Check and download each file
for company in companies:
    for date in dates:
        date_str = date.strftime('%m%d%Y')
        pdf_url = generate_pdf_url(base_url, company, date_str)
        # print(f"pdf_url:{pdf_url}")
        if pdf_url:
            download_pdf(pdf_url, storage_folder_name)
            print(f"Downloaded {pdf_url}")
        else:
            # print(f"No valid URL found for {company} on {date_str}. Moving to next.")
            next

print("Download process completed.")
