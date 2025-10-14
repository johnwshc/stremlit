from analz.utils.wv_data_2025_utils import WVGDP_2025, DATA2025, WvEmp, WvSummary
from analz.utils.wv_data_utils import WV_GDP, RealGDP, EmployByIndustry as EBI, CompGDP as Comp, CurrGDP
from analz.utils.wv_data_utils import TaxesGDP as Tax, TaxesS as Taxs, OppsGDP as Opps, SubsGDP as Subs
from analz.utils.gdp_linked_list import Node, DLL
from analz.utils.GDPTree import TNode, TNTree, TupsDict
from analz.utils.WV2022_graphs import OppSurp, Utils, DCLs, Tups, WBars, TaxSubsBars as TSBars
from config import Config
import pandas as pd

class  PA_GDP:
    sagdp_fn = f"{Config.SA_ALL_DATA_DIR}/SAGDP2_PA_1997_2024.csv"

    def __init__(self, sagdp_fn=sagdp_fn):
        if sagdp_fn.endswith('csv'):
            self.df: pd.DataFrame = pd.read_csv(sagdp_fn, header=0, sep=',')
        elif sagdp_fn.endswith('xls'):

            self.df: pd.DataFrame = pd.read_excel(sagdp_fn, sheet_name='Sheet1', header=5)

        else:
            print("bad filename: ", sagdp_fn)
        #     self.df: pd.DataFrame = pd.read_excel(sagdp_fn, header=0,sheet_name='Sheet1')
        # self.clean_raw_data()