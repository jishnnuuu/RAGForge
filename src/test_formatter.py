from json import loads
from pathlib import Path

from processors.document_formatter import (
    DocumentFormatter
)

data = loads(
    Path(
        "outputs/result.json"
    ).read_text()
)

formatter = DocumentFormatter()

for block in data["blocks"]:

    if block["block_type"] == "table":

        print(
            formatter.format_table(
                block["raw_html"]
            )
        )