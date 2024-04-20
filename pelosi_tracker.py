import requests
import zipfile
import os
import xml.etree.ElementTree as ET
import datetime

YEAR = datetime.datetime.now().year

# Step 1: Download the zip file
zip_url = f'https://disclosures-clerk.house.gov/public_disc/financial-pdfs/{YEAR}FD.zip'
zip_file_path = f'{YEAR}FD.zip'
with requests.get(zip_url) as response:
    with open(zip_file_path, 'wb') as file:
        file.write(response.content)

# Step 2: Unzip the file
with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
    zip_ref.extractall('.')

# Assuming the zip file is now extracted, we can proceed to parse the XML.
# Step 3: Parse the XML to find DocID for Nancy Pelosi
xml_file_path = f'{YEAR}FD.xml'
tree = ET.parse(xml_file_path)
root = tree.getroot()

# Initialize list to hold DocIDs
pelosi_doc_ids = []

# Iterate through each member and check for Nancy Pelosi
for member in root.findall('Member'):
    first_name = member.find('First').text
    last_name = member.find('Last').text
    if first_name == 'Nancy' and last_name == 'Pelosi':
        doc_id = member.find('DocID').text
        pelosi_doc_ids.append(doc_id)

# Step 4: Download the PDF file for Nancy Pelosi using the found DocID
directory = "reports"
if not os.path.exists(directory):
    os.makedirs(directory)

print(pelosi_doc_ids)
for doc_id in pelosi_doc_ids:
    pdf_url = f'https://disclosures-clerk.house.gov/public_disc/ptr-pdfs/{YEAR}/{doc_id}.pdf'
    pdf_file_path = os.path.join(directory, f'{doc_id}.pdf')

    with requests.get(pdf_url) as response:
        with open(pdf_file_path, 'wb') as file:
            file.write(response.content)
    print(f'Download completed: {pdf_file_path}')

if not pelosi_doc_ids:
    print('Nancy Pelosi\'s filing could not be found.')

# Step 5: Clean up by deleting the zip file and extracted files
os.remove(zip_file_path)  # Delete the zip file
os.remove(xml_file_path)  # Delete the XML file

txt_file_path = f'{YEAR}FD.txt'
if os.path.exists(txt_file_path):  # Check if the file exists before trying to delete it
    os.remove(txt_file_path)

print('Cleanup completed.')
