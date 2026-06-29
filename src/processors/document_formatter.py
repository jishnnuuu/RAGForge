from utils.table_parser import TableParser


class DocumentFormatter:

    def __init__(self):

        self.table_parser = TableParser()

    def format_table(
        self,
        raw_html: str
    ) -> str:

        matrix = self.table_parser.parse(
            raw_html
        )

        if len(matrix) < 3:
            return ""

        # ----------------------------------------
        # Build full column names
        # ----------------------------------------

        header1 = matrix[0]
        header2 = matrix[1]

        columns = []

        for upper, lower in zip(
            header1,
            header2
        ):

            upper = upper.strip()
            lower = lower.strip()

            if upper == lower:

                columns.append(
                    upper
                )

            else:

                columns.append(
                    f"{upper} {lower}"
                )

        lines = []

        current_section = None

        # ----------------------------------------
        # Data rows
        # ----------------------------------------

        for row in matrix[2:]:

            section = row[0]

            metric = row[1]

            if section != current_section:

                current_section = section

                lines.append(
                    f"\n{section}"
                )

            lines.append(
                f"\n{metric}"
            )

            for column, value in zip(
                columns[2:],
                row[2:]
            ):

                lines.append(
                    f"- {column}: {value}"
                )

        return "\n".join(
            lines
        )