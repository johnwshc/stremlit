import PyPDF2
import pandas as pd
import numpy as np
import json
import pathlib
from collections import OrderedDict
from datetime import datetime
from pydantic import BaseModel


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

    def __init__(self, sagdp_fn: str=test_fn):
        # print(sagdp_fn)
        if sagdp_fn.endswith('xlsx'):
            self.df: pd.DataFrame = pd.read_excel(sagdp_fn,header=0)
    
        else:
            raise Exception("file fuck up")
        self.clean_raw_data()
    
    def clean_raw_data(self):
        dff = self.df.iloc[4:].copy()
        scols = pd.Series(list(dff.iloc[0]))        
        cols = list(scols.apply(fixcol))
        dff.columns = list(cols)       
        goodcols = ['Description','2020', '2021', '2022', '2023']
        self.df = dff[goodcols].copy()
        self.df.reset_index(inplace=True, drop=True)
        self.df.drop(0, axis=0, inplace=True)
        self.df.reset_index(inplace=True, drop=True)


    