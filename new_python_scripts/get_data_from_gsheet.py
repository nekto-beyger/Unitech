import pandas as pd
import numpy as np
# import gspread
from google.oauth2.service_account import Credentials
from connection import gc
from read_variables import gsheet_id, field_map_gsheet, field_data_types


def visibility(df, col_name):
    return pd.to_numeric(df[col_name], errors='coerce').gt(0)


def get_data_from_gsheet():
    sh = gc.open_by_key(gsheet_id)

    worksheets = sh.worksheets()

    all_data = pd.DataFrame()

    exclude_sheets = ['import', 'Log', 'KonimboSheet']

    for worksheet in worksheets:
        if worksheet.title not in exclude_sheets:

            data = worksheet.get_all_values()
            
            gsheet_df = pd.DataFrame(data)
            
            gsheet_df.columns = gsheet_df.iloc[0]
            
            gsheet_df = gsheet_df[2:]
            gsheet_df.reset_index(drop=True, inplace=True)

            gsheet_df = gsheet_df[list(field_map_gsheet.keys())]
            gsheet_df.columns = list(field_map_gsheet.values())
            
            columns_to_correct = ['cost', 'price_1', 'price_2', 'price_3', 'price']
            
            for col in columns_to_correct:
                gsheet_df[col] = gsheet_df[col].str.replace('[₪,]', '', regex=True).str.strip()
                gsheet_df[col] = pd.to_numeric(gsheet_df[col], errors='coerce')
            
            
            gsheet_df['visible'] = visibility(gsheet_df, "quantity")
            # convert_to_boolean(gsheet_df, 'visible_')
            gsheet_df['desc'] = gsheet_df["desc"].str.strip()
            
            
            gsheet_df = gsheet_df.replace('', np.nan).infer_objects()  
            gsheet_df = gsheet_df.astype(field_data_types)

            all_data = pd.concat([all_data, gsheet_df], ignore_index=True)

    # print(all_data.info())
    return all_data


# gdata = get_data_from_gsheet()
# print(gdata.head())
# print(gdata.info())