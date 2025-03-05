import streamlit as st
import json
import os
import time
import pickle
from scr_prp import scrape_page_and_subpages_content, clean_title, scrape_page_content
import pandas as pd

# Set up logging in the UI
if 'logs' not in st.session_state:
    st.session_state.logs = []

def add_log(message):
    """Add a log message to the session state and print to console as well"""
    timestamp = time.strftime("%H:%M:%S")
    log_entry = f"[{timestamp}] {message}"
    st.session_state.logs.append(log_entry)
    print(message)  # Keep console logging too

def convert_to_formats(page_content, url):
    """Convert scraped content to different formats"""
    # Prepare base data
    
    # Directories for different formats
    directories = ['JSONs', 'Pickles', 'XMLs', 'CSVs']
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            add_log(f"Created directory: {directory}")
    
    # Generate cleaned title for filenames
    cleaned_title = clean_title(url)
    file_paths = []

    # JSON
    json_filename = f"{cleaned_title}.json"
    json_path = os.path.join("JSONs", json_filename)
    with open(json_path, "w", encoding="utf-8") as json_file:
        json.dump(page_content, json_file, ensure_ascii=False, indent=4)
    file_paths.append(json_path)

    # Pickle
    pickle_filename = f"{cleaned_title}.pkl"
    pickle_path = os.path.join("Pickles", pickle_filename)
    with open(pickle_path, "wb") as pickle_file:
        pickle.dump(page_content, pickle_file)
    file_paths.append(pickle_path)

    # CSV (for list of dictionaries)
    df = pd.DataFrame(index=pd.Series(page_content.keys(), name='Link'), data=page_content.values())
    
    csv_filename = f"{cleaned_title}.csv"
    csv_path = os.path.join("CSVs", csv_filename)
    
    df.to_csv(csv_path)
    file_paths.append(csv_path)

    return file_paths

def scrape(urls, sub_contents_bools):
    file_paths = []
    errors = []

    for url, scb in zip(urls, sub_contents_bools):
        
        url = url.strip()

        add_log(f"Starting to process: {url}")
        
        # Scrape the content of the page
        try:
            add_log(f"Scraping content from: {url}")
            if scb:
                page_content, num_links = scrape_page_and_subpages_content(url)
                add_log(f"Processed {num_links} links from {url}")
            else:
                page_content = scrape_page_content(url)
                add_log(f"Processed {url}")
        except Exception as e:
            error_message = f'Error getting page content/s from {url}: {e}'
            add_log(error_message)
            errors.append(error_message)
            page_content = False
            
        if page_content:
            try:
                # Convert to multiple formats
                if scb:
                    format_paths = convert_to_formats(page_content, url)
                    file_paths.extend(format_paths)
                    add_log(f"Saved content in multiple formats for: {url}")
                else:
                    format_paths = convert_to_formats({url: page_content}, url)
                    file_paths.extend(format_paths)
                    add_log(f"Saved content in multiple formats for: {url}")
            except Exception as e:
                error_message = f'Error converting formats for {url}: {e}'
                add_log(error_message)
                errors.append(error_message)

    add_log('Scraping job completed!')

    if errors:
        return {'files': file_paths, 'errors': errors}
    else:
        return {'files': file_paths, 'errors': 'All Completed Successfully!'}

# Set page configuration
st.set_page_config(page_title="Web Scraper", layout="wide")

# App title and description
st.title("🕸️ Scroopy-Luu 🔍")
st.markdown("Add URLs to scrape content from websites.")

# Initialize session state for URLs
if 'urls' not in st.session_state:
    st.session_state.urls = [{"url": "", "sub_contents": False}]

# Function to add a new URL entry
def add_url():
    st.session_state.urls.append({"url": "", "sub_contents": False})

# Function to remove a URL entry
def remove_url(index):
    st.session_state.urls.pop(index)

# Function to clear logs
def clear_logs():
    st.session_state.logs = []

# Function to handle form submission
def submit_scrape_job():
    # Clear previous logs when starting a new job
    st.session_state.logs = []
    
    # Prepare data for API request
    urls = []
    sub_contents_bools = []
    
    for entry in st.session_state.urls:
        if entry["url"].strip():  # Only include non-empty URLs
            urls.append(entry["url"])
            sub_contents_bools.append(entry["sub_contents"])
    
    if not urls:
        st.error("Please add at least one URL to scrape.")
        return
    
    # Display loading message
    with st.spinner("Scraping in progress..."):
        try:
            add_log("Starting scraping job...")
            results = scrape(urls, sub_contents_bools)
            
            if results.get('errors') == 'All Completed Successfully!':
                st.success("Scraping completed successfully!")
                add_log("✅ All tasks completed successfully!")
            else:
                st.warning("Scraping completed with some errors.")
                for error in results.get('errors', []):
                    add_log(f"⚠️ {error}")

            return results['files']
                
        except Exception as e:
            error_msg = f"An error occurred: {str(e)}"
            st.error(error_msg)
            add_log(f"❌ {error_msg}")
            return None

# URL management outside of form
st.subheader("URLs to Scrape")

# URL display and add/remove buttons
for i, entry in enumerate(st.session_state.urls):
    cols = st.columns([3, 1, 1, 0.5])
    
    with cols[0]:
        st.session_state.urls[i]["url"] = st.text_input(
            f"URL {i+1}", 
            value=entry["url"],
            key=f"url_{i}"
        )
    
    with cols[1]:
        st.session_state.urls[i]["sub_contents"] = st.checkbox(
            "Sub-links", 
            value=entry["sub_contents"],
            key=f"sub_contents_{i}"
        )
    
    with cols[2]:
        if i > 0:  # Don't allow removing the first URL entry
            if st.button("X", key=f"remove_{i}"):
                remove_url(i)
                st.rerun()

# Add URL button
if st.button("Add URL"):
    add_url()
    st.rerun()

# Submit form
with st.form(key="submit_form"):
    st.write("Click the button below to start scraping the URLs.")
    submit_button = st.form_submit_button(label="Start Scraping")
    
    if submit_button:
        st.session_state.files = submit_scrape_job()

# Display logs
st.header("Logs")
log_container = st.container(height=300)
with log_container:
    if st.session_state.logs:
        for log in st.session_state.logs:
            st.text(log)
    else:
        st.info("Logs will appear here during scraping.")

# Clear logs button
if st.button("Clear Logs") and st.session_state.logs:
    clear_logs()
    st.rerun()

# Results section
st.header("Results")

# Replace the info message with a download button functionality
if 'urls' in st.session_state and st.session_state.logs:
    
    if st.session_state.files:
        st.write("Download scraped data:")
        
        # Group files by format
        file_groups = {
            'JSON': [f for f in st.session_state.files if f.endswith('.json')],
            'Pickle': [f for f in st.session_state.files if f.endswith('.pkl')],
            'XML': [f for f in st.session_state.files if f.endswith('.xml')],
            'CSV': [f for f in st.session_state.files if f.endswith('.csv')]
        }

        # Create expandable sections for each format
        for format_name, files in file_groups.items():
            if files:
                with st.expander(f"{format_name} Files"):
                    for file_path in files:
                        # Read the file content
                        with open(file_path, "rb" if format_name in ['Pickle'] else "r", encoding="utf-8" if format_name != 'Pickle' else None) as f:
                            file_content = f.read()
                        
                        # Determine MIME type
                        mime_types = {
                            'JSON': 'application/json',
                            'Pickle': 'application/octet-stream',
                            'XML': 'application/xml',
                            'CSV': 'text/csv'
                        }
                        
                        # Create a download button for each file
                        st.download_button(
                            label=f"Download {os.path.basename(file_path)}",
                            data=file_content,
                            file_name=os.path.basename(file_path),
                            mime=mime_types[format_name]
                        )
    else:
        st.info("No files generated yet. Start scraping to see results.")
else:
    st.info("Run the scraper to generate downloadable results.")