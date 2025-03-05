# 🕸️ Scroopy-Luu Web Scraper 🔍

## Overview
Scroopy-Luu is a powerful web scraping application built with Streamlit that allows users to scrape content from websites, with support for single page and multi-page (sub-links) scraping.

## Features
- 🌐 Scrape individual web pages
- 🔗 Extract content from sub-links
- 💾 Multiple output formats:
  - JSON
  - Pickle
  - CSV
- �log Real-time logging and error tracking
- 🖥️ User-friendly Streamlit interface

## Prerequisites
- Python 3.8+
- Required libraries:
  - streamlit
  - requests
  - beautifulsoup4
  - pandas

## Installation
1. Clone the repository:
```bash
git clone https://github.com/yourusername/scroopy-luu.git
cd scroopy-luu
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage
Run the Streamlit app:
```bash
streamlit run app.py
```

### Scraping Workflow
1. Enter URL(s) in the interface
2. Optional: Check "Sub-links" to scrape linked pages
3. Click "Start Scraping"
4. Download scraped content in various formats

## Files
- `app.py`: Main Streamlit application
- `scr_prp.py`: Core scraping functions
  - `clean_title()`: Sanitizes filenames
  - `scrape_page_content()`: Extracts text from a single page
  - `scrape_page_and_subpages_content()`: Recursively scrapes main and sub-pages

## Customization
Modify `scr_prp.py` to:
- Change scraping logic
- Add more content extraction methods
- Customize text cleaning

## Limitations
- Respects website's `robots.txt` manually
- Limited to text content extraction
- Potential issues with dynamically loaded content

## Contributing
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License
MIT

## Disclaimer
Ensure you have permission to scrape websites. Respect websites' terms of service and legal guidelines.
