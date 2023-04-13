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

## Getting Started

To get started with this project, you can clone the source code from the repository and install the dependencies by running the following command in your terminal:

```bash
pip install -r requirements.txt
```
After installing the dependencies, you can run the script by executing the following command in your terminal:

```bash
python src/app_downloader.py
```
The script will automatically detect your operating system and download the latest version of Terraform from the official website.
Note

At the moment, this project only has one app, Terraform, but there are plans to expand it to include more apps in the future.

## Contributing

Contributions are welcome. If you would like to contribute to this project, please fork the repository and submit a pull request.
