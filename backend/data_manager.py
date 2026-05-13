import yaml
import os
from typing import Any

class DataManager:
    """Manages reading and writing of YAML data files."""

    def __init__(self, base_path: str = "backend"):
        self.base_path = self._validate_path(base_path)

    def update_base_path(self, new_base_path: str):
        """Change the YAML file path."""
        self.base_path = self._validate_path(new_base_path)

    def load_yaml(self, required_key: str = "") -> dict:
        """
        Load the YAML file and return its content.

        :param required_key: If provided, raises KeyError if the key is missing in the loaded data.
        :return: Content of the YAML file as a dictionary.
        """
        with open(self.base_path, 'r') as file:
            data = yaml.safe_load(file)

        if required_key != "" and required_key not in data:
            raise KeyError(f"Key '{required_key}' not found in YAML data.")

        return data

    def list_child_keys_yaml(self, required_key: str) -> list:
        """
        Return all keys found inside the items under required_key.

        :param required_key: Top-level key whose children's keys are returned (e.g. "tickers").
        :return: List of unique keys found in the child items.
        """
        data = self.load_yaml(required_key)
        child_data = self._find_key_recursive(data, required_key)
        return list(child_data.keys())

    def get_specific_values_yaml(self, keys: list[str]) -> Any:
        """
        Traverse the YAML structure following a sequence of keys and return the value at the end.

        :param keys: Ordered list of keys to follow (e.g. ["tickers", "sector"]).
        :param required_key: Top-level key that must exist in the YAML file.
        :return: Value found at the end of the key path.
        :raises KeyError: If any key in the path is not found.
        :raises TypeError: If an unexpected data type is encountered during traversal.
        """
        data = self.load_yaml(keys[0])
     
        for key in keys:
            next_data = []
            if isinstance(data, dict):
                if key not in data:
                    raise KeyError(f"Key '{key}' not found in dictionary.")
                data = data[key]
            elif isinstance(data, (list)):
                for item in data:
                    if isinstance(item, dict) and key in item:
                        next_data.append(item[key])
                    elif isinstance(item, (dict, list)):
                        sub_result = self._find_key_recursive(item, key)
                        if sub_result:
                            next_data.extend(sub_result)
                if not next_data:
                    raise KeyError(f"Key '{key}' not found in list of dictionaries.")
                data = next_data
            else:
                raise TypeError(f"Unexpected type '{type(data).__name__}' at key '{key}'. Expected dict.")

        return data
    
    def get_ticker(self, required_ticker: str, required_key: str) -> dict | None:
        """
        Return a single ticker dict by its name.

        :param ticker_name: Value of the "name" field to search for.
        :param required_key: Key under which the ticker list is stored (e.g. "tickers").
        :return: Ticker dict if found, None otherwise.
        """
        data = self.load_yaml(required_key)
        for ticker in data[required_key]:
            if ticker.get("ticker") == required_ticker:
                return ticker
        return None

    def add_ticker_yaml(self, ticker_data: dict, required_key: str):
        """
        Append a new ticker entry under required_key in the YAML file.

        :param ticker_data: Dictionary with ticker information to add.
        :param required_key: Key under which the ticker list is stored (e.g. "tickers").
        """
        data = self.load_yaml(required_key)

        if required_key not in data:
            data[required_key] = []

        data[required_key].append(ticker_data)

        with open(self.base_path, 'w') as file:
            yaml.safe_dump(data, file)

    def remove_ticker_yaml(self, ticker: str, required_key: str):
        """
        Remove a ticker by name from the YAML file.

        :param ticker_name: Value of the "name" field identifying the ticker to remove.
        :param required_key: Key under which the ticker list is stored (e.g. "tickers").
        :raises KeyError: If the ticker is not found.
        """
        data = self.load_yaml(required_key)

        original_length = len(data[required_key])
        data[required_key] = [t for t in data[required_key] if t.get("ticker") != ticker]

        if len(data[required_key]) == original_length:
            raise KeyError(f"Ticker \'{ticker}\' not found.")

        with open(self.base_path, 'w') as file:
            yaml.safe_dump(data, file)

    def update_ticker_yaml(self, ticker_name: str, new_data: str | dict, required_key: str):
        """
        Update fields of an existing ticker in the YAML file.

        :param ticker_name: Value of the "name" field identifying the ticker to update.
        :param new_data: New values as a dict, or a string in format 'key: value, key: value'.
        :param required_key: Key under which the ticker list is stored (e.g. "tickers").
        :raises KeyError: If a key in new_data does not exist on the ticker, or new_data type is invalid.
        """
        data = self.load_yaml(required_key)

        for ticker in data[required_key]:
            if ticker.get("name") == ticker_name:
                if isinstance(new_data, dict):
                    ticker.update(new_data)
                elif isinstance(new_data, str):
                    for value in new_data.split(","):
                        parts = value.strip().split(": ")
                        if len(parts) != 2:
                            raise KeyError(f"Invalid format in '{value}'. Expected exactly one ': '.")
                        key, val = parts
                        if key not in ticker:
                            raise KeyError(f"Ticker '{ticker_name}' has no key '{key}'.")
                        ticker[key] = val
                else:
                    raise TypeError(f"new_data must be str or dict, got '{type(new_data).__name__}'.")

        with open(self.base_path, 'w') as file:
            yaml.safe_dump(data, file)

    # Private methods
    def _validate_path(self, file_path: str) -> str:
        """
        Check that the given path points to an existing file.

        :param file_path: Path to validate.
        :return: The validated path.
        :raises ValueError: If the path is empty or None.
        :raises FileNotFoundError: If no file exists at the path.
        """
        if not file_path:
            raise ValueError("Path is empty or None.")
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"File '{file_path}' does not exist.")
        return file_path

    def _find_key_recursive(self, data: dict, key: str, i: int = 0, max_iter: int = 15) -> dict:
        """
        Recursively search for key in a nested dict and return its contents as a flat dict.
        If the value under key is a list of dicts, all their keys are merged.

        :param data: Dict to search in.
        :param key: Key to find.
        :param i: Current recursion depth.
        :param max_iter: Maximum allowed recursion depth.
        :return: Dict of key-value pairs found under the searched key.
        :raises KeyError: If max recursion depth is exceeded or data is not a dict.
        """
        results = {}

        if i >= max_iter:
            raise KeyError(f"Key '{key}' not found within {max_iter} recursion levels.")

        if not isinstance(data, dict):
            raise KeyError(f"Expected dict, got '{type(data).__name__}'.")

        for k, v in data.items():
            if k == key:
                if isinstance(v, list):
                    for item in v:
                        if isinstance(item, dict):
                            results = {**item, **results}
                elif isinstance(v, dict):
                    results = {**v, **results}
            elif isinstance(v, dict):
                results = {**results, **(self._find_key_recursive(v, key, i + 1))}

        return results


if __name__ == "__main__":
    dm = DataManager("backend/tickers.yaml")
    required_key = "tickers"
    try:
        # print(os.getcwd())
        yaml_data = dm.load_yaml(required_key)
        print(yaml_data)
        print("-" * 80)
        keys = dm.list_child_keys_yaml(required_key)
        print(keys)
        print("-" * 80)
        value = dm.get_specific_values_yaml([required_key, "ticker"])
        print(value)
        value = dm.get_ticker("AAPL",required_key)
        print(value)
    except Exception as e:
        print(f"An error occurred: {e}")
