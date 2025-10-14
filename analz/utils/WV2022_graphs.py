import pandas as pd
from analz.utils.wv_data_utils import GDPMgr, LCX, IndDescription as ID
from analz.utils.wv_data_2025_utils import WvSummary
from analz.utils.wv_data_utils import RealGDP, EmployByIndustry as EBI, CompGDP as Comp, CurrGDP
from analz.utils.wv_data_utils import TaxesGDP as Tax, TaxesS as Taxs,  SubsGDP as Subs
from analz.utils.wv_data_utils import OppsGDP as Opps
from analz.utils.GDPTree import TNTree, TupsDict

# types
from collections import namedtuple
import datetime

# graphing
import plotly.express as px
# import plotly.figure_factory as ff
# from dash import Dash, dcc, html, Input, Output
# import seaborn.objects as so
# import seaborn as sns
# import matplotlib.pyplot as plt
# import plotly.graph_objects as go


# **********************************************************************
# custom global data
# *********************************************************************

GIndex = namedtuple('GIndex', ['id', 'level'])
concord_file = "json/gdp_emp_desc_index_concordance.txt"
pd.set_option("mode.copy_on_write", True)
non_taxable = ['Government and government enterprises', 'Federal civilian',
                          'Military', 'State and local', 'State government', 'Local government']

# TUPLES of occupation and classification LEVEL in BEA spreadsheets (via spaces)

class Tups:
    def __init__(self):
        self.td = TupsDict()  #  "industrial classification / level dict"
        self.tn = TNTree.buildTNTreeFactory(self.td) #  classification tree
        self.tn.root.add_children(self.td)

#  DATA CLASSES ON EMPLOYMENT, GDP, 7 YR SUMMARY, ETC

class DCLs:
    # td = Tups().td
    # wvemp = WvEmp()  #  employee data class
    # wvgdp_tups = td.wvgdp
    # dfemp = wvemp.df_emp # employee dataframe
    # wvgdp_2025 = WVGDP_2025()
    # df_curr_gdp = wvgdp_2025.dff
    wvsumm = WvSummary() # Summary data class
    df_summ = wvsumm.df_summary
    ebi = EBI()
    gdp_mgr = GDPMgr()
    lcx: LCX = gdp_mgr.lcx
    lcs: list[ID] = lcx.lcs
    longs: list[str] = [id.long.strip() for id in lcs]
    shorts: list[str] = [id.short.strip() for id in lcs]
    taxes = Tax()
    tax_subs = Taxs()
    subs = Subs()

    # LIST OF TAXABLE INDUSTRIAL SECTORS (NON GOVERNMENTAL, MOSTLY)

    taxable = [t for t in longs if t not in non_taxable]
    # lcs_short = lcs.apply(Utils.shorty)

    # METHOD TO SET TAXABLE OR NOT ON INDUSTRIAL SECTORS

    @staticmethod
    def match_desc_to_model(desc):
        modeld = DCLs.longs
        if desc in modeld:
            return True
        else:
            return False

#  UTILITIES FOR PROCESSING DATA FRAMES

class Utils:

    yrs = ['2017','2018','2019','2020','2021','2022']

    @classmethod
    def pre_render_export(cls):
        # /// script
        # requires-python = ">=3.9"
        # dependencies = [
        #     "playwright",
        # ]
        # ///

        import os
        import subprocess
        from playwright.sync_api import sync_playwright

        input_file = "input.html"
        output_file = "output.html"

        subprocess.run(["playwright", "install", "chromium-headless-shell"], check=True)

        with sync_playwright() as p:
            with p.chromium.launch(headless=True) as browser:
                page = browser.new_page()
                page.goto(
                    f"file:///{os.path.abspath(input_file)}",
                    wait_until="networkidle",
                )
                with open(output_file, "w", encoding="utf-8") as f:
                    f.write(page.content())

    @staticmethod
    def get_taxable_func(df: pd.DataFrame):

        df.dropna(inplace=True)
        df.Description = df.Description.apply(str)
        descs = list(df.Description.apply(str.strip))
        df.Description = descs
        ser_descs = pd.Series(descs)
        in_taxable = []
        for d in list(ser_descs):
            if d in DCLs.taxable:
                # print(f"{d}  IS TRUE")
                in_taxable.append(True)
            else:
                # print(f"{d} IS FALSE")
                in_taxable.append(False)

        df['in_taxable'] = in_taxable
        df_taxable = df[df.in_taxable == True].copy(deep=True)
        # print(f"input to getlcxx\n: {df_taxable.Description.head()}")
        lcxx = DCLs.gdp_mgr.get_lcxx(df_taxable.Description)
        longs = [l.long.strip() for l in lcxx]
        shorts = [s.short.strip() for s in lcxx]
        descs = df_taxable.Description.apply(str.strip)
        ldescs = list(descs)

        # print(f"df_taxable len BEFORE isInModel: {len(df_taxable)}")

        df_taxable['isInModel'] = df_taxable.Description.apply(lambda x: True if str(x).strip() in longs else False)
        df_taxable = df_taxable[df_taxable['isInModel'] == True].copy(deep=True)
        # print(f"df_taxable len AFTER isInModel: {len(df_taxable)}")

        df_taxable.reset_index(drop=True, inplace=True)

        df_taxable['Desc'] = df_taxable.Description.apply(Utils.shorty)

        for y in Utils.yrs:
            df_taxable[y] = df_taxable[y].astype(int)
            df_taxable[y] = df_taxable[y].apply(lambda x: x * 1000)
        if 'Unit' in list(df.columns):
            df_taxable.drop('Unit', axis=1, inplace=True)
        df_taxable.drop('in_taxable', axis=1, inplace=True)

        df_taxable.reset_index(drop=True, inplace=True)
        # df_taxable.head()
        return df_taxable


    @staticmethod
    def to_datetime(yr: str):
        yrs = Utils.yrs
        # You can choose any default month and day if only the year is provided
        if yr in yrs:
            yr_int = int(yr)
            datetime_object = datetime.datetime(yr_int, 12, 31)
            return datetime_object
        else:
            raise Exception(f'Invalid year {yr}')

    @staticmethod
    def shorty(x):
        if not isinstance(x, str):
            raise Exception(f'Invalid shorty {x}')

        x = x.strip()
        lcs = DCLs.lcs
        for ls in lcs:
            l = ls.long.strip()
            if l == x:
                return ls.short.strip()

        print(f"x = {x}:  --  not found in lcs")
        return x

    #     TEST APPS ON CONCAT AND MELT FOR DATAFRAMES

    @staticmethod
    def test_melt(): # Create a sample DataFrame
        data = {'Name': ['Alice', 'Bob', 'Charlie'],
                'Score_Math': [90, 85, 92],
                'Score_Science': [88, 91, 89]}
        df_t = pd.DataFrame(data)

        # Melt the DataFrame
        df_melted2 = pd.melt(df_t, id_vars=['Name'],
                            value_vars=['Score_Math', 'Score_Science'],
                            var_name='Subject',
                            value_name='Score')

        print(df_melted2)

    @staticmethod
    def test_concat():

        # Create two Series with different sorted indexes
        s1 = pd.Series([10, 20, 30], index=[0, 2, 4])
        s2 = pd.Series([100, 200, 300], index=[1, 2, 3])

        # Concatenate along the column axis (axis=1)
        # Default join='outer' will align by index and fill NaNs
        df_concatenated = pd.concat([s1, s2], axis=1)
        print(df_concatenated)

        # Concatenate with inner join
        df_inner_join = pd.concat([s1, s2], axis=1, join='inner')
        print(df_inner_join)

        # Concatenate ignoring the index
        df_ignore_index = pd.concat([s1, s2], axis=1, ignore_index=True)
        print(df_ignore_index)

# CLASSES FOR OPERATIONAL SURPLUS, COMPENSATION AND EMPLOYMENT BY INDUSTRY

class OppSurp:

    def __init__(self):
        # COMPENSATION

        self.comp = Comp()
        self.cdf = self.comp.clean_df
        self.cdf_taxable = self.get_cdf_taxable()


        # EMPLOYMENT

        self.edf = DCLs.ebi.clean_df
        self.edf_taxable = self.get_edf_taxable()


        # OPERATIONAL SURPLUS

        self.opps = Opps()
        self.odf_taxable = self.get_opps()

    def get_cdf_taxable(self):

        cdf = self.cdf  # cdf.columns
        return Utils.get_taxable_func(cdf)
        # cdf['taxable'] = cdf['Description'].apply(lambda x: True if x in DCLs.taxable else False)
        # cdf_taxable = cdf[cdf.taxable == True].copy(deep=True)
        # cdf_taxable['Desc'] = cdf_taxable.Description.apply(Utils.shorty)
        #
        # for y in Utils.yrs:
        #     cdf_taxable[y] = cdf_taxable[y].astype(int)
        #     #  BEA units were in thousands for compensation values
        #     cdf_taxable[y] = cdf_taxable[y].apply(lambda x: x * 1000)
        # cdf_taxable.drop('Unit', axis=1, inplace=True)
        # cdf_taxable.drop('taxable', axis=1, inplace=True)
        # cdf_taxable.reset_index(drop=True, inplace=True)
        # return cdf_taxable


    def get_edf_taxable(self):
        self.edf['taxable'] = self.edf['Description'].apply(lambda x: True if x in DCLs.taxable else False)
        self.edf.Description.apply(lambda x: True if x in DCLs.taxable else False)
        edf_taxable = self.edf[self.edf.taxable == True].copy(deep=True)
        edf_taxable['Desc'] = edf_taxable.Description.apply(Utils.shorty)

        # edf_taxable.drop('Unit', axis=1, inplace=True)
        edf_taxable.drop('taxable', axis=1, inplace=True)
        edf_taxable.reset_index(drop=True, inplace=True)
        return edf_taxable

    def get_opps(self):
        odf = self.opps.clean_df
        # print(f"in get_odf, {type(odf)}")
        return Utils.get_taxable_func(odf)
        # print(odf.columns)
        # odf['taxable'] = odf['Description'].apply(lambda x: True if x in DCLs.taxable else False)
        # odf_taxable = odf[odf.taxable == True].copy(deep=True)
        # odf_taxable['Desc'] = odf_taxable.Description.apply(Utils.shorty)
        # for y in Utils.yrs:
        #     odf_taxable[y] = odf_taxable[y].astype(int)
        #     odf_taxable[y] = odf_taxable[y].apply(lambda x: x * 1000)
        # # odf_taxable.drop(['Unit'], axis=1, inplace=True)
        # odf_taxable.drop('taxable', axis=1, inplace=True)
        #
        # odf_taxable.reset_index(drop=True, inplace=True)
        # return odf_taxable


    def show_opp_surplus_2022(self):
        df = self.odf_taxable
        ddf: pd.DataFrame = df[['Description', '2022']].copy(deep=True)
        ddf['Desc'] = ddf.Description.apply(Utils.shorty)
        ddf.sort_values('2022', inplace=True, axis=0)
        ddf.reset_index(drop=True, inplace=True)
        fig = px.bar(ddf, y='2022', x='Desc', text_auto='.2s',
                     labels={'2022': 'Operational Surplus', 'Desc': 'Taxable industry descriptions'},
                     title="West Virginia Operational Surplus by Taxable Industries for 2022")
        fig.update_xaxes(tickangle=-45)
        fig.show()



    def show_compensation_2022_by_industry(self, taxable=True):
        df = self.cdf
        df['Desc'] = df.Description.apply(Utils.shorty)
        for y in Utils.yrs:
            df[y] = df[y].astype(int)
        ddf = self.cdf_taxable.copy(deep=True)
        ddf_show = ddf[['Desc', '2022']].copy(deep=True)


        ddf_show.sort_values(by='2022', inplace=True, axis=0)
        ddf_show.reset_index(drop=True, inplace=True)
        if taxable:
            # print(ddf_taxable.head())
            fig = px.bar(ddf_show, y='2022', x='Desc', text_auto='.2s',
                         labels={'2022': 'Compensation', 'Desc': 'industry description'},
                         title="West Virginia Compensation by Industry (incl. Public) for 2022")
            fig.update_xaxes(tickangle=-45)
            fig.show()
        else:
            df_show = df[['Desc', '2022']].copy(deep=True)
            df_show.sort_values(by='2022', inplace=True, axis=0)
            df_show.reset_index(drop=True, inplace=True)


            fig = px.bar(df_show, y='2022', x='Desc', text_auto='.2s',
                         labels={'2022': 'Compensation', 'Desc': 'industry description'},
                         title="West Virginia Compensation by Industries (incl. public) for 2022")
            fig.update_xaxes(tickangle=-45)
            fig.show()



    def show_employment_2022_by_industry(self, taxable=False):
        df = self.edf

        ddf: pd.DataFrame = df[['Description', '2022']].copy(deep=True)
        # ddf['2022m'] = ddf['2022']
        ddf['Desc'] = ddf.Description.apply(Utils.shorty)
        ddf['taxable'] = ddf.Description.apply(lambda x: True if x in DCLs.taxable else False)
        if taxable:
            ddf_taxable = ddf[ddf.taxable == True].copy(deep=True)
            ddf_taxable.sort_values('2022', inplace=True, axis=0)
            ddf_taxable.reset_index(drop=True, inplace=True)
            # print(ddf_taxable.head())
            fig = px.bar(ddf_taxable, y='2022', x='Desc', text_auto='.2s',
                         labels={'2022': 'Employment', 'Desc': 'Taxable industry description'},
                         title="West Virginia Employment by Taxable Industries for 2022")
            fig.update_xaxes(tickangle=-45)
            fig.show()
        else:
            ddf.sort_values('2022', inplace=True, axis=0)
            ddf.reset_index(drop=True, inplace=True)

            fig = px.bar(ddf, y='2022', x='Desc', text_auto='.2s',
                         labels={'2022': 'Employment', 'Desc': 'industry description'},
                         title="West Virginia Employment by All Industries for 2022")
            fig.update_xaxes(tickangle=-45)
            fig.show()




    def compute_comp_surp_per_emp(self):  # cmpt, empt, oppt):
        cmpt = self.cdf_taxable
        empt = self.edf_taxable
        oppt = self.odf_taxable
        et = empt[['Desc', '2022']].copy()
        ct = cmpt[['Desc', '2022']].copy()
        ot = oppt[['Desc', '2022']].copy()
        ot.rename(columns={'2022': 'Operational_Surplus'}, inplace=True)
        ecm = pd.merge(et, ct, left_index=True, right_index=True)
        ecm.columns = ['Description', 'Employment', 'Desc', 'Compensation']
        ecm.drop('Description', inplace=True, axis=1)
        # ecm.Employment = ecm.Employment.astype(int)
        # ecm.Compensation = ecm.Compensation.astype(int)
        ecm['Comp_Per_Employee'] = ecm.apply(lambda row: row.loc['Compensation'] / row.loc['Employment'], axis=1)

        df = ecm[['Desc'] + [col for col in ecm.columns if col != 'Desc']]

        ecom = pd.merge(df, ot, left_index=True, right_index=True)
        ecom.drop('Desc_y', inplace=True, axis=1)
        ecom.rename(columns={'Desc_x': 'Short_Description'}, inplace=True)
        fx = lambda row: row.loc['Operational_Surplus'] / row.loc['Employment']
        ecom['Surplus_per_employee'] = ecom.apply(fx, axis=1)

        # print(ecom.head())
        return ecom


    # def show_comp_surp_per_emp(self):



        #  @staticmethod
        #  def xygraph(df_surp, df_comp):
        #
        #
        #     # months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
        #     #           'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        #     industry = ecm['Short_Description']
        #     opps = ecm['Operational_Surplus']
        #     opps_per_emp = ecm['Surplus_per_employee']
        #     comp = ecm['Compensation']
        #
        #     fig = go.Figure()
        #     fig.add_trace(go.Bar(
        #         x=industry,
        #         y=opps,
        #         name='Operational Surplus',
        #         marker_color='indianred'
        #     ))
        #     fig.add_trace(go.Bar(
        #         x=industry,
        #         y=comp,
        #         name='Compensation',
        #         marker_color='lightsalmon'
        #     ))
        #
        #     # Here we modify the tickangle of the xaxis, resulting in rotated labels.
        #     fig.update_layout(barmode='group', xaxis_tickangle=-45)
        #     fig.show()

    def add_cols(self,r):
        x = int(r.Compensation) + int(r.Operational_Surplus)
        return x

    def show_comp_surp_bars(self, taxable=True):

        pe_df = self.compute_comp_surp_per_emp()

        pe_df['total_comp_surp'] = pe_df.apply(self.add_cols, axis=1)
        pe_df_show = pe_df[['Short_Description', 'Compensation', 'Operational_Surplus']].copy()
        df_melted = pd.melt(pe_df_show, id_vars=['Short_Description'],
                                    value_vars=['Compensation', 'Operational_Surplus'], value_name='comp_surp')
        fig = px.bar(df_melted, x='Short_Description', y='comp_surp',
                 title='West Virginia 2022 Compensation and Surplus for private, taxable Industries.',
                 hover_data=['comp_surp', 'comp_surp'], color='variable',
                 labels={'comp_surp': 'Compensation/Surplus'}, height=400)
        fig.update_xaxes(tickangle=-45)

        fig.show()

#          **************************************************************************
#                           WBARS
#          **************************************************************************

class WBars:


# Remove non taxable (government, e.g.)
    # non_taxable = Utils.non_taxable
    taxable = [t for t in DCLs.lcs if t.long not in non_taxable]
    longs = DCLs.longs
    lcs: list[ID] = DCLs.lcs
    no_guv_lcs: list[ID] = lcs[0:19].copy()
    one_guv_lcs: list[ID] = lcs[0:20].copy()

    def __init__(self):

        # summary GDP data from 2017 - 2022
        self.dfs = DCLs.df_summ

        # GDP in Current Dollars

        self.curr_gdp = CurrGDP()
        self.curr_df = self.curr_gdp.df

        # Employment by business sector

        self.ebi = DCLs.ebi
        self.edf = DCLs.ebi.df  # employee data

        # Real GDP

        self.rgdp = RealGDP()
        self.rdf = self.rgdp.df  # real gdp data
        self.rdf_taxable = self.get_rgdp_taxable()




    def get_rgdp_taxable(self) -> pd.DataFrame:
        txlongs = [w.long for w in WBars.taxable]

        self.rdf['taxable'] = self.rdf.Description.apply(lambda x: True if str(x).strip() in txlongs else False)

        rdf_taxable = self.rdf[self.rdf.taxable == True].copy(deep=True)
        rdf_taxable.drop('taxable', inplace=True, axis=1)
        # add shortened description field
        rdf_taxable['Desc'] = rdf_taxable.Description.apply(Utils.shorty)
        # set rdf  values to millions of dollars
        for y in Utils.yrs:
            rdf_taxable[y] = rdf_taxable[y].apply(lambda x: x * 1000000)
            rdf_taxable[y].astype(int)
        return rdf_taxable

    def show_real_nom_gdp(self):

        df = self.dfs[['Description', '2017', '2018', '2019', '2020', '2021', '2022']].copy()
        sdvals = ['Real GDP', 'Chained Indexes', 'Curr GDP', 'Compensation', 'Surplus',
                  'Taxes minus subsidies', 'Taxes', 'Subsidies']
        df['short_desc'] = sdvals
        # select real and curr gdp rows, separate out the gdp real index row
        df_gdp = df.iloc[[0,2]].copy(deep=True)
        df_gdp.reset_index(drop=True, inplace=True)
        ser_gdp_idx = df.iloc[1,].copy(deep=True)
        df_gdp = df_gdp.drop("Description", axis=1)
        df_gdp_disp = df_gdp[['short_desc', '2017', '2018', '2019', '2020', '2021', '2022']]
        #  make short desc column the index
        df_indexed = df_gdp_disp.set_index('short_desc')
        #  creat new row for Years values
        new_row = list(df_indexed.columns)
        years = {k:[k] for k in new_row}
        new_row_df = pd.DataFrame(years)
        dfx = pd.concat([df_indexed, new_row_df], ignore_index=False)
        # rename years row index value
        df_renamed = dfx.rename(index={0: 'Years'})
        # Transpose dataframe
        df_rt = df_renamed.T
        # df_renamed_t = get_real_nom_gdp(df_summ)
        # draw line graph of wv gdp
        fig = px.line(df_rt, x='Years', y=['Real GDP', 'Curr GDP'],
                      labels={"value": "millions of dollars"}, title='WV GDP 2017 - 2022 in MILLIONS')
        fig.show()

    def get_current_real_concat(self):
        dfc = self.curr_gdp.df
        dfc_2022 = dfc[['Description', '2022']].copy()
        dfc_2022.reset_index(drop=True, inplace=True)
        dfr = self.rdf # real gdp calcs
        dfr.reset_index(drop=True, inplace=True)
        serreal = dfr['2022']
        serreal.name = "Real_2022"
        serreal.reset_index(drop=True, inplace=True)
        df_con = pd.concat([dfc_2022, serreal], axis=1)
        return df_con

    def show_real_2022_gdp(self):
        df = self.rgdp.clean_df[['Description', '2022']].copy(deep=True)


        df['Desc'] = df['Description'].apply(Utils.shorty)
        # print(f"in show_curr_2022_gdp: shorties: \n {df.Desc.head(20)}")
        df.sort_values(by="2022", inplace=True, ascending=True)
        # df.drop('Description',inplace=True, axis=1)
        # df["Description"] = df.Desc
        # df.drop([0, 1], inplace=True, axis=0)

        df.reset_index(drop=True, inplace=True)

        fig1 = px.bar(df, y='2022', x='Desc', text_auto='.2s',
                      labels={'Desc': 'Industry Description', '2022': "WV GDP (millions of 2022 'Real' dollars)"},
                      height=600,
                      title="WV 2022 'REAL' GDP by Industry, including Government")

        fig1.update_xaxes(tickangle=-45)
        fig1.show()


    def show_curr_2022_gdp(self):
        df = self.curr_gdp.clean_df[['Description', '2022']].copy(deep=True)
        df = df.dropna()


        df['Desc'] = df['Description'].apply(Utils.shorty)
        # print(f"in show_curr_2022_gdp: shorties: \n {df.Desc.head(20)}")
        df.sort_values(by="2022", inplace=True, ascending=True)
        # df.drop('Description',inplace=True, axis=1)
        # df["Description"] = df.Desc
        # df.drop([0,1], inplace=True, axis=0)



        df.reset_index(drop=True, inplace=True)

        fig1 = px.bar(df, y='2022', x='Desc', text_auto='.2s',
                      labels={'Desc': 'Industry Description', '2022': 'GDP (millions of Current dollars)'},
                      height=600,
                      title="WV 2022 'CURRENT DOLLAR' GDP by Industry, including Government")

        fig1.update_xaxes(tickangle= -45)
        fig1.show()


class TaxSubsBars:
    def __init__(self):

        self.taxes = DCLs.taxes
        self.tdf = DCLs.taxes.df
        self.tdf_taxable = Utils.get_taxable_func(self.tdf)


        self.subs = DCLs.subs
        self.sdf = DCLs.subs.df
        self.sdf_taxable = Utils.get_taxable_func(self.sdf)

        self.tax_subs = DCLs.tax_subs
        self.tsdf = DCLs.tax_subs.df
        self.tax_subs_taxable = Utils.get_taxable_func(self.tsdf)


    def show_taxes_bars(self):
        df = self.tdf
        cdf = self.tdf_taxable
        cdf = cdf[['Description', '2022']].copy(deep=True)
        cdf.sort_values('2022', inplace=True)
        cdf['Desc'] = cdf.Description.apply(Utils.shorty)
        cdf.reset_index(drop=True, inplace=True)
        # print(df.head())
        fig = px.bar(cdf, y='2022', x='Desc', text_auto='.2s',
                     labels={'2022': '2022 Current Dollars', 'Desc': "Taxable Industries"},
                     title="Taxes by Industry for 2022")
        fig.update_xaxes(tickangle=-45)
        fig.show()


    def show_subs_bars(self):
        df = self.sdf_taxable
        df = df[['Description', '2022']].copy(deep=True)
        df.sort_values('2022', inplace=True)
        df['Desc'] = df.Description.apply(Utils.shorty)
        df.reset_index(drop=True, inplace=True)
        fig = px.bar(df, y='2022', x='Desc', text_auto='.2s',
                     labels={'2022': '2022 Current Dollars', 'Desc': "Taxable Industries"},
                     title="Subsides by Industry for 2022")

        fig.update_xaxes(tickangle=-45)
        fig.show()

    def show_tax_minus_subs_bars(self):
        df = self.tax_subs_taxable
        df = df[['Description', '2022']].copy(deep=True)
        df.sort_values('2022', inplace=True)
        df['Desc'] = df.Description.apply(Utils.shorty)
        df.reset_index(drop=True, inplace=True)
        fig = px.bar(df, y='2022', x='Desc', text_auto='.2s',
                     labels={'2022': '2022 Current Dollars', 'Desc': "Taxable Industries"},
                     title="Taxes Minus Subsides by Industry for 2022")

        fig.update_xaxes(tickangle=-45)
        fig.show()






