import yaml
import os

class DataManager:
    """
    A class to manage data operations such as loading and manipulating YAML files.
    """

# update for version with path in inti and create function for update path  
    def __init__(self, base_path="backend"):
        self.base_path = base_path

    def _control_path(self, file_path: str) -> str:
        """
        Validate that the given path is a file.

        :param path: Path to validate.
        :return: The validated path (unchanged).
        :raises ValueError: If the path is None or empty.
        :raises FileNotFoundError: If the path does not point to an existing file.
        """
        if not file_path:
            raise ValueError("Provided path is empty or None.")
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"The file '{file_path}' does not exist.")
        return file_path

    def load_yaml(self, file_path : str) -> dict:
        """
        Load a YAML file and return its content.
        
        :param file_path: Path to the YAML file.
        :return: Content of the YAML file as a dictionary.
        """
        file_path = self._control_path(file_path)
        
        with open(file_path, 'r') as file:
            data = yaml.safe_load(file)
        
        return data


# Update this function  for get all keys ( for dict list of list ["tickers","ticker"])
    def list_keys_yaml(self, file_path : str) -> list:
        """
        List all keys in a YAML file.
        
        :param file_path: Path to the YAML file.
        :return: List of keys in the YAML file.
        """
        file_path = self._control_path(file_path)
        data = self.load_yaml(file_path)
        return list(data.keys())

    def get_specific_values_yaml(self, file_path: str, keys: list[str]) -> any:
        """
        Traverses a YAML data structure following a sequence of keys.
        Handles any depth and combination of dicts/lists.

        :param file_path: path to the YAML file
        :param keys: list of keys to follow (e.g., ["tickers", "ticker"])
        :return: value(s) corresponding to the last key
        """
        file_path = self._control_path(file_path)
        data = self.load_yaml(file_path)

        for key in keys:
            next_data = []

            if isinstance(data, dict):
                # If data is a dictionary, go directly to the next level
                if key not in data:
                    raise KeyError(f"Key '{key}' not found in dictionary.")
                data = data[key]

            elif isinstance(data, list):
                # If data is a list, search for the key inside each element
                for item in data:
                    if isinstance(item, dict) and key in item:
                        next_data.append(item[key])
                    # If nested deeper, search recursively
                    elif isinstance(item, (dict, list)):
                        sub_result = self._find_key_recursive(item, key)
                        if sub_result:
                            next_data.extend(sub_result)

                if not next_data:
                    raise KeyError(f"Key '{key}' not found in list of dictionaries.")
                data = next_data

            else:
                raise TypeError(f"Unexpected type {type(data)} while searching for key '{key}'.")

        return data


    def _find_key_recursive(self, data, key):
        """Helper function: recursively searches for a key anywhere within the structure."""
        results = []
        if isinstance(data, dict):
            for k, v in data.items():
                if k == key:
                    results.append(v)
                elif isinstance(v, (dict, list)):
                    results.extend(self._find_key_recursive(v, key))
        elif isinstance(data, list):
            for item in data:
                results.extend(self._find_key_recursive(item, key))
        return results


if __name__ == "__main__":
    # Example usage
    dm = DataManager()
    try:
        print(os.getcwd())
        yaml_data = dm.load_yaml("backend/tickers.yaml")
        print(yaml_data)
        print( "--------------- ------------------ ------------------ ------------------     ------------------ ------------------")
        keys = dm.list_keys_yaml("backend/tickers.yaml")
        print(keys)
        print( "--------------- ------------------ ------------------ ------------------     ------------------ ------------------")
        # value = dm.get_value_yaml("backend/tickers.yaml", "tickers")
        value = dm.get_specific_values_yaml("backend/tickers.yaml", ["tickers","ticker"])
        
        print(value)
    except Exception as e:
        print(f"An error occurred: {e}")
    

