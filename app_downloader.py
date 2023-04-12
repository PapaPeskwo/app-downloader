import os
import platform
import requests
from bs4 import BeautifulSoup
import zipfile
import json


def extract_zip(zip_file, output_path):
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall(output_path)


def download_file(url, output_file):
    response = requests.get(url, stream=True)
    with open(output_file, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)

def get_os():
    system = platform.system()
    if system == "Windows":
        return "windows"
    elif system == "Linux":
        return "linux"
    else:
        return None

def get_latest_terraform_url(os_name):
    api_url = "https://checkpoint-api.hashicorp.com/v1/check/terraform"
    response = requests.get(api_url)
    if response.status_code != 200:
        raise ValueError("Unable to fetch the latest Terraform version from Checkpoint API.")

    data = json.loads(response.content)
    latest_version = data.get("current_version")

    url = json.loads(response.content)
    current_download_url = url.get("current_download_url")

    if not latest_version:
        raise ValueError("Unable to find the latest Terraform version from Checkpoint API.")
    
    os_name = "windows" if os_name == "windows" else "linux"
    arch = "386" if os_name == "windows" else "amd64"
    download_url = current_download_url + f"/terraform_{latest_version}_{os_name}_{arch}.zip"

    return download_url

def download_file(url, output_file=None):
    response = requests.get(url, stream=True)
    if output_file is None:
        output_file = url.split("/")[-1]
    with open(output_file, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    return output_file

def download_apps(os_name):
    terraform_url = get_latest_terraform_url(os_name)
    print(f"Downloading terraform for {os_name}...")
    terraform_output = download_file(terraform_url)
    print(f"terraform downloaded successfully as {terraform_output}.")
    print("Extracting terraform...")
    extract_zip(terraform_output, ".")
    print("terraform extracted successfully.")



if __name__ == "__main__":
    os_name = get_os()
    if os_name:
        download_apps(os_name)
    else:
        print("This script does not support your operating system.")
