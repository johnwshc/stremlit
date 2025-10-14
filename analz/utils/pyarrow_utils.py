import pyarrow as pa
import pandas as pd


fn = "D:\\python_apps\\Pynotebook_marimo\\notebooks\\soc_econ\\data\\SAGDP2025\\labor-productivity-detailed-industries.xlsx"

def fix(x):
    if isinstance(x,float):
        xx = int(x)
        return str(xx)
    else:
        return x

def get_df():
    df = pd.read_excel(fn)
    cols = df.iloc[1,].copy()
    cols_ser = pd.Series(list(cols))
    cols_ser = cols_ser.apply(fix)
    df = df.iloc[2:,].copy()
    df.columns = cols_ser
    return df

def get_pa():
    df = get_df()
    table = pa.Table.from_pandas(df)
    return table, df