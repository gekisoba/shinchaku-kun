import pandas as pd
import streamlit as st
from bs4 import BeautifulSoup
import requests
import urllib.parse
import base64

def scrape_website(url, selector):
    website_data = []

    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    website_name = soup.find('title').text.strip()
    st.write(f"Website Name: {website_name}")
    st.write(f"URL: {url}\n")

    elements = soup.select(selector)
    for element in elements:
        title = element.text.strip()
        href = element.get('href')
        if href:
            href = urllib.parse.urljoin(url, href)
        st.write(f'Title: {title}\nURL: {href}\n')

        website_data.append({"Website Name": website_name, "URL": url, "Title": title, "Link": href})

    st.markdown('---')  # ここで仕切り線を挿入

    return website_data


def main():
    st.title("Website Scraper")

    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        if st.button("Scrape Websites"):
            all_website_data = []
            for _, row in df.iterrows():
                url = row['url']
                selector = row['selector']
                website_data = scrape_website(url, selector)
                all_website_data.extend(website_data)

            # To Download
            results_df = pd.DataFrame(all_website_data)
            csv = results_df.to_csv(index=False)
            b64 = base64.b64encode(csv.encode()).decode()
            href = f'<a href="data:file/csv;base64,{b64}" download="webscraping_results.csv">Download CSV File</a>'
            st.markdown(href, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
