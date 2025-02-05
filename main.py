#UI for streamlit and for website to enter the details as per the user.

import streamlit as st
from scrape import scrape_website

st.title(" AI Web Scraper")
url = st.text_input("Enter a website URL:")

if st.button("Scrape Site"):
    st.write("Scraping the Website")
    result = scrape_website(url)
    print(result)
