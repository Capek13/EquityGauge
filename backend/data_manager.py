import yaml
import os

class DataManager:
    """
    A class to manage data operations such as loading and manipulating YAML files.
    """

    def __init__(self, base_path:str="backend"):
        """Initialize the DataManager with a base path for YAML files."""
        self.base_path = self._validate_path(base_path)

    def update_base_path(self, new_base_path: str):
        """Update the base path for YAML files."""
        self.base_path = self._validate_path(new_base_path)


# Functions for work with yaml file
    def load_yaml(self, required_key:str = "") -> dict:
        """
        Load a YAML file and return its content.
        
        :return: Content of the YAML file as a dictionary.
        """

        with open(self.base_path, 'r') as file:
            data = yaml.safe_load(file)

        if required_key != "" and required_key not in data:
            raise KeyError(f"Value '{required_key}' is not found in loaded data.") 
            
        return data

    # Update this function  for get all keys ( for dict list of list ["tickers","ticker"])
    def list_child_keys_yaml(self, required_key:str) -> list:
        """
        List all keys in a YAML file.
        
        :return: List of keys in the YAML file.
        """
        data = self.load_yaml(required_key)
        child_data = self._find_key_recursive(data, required_key)

        return list(child_data.keys())

    def get_specific_values_yaml(self, keys: list[str],required_key:str) -> any:
        """
        Traverses a YAML data structure following a sequence of keys.
        Handles any depth and combination of dicts/lists.

        :param keys: list of keys to follow (e.g., ["tickers", "ticker"])
        :return: value(s) corresponding to the last key
        """
        data = self.load_yaml(required_key)

        for key in keys:

            if isinstance(data, dict):
                # If data is a dictionary, go directly to the next level
                if key not in data:
                    raise KeyError(f"Key '{key}' not found in dictionary.")
                data = data[key]

            # elif isinstance(data, list):
            #     # If data is a list, search for the key inside each element
            #     for item in data:
            #         if key in item:
            #             next_data.append(item[key])
            #         # If nested deeper, search recursively
            #         else:
            #             sub_result = self._find_key_recursive(item, key)
            #             if sub_result:
            #                 next_data.extend(sub_result)

                # if not next_data:
                #     raise KeyError(f"Key '{key}' not found in list of dictionaries.")
                # data = next_data

            else:
                raise TypeError(f"Unexpected type {type(data).__name__} while searching for key '{key}'. Function expect only dict")

        return data

    def add_ticker_yaml(self, ticker_data: dict, required_key:str ):
        """
        Add a new ticker to the YAML file.

        :param ticker_data: A dictionary containing the ticker information to add.
        """
        data = self.load_yaml("")

        if required_key not in data:
            data[required_key] = []

        data[required_key].append(ticker_data)

        with open(self.base_path, 'w') as file:
            yaml.safe_dump(data, file)

    def remove_ticker_yaml(self, ticker_name: str,required_key: str):
        """
        Remove a ticker from the YAML file by its name.

        :param ticker_name: The name of the ticker to remove.
        """
        data = self.load_yaml(required_key)

        original_length = len(data[required_key])
        data[required_key] = [ticker for ticker in data[required_key] if ticker.get("name") != ticker_name]

        if len(data[required_key]) == original_length:
            raise KeyError(f"Ticker with name '{ticker_name}' not found.")

        with open(self.base_path, 'w') as file:
            yaml.safe_dump(data, file)

    def update_ticker_yaml(self, ticker_name: str, new_data : str | dict, required_key: str):
        data = self.load_yaml(required_key)
        for ticker in data[required_key]:
            if ticker.get("name") == ticker_name:
                if isinstance(new_data, dict):
                    for key in new_data:
                        ticker[key] = new_data[key]
                elif isinstance(new_data, str):
                    for value in new_data.split(","):
                        parts = value.split(": ")
                        if len(parts) != 2: 
                            raise KeyError(f"String \"{value}\" included any or more than one :. ")
                        key, val = parts
                        if key in ticker:
                            ticker[key] = val
                        else:
                            raise KeyError(f"ticker \"{ticker}\" doesn't include key: {key}")
                else: 
                    raise KeyError(f"data for update are in bad type. New values can be in data type string or dict. Aktual inserted data are in data type: {type(new_data).__name__ }")

        with open(self.base_path, 'w') as file:
            yaml.safe_dump(data, file)

        
# Private methods
    def _validate_path(self, file_path: str) -> str:
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
    
    def _find_key_recursive(self, data:dict, key:str , i:int = 0, max_iter:int = 15) -> dict:
        """Helper function: recursively searches for a key anywhere within the structure."""
        results = {}
        if i >= max_iter:
             raise KeyError(f"Key \"{key}\" wasn't find in {max_iter} iterations")

        if isinstance(data, dict):
            for k, v in data.items():
                if k == key:
                    for ch_key in v:
                        results[ch_key] = v[ch_key]
                elif isinstance(v, (dict)):
                    results = {**(self._find_key_recursive(v, key, i+1)), **results}
        else:
            raise KeyError(f"Function _find_key_recursive working only with dict data input. Yout inserted data are in data type: {type(data).__name__ }")
        return results

if __name__ == "__main__":
    # Example usage
    dm = DataManager("backend/tickers.yaml")
    required_key = "tickers"
    try:
        print(os.getcwd())
        yaml_data = dm.load_yaml(required_key)
        print(yaml_data)
        print( "--------------- ------------------ ------------------ ------------------     ------------------ ------------------")
        keys = dm.list_child_keys_yaml(required_key)
        print(keys)
        print( "--------------- ------------------ ------------------ ------------------     ------------------ ------------------")
        value = dm.get_specific_values_yaml([required_key,"ticker"],required_key)

        print(value)
    except Exception as e:
        print(f"An error occurred: {e}")
    

