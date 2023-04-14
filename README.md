![CI/CD Pipeline](https://github.com/PapaPeskwo/app-downloader/actions/workflows/ci-cd.yml/badge.svg)


# App Downloader

This project is a Python script that can download and install Terraform on Windows and Linux machines.


## Prerequisites

- Python 3.x installed
- requests==2.26.0
- beautifulsoup4==4.10.0
- lxml==4.6.3
- tqdm==4.65.0
- pytest==7.2.0
- pytest-cov==4.0.0
- pytest-django==4.5.2
- bs4==0.0.1


## Supported apps 
- Terraform
- Docker
- Balena Etcher
- Prometheus

## Getting Started

To get started with this project, you can clone the source code from the repository and install the dependencies by running the following command in your terminal:

```bash
pip install -r requirements.txt
```
After installing the dependencies, you can run the script by executing the following command in your terminal:

```bash
python src/app_downloader.py
```
The script will present a menu with options to list and download supported applications. It automatically detects your operating system and downloads the latest version of the selected apps from their official sources.


## Contributing

Contributions are welcome. If you would like to contribute to this project, please fork the repository and submit a pull request.
