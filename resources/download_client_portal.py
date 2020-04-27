import pathlib
import requests
import zipfile
import io

# Request the Client Portal
response = requests.get('https://download2.interactivebrokers.com/portal/clientportal.beta.gw.zip')

# Download the Zip File.
zip_file_content = zipfile.ZipFile(io.BytesIO(response.content))

# Define the download folder.
download_folder = pathlib.Path(__file__).parent.joinpath('clientportal.beta.gw').resolve()

# Extract the Content to the new folder.
zip_file_content.extractall(path="/clientportal.beta.gw")