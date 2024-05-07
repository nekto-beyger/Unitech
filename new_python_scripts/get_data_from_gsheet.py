import pandas as pd
import numpy as np
# import gspread
from google.oauth2.service_account import Credentials
from connection import gc
from read_variables import gsheet_id, field_map_gsheet, field_data_types


def clean_data(df):
    """
    Clean and preprocess data.
    """
    df.columns = list(field_map_gsheet.values())
    # Process and clean price columns, removing currency symbols and commas, and convert to numeric
    columns_to_correct = ['cost', 'price_1', 'price_2', 'price_3', 'price']
    for col in columns_to_correct:
        df[col] = df[col].str.replace('[₪,]', '', regex=True).str.strip()
        df[col] = pd.to_numeric(df[col], errors='coerce')

    # Convert 'quantity' to boolean where true indicates visibility
    df['visible'] = pd.to_numeric(df['quantity'], errors='coerce').gt(0)

    # Trim leading and trailing spaces from the 'desc' column
    df['desc'] = df['desc'].str.strip()

    return df


def get_data_from_gsheet():
    sh = gc.open_by_key(gsheet_id)

    worksheets = sh.worksheets()

    all_data = pd.DataFrame()

    # List of sheets to exclude from data extraction
    exclude_sheets = ['import', 'Log', 'KonimboSheet']

    for worksheet in worksheets:
        if worksheet.title not in exclude_sheets:

            data = worksheet.get_all_values()
            # Initialize dataframe with the first row as headers and clean data
            gsheet_df = pd.DataFrame(data, columns=data.pop(0))
            print(gsheet_df[list(field_map_gsheet.keys())])
            # Clean the data using the defined function
            gsheet_df = clean_data(gsheet_df[list(field_map_gsheet.keys())])
            # Assign meaningful column names based on mapping
            # gsheet_df.columns = list(field_map_gsheet.values())
            # Concatenate dataframes from all sheets into one
            all_data = pd.concat([all_data, gsheet_df], ignore_index=True)

    # Replace empty strings with NaN and infer data types automatically
    all_data = all_data.replace('', np.nan).infer_objects()
    # Convert data types according to predefined schema
    all_data = all_data.astype(field_data_types)

    return all_data


# gdata = get_data_from_gsheet()
# print(gdata.head())
# print(gdata.info())
