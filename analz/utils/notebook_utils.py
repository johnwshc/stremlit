import nbconvert
import nbformat
from nbformat import NotebookNode
from pydantic import BaseModel
from config import Config
from typing import List, Optional

import subprocess
import markdown

class GImage(BaseModel):
    url: str
    fn: str

    def get_GImage(self):
        if


class NBCell(BaseModel):
    ctype: str
    source: str
    imageUrl: Optional[str] = None
    html: Optional[str] = None
    id: Optional[int] = None

    def set_id(self, id: int):
        self.id = id

class NB(BaseModel):
    cells: List[NBCell]
    path: str

    def set_c_index(self ):
        rr = list(range(len(self.cells)))
        for r in rr:
            self.cells[r].set_id(r)

    def get_md_cells(self):
        mcells = [c for c in self.cells if c.ctype == "markdown"]
        return mcells

    def get_code_cells(self):
        ccells = [c for c in self.cells if c.ctype == "code"]
        return ccells

    def merge_mcells(self):
        mcells = self.get_md_cells()
        md_doc = ""
        for  mc in mcells:
            md_doc = md_doc.join(mc.source)
            md_doc = md_doc.join("\n\n********************\n\n")
        return md_doc

    def drop_bad_code_cells(self):
        good_cells = []
        for c in self.cells:
            if c.ctype == "code":
                if "show" in c.source:
                    good_cells.append(c)






class NBUtils:
    test_pth = f"{Config.basedir}/gdp_2025.ipynb"
    test_cmd = f"marimo export md gdp_2025.py -o moutputs/gdp_2022_b.md"
    image_tups = [("show_real_nom", "https://photos.app.goo.gl/qQmYxS3Cqi1eSHTj7"),
                  ("ls_table", "https://photos.app.goo.gl/E8s3ujLg6dWkG3tG7"),
                  ("show_real_2022", "https://photos.app.goo.gl/PeikTtaN79qFbPvg8"),
                  ("show_curr_2022", "https://photos.app.goo.gl/g6hTcjRZCtdUUgPx8"),
                  ("show_employment", "https://photos.app.goo.gl/sf3N1mRxi1HiKetJ6"),
                  ("show_comp", "https://photos.app.goo.gl/Bx4RSbKVcZ2PjVraA"),
                  ("show_opp_surp", "https://photos.app.goo.gl/4mZo8Ex4TRrowWNb8"),
                  ("show_comp_surp", "https://photos.app.goo.gl/PatHFr8ZpUQwtjcf8"),
                  ("tsbars.show_taxes_bars", "https://photos.app.goo.gl/SZbY3Vm5BX6AnM7d8"),
                  ("show_subs", "https://photos.app.goo.gl/WJFrCMCaUVayw4PT6"),
                  ("show_tax_minus", "https://photos.app.goo.gl/AazdpFz6u6qghHAAA")]
    img_json_fn = f"{Config.basedir}/json/gdp_2022_charts.json"

    @classmethod
    def save_gdp_2022_charts(cls):
        import json
        fn = f"{Config.basedir}/json/gdp_2022_charts.json"
        dcharts = {c[0]:c[1] for c in NBUtils.image_tups}
        with open(fn, "w") as f:
            json.dump(dcharts, f)

    @classmethod
    def load_gdp_2022_charts(cls):
        import json
        with open(cls.img_json_fn) as f:
            d: dict = json.load(f)
            return d


    @staticmethod
    def get_marimo_md():
        m_cmd = "marimo export md gdp_2025.py -o moutputs/output.md"


    @classmethod
    def get_cell_types(cls):
        cnt = cls.get_nb_content(None)
        cell_types = []
        for cell in cnt["cells"]:
            cell_types.append(cell["cell_type"])
        return cell_types

    @classmethod
    def get_nb_content(cls, nb_path=None)->NotebookNode:
        pth = nb_path if nb_path else cls.test_pth


        notebook_path = pth # Replace with your notebook's path

        with open(notebook_path, 'r', encoding='utf-8') as f:
            notebook_content = nbformat.read(f, as_version=4)
            return notebook_content

    @classmethod
    def get_nb(cls, nb_path=None) -> NB:
        img_dict = NBUtils.load_gdp_2022_charts()
        keys = img_dict.keys()
        print(f"img_dict keys:\n {keys}")
        if nb_path is None:
            nb_path = cls.test_pth
        cells:List[NBCell] = []
        nb_content = cls.get_nb_content(nb_path)
        for cell in nb_content["cells"]:
            ctype = cell["cell_type"]
            if ctype == "markdown":
                html = NBUtils.convert_md_2_htm(cell["source"])
                c_dict = {'ctype': cell["cell_type"], 'source': cell["source"], 'html': html, 'imageUrl':None}
                nbc = NBCell(**c_dict)
                cells.append(nbc)

            elif ctype == "code":

                src = cell["source"]
                if src.startswith("def"):
                    continue
                for k in keys:
                    if k in src:
                        url = img_dict.get(k)
                        c_dict = {'ctype': ctype, 'source': src, 'html': None, 'imageUrl':url}
                        nbc2 = NBCell(**c_dict)
                        cells.append(nbc2)
                        break
            else:
                continue
        cs_dict = {'cells': cells, 'path': nb_path}
        nb = NB(**cs_dict)
        nb.set_c_index()
        return nb



    @classmethod
    def get_nb_md(cls, nb_fn:str=None) -> list|None:
        notebook_content = cls.get_nb_content(nb_fn)
        text_cells_content: list = []
        for cell in notebook_content.cells:
            if cell.cell_type in ['markdown']:
                text_cells_content.append(cell.source)

        # Now, text_cells_content contains a list of strings, where each string is the content of a text cell.
        for content in text_cells_content:
            print(content)
            print("-" * 20)  # Separator for clarity
        return text_cells_content


    @classmethod
    def sh_cmd(cls, cmd:str = test_cmd):


        if cmd is None:

            # Running a simple command and capturing output
            result = subprocess.run(['pythons', '-V'], capture_output=True, text=True, check=True)
            print("STDOUT:", result.stdout)
            print("STDERR:", result.stderr)

            # Running a command with shell=True (use with caution, potential security risk)
            # This allows you to pass a single string containing the full shell command
            # result_shell = subprocess.run('echo "Hello from shell!"', shell=True, capture_output=True, text=True)
            # print("Shell command output:", result_shell.stdout)
        else:
            result_shell = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            print("Shell command output:", result_shell.stdout)

    @classmethod
    def convert_md_2_htm(cls, md_pth: str|None = None)->str|None:
        markdown_text = md_pth
        if not md_pth:
            return None

        html_output: str = markdown.markdown(markdown_text)
        # print(html_output)
        return html_output


    @classmethod
    def build_gdp_page(cls,notebook_fn: str|None = None):


        nb = NBUtils.get_nb(notebook_fn)

        return nb
