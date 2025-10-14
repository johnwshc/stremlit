import pandas as pd
import plotly.express as px
import os
import plotly.graph_objects as go
import numpy as np

from analz.soc_econ.wv_data_utils import (WV_GDP,
                                          EmployByIndustry as EBI,
                                          RealGDP as RG, SubsGDP, CompGDP, TaxesGDP,
                                          OppsGDP)

class Tests:

    @staticmethod
    def test_penguins(self):
        pass

    @staticmethod
    def fix_2022(x: str):
        if x == '(NA)':
            x = '0'
        x = float(x)
        return x


    @staticmethod
    def testArrow():
        import pyarrow as pa

        # Create a Pandas DataFrame
        data = {'Name': ['John', 'Alice', 'Bob'],
                'Age': [25, 30, 35],
                'Salary': [50000, 60000, 70000]}
        df = pd.DataFrame(data)

        # Convert the DataFrame to an Arrow Table
        table = pa.Table.from_pandas(df)
        return table


    @staticmethod
    def test_taxable_gplot_by_yr(top=0,
                                 name='SubsGDP',
                                 yr='2022',
                                 ascending=True,
                                 istaxable=True):
        taxable = ['Nat_resource', 'Real_estate', 'Mfg', 'Retail_trade',
                   'Utils', 'Information', 'Other_priv_svs', 'Management', 'Arts',
                   'Ed_svs', 'Professional', 'Whole_trade', 'Fin', 'Transport',
                   'Construction', 'Health']
        ebi = EBI()
        df: pd.DataFrame = None
        data_cols: list =  ['Description', yr]
        if name == 'EBI':
            title = f'Total Employed persons by Industrial Sector for {yr}'
            df = ebi.getCleanDataByYear(yr)
            df = df.iloc[3:,].copy()
            ascending = False


        elif name == 'SubsGDP':
            title = f'WV Public Subsidies by Industrial Sector for {yr} in thousands of dollars'
            gdp_sector = SubsGDP(lcs=ebi.lcs)
            df: pd.DataFrame = gdp_sector.df
            # return df, data_cols
        elif name == 'RG':   # RealGDP
            title = f"WV Real Gross Domestic Product by Industrial Sector for {yr}, in millions of dollars"
            gdp_sector = RG(lcs=ebi.lcs)
            df: pd.DataFrame = gdp_sector.df
            ascending = False
        elif name == 'OppsGDP':  # Operational surplus by Industrial sector for {yr}
            title = f"Operational surplus by Industrial sector for {yr}, in thousands of dollars"
            gdp_sector = OppsGDP(lcs=ebi.lcs)
            df: pd.DataFrame = gdp_sector.df
            ascending = False

        elif name == 'TaxesGDP':
            title = f"Taxes paid by Industrial sector for {yr}, in thousands of dollars"
            gdp_sector = TaxesGDP(lcs=ebi.lcs)
            df: pd.DataFrame = gdp_sector.df
            ascending = False

        elif name == "CompGDP":
            title = f"Compensation by Industrial sector for {yr}, in thousands of dollars"
            gdp_sector = CompGDP(lcs=ebi.lcs)
            df: pd.DataFrame = gdp_sector.df
            ascending = False

        else:
            raise Exception("one at a time, please")
        pldf: pd.DataFrame = df[data_cols].copy(deep=True)
        pldf[yr] = pldf[yr].apply(Tests.fix_2022)
        # pldf.drop('Unit', axis=1, inplace=True)


        dabrevs: dict = WV_GDP.get_desc_abrevs()
        abrevs = list(dabrevs.keys())
        pldf['Description'] = abrevs
        pldf.sort_values(by=yr, axis=0, inplace=True, ascending=ascending)
        print(f"taxable = {istaxable}")
        if istaxable:
            pldf['taxable'] = pldf['Description'].apply(lambda x: True if x in taxable else False)
            df_taxable = pldf[pldf.taxable == True].copy()
            df_taxable.reset_index(drop=True, inplace=True)
            df_taxable.drop('taxable', axis=1, inplace=True)

            return pldf, df_taxable, title

        else:
            non_taxable = ['Gov','Fed_civ','Military','State_gov']
            pldf['notax'] = pldf.Description.apply(lambda x: True if x in non_taxable else False)
            df_untaxable = pldf[pldf.notax == True].copy()
            df_untaxable.reset_index(drop=True, inplace=True)
            df_untaxable.drop('notax', axis=1, inplace=True)
            return pldf, df_untaxable, title
class TPlotly:


    @staticmethod
    def my_save_png(fn='myimg.png'):

        if not os.path.exists("images"):
            os.mkdir("images")

        np.random.seed(1)

        N = 100
        x = np.random.rand(N)
        y = np.random.rand(N)
        colors = np.random.rand(N)
        sz = np.random.rand(N) * 30

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=x,
            y=y,
            mode="markers",
            marker=go.scatter.Marker(
                size=sz,
                color=colors,
                opacity=0.6,
                colorscale="Viridis"
            )
        ))

        # fig.write_image(f"images/{fn}")

        fig.show()



