from bs4 import BeautifulSoup


class TableParser:

    def parse(
        self,
        html: str
    ) -> list[list[str]]:

        if not html:
            return []

        soup = BeautifulSoup(
            html,
            "html.parser"
        )

        table = soup.find("table")

        if table is None:
            return []

        rows = []

        for tr in table.find_all("tr"):

            current_row = []

            for cell in tr.find_all(
                ["th", "td"],
                recursive=False
            ):

                text = cell.get_text(
                    " ",
                    strip=True
                )

                rowspan = int(
                    cell.get(
                        "rowspan",
                        1
                    )
                )

                colspan = int(
                    cell.get(
                        "colspan",
                        1
                    )
                )

                current_row.append(
                    {
                        "text": text,
                        "rowspan": rowspan,
                        "colspan": colspan
                    }
                )

            rows.append(
                current_row
            )

        return self._expand(
            rows
        )

    # --------------------------------------------------

    def _expand(
        self,
        rows
    ):

        grid = []

        pending = {}

        for row_idx, row in enumerate(rows):

            output = []

            col = 0

            while (
                row_idx,
                col
            ) in pending:

                value, remaining = pending[
                    (
                        row_idx,
                        col
                    )
                ]

                output.append(
                    value
                )

                if remaining > 1:

                    pending[
                        (
                            row_idx + 1,
                            col
                        )
                    ] = (
                        value,
                        remaining - 1
                    )

                del pending[
                    (
                        row_idx,
                        col
                    )
                ]

                col += 1

            for cell in row:

                while (
                    row_idx,
                    col
                ) in pending:

                    value, remaining = pending[
                        (
                            row_idx,
                            col
                        )
                    ]

                    output.append(
                        value
                    )

                    if remaining > 1:

                        pending[
                            (
                                row_idx + 1,
                                col
                            )
                        ] = (
                            value,
                            remaining - 1
                        )

                    del pending[
                        (
                            row_idx,
                            col
                        )
                    ]

                    col += 1

                for _ in range(
                    cell["colspan"]
                ):

                    output.append(
                        cell["text"]
                    )

                    if (
                        cell["rowspan"] > 1
                    ):

                        pending[
                            (
                                row_idx + 1,
                                col
                            )
                        ] = (
                            cell["text"],
                            cell["rowspan"] - 1
                        )

                    col += 1

            while (
                row_idx,
                col
            ) in pending:

                value, remaining = pending[
                    (
                        row_idx,
                        col
                    )
                ]

                output.append(
                    value
                )

                if remaining > 1:

                    pending[
                        (
                            row_idx + 1,
                            col
                        )
                    ] = (
                        value,
                        remaining - 1
                    )

                del pending[
                    (
                        row_idx,
                        col
                    )
                ]

                col += 1

            grid.append(
                output
            )

        return grid