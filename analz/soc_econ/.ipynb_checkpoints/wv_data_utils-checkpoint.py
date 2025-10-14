
import pandas as pd
import numpy as np
import pathlib
from collections import OrderedDict
from pydantic import BaseModel


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


        df.LineCode = df.LineCode.astype(int)
        df.Description = df.Description.astype(str)
        # df.drop('IndustryClassification', axis=1, inplace=True)
        df.reset_index(inplace=True, drop=True)
        self.data = df.to_dict()


class WV_GDP:
    #  LINE Codesin state gdp reports for major industrial classifications
    # lcs = [1, 4, 5, 6, 10, 11, 12, 34, 35, 36, 45, 51, 56, 60, 64, 66, 69, 70, 76, 79, 82, 83, 84, 85, 86]
    lcs: pd.Series =  None
    good15 = ['GeoFIPS', 'GeoName', 'Region', 'TableName', 'LineCode',
              'IndustryClassification', 'Description', 'Unit', '2017', '2018', '2019',
              '2020', '2021', '2022', '2023']
    good14 = ['GeoFIPS', 'GeoName', 'Region', 'TableName', 'LineCode',
              'IndustryClassification', 'Description', 'Unit', '2017', '2018', '2019',
              '2020', '2021', '2022']
    src_dir = "f:/python_apps/flaskER/notebooks/soc_econ/data/SAGDP/"
    json_out_dir = 'f:/python_apps/flaskER/notebooks/soc_econ/data/json/'
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


    @staticmethod
    def get_desc_abrevs():
        fn = WV_GDP.desc_abrevs_fn
        with open(fn) as f:
            lines = f.readlines()
        abrevs = {}
        for l in lines:
            s_l = l.split(sep=' ', maxsplit=1)
            if len(s_l) != 2:
                print(f"bad line: {l}")
                raise Exception("bad line in desc_abrev.txt")
            else:
                desc_ab = s_l[1]
                desc_ab = desc_ab.strip()
                s_da = desc_ab.split(sep=' --- ')
                abrevs[s_da[1]] = s_da[0]
        return abrevs

    def __init__(self, sagdp_fn: str):
        # print(sagdp_fn)
        self.fn = pathlib.Path(sagdp_fn).name
        if sagdp_fn.endswith('csv'):
            self.df: pd.DataFrame = pd.read_csv(sagdp_fn, header=0, sep=',')
        elif sagdp_fn.endswith('xls'):
            if self.fn == 'SA_EMPL_IND_WV_2017_2022.xls':
                self.df: pd.DataFrame = pd.read_excel(sagdp_fn, sheet_name='Sheet1', header=5)

            else:
                self.df: pd.DataFrame = pd.read_excel(sagdp_fn, header=0,sheet_name='Sheet1')
        # self.clean_raw_data()


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
    SA_DATA_DIR = f"f:/python_apps/flaskER/notebooks/soc_econ/data/SAGDP/"


    def __init__(self, sagdp_fn: str = f"{SA_DATA_DIR}{state_name}"):
        super().__init__(sagdp_fn)
        self.bea_report = self.getReport( clean=False)
        self.df: pd.DataFrame = self.bea_report.to_DF()
        self.clean()

    def clean(self):
        # remove non-model rows (0:7)
        self.df: pd.DataFrame = self.df.iloc[7:36, ].copy(deep=True)
        self.df.reset_index(drop=True, inplace=True)
        # Remove state and local detail
        self.df = self.df.iloc[0:-2,]
        self.df['LineCode'] = self.df['LineCode'].replace(np.nan, 0)
        self.df = self.df[self.df.LineCode != 0].copy()
        self.df.LineCode = self.df.LineCode.astype(int)
        self.df.Description = self.df.Description.apply(lambda x: x.strip())
        self.df = self.df.iloc[3:,].copy(deep=True)
        self.df.reset_index(drop=True, inplace=True)
        # df.reset_index(drop=True, inplace=True)
        self.lcs: pd.Series = self.df.Description.copy()
        # drop top general cats
        self.lcs.reset_index(drop=True, inplace=True)

        new_edf_columns = ['Description', '2017', '2018', '2019', '2020', '2021', '2022']
        self.df = self.df[new_edf_columns].copy(deep=True)

        self.df = self.df.astype({c: "int64" for c in self.df.columns[1:]})

        self.bea_report.data = self.df.to_dict()

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


class RealGDP(WV_GDP):
    fn = 'SAGDP9N_WV_2017_2023.csv'
    DATA_DIR = WV_GDP.src_dir
    def __init__(self,  sagdp_fn: str = f"{DATA_DIR}{fn}", lcs: pd.Series = None):
        super().__init__(sagdp_fn)
        self.lcs = lcs
        if lcs is None:
            raise Exception("LCS model industry list missing")
        self.bea_report = self.getReport( clean=False)
        self.df: pd.DataFrame = self.bea_report.to_DF()
        self.clean()


    def match_desc_to_model(self, desc):
        modeld = self.lcs
        for d in modeld:
            if desc == d:
                # print(f"{desc} is IN the model")
                return True
        else:
            # print(f"{desc} is NOT IN model lcs list.")
            return False

    def clean(self):
        self.df.drop(['Region', 'TableName', 'IndustryClassification'], inplace=True, axis=1)
        self.df = self.df.iloc[0:91,].copy()
        self.df.Description = self.df.Description.apply(lambda x: x.strip())
        self.df['isinModel'] = self.df.Description.apply(self.match_desc_to_model)
        self.df = self.df[self.df['isinModel'] == True]
        self.df.drop(['isinModel', 'GeoFIPS', 'LineCode'], inplace=True, axis=1)
        new_columns = ['Description', 'Unit', '2017', '2018', '2019', '2020', '2021', '2022', '2023']
        self.df = self.df[new_columns].copy(deep=True)
        self.df.reset_index(drop=True, inplace=True)

    def getCleanDataByYear(self, yr: str= '2022'):
        data_years = ['2017', '2018', '2019', '2020', '2021', '2022']
        allcols = ['Description', 'Unit']
        allcols.extend(data_years)
        # print(f"cols: {allcols}")
        if yr in data_years:
            cols = ['Description', 'Unit',yr]
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
    def __init__(self,  sagdp_fn: str = f"{datadir}{fn}", lcs: pd.Series = None):
        super().__init__(sagdp_fn)
        self.lcs = lcs
        if lcs is None:
            raise Exception("LCS model industry list missing")
        self.bea_report = self.getReport( clean=False)
        self.df: pd.DataFrame = self.bea_report.to_DF()
        self.clean()

    def match_desc_to_model(self, desc):
        modeld = self.lcs
        for d in modeld:
            if desc == d:
                return True
        else:
            return False

    def clean(self):
        self.df.drop(['GeoName','Region', 'TableName', 'IndustryClassification'], inplace=True, axis=1)
        self.df = self.df.iloc[0:91, ].copy()
        self.df.Description = self.df.Description.apply(lambda x: x.strip())
        self.df['isinModel'] = self.df.Description.apply(self.match_desc_to_model)
        self.df = self.df[self.df['isinModel'] == True].copy(deep=True)
        self.df.drop(['isinModel', 'GeoFIPS','LineCode'], inplace=True, axis=1)
        self.df.reset_index(drop=True, inplace=True)

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

    def __init__(self, sagdp_fn: str = f"{datadir}{fn}", lcs: pd.Series = None):
        super().__init__(sagdp_fn)
        self.lcs = lcs
        if lcs is None:
            raise Exception("LCS model industry list missing")
        self.bea_report = self.getReport(clean=False)
        self.df: pd.DataFrame = self.bea_report.to_DF()
        self.clean()

    def match_desc_to_model(self, desc):
        modeld = self.lcs
        for d in modeld:
            if desc == d:
                return True
        else:
            return False

    def clean(self):
        print("in upper Opps")
        self.df.drop(['GeoName', 'Region', 'TableName', 'IndustryClassification'], inplace=True, axis=1)
        self.df = self.df.iloc[0:91, ].copy()
        self.df.Description = self.df.Description.apply(lambda x: x.strip())
        self.df['isinModel'] = self.df.Description.apply(self.match_desc_to_model)
        self.df = self.df[self.df['isinModel'] == True]
        self.df.drop(['isinModel', 'GeoFIPS', 'LineCode'], inplace=True, axis=1)

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

    def __init__(self, sagdp_fn: str = f"{datadir}{fn}", lcs: pd.Series = None):
        super().__init__(sagdp_fn)
        self.lcs = lcs
        if lcs is None:
            raise Exception("LCS model industry list missing")
        self.bea_report = self.getReport(clean=False)
        self.df: pd.DataFrame = self.bea_report.to_DF()
        self.clean()

    def match_desc_to_model(self, desc):
        modeld = self.lcs
        for d in modeld:
            if desc == d:
                return True
        else:
            return False

    def clean(self):
        self.df.drop(['GeoName', 'Region', 'TableName', 'IndustryClassification'], inplace=True, axis=1)
        self.df = self.df.iloc[0:91, ].copy()
        self.df.Description = self.df.Description.apply(lambda x: x.strip())
        self.df['isinModel'] = self.df.Description.apply(self.match_desc_to_model)
        self.df = self.df[self.df['isinModel'] == True]
        self.df.drop(['isinModel', 'GeoFIPS', 'LineCode'], inplace=True, axis=1)

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

    def __init__(self, sagdp_fn: str = f"{datadir}{fn}", lcs: pd.Series = None):
        super().__init__(sagdp_fn)
        self.lcs = lcs
        if lcs is None:
            raise Exception("LCS model industry list missing")
        self.bea_report = self.getReport(clean=False)
        self.df: pd.DataFrame = self.bea_report.to_DF()
        self.clean()

    def match_desc_to_model(self, desc):
        modeld = self.lcs
        for d in modeld:
            if desc == d:
                return True
        else:
            return False

    def clean(self):
        self.df.drop(['GeoName', 'Region', 'TableName', 'IndustryClassification'], inplace=True, axis=1)
        self.df = self.df.iloc[0:91, ].copy()
        self.df.Description = self.df.Description.apply(lambda x: x.strip())
        self.df['isinModel'] = self.df.Description.apply(self.match_desc_to_model)
        self.df = self.df[self.df['isinModel'] == True]
        self.df.drop(['isinModel', 'GeoFIPS', 'LineCode'], inplace=True, axis=1)

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

    def __init__(self, sagdp_fn: str = f"{datadir}{fn}", lcs: pd.Series = None):
        super().__init__(sagdp_fn)
        self.lcs = lcs
        if lcs is None:
            raise Exception("LCS model industry list missing")
        self.bea_report = self.getReport(clean=False)
        self.df: pd.DataFrame = self.bea_report.to_DF()
        self.clean()

    def match_desc_to_model(self, desc):
        modeld = self.lcs
        for d in modeld:
            if desc == d:
                return True
        else:
            return False

    def clean(self):
        self.df.drop(['GeoName', 'Region', 'TableName', 'IndustryClassification'], inplace=True, axis=1)
        self.df = self.df.iloc[0:91, ].copy()
        self.df.Description = self.df.Description.apply(lambda x: x.strip())
        self.df['isinModel'] = self.df.Description.apply(self.match_desc_to_model)
        self.df = self.df[self.df['isinModel'] == True]
        self.df.drop(['isinModel', 'GeoFIPS', 'LineCode'], inplace=True, axis=1)

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
























