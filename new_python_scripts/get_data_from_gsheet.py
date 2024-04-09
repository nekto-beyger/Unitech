import pandas as pd
import numpy as np
# import gspread
from google.oauth2.service_account import Credentials
from connection import gc
from read_variables import gsheet_id, field_map, field_data_types

sh = gc.open_by_key(gsheet_id)
worksheet = sh.get_worksheet(2) 

# ranges = [f"{col}1:{col}" for col in columns]
 
data = worksheet.get_all_values()

# data_combined = [list(row) for row in zip(*[col for range_data in data for col in range_data])]

gsheet_df = pd.DataFrame(data)

# print(data)
# print('=======================')
# print(data_combined)
# print('=======================')
# print(data)
# print('+++++++++++++++++++++')
gsheet_df.columns = gsheet_df.iloc[0] 
gsheet_df = gsheet_df[2:]
gsheet_df = gsheet_df[list(field_map.keys())]
gsheet_df.columns = list(field_map.values())

gsheet_df = gsheet_df.replace('', np.nan)
gsheet_df = gsheet_df.astype(field_data_types)
print(gsheet_df.head())
