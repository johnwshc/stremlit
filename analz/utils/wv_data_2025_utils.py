
import pandas as pd
import numpy as np
import json
import pathlib
from collections import OrderedDict
from datetime import datetime
from pydantic import BaseModel
import itertools
import warnings


def fixcol(c):
    tc = type(c)
    
    if (tc == np.float64):
        return str(int(c))
        
    if tc == str:
        return c
    return f"fuck it {c} your type is {tc}"


class WVGDP_2025:
    src_dir = "d:/python_apps/flaskER/notebooks/soc_econ/data/SAGDP2025/"
    json_out_dir = 'd:/python_apps/flaskER/notebooks/soc_econ/data/json/'
    desc_abrevs_fn = f"{src_dir}/desc_abrev.txt"
    test_fn = f"{src_dir}sagdp2.xlsx"
    goodcols = ['LineCode', 'Description', '2020', '2021', '2022', '2023']  #  last 4
    ocolls = ['LineCode', 'Description', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015']  # Obama yrs
    tcolls = ['LineCode', 'Description', '2016', '2017', '2018', '2019']  #  Trump yrs
    ecolls = ['LineCode', 'Description', '2017', '2018', '2019', '2020', '2021', '2022']
    usecols = ecolls

    @classmethod
    def count_leading_spaces(cls, text):
        return int(sum(1 for _ in itertools.takewhile(str.isspace, text)) / 2)

    def __init__(self, sagdp_fn: str=test_fn):
        # print(sagdp_fn)
        if sagdp_fn.endswith('xlsx'):
            warnings.filterwarnings('ignore', category=UserWarning, module='openpyxl')
            self.df: pd.DataFrame = pd.read_excel(sagdp_fn)
        else:
            raise Exception("file fuck up")
        self.clean_raw_data()
    
    def clean_raw_data(self):
        print("cleaning raw data")
        dff = self.df.iloc[4:].copy()
        scols = pd.Series(list(dff.iloc[0]))        
        self.all_cols = list(scols.apply(fixcol))
        dff.columns = self.all_cols
        self.df = dff[WVGDP_2025.usecols].copy()
        self.df.reset_index(inplace=True, drop=True)
        self.df.drop(0, axis=0, inplace=True)
        self.df.reset_index(inplace=True, drop=True)
        dff = self.df.iloc[0:92,].copy()
        self.df = dff
        self.df.dropna(inplace=True)
        self.df.reset_index(inplace=True, drop=True)
        self.dff = self.df.iloc[0:86,].copy(deep=True)
        #  add layer numbers
        self.dff['layer'] = self.dff.Description.apply(WVGDP_2025.count_leading_spaces)
        self.addendums = self.df.iloc[86:,].copy(deep=True)

    def clean_model(self):
        self.df.drop(['Region', 'TableName', 'IndustryClassification'], inplace=True, axis=1)
        self.df = self.df.iloc[0:91, ].copy()
        self.df.Description = self.df.Description.apply(lambda x: x.strip())
        self.df['isinModel'] = self.df.Description.apply(self.match_desc_to_model)
        self.df = self.df[self.df['isinModel'] == True]
        self.df.drop(['isinModel', 'GeoFIPS', 'LineCode'], inplace=True, axis=1)
        new_columns = ['Description', 'Unit', '2017', '2018', '2019', '2020', '2021', '2022', '2023']
        self.df = self.df[new_columns].copy(deep=True)
        self.df.reset_index(drop=True, inplace=True)
        

class DATA2025:
    bea_2025_reports = OrderedDict()
    b2025path = "d:/python_apps/flaskER/notebooks/soc_econ/data/SAGDP2025/"

    bea_2025_reports['summary'] = 'sagdp1.xlsx'
    bea_2025_reports['gdp'] = 'sagdp2.xlsx'
    bea_2025_reports['taxes_less_subs'] = 'sagdp3.xlsx'
    bea_2025_reports['compensation'] = 'sagdp4.xlsx'
    bea_2025_reports['subsidies'] = 'sagdp5.xlsx'
    bea_2025_reports['taxes_with_subs'] = 'sagdp6.xlsx'
    bea_2025_reports['surplus'] ='sagdp7.xlsx'
    bea_2025_reports['chained_GDP_IDX'] = 'sagdp8.xlsx'
    bea_2025_reports['real gdp'] = 'sagdp9.xlsx'
    bea_2025_reports['gdp_change'] = 'sagdp11.xlsx'
    bea_2025_reports['wv_emp_by_industry'] = 'SA_EMPL_IND_WV_2017_2022.csv'
    bea_2025_reports['all_emp_by_industry'] =  'SA_EMPL_IND_ALL_2017_2022.csv'
    bea_2025_reports['concordance'] = 'emp_gdp_index_concordance.json'
    bea_2025_reports['df_employees_2017_2022'] = 'df_employees_2017_2022_categorized.json'


class WvSummary:
    src_dir = WVGDP_2025.src_dir
    json_out_dir = WVGDP_2025.json_out_dir
    src_fn = f"{DATA2025.b2025path}{DATA2025.bea_2025_reports['summary']}"

    def __init__(self):
        self.df_summary = pd.read_excel(self.src_fn, header=5)
        self.df_summary.dropna(inplace=True)
        good_colls = ['LineCode', 'Description', '2017', '2018', '2019', '2020', '2021', '2022']
        self.df_summary = self.df_summary[good_colls].copy(deep=True)
        # self.subdfs = self.df_summary.iloc[2:6, ].copy()
        # sdvals = ['GDP', 'Compensation', 'Surplus', 'Taxes minus subsidies']
        # self.subdfs.Description = pd.Series(sdvals)




class WvEmp:
    src_fl = f"{DATA2025.b2025path}{DATA2025.bea_2025_reports['wv_emp_by_industry']}"
    con_fl = f"{DATA2025.b2025path}{DATA2025.bea_2025_reports['concordance']}"
    cats1 = ['service', 'mfg', 'ag', 'nr/energy', 'none', 'construction', 'transport']
    cats2 = ['public', 'private', 'none']
    df_cats_json = f"{DATA2025.b2025path}{DATA2025.bea_2025_reports['df_employees_2017_2022']}"

    em_cats_data = pd.Series([
        2, 4, 4, 3, 3, 3, 5, 1, 0, 0,
        6, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0
    ])
    em_pub_priv_data = pd.Series([
        1, 2, 1, 1, 1, 1, 1, 1, 1, 1,
        1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
        1, 1, 0, 0, 0, 0, 0, 0
    ])

    @staticmethod
    def set_category(x):
        return  WvEmp.cats1[x]

    @staticmethod
    def set_pub(x):
        return WvEmp.cats2[x]

    @staticmethod
    def save_df_cats(df: pd.DataFrame):
        fn = WvEmp.df_cats_json
        df.to_json(fn, orient='records')

    @staticmethod
    def read_df_cats() -> pd.DataFrame:
        fn = WvEmp.df_cats_json
        df = pd.read_json(fn, orient='records')
        return df


    @staticmethod
    def fix_desc(x):
        if len(x) < 20:
            return x
        else:
            return f"{x[:20]}..."


    @classmethod
    def add_tups(cls, df: pd.DataFrame, concord: dict) -> pd.DataFrame:
        elevs = list(df.level)
        gids = []
        eids = []
        tups = []
        for i in range(len(elevs)):
            s_i = int
            eid = i + 1
            eids.append(eid)
            lv = elevs[i]
            gid = concord.get(i, -1)
            gids.append(gid)
            tups.append((lv, i, eid, gid))
        df['tups'] = tups
        df['gids'] = gids
        df['eids'] = eids
        return df

    def __init__(self):
        print(f"init wvemp, loading src: {WvEmp.src_fl}")
        self.df_e1: pd.DataFrame = pd.read_csv(WvEmp.src_fl, header=5)
        good_colls = ['LineCode', 'level', 'Description', '2017', '2018', '2019', '2020', '2021', '2022']
        self.df_emp = self.df_e1[good_colls].copy(deep=True)
        self.df_emp = self.df_e1.iloc[8:, ].copy(deep=True)  ## remove summary and na lines
        self.df_emp.dropna(inplace=True)
        self.df_emp.reset_index(drop=True, inplace=True)
        self.df_emp.level = self.df_emp.level.apply(lambda x: int(x))
        with open(WvEmp.con_fl, 'r') as f:
            self.emp_gdp_con_idx: dict = json.load(f)
            self.emp_gdp_con_idx = {int(k): v for k, v in self.emp_gdp_con_idx.items()}
        self.emp_gdp_con_ids = [(int(e)+1, g+1) for e, g in self.emp_gdp_con_idx.items()]
        self.df_emp = WvEmp.add_tups(self.df_emp, self.emp_gdp_con_idx)
        self.df_emp_categorized =  self.categorize()

    def categorize(self):
        df_cats = self.df_emp.copy(deep=True)
        df_cats['pdomain'] = WvEmp.em_pub_priv_data.apply(WvEmp.set_pub)
        df_cats['category'] = WvEmp.em_cats_data.apply(WvEmp.set_category)
        return df_cats



    def get_2022_display_df(self, sorted=True) -> pd.DataFrame:
        dfe_display = self.df_emp.copy(deep=True)
        dfe_display['short_desc'] = dfe_display['Description'].apply(WvEmp.fix_desc)

        if sorted:
            dfe_sorted_display = dfe_display.sort_values(by='2022', ascending=False)
            dfe_sorted_display.drop([1,2], inplace=True)
            dfe_sorted_display.reset_index(drop=True)
            return dfe_sorted_display[['short_desc', '2022']].copy(deep=True)
        else:
            return dfe_display[['Description', '2022']].copy(deep=True)








