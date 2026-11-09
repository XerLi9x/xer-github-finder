# Xer GitHub Finder

A simple Python application for searching GitHub repositories through the GitHub Search API.

## Features

- Search repositories by keywords
- Filter repositories by programming language
- Set a minimum number of stars
- Sort results by stars or last update
- Display repository information and GitHub links
- Terminal interface with Rich
- Local web dashboard powered by Flask

## Requirements

- Python 3.10+
- pip

## Installation

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/xer-github-finder.git
cd xer-github-finder
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it:

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Terminal Interface

```bash
python main.py --cli
```

### Web Dashboard

```bash
python main.py --web
```

Then open your browser:

```text
http://127.0.0.1:5000
```

## Technologies

- Python
- Requests
- Flask
- Rich
- GitHub REST API

## Notes

GitHub API rate limits apply to unauthenticated requests.

## Project Status

Under development.

## License

MIT License
