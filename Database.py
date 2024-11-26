import streamlit as st
import pandas as pd
from fuzzywuzzy import process
import Levenshtein  # Ensures fuzzywuzzy uses python-Levenshtein for better performance


# Load the dataset
df = pd.read_excel("ICAM_2023_2022_2021.xlsx")


def fuzzy_filter(df, column, search_term, limit=10):
    """
    Perform fuzzy search on a specific column of the DataFrame.
    Return all rows that match the search term based on fuzzy matching.
    """
    if not search_term:
        return df

    # Perform fuzzy matching on the unique values in the column
    matches = process.extract(search_term, df[column].dropna().unique(), limit=limit)

    # Extract all matching values with a threshold > 50
    matched_values = [match[0] for match in matches if match[1] > 50]

    # Filter the dataframe to include all rows that have matching values
    return df[df[column].str.contains('|'.join(matched_values), case=False, na=False)]


def main():
    st.set_page_config(layout="wide")  # Set the layout to wide
    st.title("Searchable ICAM Database")
    
    # Sidebar Filters
    st.sidebar.header("Filters by Column")
    
    # Fuzzy Search Filters for Text Columns
    symposium_filter = st.sidebar.text_input("Search by Symposium")
    title_filter = st.sidebar.text_input("Search by Title")
    type_filter = st.sidebar.text_input("Search by Type")
    organization_filter = st.sidebar.text_input("Search by Organization")
    speaker_filter = st.sidebar.text_input("Search by Speaker")
    speaker_category_filter = st.sidebar.text_input("Search by Speaker Category")
    
    # Exact Match/Multiselect Filter for Numeric Columns
    year_filter = st.sidebar.multiselect("Filter by Year", options=df["Year"].unique(), default=df["Year"].unique())
    
    # Apply Filters
    filtered_df = df.copy()
    
    # Apply fuzzy filters for text-based columns
    if symposium_filter:
        filtered_df = fuzzy_filter(filtered_df, "Symposium", symposium_filter)
    if title_filter:
        filtered_df = fuzzy_filter(filtered_df, "Title", title_filter)
    if type_filter:
        filtered_df = fuzzy_filter(filtered_df, "Type", type_filter)
    if organization_filter:
        filtered_df = fuzzy_filter(filtered_df, "Organization", organization_filter)
    if speaker_filter:
        filtered_df = fuzzy_filter(filtered_df, "Speaker", speaker_filter)
    if speaker_category_filter:
        filtered_df = fuzzy_filter(filtered_df, "Speaker Category", speaker_category_filter)
    
    # Apply exact match filter for Year
    filtered_df = filtered_df[filtered_df["Year"].isin(year_filter)]
    
    # Display Results
    st.subheader("Filtered Results")
    
    # Make table wider
    st.dataframe(filtered_df, use_container_width=True)

if __name__ == "__main__":
    main()
