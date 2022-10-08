# Word Cloud

## Links
[Download Executable](https://github.com/Bryan3838/text-cloud/releases/download/v1.0.0/Word.Cloud.exe)

[Releases](https://github.com/Bryan3838/text-cloud/releases/tag/v1.0.0)

## Prerequisites

- [Python 3.10.2+](https://www.python.org/downloads/release/python-370/)

## Setting up
Installing `pip`
```bash
python -m ensurepip --upgrade
```

Installing requirements.txt
```bash
pip install -r requirements.txt
```

Installing `pyinstaller`
```bash
pip install -U pyinstaller
```

### NOTE
Ensure that you have pytesseract installed. If installing through pip doesn't work, download pyinstaller through https://github.com/UB-Mannheim/tesseract/wiki.
After installing the .exe, add the filepath to your environment variables.

## Build .exe file
```bash
pyinstaller main.spec
```