import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent / "src"))

import os
import pytest
from src.downloaders import (
    download_file,
    get_latest_terraform_url,
    get_latest_balena_etcher_url,
    get_latest_prometheus_url,
    get_download_location,
    download_python,
)
from src.settings import (
    load_settings
)


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

def test_download_balena_etcher():
    balena_etcher_url = get_latest_balena_etcher_url()
    output_file = download_file(balena_etcher_url)
    assert os.path.isfile(output_file)
    os.remove(output_file)

def test_download_prometheus():
    prometheus_url = get_latest_prometheus_url()
    output_file = download_file(prometheus_url)
    assert os.path.isfile(output_file)
    os.remove(output_file)
