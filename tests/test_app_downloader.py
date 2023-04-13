import os
import pytest
from src.app_downloader import download_file, get_latest_terraform_url

def get_latest_terraform_url(os_name="windows"):
    os_name = "windows"
    terraform_url = get_latest_terraform_url(os_name)
    output_file = download_file(terraform_url)
    assert os.path.isfile(output_file)
    os.remove(output_file)

def test_download_docker():
    docker_url = "https://desktop.docker.com/win/main/amd64/Docker%20Desktop%20Installer.exe"
    output_file = download_file(docker_url)
    assert os.path.isfile(output_file)
    os.remove(output_file)
