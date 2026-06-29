from bs4 import BeautifulSoup


class HTMLParser:

    def parse(
        self,
        html: str
    ) -> str:

        if not html:
            return ""

        soup = BeautifulSoup(
            html,
            "html.parser"
        )

        # -------------------------
        # Tables
        # -------------------------

        table = soup.find("table")

        if table:
            return self._parse_table(
                table
            )

        # -------------------------
        # Lists
        # -------------------------

        ul = soup.find(["ul", "ol"])

        if ul:
            return self._parse_list(
                ul
            )

        # -------------------------
        # Links
        # -------------------------

        for a in soup.find_all("a"):

            href = a.get(
                "href",
                ""
            )

            text = a.get_text(
                " ",
                strip=True
            )

            if href:

                a.replace_with(
                    f"{text} ({href})"
                )

        # -------------------------
        # Default
        # -------------------------

        return soup.get_text(
            separator=" ",
            strip=True
        )

    # =====================================================

    def _parse_list(
        self,
        node
    ) -> str:

        items = []

        for li in node.find_all(
            "li",
            recursive=False
        ):

            items.append(
                "- "
                + li.get_text(
                    " ",
                    strip=True
                )
            )

        return "\n".join(
            items
        )

    # =====================================================

    def _parse_table(
        self,
        table
    ) -> str:

        rows = []

        for tr in table.find_all("tr"):

            cols = []

            for cell in tr.find_all(
                ["th", "td"]
            ):

                cols.append(
                    cell.get_text(
                        " ",
                        strip=True
                    )
                )

            if cols:

                rows.append(cols)

        if not rows:

            return ""

        markdown = []

        markdown.append(
            "| "
            + " | ".join(rows[0])
            + " |"
        )

        markdown.append(
            "| "
            + " | ".join(
                "---"
                for _ in rows[0]
            )
            + " |"
        )

        for row in rows[1:]:

            while len(row) < len(rows[0]):

                row.append("")

            markdown.append(
                "| "
                + " | ".join(row)
                + " |"
            )

        return "\n".join(
            markdown
        )