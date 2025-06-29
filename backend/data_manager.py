import yaml
import os

class DataManager:
    """
    A class to manage data operations such as loading and manipulating YAML files.
    """

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

    def list_keys_yaml(self, file_path : str) -> list:
        """
        List all keys in a YAML file.
        
        :param file_path: Path to the YAML file.
        :return: List of keys in the YAML file.
        """
        file_path = self._control_path(file_path)
        data = self.load_yaml(file_path)
        return list(data.keys())

    def get_value_yaml(self, file_path : str, key : str) -> any:
        """
        Get the value of a specific key in a YAML file.
        
        :param file_path: Path to the YAML file.
        :param key: Key whose value is to be retrieved.
        :return: Value associated with the key.
        """
        file_path = self._control_path(file_path)
        data = self.load_yaml( file_path)
        
        if key in data:
            return data[key]
        else:
            raise KeyError(f"The key {key} does not exist in the YAML file.")
        


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
        value = dm.get_value_yaml("backend/tickers.yaml", "tickers")
        
        print(value)
    except Exception as e:
        print(f"An error occurred: {e}")
    

