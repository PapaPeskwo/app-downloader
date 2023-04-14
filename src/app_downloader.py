import os
import platform
import requests
import zipfile
import json
from tqdm import tqdm
from bs4 import BeautifulSoup
import json
import sys
from urllib.parse import urlparse

SETTINGS_FILE = 'settings.json'

def load_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, 'r') as f:
            return json.load(f)
    else:
        return {}

def save_settings(settings):
    with open(SETTINGS_FILE, 'w') as f:
        json.dump(settings, f, indent=2)

def set_standard_download_location():
    settings = load_settings()
    print("Current standard download location:", settings.get('standard_download_location', 'Not set'))
    new_location = input("Enter the new standard download location (or leave blank to cancel):\n").strip()
    if new_location:
        if os.path.exists(new_location) and os.path.isdir(new_location):
            settings['standard_download_location'] = new_location
            save_settings(settings)
            print("Standard download location has been updated.")
        else:
            print("Invalid directory. Please enter a valid directory.")

def get_download_location():
    settings = load_settings()
    return settings.get('standard_download_location', '')

def extract_zip(zip_file, output_path):
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall(output_path)

def download_file(url):
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    
    filename = url.split("/")[-1]
    output_file = os.path.join(get_download_location(), filename)

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

python_versions = {
    "3.7": "https://www.python.org/ftp/python/3.7.12/python-3.7.12-amd64.exe",
    "3.8": "https://www.python.org/ftp/python/3.8.13/python-3.8.13-amd64.exe",
    "3.9": "https://www.python.org/ftp/python/3.9.10/python-3.9.10-amd64.exe",
    "3.10": "https://www.python.org/ftp/python/3.10.7/python-3.10.7-amd64.exe",
    "3.11": "https://www.python.org/ftp/python/3.11.3/python-3.11.3-amd64.exe",
}

def download_python():
    from packaging import version

    base_url = "https://www.python.org"
    version_list_url = "https://www.python.org/downloads/windows/"
    response = requests.get(version_list_url)
    soup = BeautifulSoup(response.content, "html.parser")

    python_versions = {}
    for link in soup.find_all("a"):
        url = link.get("href", "")
        if "/ftp/python/" in url and "amd64.exe" in url:
            version_str = urlparse(url).path.split("/")[-2]
            major_minor_version = ".".join(version_str.split(".")[:2])
            if version.parse(major_minor_version) >= version.parse("3.7"):
                python_versions[major_minor_version] = url

    sorted_versions = sorted(python_versions.keys(), key=lambda ver: version.parse(ver), reverse=True)

    print("Available Python versions:")
    for ver in sorted_versions:
        print(ver)

    selected_version = input("Enter the Python version you want to download: ")
    if selected_version in python_versions:
        url = python_versions[selected_version]
        file_name = f"python-{selected_version}-amd64.exe"
        output_file = os.path.join(get_download_location(), file_name)
        print(f"Downloading {file_name}...")
        download_file(url)
        print(f"Downloaded {file_name} successfully.")
        return output_file
    else:
        print("Invalid Python version selected.")
        return None




def download_apps(app_list):
    apps = {
        "terraform": get_latest_terraform_url(),
        "docker": "https://desktop.docker.com/win/main/amd64/Docker%20Desktop%20Installer.exe",
        "balena_etcher": get_latest_balena_etcher_url(),
        "prometheus": get_latest_prometheus_url(),
        "python": None,  
    }

    for app_name in app_list:
        url = apps.get(app_name)
        if url:
            output_file = download_file(url)
            print(f"{app_name} downloaded successfully as {output_file}.")
        elif app_name == "python":  
            download_python()
        else:
            print(f"{app_name} is not available for download.")



def list_available_downloads():
    print("List of available downloads:")
    print("1. Terraform")
    print("2. Docker")
    print("3. Balena Etcher")
    print("4. Prometheus")
    print("5. Python")

def main_menu():
    print("\n" + "=" * 30)
    print("Main Menu:")
    print("=" * 30)
    print("1. List all available downloads")
    print("2. Download applications")
    print("3. Settings")
    print("4. Exit")
    choice = int(input("\nChoose an option (1-4): "))
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
        "4": "prometheus",
        "5": "python"
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

def settings_menu():
    print("\n" + "=" * 30)
    print("Settings Menu:")
    print("=" * 30)
    print("1. Set standard download location")
    print("2. Go back to the main menu")
    choice = int(input("\nChoose an option (1-2): "))

    if choice == 1:
        set_standard_download_location()
    elif choice == 2:
        return
    else:
        print("Invalid choice. Please try again.")


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
                    settings_menu()
            elif choice == 4:
                print("Exiting...")
                break
            else:
                print("Invalid choice. Please try again.")
    else:
        print("This script does not support your operating system.")
