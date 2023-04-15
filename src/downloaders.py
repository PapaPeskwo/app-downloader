import os
import requests
import zipfile
import json
from tqdm import tqdm
from bs4 import BeautifulSoup
import json
import sys
from urllib.parse import urlparse

from settings import load_settings, get_download_location

APPS = ["terraform", "docker", "balena_etcher", "prometheus", "python", "java", "notepad_plus_plus"]

def list_available_downloads():
    print("\nAvailable downloads:")
    for index, app_name in enumerate(APPS, start=1):
        print(f"{index}. {app_name}")

def extract_zip(zip_file, output_path):
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall(output_path)

def show_progress(current, total, file_path):
    progress = (current / total) * 100
    progress_str = "{:.1f}%".format(progress)
    bar_width = 10
    filled_bars = int(progress / (100 / bar_width))
    empty_bars = bar_width - filled_bars
    bar = f"{filled_bars * '|'}{empty_bars * ' '}"

    sys.stdout.write(f"{file_path}: {progress_str}|{bar}|\r")
    sys.stdout.flush()

    if current == total:
        print("\n")



def download_file(url):
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))

    filename = url.split("/")[-1]
    output_file = os.path.join(get_download_location(), filename)

    try:
        with open(output_file, 'wb') as f:
            current_size = 0
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
                current_size += len(chunk)
                show_progress(current_size, total_size, output_file)
    except KeyboardInterrupt:
        print("\nDownload interrupted. Cleaning up the partially downloaded file.")
        f.close()
        os.remove(output_file)
        sys.exit(1)
    return output_file

def download_apps(app_list):
    apps = {
        "terraform": get_latest_terraform_url(),
        "docker": "https://desktop.docker.com/win/main/amd64/Docker%20Desktop%20Installer.exe",
        "balena_etcher": get_latest_balena_etcher_url(),
        "prometheus": get_latest_prometheus_url(),
        "python": None,
        "java": None,
        "notepad_plus_plus": get_latest_notepad_plus_plus_url(),
    }

    for app_name in app_list:
        url = apps.get(app_name)
        if url:
            output_file = download_file(url)
            print(f"\n{app_name} downloaded successfully as {output_file}\n")
        elif app_name == "python":
            download_python()
        elif app_name == "java":
            download_java()
        else:
            print(f"{app_name} is not available for download.")


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
        "5": "python",
        "6": "java",
        "7": "notepad_plus_plus",
    }


    app_list = [app_map.get(app) for app in selected_apps]
    download_apps(app_list)

def download_all_apps_menu():
    list_available_downloads()
    confirm = input("Do you want to download all apps? [y/N]: ")
    if confirm.lower() == 'y':
        app_list = APPS[:-1]  # Exclude "python" from the list of apps
        download_apps(app_list)
        download_python()
    else:
        print("Cancelled download all apps.")


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

def download_python(selected_version=None):
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

    if not selected_version:
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


def download_java(selected_version=None):
    java_versions = {
        "20": "https://download.oracle.com/java/20/latest/jdk-20_windows-x64_bin.exe",
        "17": "https://download.oracle.com/java/17/latest/jdk-17_windows-x64_bin.exe",
    }

    if not selected_version:
        print("Available Java LTS versions:")
        for version in java_versions:
            print(f"Java {version}")

        selected_version = input("Enter the Java LTS version you want to download (17 or 20): ")

    if selected_version in java_versions:
        url = java_versions[selected_version]
        file_name = f"jdk-{selected_version}_windows-x64_bin.exe"
        output_file = os.path.join(get_download_location(), file_name)
        print(f"Downloading {file_name}...")
        download_file(url)
        print(f"Downloaded {file_name} successfully.")
        return output_file
    else:
        print("Invalid Java LTS version selected.")
        return None


def get_latest_notepad_plus_plus_url():
    api_url = "https://api.github.com/repos/notepad-plus-plus/notepad-plus-plus/releases/latest"
    response = requests.get(api_url)
    if response.status_code != 200:
        raise ValueError("Unable to fetch the latest Notepad++ version from GitHub API.")

    data = json.loads(response.content)
    assets = data.get("assets")
    if not assets:
        raise ValueError("Unable to find the latest Notepad++ release from GitHub API.")

    for asset in assets:
        if asset["name"].startswith("npp") and asset["name"].endswith("Installer.x64.exe"):
            return asset["browser_download_url"]

    raise ValueError("Unable to find the latest Notepad++ download URL for Windows.")