from pathlib import Path

from bs4 import BeautifulSoup

from utils.table_parser import TableParser


html = Path(
    "outputs/result.json"
).read_text()

parser = TableParser()

from json import loads

data = loads(html)

for block in data["blocks"]:

    if block["block_type"] == "table":

        matrix = parser.parse(
            block["raw_html"]
        )

        for row in matrix:

            print(row)