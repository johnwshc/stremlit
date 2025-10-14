import pandas as pd
import numpy as np
from analz.soc_econ.wv_data_utils import WV_GDP

class NSF_Indicators:
    src_dir = f"/notebooks/soc_econ/nsf/"
    county_state_id_fn = 'swbinv-1.xlsx'
    f = f"{src_dir}{county_state_id_fn}"
    sheetnames_dict = {'Counties': 'Table SWBINV1-1',
                       'Index': 'Index',
                       'Semiconductors': 'Table SWBINV1-10'}

    def __init__(self, sname='Counties', header=3):
        ssname = NSF_Indicators.sheetnames_dict.get(sname, None)
        self.df = pd.read_excel(f"{NSF_Indicators.f}", sheet_name=ssname, header=header)



class Index(NSF_Indicators):
    def __init__(self, sheet: str, header=0):
        super().__init__(sheet, header=header)
        self.df.columns = ['sheet_name', 'description']

class USCounties(NSF_Indicators):
    sheet_name = NSF_Indicators.sheetnames_dict.get('Counties', None)
    def __init__(self, sheet: str, header=0):
        super().__init__(sheet)
        self.df.columns = ['County_code', 'County', 'State']


    def getStateCounties(self, state):

        state_df: pd.DataFrame = self.df[self.df.State == state].copy()
        return state_df


class Semiconductors(NSF_Indicators):

    def __init__(self, sheet: str, header=3):
        super().__init__(sheet, header=header)
        self.sheet_name = NSF_Indicators.sheetnames_dict.get(sheet, None)
        self.title = f"USPTO utility patents granted to U.S. inventors in semiconductors,1998--2022, by county"
        self.count_index = USCounties('Counties')
        self.df = self.df.rename(columns={'U.S. county': 'UScounty'})

    def match_county_code(self, code):
        for c in self.countyCodes:
            if c == code:
                return True
        else:
            return False



    def getStateCounties(self, state) -> pd.DataFrame:
        idf = self.count_index.df
        mask = idf.State == state
        stateCounties: pd.DataFrame = idf[mask].copy()
        self.countyCodes = stateCounties.County_code

        self.df['in_state'] = self.df['UScounty'].apply(self.match_county_code)
        ccdf: pd.DataFrame = self.df[self.df.in_state == True].copy()
        ccdf.reset_index(drop=True, inplace=True)
        ccdf.drop('in_state', axis=1, inplace=True)
        ccdf.reset_index(drop=True, inplace=True)
        return ccdf







