import streamlit as st
import pandas as pd

# Load the dataset
@st.cache_data
def load_data():
    return pd.read_excel("ICAM_2023_2022_2021.xlsx")

# Filter function
def filter_dataframe(df, column, search_term):
    """
    Filters the DataFrame for rows where the specified column contains the search term.
    """
    if not search_term:
        return df
    return df[df[column].str.contains(search_term, case=False, na=False)]

# Main app
def main():
    st.set_page_config(layout="wide")  # Set the layout to wide
    st.title("Searchable Database")
    
    # Load data
    df = load_data()
    
    # Create sidebar for search inputs
    st.sidebar.header("Search Filters")
    
    # Create a search box for each column
    search_terms = {}
    for column in df.columns:
        search_terms[column] = st.sidebar.text_input(f"Search by {column}", "")
    
    # Apply filters
    filtered_df = df.copy()
    for column, search_term in search_terms.items():
        if search_term:  # Only apply filter if there's a search term
            filtered_df = filter_dataframe(filtered_df, column, search_term)
    
    # Display filtered results
    st.subheader("Filtered Results")
    st.dataframe(filtered_df, use_container_width=True)

if __name__ == "__main__":
    main()
