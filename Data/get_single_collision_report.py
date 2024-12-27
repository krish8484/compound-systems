import requests

# URL of the file to download
file_url = 'https://www.dmv.ca.gov/portal/file/weride_06102024-pdf/'

# Function to download the file
def download_file(url, filename):
    response = requests.get(url)
    with open(filename, 'wb') as file:
        file.write(response.content)

# Specify the filename to save the file
filename = 'weride_06102024.pdf'

# Download the file
download_file(file_url, filename)

print(f"Downloaded {filename}")

