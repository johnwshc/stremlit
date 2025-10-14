
import pandas as pd
import numpy as np
import json
import pathlib
from collections import OrderedDict
from datetime import datetime
from pydantic import BaseModel, field_validator
from config import Config
import pendulum as pdt



class IndDescription(BaseModel):
    long:str
    short:str

    @field_validator('long')
    @classmethod
    def validate_long(cls, v: str) -> str:

        return v.strip()

    @field_validator('short')
    @classmethod
    def validate_short(cls, v: str) -> str:

        return v.strip()

class LCX(BaseModel):
    lcs:list[IndDescription]

    def get_longs(self):
        return pd.Series([l.long.strip() for l in self.lcs])

    def get_shorts(self):
        return pd.Series([l.short.strip() for l in self.lcs])

    def save_to_json(self, rname=False):

        curr_json_fn = Config.INDUSTRY_DESC_JSON
        pth = pathlib.Path(curr_json_fn)
        if rname:
            ts = str(pdt.now().timestamp())
            target = f"{pth}_{ts}.old"
            pth.rename(target)
        with open(curr_json_fn, 'w') as fff:
            md = self.model.dict()
            json.dump(md,fff)


    def get_lcxx(self, descs: pd.Series):
        sdescs = descs.apply(str.strip)
        lcxx = []
        model = self.lcs
        for l in model:
            long = l.long.strip()
            if long in sdescs:
                lcxx.append(l)
        return lcxx






class GDPMgr:
    default_props = {'industry_desc_json': Config.INDUSTRY_DESC_JSON,
                     }
    def __init__(self, props=None):

        self.props = props or self.default_props
        fn = self.props['industry_desc_json']
        self.lcx: LCX = GDPMgr.get_lCX(jfile=fn)

    @classmethod
    def get_lCX(cls, jfile=None):
        jfile = jfile or Config.INDUSTRY_DESC_JSON
        with open(jfile) as f:
            dd = json.load(f)
        lcx = LCX(**dd)
        return lcx


    def get_lcxx(self, descs: pd.Series) -> list:
        # print(f"opps gdp descriptions before dropns\n{descs}")
        descs.dropna(inplace=True)
        descs = descs.apply(str.strip)
        ldescs = list(descs)
        lcxx = []
        lcs: list[IndDescription] = self.lcx.lcs
        for l in lcs:
            if l.long in ldescs:
                lcxx.append(l)
        # print(f"lcxx result\n{lcxx}")
        return lcxx

    def get_all_prod_descs(self):
        curr_2022_prod = CurrGDP()
        return curr_2022_prod.df




class GDPReport(BaseModel):
    name: str
    for_years: str
    description: str
    data: dict
    mode: str

    def to_json(self):
        return self.to_json()

    def to_DF(self):
        return pd.DataFrame(self.data)

    def clean_raw_data(self):

        # remove non data rows
        df = pd.DataFrame(self.data)
        # all_states = True if "ALL" in self.name else False
        # delete footnote rows
        df = df.iloc[0:86,].copy(deep=True)

        # handle bad column headers
        bad_col_reports: list = ['SAGDP1_ALL_AREAS_2017_2023.xls']
        if self.name in bad_col_reports:
            if len(df.columns) == 15:
                df.columns = WV_GDP.good15
            else:
                if len(df.columns) == 14:
                    df.columns = WV_GDP.good14
                else:
                    raise Exception(f"omva;od column length: {len(df.columns)}")
        #  Fix columns: set type on GeoName and GeoFIPS to str
        df.GeoName = df.GeoName.astype(str)

        strs = " \"*"   # chars to strip from fields
        df.GeoName = df.GeoName.apply(lambda x: x.strip(strs))
        df.GeoFIPS = df.GeoFips.astype(str)
        df.GeoFIPS = df.GeoFips.apply(lambda x: x.strip(strs))
        df.Description = df.Description.apply(str.strip)


        df.LineCode = df.LineCode.astype(int)
        df.Description = df.Description.astype(str)
        # df.drop('IndustryClassification', axis=1, inplace=True)
        df.reset_index(inplace=True, drop=True)
        self.data = df.to_dict()



class WV_GDP:
    #  LINE Codesin state gdp reports for major industrial classifications
    # lcs = [1, 4, 5, 6, 10, 11, 12, 34, 35, 36, 45, 51, 56, 60, 64, 66, 69, 70, 76, 79, 82, 83, 84, 85, 86]
    # lcs: pd.Series =  None
    good15 = ['GeoFIPS', 'GeoName', 'Region', 'TableName', 'LineCode',
              'IndustryClassification', 'Description', 'Unit', '2017', '2018', '2019',
              '2020', '2021', '2022', '2023']
    good14 = ['GeoFIPS', 'GeoName', 'Region', 'TableName', 'LineCode',
              'IndustryClassification', 'Description', 'Unit', '2017', '2018', '2019',
              '2020', '2021', '2022']
    src_dir = Config.SA_DATA_DIR
    json_out_dir = Config.JSON_DIR
    desc_abrevs_fn = f"{src_dir}/desc_abrev.txt"

    industries = [

        'Forestry, fishing, and related activities',
        'Mining, quarrying, and oil and gas extraction',
        'Utilities',
        'Construction',
        'Manufacturing',
        'Wholesale trade',
        'Retail trade',
        'Transportation and warehousing',
        'Information',
        'Finance and insurance',
        'Real estate and rental and leasing',
        'Professional, scientific, and technical services',
        'Management  of companies and enterprises',
        'Administrative and support and waste managemen...',
        'Educational services',
        'Health care and social assistance',
        'Arts, entertainment, and recreation',
        'Accommodation and food services',
        'Other services(except government and governme...)',
        'Government and government  enterprises',
        'Federal',
        'civilian',
        'Military',
        'State and local',
        'Farms'

        ]

    # json_out_f1 = f"{json_out_dir}/f1.json"
    bea_reps = OrderedDict()

    bea_reps['SAGDP1_ALL_AREAS_2017_2023.xls'] = 'Real GDP'
    bea_reps['SAGDP2N_WV_2017_2023.csv'] = 'Gross Domestic Product (GDP) is in millions of current dollars (not adjusted for inflation)'
    bea_reps['SAGDP2N_ALL_AREAS_2017_2023.csv'] = 'GDP unadjusted for all states'
    bea_reps['SAGDP3N_WV_2017_2022.csv'] = 'Taxes on production and imports less subsidies is in thousands of current dollars (not adjusted for inflation)'
    bea_reps['SAGDP3N_ALL_AREAS_2017_2022.csv'] = 'Taxes less subs on all states'
    bea_reps['SAGDP4N_WV_2017_2022.csv'] = 'Compensation is in thousands of current dollars (not adjusted for inflation)'
    bea_reps['SAGDP4N_ALL_AREAS_2017_2022.csv'] = 'Compensation on all states'
    bea_reps['SAGDP5N_WV_2017_2022.csv'] = 'Subsidies is in thousands of current dollars (not adjusted for inflation).'
    bea_reps['SAGDP5N_ALL_AREAS_2017_2022.csv'] = 'Subsidies on all states'
    bea_reps['SAGDP6N_WV_2017_2022.csv'] = 'Taxes on production and imports is in thousands of current dollars (not adjusted for inflation)'
    bea_reps['SAGDP6N_ALL_AREAS_2017_2022.csv'] = 'Taxes (including subsidies) for all states'
    bea_reps['SAGDP7N_WV_2017_2022.csv'] ='Gross operating surplus is in thousands of current dollars (not adjusted for inflation)'
    bea_reps['SAGDP7N_ALL_AREAS_2017_2022.csv'] = 'operating surplus'
    bea_reps['SAGDP8N_WV_2017_2023.csv'] = 'GDP delta from 2017 100.0 base'
    bea_reps['SAGDP8N_ALL_AREAS_2017_2023.csv'] = 'GDP delta'
    bea_reps['SAGDP9N_WV_2017_2023.csv'] = 'Real GDP is in millions of chained 2017 dollars. '
    bea_reps['SAGDP9N_ALL_AREAS_2017_2023.csv'] = 'Real GDP'
    bea_reps['SAGDP11N_WV_2018_2023.csv'] = 'GDP percent change detail'
    bea_reps['SAGDP11N_ALL_AREAS_2018_2023.csv'] = 'GDP percent change'
    bea_reps['SA_EMPL_IND_WV_2017_2022.xls'] = 'WV employment by industry'
    bea_reps['SA_EMPL_IND_ALL_2017_2022.xls'] =  'ALL employment by industry'



    def __init__(self, sagdp_fn: str, mgr: GDPMgr = None):
        # print(sagdp_fn)
        if mgr is None:
            self.mgr = GDPMgr()
        else:
            self.mgr = mgr
        self.fn = pathlib.Path(sagdp_fn).name
        if sagdp_fn.endswith('csv'):
            self.df: pd.DataFrame = pd.read_csv(sagdp_fn, header=0, sep=',')
        elif sagdp_fn.endswith('xls'):
            if self.fn == 'SA_EMPL_IND_WV_2017_2022.xls':
                self.df: pd.DataFrame = pd.read_excel(sagdp_fn, sheet_name='Sheet1', header=5)

            else:
                self.df: pd.DataFrame = pd.read_excel(sagdp_fn, header=0,sheet_name='Sheet1')
        else:
            raise NotImplementedError("unrecognized sagdp format")




    def getReport(self, clean=True, mode='RAW'):
        # print(f"Report for {self.fn}")
        desc = self.bea_reps.get(self.fn)

        report_params = {
            'name': self.fn,
            'for_years': self.fn[-13:-4],
            'description': desc,
            'data': self.df.to_dict(),
            'mode': mode
        }
        gdp_report = GDPReport(**report_params)
        if clean:
            gdp_report.clean_raw_data()
        else:
            pass
            # print("report not cleaned")

        return gdp_report

    @staticmethod
    def getReports(st: str = 'WV', clean=True):
        reports: list[GDPReport] = []
        fnd = {k: v for k, v in WV_GDP.bea_reps.items() if st in k}
        fdir = WV_GDP.src_dir
        for f, desc in fnd.items():
            ff = f"{fdir}{f}"
            if st in f:
                wv_gdp = WV_GDP(ff)
                mode = "RAW"
                report_params = {
                    'name': f,
                    'for_years': f[-13:-4],
                    'description': desc,
                    'data': wv_gdp.df.to_dict(),
                    'mode': mode
                }
                gdp_report = GDPReport(**report_params)
                gdp_report.clean_raw_data()
                reports.append(gdp_report)
        return reports




class EmployByIndustry(WV_GDP):

    state_name = 'SA_EMPL_IND_WV_2017_2022.xls'
    national_name = 'SA_EMPL_IND_ALL_2017_2022.xls'
    SA_DATA_DIR = Config.SA_DATA_DIR
    sample_lcs_props = {'gov_details': True, 'add_Farms': True }

    def __init__(self, sagdp_fn: str = f"{SA_DATA_DIR}/{state_name}", props=None):
        super().__init__(sagdp_fn)
        self.props = props
        self.bea_report = self.getReport( clean=False)
        self.df: pd.DataFrame = self.bea_report.to_DF()
        # ****************************
        #    These are vector values: 2017-2022
        self.total_employment = self.get_total_employment()
        self.wage_employment = self.get_all_wage_employment()
        self.prop_employment = self.get_prop_employment()
        self.farm_prop_employment = self.get_farm_prop_employment()
        self.farm_employment = self.get_farm_employment()
        self.non_farm_employment = self.get_non_farm_employment()
        # self.non_farm_prop_employment = self.prop_employment.sub(self.farm_prop_employment)

        #   *************************************

        if not props:
            self.gov_detail = EmployByIndustry.sample_lcs_props.get('gov_details')
            self.add_Farms = False
        else:
            self.gov_detail = props.get('gov_details', False)
            self.add_Farms = False

        self.descs = self.df.Description  #  uncleaned description field
        self.descs.dropna(inplace=True)
        self.descs.apply(str.strip)
        self.ldescs = list(self.descs)
        self.ldescs = [s.strip() for s in self.ldescs]
        self.lcxx: list = self.mgr.get_lcxx(descs=self.descs)  #  series of long/short Descriptions for this table
        self.longs: list = [l.long for l in self.lcxx]  #  series of long descriptions for this table
        self.longs = [s.strip() for s in self.longs]
        print(f"len of longs: {len(self.longs)}")
        self.clean_df: pd.DataFrame = self.clean(gov_detail=self.gov_detail)  #  cleaned table


    def get_total_employment(self):
        temp: pd.DataFrame = self.df.iloc[1,]
        te: pd.Series = temp.iloc[3:].copy()
        te = te.iloc[1:].copy()
        te.name = 'Total Employment'
        # new_edf_columns = ['Description', '2017', '2018', '2019', '2020', '2021', '2022']
        te.name="Total Employment"

        return te

    def get_all_wage_employment(self):
        temp: pd.DataFrame = self.df.iloc[3,].copy()
        te: pd.Series = temp.iloc[3:].copy()
        te = te.iloc[1:].copy()
        te.name = 'All Wage Employment'
        return te

    def get_prop_employment(self):
        temp = self.df.iloc[4,].copy()
        te = temp.iloc[3:].copy()
        te = te.iloc[1:].copy()
        te.name = 'Prop Employment'
        return te

    def get_farm_prop_employment(self):
        temp = self.df.iloc[5,].copy()
        te: pd.Series = temp.iloc[3:].copy()
        te = te.iloc[1:].copy()
        te.name = 'Farm Prop Employment'
        return te

    def get_farm_employment(self):
        temp = self.df.iloc[8,].copy()
        te = temp.iloc[3:].copy()
        te = te.iloc[1:].copy()
        te.name = 'Farm Employment'
        return te

    def get_non_farm_employment(self):
        temp = self.df.iloc[9,].copy()
        te = temp.iloc[3:].copy()
        te = te.iloc[1:].copy()
        te.name = 'Non-Farm Employment'
        return te

    def get_non_farm_prop_employment(self):
        tprop = self.total_employment.copy()
        fprop = self.farm_prop_employment.copy()
        nfprop = tprop.sub(fprop)
        nfprop.name = 'Non-Farm Prop Employment'
        return nfprop.copy()


    def clean(self, gov_detail: bool = True) -> pd.DataFrame:
        df_copy = self.df.copy(deep=True)
        df_copy.dropna(inplace=True)
        df_copy.Description = df_copy.Description.apply(str.strip)
        # remove summary rows
        df_copy['inModel'] = df_copy['Description'].apply(lambda x: True if x in self.longs else False)
        mask = df_copy['inModel'] == True
        df_emp = df_copy[mask].copy()
        # print(f"len df_emp: {len(df_emp)}")
        # print(f"len df_copy: {len(df_copy)}")

        # employment categories to display, including farm, government and proprietors numbers
        # self.df.reset_index(drop=True, inplace=True)
        # Remove state and local detail?
        if not gov_detail:
            df_emp = df_emp.iloc[0:-6,].copy()
            df_emp.reset_index(drop=True, inplace=True)

        df_emp['LineCode'] = df_emp['LineCode'].replace(np.nan, 0)
        df_emp = df_emp[df_emp.LineCode != 0].copy()
        df_emp.LineCode = df_emp.LineCode.astype(int)
        df_emp.reset_index(drop=True, inplace=True)
        new_edf_columns = ['Description', '2017', '2018', '2019', '2020', '2021', '2022']
        df_emp = df_emp[new_edf_columns].copy(deep=True)

        df_emp = df_emp.astype({c: "int64" for c in df_emp.columns[1:]})

        return df_emp



    def getCleanDataByYear(self, yr: str= '2022'):
        data_years = ['2017', '2018', '2019', '2020', '2021', '2022']
        allcols = ['Description']
        allcols.extend(data_years)
        # print(f"cols: {allcols}")
        if yr in data_years:
            cols = ['Description', yr]
            ddf:pd.DataFrame = self.df[cols].copy(deep=True)
            ddf.reset_index(drop=True, inplace=True)
            return ddf
        elif yr == 'ALL':

            ddf: pd.DataFrame = self.df[allcols].copy(deep=True)
            ddf.reset_index(drop=True, inplace=True)
            return ddf

        else:
            raise Exception(f"Invalid year: {yr}")


class CurrGDP(WV_GDP):
    fn = 'SAGDP2N_WV_2017_2023.csv'
    DATA_DIR = WV_GDP.src_dir

    def __init__(self, sagdp_fn: str = f"{DATA_DIR}/{fn}"):
        super().__init__(sagdp_fn)

        self.bea_report = self.getReport(clean=False)
        self.df: pd.DataFrame = self.bea_report.to_DF()

        big_cats = ["All industry  total",
        "Private industries",
        "Agriculture, forestry, fishing and hunting"]


        self.all_industry_cgdp = self.get_all_industry()
        self.all_private_industry_cgdp = self.get_all_private_industry()
        self.all_agriculture_cgdp = self.get_all_agriculture()


        self.descs = self.df.Description
        self.lcxx = self.mgr.get_lcxx(descs=self.descs)
        self.longs = [l.long.strip() for l in self.lcxx]
        self.clean_df = self.clean()

    def get_all_industry(self):
        ai = self.df.iloc[0,].copy()
        drop_labels = ['GeoFIPS', 'GeoName', 'Region', 'TableName', 'LineCode',
                       'IndustryClassification', 'Unit', '2023']
        ai.drop(labels=drop_labels, inplace=True)
        ai.name = "All industry"
        return ai

    def get_all_private_industry(self):
        ap =  self.df.iloc[1,].copy()
        drop_labels = ['GeoFIPS', 'GeoName', 'Region', 'TableName', 'LineCode',
                       'IndustryClassification', 'Unit', '2023']
        ap.drop(labels=drop_labels, inplace=True)
        ap.name = "Private industries"
        return ap

    def get_all_agriculture(self):
        ag = self.df.iloc[2,].copy()
        drop_labels = ['GeoFIPS', 'GeoName', 'Region', 'TableName', 'LineCode',
                       'IndustryClassification', 'Unit', '2023']
        ag.drop(labels=drop_labels, inplace=True)
        ag.name = "All Agriculture"

        return ag


    def match_desc_to_model(self, desc):
        modeld = self.longs
        if desc in modeld:
            return True
        else:
            return False


    def clean(self):
        clean_df = self.df.copy(deep=True)
        clean_df.drop(['Region', 'TableName', 'IndustryClassification'], inplace=True, axis=1)
        clean_df = clean_df.iloc[0:91,].copy()
        clean_df.Description = clean_df.Description.apply(lambda x: x.strip())
        clean_df['isinModel'] = clean_df.Description.apply(self.match_desc_to_model)
        clean_df = clean_df[clean_df['isinModel'] == True]
        clean_df.drop(['isinModel', 'GeoFIPS', 'LineCode'], inplace=True, axis=1)
        new_columns = ['Description', 'Unit', '2017', '2018', '2019', '2020', '2021', '2022', '2023']
        clean_df = clean_df[new_columns].copy(deep=True)
        clean_df.reset_index(drop=True, inplace=True)
        return clean_df


class RealGDP(WV_GDP):
    fn = 'SAGDP9N_WV_2017_2023.csv'
    DATA_DIR = WV_GDP.src_dir
    def __init__(self,  sagdp_fn: str = f"{DATA_DIR}/{fn}"):
        super().__init__(sagdp_fn)

        self.bea_report = self.getReport( clean=False)
        self.df : pd.DataFrame = self.bea_report.to_DF()
        self.descs = self.df.Description
        #  drop any NA rows
        self.descs.dropna(inplace=True)
        # strip any whitespace around strings in description column
        self.descs = self.descs.apply(lambda x: x.strip())
        # filter Description fields with model from LCX
        self.lcxx: list[IndDescription] = self.mgr.get_lcxx(descs=self.descs)
        self.longs = [l.long.strip() for l in self.lcxx]

        self.all_industry_rgdp = self.get_all_industry()
        self.all_private_industry_rgdp = self.get_all_private_industry()
        self.all_agriculture_rgdp = self.get_all_agriculture()

        self.clean_df = self.clean()


    def get_all_industry(self):

        return self.df.iloc[0,].copy()

    def get_all_private_industry(self):
        return self.df.iloc[1,].copy()

    def get_all_agriculture(self):
        return self.df.iloc[2,].copy()
    def clean(self):
        clean_df = self.df.copy(deep=True)
        clean_df.drop(['Region', 'TableName', 'IndustryClassification'], inplace=True, axis=1)
        clean_df = clean_df.iloc[0:91,].copy()
        clean_df.Description = clean_df.Description.apply(lambda x: x.strip())
        clean_df['isinModel'] = clean_df.Description.apply(lambda x: True if x in self.longs else False)
        clean_df = clean_df[clean_df['isinModel'] == True]
        clean_df.drop(['isinModel', 'GeoFIPS', 'LineCode'], inplace=True, axis=1)
        new_columns = ['Description', 'Unit', '2017', '2018', '2019', '2020', '2021', '2022', '2023']
        clean_df = clean_df[new_columns].copy(deep=True)
        clean_df.reset_index(drop=True, inplace=True)
        return clean_df

    def getCleanDataByYear(self, yr: str= '2022'):
        data_years = ['2017', '2018', '2019', '2020', '2021', '2022']
        allcols = ['Description', 'Unit']
        allcols.extend(data_years)
        # print(f"cols: {allcols}")
        if yr in data_years:
            cols = ['Description', 'Unit', yr]
            ddf:pd.DataFrame = self.df[cols].copy(deep=True)
            ddf.reset_index(drop=True, inplace=True)
            return ddf
        elif yr == 'ALL':

            ddf: pd.DataFrame = self.df[allcols].copy(deep=True)
            ddf.reset_index(drop=True, inplace=True)
            return ddf

        else:
            raise Exception(f"Invalid year: {yr}")

class CompGDP(WV_GDP):
    fn = 'SAGDP4N_WV_2017_2022.csv'
    datadir = WV_GDP.src_dir

    def __init__(self, sagdp_fn: str = f"{datadir}/{fn}"):
        super().__init__(sagdp_fn)

        if not self.mgr:
            raise Exception("manager  missing")
        self.bea_report = self.getReport( clean=False)
        self.df: pd.DataFrame = self.bea_report.to_DF()
        self.descs = self.df.Description
        self.descs.dropna(inplace=True)
        self.descs = self.descs.apply(lambda x: x.strip())
        self.lcxx: list[IndDescription] = self.mgr.get_lcxx(descs=self.descs)
        self.longs: list = [l.long.strip() for l in self.lcxx]
        self.all_industry_comp_gdp = self.get_all_industry()
        self.all_private_comp_gdp = self.get_all_private_industry()
        self.all_agriculture_gdp = self.get_all_agriculture()

        self.clean_df = self.clean()


    def get_all_industry(self):

        return self.df.iloc[0,].copy()

    def get_all_private_industry(self):
        return self.df.iloc[1,].copy()

    def get_all_agriculture(self):
        return self.df.iloc[2,].copy()

    def match_desc_to_model(self, desc):
        modeld = self.longs
        if desc in modeld:
                return True
        else:
            return False

    def clean(self):
        clean_df = self.df.copy(deep=True)
        clean_df.drop(['GeoName','Region', 'TableName', 'IndustryClassification'], inplace=True, axis=1)
        clean_df = clean_df.iloc[0:91, ].copy()
        clean_df.Description = clean_df.Description.apply(lambda x: x.strip())
        clean_df['isinModel'] = clean_df.Description.apply(self.match_desc_to_model)
        clean_df = clean_df[clean_df['isinModel'] == True].copy(deep=True)
        clean_df.drop(['isinModel', 'GeoFIPS','LineCode'], inplace=True, axis=1)
        clean_df.reset_index(drop=True, inplace=True)
        return clean_df

    def getCleanDataByYear(self, yr: str = '2022'):
        data_years = ['2017', '2018', '2019', '2020', '2021', '2022']
        allcols = ['Description', 'Unit']
        allcols.extend(data_years)
        # print(f"cols: {allcols}")
        if yr in data_years:
            cols = ['Description', 'Unit', yr]
            ddf: pd.DataFrame = self.df[cols].copy(deep=True)
            ddf.reset_index(drop=True, inplace=True)
            return ddf
        elif yr == 'ALL':

            ddf: pd.DataFrame = self.df[allcols].copy(deep=True)
            ddf.reset_index(drop=True, inplace=True)
            return ddf

        else:
            raise Exception(f"Invalid year: {yr}")


class OppsGDP(WV_GDP):
    fn = 'SAGDP7N_WV_2017_2022.csv'
    datadir = WV_GDP.src_dir

    def __init__(self, sagdp_fn: str = f"{datadir}/{fn}"):
        super().__init__(sagdp_fn)

        if not self.mgr:
           raise Exception("manager  missing")

        self.bea_report = self.getReport(clean=False)
        self.df: pd.DataFrame = self.bea_report.to_DF()
        self.descs = self.df.Description
        self.descs.dropna(inplace=True)
        self.descs = self.descs.apply(lambda x: x.strip())
        self.lcxx: list[IndDescription] = self.mgr.get_lcxx(descs=self.descs)
        self.longs: list = [l.long for l in self.lcxx]

        self.all_industry_ogdp = self.get_all_industry()
        self.all_private_ogdp = self.get_all_private_industry()
        self.all_agriculture_gdp = self.get_all_agriculture()
        self.clean_df = self.clean()

    def get_all_industry(self):
        return self.df.iloc[0,].copy()

    def get_all_private_industry(self):
        return self.df.iloc[1,].copy()

    def get_all_agriculture(self):
        return self.df.iloc[2,].copy()

    def match_desc_to_model(self, desc):
        modeld = self.longs
        if desc in modeld:
            return True
        else:
            return False

    def clean(self):
        clean_df = self.df.copy(deep=True)
        # print("in local Opps")
        clean_df.drop(['GeoName', 'Region', 'TableName', 'IndustryClassification'], inplace=True, axis=1)
        clean_df = clean_df.iloc[0:91, ].copy()
        clean_df.Description = clean_df.Description.apply(lambda x: x.strip())
        clean_df['isinModel'] = clean_df.Description.apply(self.match_desc_to_model)
        clean_df = clean_df[clean_df['isinModel'] == True]
        # print(f'clean opps: len of inModel df: {len(clean_df)}')
        clean_df.drop(['isinModel', 'GeoFIPS', 'LineCode'], inplace=True, axis=1)
        return clean_df

    def getCleanDataByYear(self, yr: str = '2022'):
        data_years = ['2017', '2018', '2019', '2020', '2021', '2022']
        allcols = ['Description', 'Unit']
        allcols.extend(data_years)
        # print(f"cols: {allcols}")
        if yr in data_years:
            cols = ['Description', 'Unit', yr]
            ddf: pd.DataFrame = self.df[cols].copy(deep=True)
            ddf.reset_index(drop=True, inplace=True)
            return ddf
        elif yr == 'ALL':

            ddf: pd.DataFrame = self.df[allcols].copy(deep=True)
            ddf.reset_index(drop=True, inplace=True)
            return ddf

        else:
            raise Exception(f"Invalid year: {yr}")


class TaxesS(WV_GDP):
    fn = 'SAGDP3N_WV_2017_2022.csv'
    datadir = WV_GDP.src_dir

    def __init__(self, sagdp_fn: str = f"{datadir}/{fn}"):
        super().__init__(sagdp_fn)

        self.bea_report = self.getReport(clean=False)
        self.df: pd.DataFrame = self.bea_report.to_DF()
        self.descs = self.df.Description
        self.descs.dropna(inplace=True)
        self.descs = self.descs.apply(lambda x: x.strip())
        self.lcxx: list[IndDescription] = self.mgr.get_lcxx(descs=self.descs)
        self.longs: list = [l.long for l in self.lcxx]

        self.all_industry_ts = self.get_all_industry()
        self.all_private_ts = self.get_all_private_industry()
        self.all_agriculture_ts = self.get_all_agriculture()



        self.clean_df = self.clean()

    def get_all_industry(self):
        return self.df.iloc[0,].copy()

    def get_all_private_industry(self):
        return self.df.iloc[1,].copy()

    def get_all_agriculture(self):
        return self.df.iloc[2,].copy()

    def match_desc_to_model(self, desc):
        modeld = self.longs
        if desc in modeld:
            return True
        else:
            return False

    def clean(self):
        clean_df = self.df.copy(deep=True)
        clean_df.drop(['GeoName', 'Region', 'TableName', 'IndustryClassification'], inplace=True, axis=1)
        clean_df = clean_df.iloc[0:91, ].copy()
        clean_df.Description
        clean_df.Description = clean_df.Description.apply(lambda x: x.strip())
        clean_df['isinModel'] = clean_df.Description.apply(self.match_desc_to_model)
        clean_df = clean_df[clean_df['isinModel'] == True]
        clean_df.drop(['isinModel', 'GeoFIPS', 'LineCode'], inplace=True, axis=1)
        clean_df.reset_index(drop=True, inplace=True)
        return clean_df


    def getCleanDataByYear(self, yr: str = '2022'):
        data_years = ['2017', '2018', '2019', '2020', '2021', '2022']
        allcols = ['Description', 'Unit']
        allcols.extend(data_years)
        # print(f"cols: {allcols}")
        if yr in data_years:
            cols = ['Description', 'Unit', yr]
            ddf: pd.DataFrame = self.df[cols].copy(deep=True)
            ddf.reset_index(drop=True, inplace=True)
            return ddf
        elif yr == 'ALL':

            ddf: pd.DataFrame = self.df[allcols].copy(deep=True)
            ddf.reset_index(drop=True, inplace=True)
            return ddf

        else:
            raise Exception(f"Invalid year: {yr}")

class TaxesGDP(WV_GDP):
    fn = 'SAGDP6N_WV_2017_2022.csv'
    datadir = WV_GDP.src_dir

    def __init__(self, sagdp_fn: str = f"{datadir}/{fn}"):
        super().__init__(sagdp_fn)

        self.bea_report = self.getReport(clean=False)

        self.df: pd.DataFrame = self.bea_report.to_DF()
        self.descs = self.df.Description
        self.descs.dropna(inplace=True)
        self.descs = self.descs.apply(lambda x: x.strip())
        self.lcxx = self.mgr.get_lcxx(descs=self.descs)
        self.longs = [l.long for l in self.lcxx]

        self.all_industry_tgdp = self.get_all_industry()
        self.all_private_tgdp = self.get_all_private_industry()
        self.all_agriculture_tgdp = self.get_all_agriculture()

        self.clean_df = self.clean()

    def get_all_industry(self):
        return self.df.iloc[0,].copy()

    def get_all_private_industry(self):
        return self.df.iloc[1,].copy()

    def get_all_agriculture(self):
        return self.df.iloc[2,].copy()


    def match_desc_to_model(self, desc):
        modeld = self.longs
        if desc in modeld:
            return True
        else:
            return False

    def clean(self):
        clean_df = self.df.copy(deep=True)
        clean_df.drop(['GeoName', 'Region', 'TableName', 'IndustryClassification'], inplace=True, axis=1)
        clean_df = clean_df.iloc[0:91, ].copy()
        clean_df.Description = clean_df.Description.apply(lambda x: x.strip())
        clean_df['isinModel'] = clean_df.Description.apply(self.match_desc_to_model)
        clean_df = clean_df[clean_df['isinModel'] == True]
        clean_df.drop(['isinModel', 'GeoFIPS', 'LineCode'], inplace=True, axis=1)
        clean_df.reset_index(drop=True, inplace=True)
        return clean_df

    def getCleanDataByYear(self, yr: str = '2022'):
        data_years = ['2017', '2018', '2019', '2020', '2021', '2022']
        allcols = ['Description', 'Unit']
        allcols.extend(data_years)
        # print(f"cols: {allcols}")
        if yr in data_years:
            cols = ['Description', 'Unit', yr]
            ddf: pd.DataFrame = self.df[cols].copy(deep=True)
            ddf.reset_index(drop=True, inplace=True)
            return ddf
        elif yr == 'ALL':

            ddf: pd.DataFrame = self.df[allcols].copy(deep=True)
            ddf.reset_index(drop=True, inplace=True)
            return ddf

        else:
            raise Exception(f"Invalid year: {yr}")


class SubsGDP(WV_GDP):
    fn = 'SAGDP5N_WV_2017_2022.csv'
    datadir = WV_GDP.src_dir

    def __init__(self, sagdp_fn: str = f"{datadir}/{fn}"):
        super().__init__(sagdp_fn)
        self.bea_report = self.getReport(clean=False)
        self.df: pd.DataFrame = self.bea_report.to_DF()
        self.descs = self.df.Description
        self.descs.dropna(inplace=True)
        self.descs = self.descs.apply(lambda x: x.strip())
        self.lcxx: list[IndDescription] = self.mgr.get_lcxx(descs=self.descs)
        self.longs: list[str] = [l.long for l in self.lcxx]

        self.all_industry_sgdp = self.get_all_industry()
        self.all_private_sgdp = self.get_all_private_industry()
        self.all_agriculture_sgdp = self.get_all_agriculture()

        self.clean_df = self.clean()

    def get_all_industry(self):
        return self.df.iloc[0,].copy()

    def get_all_private_industry(self):
        return self.df.iloc[1,].copy()

    def get_all_agriculture(self):
        return self.df.iloc[2,].copy()

    def match_desc_to_model(self, desc):
        modeld = self.longs
        if desc in modeld:
            return True
        else:
            return False

    def clean(self):
        clean_df = self.df.copy(deep=True)
        clean_df.drop(['GeoName', 'Region', 'TableName', 'IndustryClassification'], inplace=True, axis=1)
        clean_df = clean_df.iloc[0:91, ].copy()
        clean_df.Description = clean_df.Description.apply(lambda x: x.strip())
        clean_df['isinModel'] = clean_df.Description.apply(self.match_desc_to_model)
        clean_df = clean_df[clean_df['isinModel'] == True]
        clean_df.drop(['isinModel', 'GeoFIPS', 'LineCode'], inplace=True, axis=1)
        return clean_df

    def getCleanDataByYear(self, yr: str = '2022'):
        data_years = ['2017', '2018', '2019', '2020', '2021', '2022']
        allcols = ['Description', 'Unit']
        allcols.extend(data_years)
        # print(f"cols: {allcols}")
        if yr in data_years:
            cols = ['Description', 'Unit', yr]
            ddf: pd.DataFrame = self.df[cols].copy(deep=True)
            ddf.reset_index(drop=True, inplace=True)
            return ddf
        elif yr == 'ALL':

            ddf: pd.DataFrame = self.df[allcols].copy(deep=True)
            ddf.reset_index(drop=True, inplace=True)
            return ddf

        else:
            raise Exception(f"Invalid year: {yr}")
























