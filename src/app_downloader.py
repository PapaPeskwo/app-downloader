import os
import platform
import requests
import zipfile
import json
from tqdm import tqdm
from bs4 import BeautifulSoup


def extract_zip(zip_file, output_path):
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall(output_path)

def download_file(url, output_file=None):
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    
    if output_file is None:
        output_file = url.split("/")[-1]

    with open(output_file, 'wb') as f:
        for chunk in tqdm(response.iter_content(chunk_size=8192), total=total_size // 8192, unit='KB', desc=output_file):
            f.write(chunk)
    return output_file

def get_latest_terraform_url():
    api_url = "https://checkpoint-api.hashicorp.com/v1/check/terraform"
    response = requests.get(api_url)
    if response.status_code != 200:
        raise ValueError("Unable to fetch the latest Terraform version from Checkpoint API.")

    data = json.loads(response.content)
    latest_version = data.get("current_version")

    if not latest_version:
        raise ValueError("Unable to find the latest Terraform version from Checkpoint API.")
    
    download_url = f"https://releases.hashicorp.com/terraform/{latest_version}/terraform_{latest_version}_windows_amd64.zip"

    return download_url

def get_latest_balena_etcher_url():
    api_url = "https://api.github.com/repos/balena-io/etcher/releases/latest"
    response = requests.get(api_url)
    if response.status_code != 200:
        raise ValueError("Unable to fetch the latest Balena Etcher version from GitHub API.")

    data = json.loads(response.content)
    assets = data.get("assets")
    if not assets:
        raise ValueError("Unable to find the latest Balena Etcher release from GitHub API.")

    for asset in assets:
        if asset["name"].startswith("balenaEtcher-Setup-") and asset["name"].endswith(".exe"):
            return asset["browser_download_url"]

    raise ValueError("Unable to find the latest Balena Etcher download URL for Windows.")

def get_latest_prometheus_url():
    api_url = "https://api.github.com/repos/prometheus/prometheus/releases/latest"
    response = requests.get(api_url)
    if response.status_code != 200:
        raise ValueError("Unable to fetch the latest Prometheus version from GitHub API.")

    data = json.loads(response.content)
    assets = data.get("assets")
    if not assets:
        raise ValueError("Unable to find the latest Prometheus release from GitHub API.")

    for asset in assets:
        if asset["name"].startswith("prometheus") and asset["name"].endswith("windows-amd64.zip"):
            return asset["browser_download_url"]

    raise ValueError("Unable to find the latest Prometheus download URL for Windows.")


def download_apps(app_list):
    apps = {
        "terraform": get_latest_terraform_url(),
        "docker": "https://desktop.docker.com/win/main/amd64/Docker%20Desktop%20Installer.exe",
        "balena_etcher": get_latest_balena_etcher_url(),
        "prometheus": get_latest_prometheus_url()
    }

    for app_name in app_list:
        url = apps.get(app_name)
        if url:
            output_file = download_file(url)
            print(f"{app_name} downloaded successfully as {output_file}.")
        else:
            print(f"{app_name} is not available for download.")


def list_available_downloads():
    print("List of available downloads:")
    print("1. Terraform")
    print("2. Docker")
    print("3. Balena Etcher")
    print("4. Prometheus")

def main_menu():
    print("\n" + "=" * 30)
    print("Main Menu:")
    print("=" * 30)
    print("1. List all available downloads")
    print("2. Download applications")
    print("3. Exit")
    choice = int(input("\nChoose an option (1-3): "))
    return choice

def download_menu():
    print("\n" + "=" * 30)
    print("Download Menu:")
    print("=" * 30)
    print("1. Download apps")
    print("2. Download all apps")
    choice = int(input("\nChoose an option (1-2): "))
    return choice

def download_apps_menu():
    list_available_downloads()
    print("Enter the numbers of the apps you want to download, separated by commas:")
    selected_apps = input().split(',')
    selected_apps = [app.strip() for app in selected_apps]
    
    app_map = {
        "1": "terraform",
        "2": "docker",
        "3": "balena_etcher",
        "4": "prometheus"
    }

    app_list = [app_map.get(app) for app in selected_apps]
    download_apps(app_list)

def download_all_apps_menu():
    list_available_downloads()
    confirm = input("Do you want to download all apps? [y/N]: ")
    if confirm.lower() == 'y':
        app_list = ["terraform", "docker", "balena etcher"]
        download_apps(app_list)
    else:
        print("Cancelled download all apps.")

if __name__ == "__main__":
    os_name = platform.system()
    if os_name == "Windows":
        while True:
            choice = main_menu()
            if choice == 1:
                list_available_downloads()
            elif choice == 2:
                download_choice = download_menu()
                if download_choice == 1:
                    download_apps_menu()
                elif download_choice == 2:
                    download_all_apps_menu()
                else:
                    print("Invalid choice. Please try again.")
            elif choice == 3:
                print("Exiting...")
                break
            else:
                print("Invalid choice. Please try again.")
    else:
        print("This script does not support your operating system.")
