from analz.soc_econ.wv_data_utils import WV_GDP
import json
import pandas as pd
import numpy as np


class StateEMPL:

    datadir = 'f:/python_apps/flaskER/notebooks/soc_econ/data/schools/'
    src_state_employment = f"{datadir}/state_M2023_dl.xlsx"
    em_sheet1 = "state_M2023_dl"
    em_sheet2 = "Field Descriptions"
    json_dir = f"/notebooks/soc_econ/data/json/"
    prim_state_fn = f"{json_dir}prim_states.json"
    cols = ['AREA', 'AREA_TITLE', 'AREA_TYPE', 'PRIM_STATE',
            'OCC_CODE', 'OCC_TITLE', 'O_GROUP', 'TOT_EMP',
            'EMP_PRSE',	'JOBS_1000', 'LOC_QUOTIENT',
            'PCT_TOTAL', 'H_MEAN', 'A_MEAN', 'H_MEDIAN']

    @staticmethod
    def test_it():
        # df = StateEMPL.get_raw_state_dataframe(state='West Virginia')
        sempl = StateEMPL(st='West Virginia')
        return sempl

    @staticmethod
    def get_prim_state(st: str) -> [str, None]:
        print(f"in get_prim_state")
        with open(StateEMPL.prim_state_fn) as f:
            d: dict = json.load(f)
            if st in d.keys():
                return d[st]

            else:
                return None

    @staticmethod
    def get_raw_field_desc() -> pd.DataFrame:
        df_desc: pd.DataFrame = pd.read_excel(StateEMPL.src_state_employment, sheet_name=StateEMPL.em_sheet2)
        return df_desc


    @staticmethod
    def get_raw_state_dataframe(state=None) -> pd.DataFrame:

        print("in get raw state dataframe")
        df_data: pd.DataFrame = pd.read_excel(StateEMPL.src_state_employment, sheet_name=StateEMPL.em_sheet1)
        if state:
            mask = df_data.AREA_TITLE == state
            state_emp_2023_data: pd.DataFrame = df_data[mask]
            return state_emp_2023_data
        else:
            return df_data

    # *******************     StateEMPL INIT     *****************

    def __init__(self, st = 'West Virginia'):
        import os
        self.st = st
        self.prim_state = StateEMPL.get_prim_state(st)
        if not self.prim_state:
            print(f"Invalid state: {self.st}")
            raise Exception(f"InVALID STATE: {self.prim_state}")
        self.fn = f"{StateEMPL.json_dir}{self.prim_state}_2023_employment.json"
        if os.path.exists(self.fn):
            print("JSON data found")
            self.wv_df = pd.read_json(self.fn)
        else:
            print("JSON data not found: creating state df from raw data")
            self.wv_df: pd.DataFrame = StateEMPL.get_raw_state_dataframe(state=self.st)
            # remove unused columns in raw data
            self.wv_df = self.wv_df[StateEMPL.cols].copy()

    def isEd(self, x: str):
        lx = x.lower()
        if 'education' in lx:
            return True
        else:
            return False

    def save_teacher_st_data(self, st='West Virginia'):
        import os
        # get teacher df for given state, from a json file if such exists. If not save
        #  a fresh json file for quicker loading parsed vs raw data from csv or xsl
        prim_state = StateEMPL.get_prim_state(st)
        if not prim_state:
            print(f"Invalid state: {self.st}")
            raise Exception(f"InVALID STATE: {self.prim_state}")
        fn = f"{StateEMPL.json_dir}{prim_state}_2023_teachers.json"
        print(f"json file for {prim_state}:   {fn}")
        if os.path.exists(fn):
            print(f"JSON data ({fn})found")
            df: pd.DataFrame = pd.read_json(fn)
            return df
        else:
            print("JSON data not found: creating state df from raw data")
            df: pd.DataFrame = StateEMPL.get_raw_state_dataframe(state=self.st)
            # remove unused columns in raw data
            df = df[StateEMPL.cols].copy()
            # save to json file
            with open(fn, "w") as f:
                df.to_json(f, indent=4)
            return df

    def getWVTeachers(self):
        ddf = self.save_teacher_st_data(st='West Virginia')
        ddf['isEd'] = ddf.OCC_TITLE.apply(self.isEd)
        ddf = ddf[ddf['isEd'] == True].copy()
        return ddf

    def getMDTeachers(self):
        ddf: pd.DataFrame = self.save_teacher_st_data(st='Maryland')
        ddf['isEd'] = ddf.OCC_TITLE.apply(self.isEd)
        ddf = ddf[ddf['isEd'] == True].copy()
        return ddf

    def getVATeachers(self):
        ddf: pd.DataFrame = self.save_teacher_st_data(st='Virginia')
        ddf['isEd'] = ddf.OCC_TITLE.apply(self.isEd)
        ddf = ddf[ddf['isEd'] == True].copy()
        return ddf


    def getMgmtDF(self):
        ddf = self.wv_df.copy()
        ddf['isMgmt'] = self.wv_df.OCC_CODE.apply(lambda x: True if x.startswith("11-") else False)
        return ddf[ddf['isMgmt']]

    def getNonMgmtDF(self):
        ddf: pd.DataFrame = self.wv_df.copy()
        ddf['isMgmt'] = self.wv_df.OCC_CODE.apply(lambda x: True if x.startswith("11-") else False)
        non_mgmt_df = ddf[ddf['isMgmt'] == False]
        return non_mgmt_df

    def save2json(self):

        print("saving state_empl dataframe to json")
        self.wv_df.to_json(self.fn)

class SchoolSalaries:
    fn = 'school_salaries.txt'
    datadir = f"f:/python_apps/flaskER/notebooks/soc_econ/data/schools/"
    def __init__(self):
        self.ftxt = f"{SchoolSalaries.datadir}{SchoolSalaries.fn}"
        self.df = self.parseFile()


    def parseFile(self):
        with open(self.ftxt) as f:
            lines: list[str] = f.readlines()
            state_pay_list = {}
            for l in lines:
                ls  = l.split(sep=' ', maxsplit=1)
                spay =  ls[1]
                lss = spay.split(sep=' ')
                state_pay_list[lss[0]] = [lss[1]]
            df = pd.DataFrame.from_dict(state_pay_list, orient='index')
            df.columns = ['pay']
            df.pay = df.pay.apply(lambda x: x.strip("\n"))
            df.pay = df.pay.apply(lambda x: x.replace('$', ''))
            df.pay = df.pay.apply(lambda x: x.replace(',', ''))
            df.pay = df.pay.astype(int)
            return df

class NCES_WV_DATA:
    fn = 'ncesdata_D5A6AECF.xls'
    datadir = f"f:/python_apps/flaskER/notebooks/soc_econ/data/schools/"
    def init(self):
        self.df: pd.DataFrame = pd.read_excel()


