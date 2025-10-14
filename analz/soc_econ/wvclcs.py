import pydantic
from pydantic import BaseModel
from typing import Optional, List
from analz.mongo.mongo_conn import MongoERConn
import json
from config import Config
from pathlib import Path


# mconn = MongoERConn(serv='localhost')
# mclient = mconn.mc

data_title = "West Virginia AFL-CIO Central Labor Councils"
orig_data_file = 'D:\\python_apps\\Pynotebook_marimo\\clc_pres_data_edit.txt'
with open(orig_data_file, 'r', encoding='utf-8') as f:
    orig_txt = f.read()

# otxt = """Brooke-Hancock Labor Council, AFL-CIO;Fritz Frohnapfel;ffritzclc@amail.com;1-304-479-9913;Brooke & Hancock;
#  6:30 PM — 2" Monday;USW #2911 Union Hall, 2971 West Street, Weirton, WV 26062;1532 Walker Road, Follansbee, WV 26037
#
#
# Eastern Panhandle Central Labor Council, AFL-CIO;jbc4re@yahoo.com;1-410-499-4873;Berkeley, Grant,
# Hampshire, Hardy, Jefferson, Mineral & Morgan;
# 5:30 PM - 3 Tuesday;IBEW Local Union 307 Office, 3372 Winchester Ave., Martinsburg, WV 25401;
# SAME
#
# Kanawha Valley Labor Council, AFL-CIO;Paul Breedlove;pbreedlove@uanet.org;
# (304) 553-3939;Boone, Braxton, Clay, Kanawha, Putnam, & part of Fayette;5:30 PM
# 24 Monday; VW State Building Trades, 600 Leon Sullivan Way, Charleston, WV 25301;SAME
#
# Marion County, AFL-CIO;Mark Dorsey;markdorseyumwa@live.com;304-777-7642;Marion;6:00 PM — 2" Thursday;UMWA Bldg.
# 1414 Country Club Rd., Fairmont, WV 26554;SAME
#
# Marshall, Wetzel, Tyler Central Labor Council, AFL-CIO; — Art (Sonny) Oakland;, President
# awo53@frontier.com;304-551-3013;Marshall, Wetzel, & Tyler;7:00 PM -- 1s* Wednesday;
# Marshall County Courthouse, 7'" Street, Moundsville, WV 26041;1320 9" Street, Moundsville, WV 26041
#
# Mason-Jackson-Roane Labor Council, AFL-CIO;Dave Martin;davem@casinternet.net;
# 304-532-2842;Jackson, Mason & Roane;6:00 PM — 2" Tuesday;USW 5668 Union Hall
# #52 NuChance Drive, Rt. 2 South, Ravenswood, WV 26164;104 Ernest Street - Spencer, WV 26276
#
# Monongalia-Preston Labor Council, AFL-CIO;Andy Walters;awalters@wvaficio.org;
# 304-344-3557; Monongalia, Preston, & Tucker;5:30 PM — 3 Monday;U.A. Plumbers
# & Pipefitters 152 Union Hall, 100 Richard Road, Morgantown, 26501; 501 Leon Sullivan Way, Charleston, WV 25301
#
# North Central West Virginia Labor Council, AFL-CIO;Steve Perdue;
# sperdue9609@yahoo.com; 304-203-8744; Barbour, Doddridge, Gilmer Harrison, Lewis, Upshur & Taylor;
# 6:30 PM Currently, meetings are by conference call, contact President Perdue for information;
# 609 Drummond Street, Clarksburg, WV 26301
#
# Ohio Valley Trades & Labor Assembly, AFL-CIO;Dave Cantrell;cantrelld304@amail.com;1-304-
# 281-3387; Ohio;7:00 PM -- 24 Thursday; IBEW Local 141 Union Hall, 82 Burkham Court, Wheeling, WV 26003;
# P.O. Box 6440, Wheeling, WV 26003
#
# Parkersburg Area Labor Council, AFL-CIO;Andrew Stump;
# andrew.p.stump@gmail.com;304-991-6890; Calhoun, Pleasanis, Ritchie, Wirt, & Wood;
#  7:00 PM -- 4 Monday;Parkersburg-Marietta Building & Construction Trades Office, 2400 %
# Garfield Avenue, Parkersburg, WV 26101;P.O. Box 102, Parkersburg, WV 26102
#
# South Central Labor Council, AFL-CIO;Randy Halsey; rhalsey@aft.wvorg; (304) 575-0050;
# McDowell; Mercer, Raleigh, Summers, Wyoming & part of Fayette;6:30 PM — 2"¢ Tues.; UMWA
# Union Hall, 2306 South Fayette Street, Beckley, WV 25801; P.O. Box 322 Beckley WV 25812
#
# Southeastern Central Labor Council, AFL-CIO; Phil Bostic;
# local_1182@yahoo.com; 304-536-2055; Greenbrier, Monroe, Nicholas, Pocahontas & Webster;
# 7:00 PM. 2" Wednesday; Workers United Hall, 500 Main Street West, White Sulphur Springs, WV
# 24986; SAME
#
# Southwestern District Labor Council, AFL-CIO;Justin Altizer; mutrumpeter1@qmail.com;
# (304) 360-2587; Cabell, Wayne, Lincoln, Logan, & Mingo;6:00 PM — 2"4 Monday;
# SEIU 1199 Union Office, 501 5" Avenue - Suite #2, Huntington, WV 25701;SAME"""
#




class CLC_Prez(BaseModel):
    name: str
    president: str
    email: str
    phone: str
    counties: List[str]
    meeting: str
    meeting_address: str
    postal_address: str


class WVCLC:
    presidents_file = Path(f"{Config.basedir}/json/clc_presidents.json")
    csv_file = f"{Config.basedir}/csv/clc_presidents.csv"
    labels = ['name', 'president', 'email', 'phone', 'counties', 'meeting', 'meeting_address', 'postal_address']
    short_labels = ['name', 'president', 'email', 'phone', 'meeting', 'meeting_address', 'postal_address']
    short_short_labels = ['name', 'president', 'email', 'phone']


    @classmethod
    def clc_pres_data_from_json(cls):
        with open(cls.presidents_file.as_posix(), 'r', encoding='utf-8') as f:
            dclcs = json.load(f)
            clcs =  {k:CLC_Prez(**v)for k,v in dclcs.items()}
            return clcs

    @classmethod
    def clc_presidents_parser1(cls):

        cdata = []
        clcs = []
        paras = orig_txt.split('\n\n')
        for p in paras:
            p = p.strip()
            cdata.append(p)

        for c in cdata:
            attrs = c.split(';')
            catters = [at.strip() for at in attrs]
            cz = list(zip(WVCLC.labels, catters))
            dcz = {k: v for k, v in cz}
            counties = dcz['counties'].split(',')
            dcz['counties'] = counties
            clc_p = CLC_Prez(**dcz)
            clcs.append(clc_p)
        d_clcs = {clc.name:clc for clc in clcs}
        return d_clcs


    def __init__(self):
        self.clc_presidents: dict = {}
        if Path.exists(WVCLC.presidents_file):

            self.clc_presidents = WVCLC.clc_pres_data_from_json()
        else:
            self.clc_presidents = self.clc_presidents_parser1()

        self.df = self.to_DF()

    def to_dict(self):
        clcs: dict = self.clc_presidents
        clcs_dict = {k: v.model_dump() for k,v in clcs.items()}
        return clcs_dict

    def to_json(self):
        clcs_dict = self.to_dict()
        with open(f'{Config.basedir}/json/clc_presidents.json', 'w', encoding='utf-8') as f:
            json.dump(clcs_dict, f, ensure_ascii=False, indent=4)
        return json.dumps(clcs_dict)

    def to_DF(self, short=True):
        import pandas as pd
        data = []
        for k,v in self.clc_presidents.items():
            dv = v.model_dump()
            del dv['counties']
            if short:
                del dv['meeting']
                del dv['meeting_address']
                del dv['postal_address']
            data.append(dv)
        df = pd.DataFrame(data)
        return df

    def to_gmail_csv(self):
        df = self.to_DF(short=False)
        dff = df[['name', 'president','email', 'phone']].copy(deep=True)
        dff.columns = ["Organization Name", "Last Name", "Email", "Phone"]
        dff.to_csv(WVCLC.csv_file, index=False)

        #  "Name" and "E-mail 1 – Value"


    def find_pres(self, expr:str) -> List[CLC_Prez]|list[None]:
        matches = []
        for k, v in self.clc_presidents.items():
            if expr in k:
                matches.append(v)
        return matches


# def parser2(cdata: List[str]):
#     labels = ['name', 'president', 'email', 'phone', 'counties', 'meeting', 'meeting_address', 'postal_address']
#     for para in cdata:




