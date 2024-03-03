import os
import pandas as pd
from fuzzywuzzy import fuzz


def compare_titles_en():
    if os.path.isfile('Files/combined_data.csv'):  # Check if the file exists
        existing_data = pd.read_csv('Files/combined_data.csv')  # Read data from existing CSV file
    else:  # Create an empty DataFrame if the file doesn't exist
        existing_data = pd.DataFrame()  # Create an empty DataFrame

    # Read data from new CSV files
    douban_data = pd.read_csv('Files/douban.csv')  # Read data from douban.csv
    mdl_data = pd.read_csv('Files/MDL.csv')  # Read data from MDL.csv

    douban_data = douban_data.drop_duplicates(subset='English Title')  # Remove duplicates based on 'English Title'
    mdl_data = mdl_data.drop_duplicates(subset='English Title')  # Remove duplicates based on 'English Title'

    matching_titles = [] # Initialize an empty list to store matching titles

    for douban_title in douban_data['English Title']:
        for mdl_title in mdl_data['English Title']:
            similarity_score = fuzz.ratio(str(douban_title), str(mdl_title))
            if similarity_score > 70: # If similarity score is above 70%, append the titles to matching_titles
                matching_titles.append((douban_title, mdl_title))

    # Filter rows with matching titles and select specific columns for English Title
    douban_matching_rows_english = douban_data[douban_data['English Title'].isin([x[0] for x in matching_titles])][
        ['English Title', 'Rating', 'Number of Raters', 'ID']]  # Retain 'English Title' column
    mdl_matching_rows_english = mdl_data[mdl_data['English Title'].isin([x[1] for x in matching_titles])][
        ['English Title', 'Native Title', 'Year', 'Country', 'Rating', 'Number of Raters',
         'URL']]  # Retain 'English Title' column

    # Merge matching rows on 'English Title'
    combined_data_english = pd.merge(douban_matching_rows_english, mdl_matching_rows_english, on='English Title',
                                     suffixes=('_douban', '_mdl'))

    # Append new data to existing database
    updated_data = pd.concat([existing_data, combined_data_english], ignore_index=True)

    # Save updated data to CSV
    updated_data.to_csv('combined_data.csv', index=False)


def remove_title(file):
    try:
        existing_data = pd.read_csv(file)
        douban_data = pd.read_csv('Files/douban.csv')
        mdl_data = pd.read_csv('Files/MDL.csv')
        combined_data = pd.read_csv(file)

        print("Length of douban_data before removal:", len(douban_data))
        print("Length of mdl_data before removal:", len(mdl_data))

        if not combined_data.empty:
            # Remove rows from douban_data that have IDs matching those in combined_data
            douban_data = douban_data[~douban_data['ID'].isin(combined_data['ID'])]

            # Remove rows from mdl_data that have URLs matching those in combined_data
            mdl_data = mdl_data[~mdl_data['URL'].isin(combined_data['URL'])]

            # Write updated data back to CSV files
            douban_data.to_csv('douban.csv', index=False)
            mdl_data.to_csv('MDL.csv', index=False)

        print("Length of douban_data after removal:", len(douban_data))
        print("Length of mdl_data after removal:", len(mdl_data))

        return douban_data, mdl_data

    except FileNotFoundError:
        print("Error: One or more CSV files not found.")
        return None, None
    except Exception as e:
        print("An error occurred:", e)
        return None, None


def compare_titles_native():
    # Read data from existing CSV files
    if os.path.isfile('Files/combined_data_native.csv'):
        # Read data from existing CSV file
        existing_data = pd.read_csv('Files/combined_data_native.csv')
    else:
        # Create an empty DataFrame if the file doesn't exist
        existing_data = pd.DataFrame()

    # Read data from new CSV files
    douban_data = pd.read_csv('Files/douban.csv')
    mdl_data = pd.read_csv('Files/MDL.csv')

    # Remove duplicates
    douban_data = douban_data.drop_duplicates(subset='Native Title')
    mdl_data = mdl_data.drop_duplicates(subset='Native Title')

    # Initialize an empty list to store matching titles
    matching_titles = []

    # Iterate over each title in douban_data and mdl_data
    for douban_title in douban_data['Native Title']:
        for mdl_title in mdl_data['Native Title']:
            # Calculate the similarity score between titles using fuzz ratio
            similarity_score = fuzz.ratio(str(douban_title), str(mdl_title))
            # If similarity score is above 80%, append the titles to matching_titles
            if similarity_score > 70:
                print(douban_title, mdl_title, similarity_score)
                matching_titles.append((douban_title, mdl_title))

    # Filter rows with matching titles and select specific columns for Native Title
    douban_matching_rows_native = douban_data[douban_data['Native Title'].isin([x[0] for x in matching_titles])][
        ['Native Title', 'Rating', 'Number of Raters', 'ID']]  # Retain 'Native Title' column
    mdl_matching_rows_native = mdl_data[mdl_data['Native Title'].isin([x[1] for x in matching_titles])][
        ['Native Title', 'English Title', 'Year', 'Country', 'Rating', 'Number of Raters',
         'URL']]  # Retain 'Native Title' column

    # Merge matching rows on 'Native Title'
    combined_data_native = pd.merge(douban_matching_rows_native, mdl_matching_rows_native, on='Native Title',
                                    suffixes=('_douban', '_mdl'))

    # Append new data to existing database
    updated_data = pd.concat([existing_data, combined_data_native], ignore_index=True)

    # Save updated data to CSV
    updated_data.to_csv('combined_data_native.csv', index=False)


def reorder_columns_inplace(csv_file, column_order):
    data = pd.read_csv(csv_file)
    data = data[column_order]
    data.to_csv(csv_file, index=False)


def combine_data(csv_file1, csv_file2, output_csv):
    try:
        # Read data from CSV files
        data1 = pd.read_csv(csv_file1)
        data2 = pd.read_csv(csv_file2)

        # Concatenate data vertically
        combined_data = pd.concat([data1, data2], ignore_index=True)

        # Save combined data to a new CSV file
        combined_data.to_csv(output_csv, index=False)

        print(f"Combined data saved to {output_csv}")
        return combined_data
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == '__main__':
    compare_titles_en()
    remove_title('combined_data.csv')
    compare_titles_native()
    remove_title('combined_data_native.csv')
    column = ['English Title', 'Native Title', 'Year', 'Country', 'Rating_mdl', 'Number of Raters_mdl','Rating_douban', 'Number of Raters_douban', 'ID', 'URL']
    reorder_columns_inplace('Files/combined_data.csv', column)
    reorder_columns_inplace('Files/combined_data_native.csv', column)
    combine_data('combined_data.csv', 'combined_data_native.csv', 'Final.csv')
