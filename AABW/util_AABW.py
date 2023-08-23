import pathlib
import requests


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
