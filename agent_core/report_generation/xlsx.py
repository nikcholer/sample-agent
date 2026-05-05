from __future__ import annotations

import html
import zipfile
from pathlib import Path
from typing import Any


def write_xlsx(
    path: Path,
    sheets: dict[str, list[dict[str, Any]]],
) -> None:
    """Write a small XLSX workbook without third-party dependencies."""

    path.parent.mkdir(parents=True, exist_ok=True)
    sheet_names = list(sheets)
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("[Content_Types].xml", _content_types(sheet_names))
        archive.writestr("_rels/.rels", _root_rels())
        archive.writestr("xl/workbook.xml", _workbook(sheet_names))
        archive.writestr("xl/_rels/workbook.xml.rels", _workbook_rels(sheet_names))
        archive.writestr("xl/styles.xml", _styles())
        for index, name in enumerate(sheet_names, start=1):
            archive.writestr(
                f"xl/worksheets/sheet{index}.xml",
                _worksheet(sheets[name]),
            )


def _content_types(sheet_names: list[str]) -> str:
    sheet_overrides = "\n".join(
        f'<Override PartName="/xl/worksheets/sheet{index}.xml" '
        'ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>'
        for index, _ in enumerate(sheet_names, start=1)
    )
    return f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>
  <Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>
  {sheet_overrides}
</Types>"""


def _root_rels() -> str:
    return """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>
</Relationships>"""


def _workbook(sheet_names: list[str]) -> str:
    sheets_xml = "\n".join(
        f'<sheet name="{_xml(name)}" sheetId="{index}" r:id="rId{index}"/>'
        for index, name in enumerate(sheet_names, start=1)
    )
    return f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"
          xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
  <sheets>
    {sheets_xml}
  </sheets>
</workbook>"""


def _workbook_rels(sheet_names: list[str]) -> str:
    rels = [
        f'<Relationship Id="rId{index}" '
        'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" '
        f'Target="worksheets/sheet{index}.xml"/>'
        for index, _ in enumerate(sheet_names, start=1)
    ]
    rels.append(
        f'<Relationship Id="rId{len(sheet_names) + 1}" '
        'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" '
        'Target="styles.xml"/>'
    )
    return f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  {' '.join(rels)}
</Relationships>"""


def _styles() -> str:
    return """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
  <fonts count="1"><font><sz val="11"/><name val="Calibri"/></font></fonts>
  <fills count="1"><fill><patternFill patternType="none"/></fill></fills>
  <borders count="1"><border><left/><right/><top/><bottom/><diagonal/></border></borders>
  <cellStyleXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0"/></cellStyleXfs>
  <cellXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0"/></cellXfs>
</styleSheet>"""


def _worksheet(rows: list[dict[str, Any]]) -> str:
    headers = list(rows[0]) if rows else []
    all_rows = [headers] + [[row.get(header, "") for header in headers] for row in rows]
    row_xml = "\n".join(
        f'<row r="{row_index}">'
        + "".join(
            _cell(row_index, col_index, value)
            for col_index, value in enumerate(row_values, start=1)
        )
        + "</row>"
        for row_index, row_values in enumerate(all_rows, start=1)
    )
    return f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
  <sheetData>
    {row_xml}
  </sheetData>
</worksheet>"""


def _cell(row_index: int, col_index: int, value: Any) -> str:
    ref = f"{_column_name(col_index)}{row_index}"
    if isinstance(value, int | float):
        return f'<c r="{ref}"><v>{value}</v></c>'
    return f'<c r="{ref}" t="inlineStr"><is><t>{_xml(str(value))}</t></is></c>'


def _column_name(index: int) -> str:
    name = ""
    while index:
        index, remainder = divmod(index - 1, 26)
        name = chr(65 + remainder) + name
    return name


def _xml(value: str) -> str:
    return html.escape(value, quote=True)
