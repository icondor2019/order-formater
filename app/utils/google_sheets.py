import gspread
import pandas as pd
from configuration.settings import settings


class GoogleSheets:

    def __init__(self):
        SERVICE_ACCOUNT_FILE = settings.GSHEET_CRED_PATH
        self.gc = gspread.service_account(SERVICE_ACCOUNT_FILE)

    def get_sheet_df(self, sheet_name):
        # Function to get a given google sheets in a data frame
        gs = self.gc.open_by_key(self.tables_id[sheet_name])
        sheet = gs.worksheet(sheet_name)
        return (pd.DataFrame(sheet.get_all_records(head=1)))

    def ws_to_pd(self, worksheet_key, sheet_name):
        sheet = self.gc.open_by_key(worksheet_key).worksheet(sheet_name)
        return pd.DataFrame(sheet.get_all_records(head=1))

    def update_on_sheets(self, df, sheet_key, sheet_name):
        df = df.to_numpy().tolist()
        sheet = self.gc.open_by_key(sheet_key)
        return sheet.values_append(sheet_name,
                                   {'valueInputOption': 'USER_ENTERED'},
                                   {'values': df})

    def update_from_scratch(self, df, sheet_key, sheet_name):
        sheet = self.gc.open_by_key(sheet_key).worksheet(sheet_name)
        sheet.clear()
        return sheet.update([df.columns.values.tolist()] + df.values.tolist())

    def prepare_data_today(self, sheet_key, sheet_name, range_data):
        sh = self.gc.open_by_key(sheet_key)
        return sh.values_clear(sheet_name + "!" + range_data)
