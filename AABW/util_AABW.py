import pathlib
import requests
import pandas as pd
from collections import namedtuple


def RetrieveDataSet(file_name: str) -> bool:
    """
    Retrieves a dataset from a this GitHub and saves it locally,
    if it doesn't exist.

    Args:
        file_name (str): The name of the dataset file.

    Returns:
        bool: True if the dataset exists locally or was successfully retrieved,
              False otherwise.
    """
    if pathlib.Path(file_name).is_file():
        return True
    url = f'https://github.com/gromicho/data/raw/main/AABW/{file_name}'
    response = requests.get(url)
    if response.status_code == 200:
        with open(file_name, 'wb') as file:
            file.write(response.content)
            return True
    return False


def ReadWorkbookIntoNamedTuple(file_name: str, idx_col=None) -> namedtuple:
    """
    Reads an Excel workbook into a named tuple of DataFrames,
    using sheet names as field names.

    Args:
        file_name (str): The name of the Excel file to read.

    Returns:
        namedtuple: A named tuple where field names correspond to sheet names,
        and values are DataFrames.
    """
    def valid_identifier(name: str) -> str:
        name = ''.join(
            (w[0].upper()+w[1:]).replace(' ', '').replace('-', '')
            for w in name.split()
        )
        if name[0].isdigit():
            name = '_' + name
        return name

    xls = pd.ExcelFile(file_name)
    sheets = {valid_identifier(n): pd.read_excel(xls, n, index_col=idx_col)
              for n in xls.sheet_names}
    SheetData = namedtuple('SheetData', sheets.keys())
    return SheetData(**sheets)


def WriteNamedTupleIntoWorkbook(data: namedtuple, file_name: str) -> None:
    """
    Writes a named tuple of DataFrames into an Excel workbook with sheet
    names corresponding to field names.

    Args:
        data (namedtuple): A named tuple containing DataFrames.
        file_name (str): The name of the Excel file to create or overwrite.

    Returns:
        None
    """
    with pd.ExcelWriter(file_name, engine='xlsxwriter') as writer:
        for name, df in zip(data._fields, data):
            df.to_excel(writer, sheet_name=name, index=False)
