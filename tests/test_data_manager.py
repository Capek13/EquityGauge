import pytest
from unittest.mock import patch, mock_open, MagicMock
from backend.data_manager import DataManager

@pytest.fixture
def manager():
    return DataManager(base_path="tests/fixtures/tickers_test.yaml")

FAKE_YAML = """
tickers:
  - ticker: AAPL
    name: Apple Inc.
    sector: Technology
"""

FAKE_YAML_DEAPER = """
something:
  test:
    tickers:
      - ticker: META
        name: Meta Inc.
        sector: Technology
    
something2:
  tickers:
    - ticker: META
      name: Meta Inc.
      sector: Technology
    - ticker: AAPL
      name: Apple Inc.
      sector: Technology
tickers:
  - ticker: AAPL
    name: Apple Inc.
    sector: Technology
  - ticker: XXXX
    name: Apple Inc.
    sector: Technology
test:
  test:
    test:
      test:
        test:
          test:
            test:
              test:
                test:
                  tickers:
                    - ticker: TEST
"""

class TestUpdateBasePath():
    def test_change_base_path(self, manager):
        new_path = "TEST/TEST/TEST.test"
        with patch("backend.data_manager.os.path.isfile", return_value=True):
            manager.update_base_path(new_path)
        assert manager.base_path == new_path
    
    def test_change_base_path_with_not_exist_path(self, manager):
        new_path = "TEST/TEST/TEST.test"
        with pytest.raises(FileNotFoundError):
            manager.update_base_path(new_base_path=new_path)

    def test_change_base_path_with_boolean(self, manager):
        with pytest.raises(TypeError):
            manager.update_base_path(new_base_path=True)

    def test_change_base_path_with_int(self, manager):
        with pytest.raises(TypeError):
            manager.update_base_path(new_base_path=34567)

class TestLoadYaml:
    def test_returns_dict_with_requirement(self,manager):
        with patch("builtins.open", mock_open(read_data=FAKE_YAML)):
            result = manager.load_yaml("tickers")
        assert isinstance(result, dict)
        assert "tickers" in result
    
    def test_raise_if_requirement_is_not_found(self,manager):
        with patch("builtins.open", mock_open(read_data=FAKE_YAML)):
            with pytest.raises(KeyError, match="Key 'TEST' not found in YAML data."):
                result = manager.load_yaml("TEST")
    
    def test_returns_dict_without_requirement(self,manager):
        with patch("builtins.open", mock_open(read_data=FAKE_YAML)):
            result = manager.load_yaml()
        assert isinstance(result, dict)
        assert "tickers" in result

    def test_raises_if_key_missing(self, manager):
        with patch("builtins.open", mock_open(read_data=FAKE_YAML)):
            with pytest.raises(KeyError, match="missing_key"):
                manager.load_yaml(required_key="missing_key")

class TestListChildKeysYaml():
    def test_list_child_keys_yaml(self,manager):
        with patch("builtins.open", mock_open(read_data=FAKE_YAML_DEAPER)):
            result = manager.list_child_keys_yaml("tickers")
        assert isinstance(result, list)
        assert "ticker" in result
        assert "name" in result
        assert "sector" in result
        assert len(result) == 3

    def test_raises_if_key_missing(self, manager):
        with patch.object(manager, "load_yaml", side_effect=KeyError("missing_key")):
            with pytest.raises(KeyError):
                manager.list_child_keys_yaml("missing_key")

class TestGetSpecificValuesYaml():
    def test_get_specific_values_yaml(self, manager):
        with patch("builtins.open", mock_open(read_data=FAKE_YAML_DEAPER)):
            result = manager.get_specific_values_yaml(["tickers"])
        assert "ticker" in result[0]
        assert "XXXX" in result[1]["ticker"]
        assert len(result) == 2

    def test_get_specific_values_yaml_2(self, manager):
        with patch("builtins.open", mock_open(read_data=FAKE_YAML_DEAPER)):
            result = manager.get_specific_values_yaml(["tickers","ticker"])
        assert 'AAPL' in result
        assert len(result) == 2

    def test_raises_if_key_missing(self, manager):
        with patch.object(manager, "load_yaml", side_effect=KeyError("missing_key")):
            with pytest.raises(KeyError):
                manager.get_specific_values_yaml("missing_key")

class TestGetTicker:
    def test_found(self,manager):
        with patch.object(manager, "load_yaml", return_value={"tickers": [
            {"ticker": "AAPL", "name": "Apple Inc.", "sector": "Technology"}
        ]}):
             result = manager.get_ticker("AAPL", "tickers")
        assert result["name"] == "Apple Inc."
        assert result["sector"] == "Technology"

    def test_not_found_returns_none(self, manager):
        with patch.object(manager, "load_yaml", return_value={"tickers": [
            {"ticker": "AAPL", "name": "Apple Inc.", "sector": "Technology"}
        ]}):
            result = manager.get_ticker("TSLA", "tickers")
        assert result is None

class TestAddTicker:
    def test_appends_ticker(self, manager):
        fake_data = {"tickers": [{"ticker": "AAPL"}]}
        new_ticker = {"ticker": "TSLA", "name": "Tesla"}

        with patch.object(manager, "load_yaml", return_value=fake_data), \
             patch.object(manager, "_save_yaml") as mock_save:
            manager.add_ticker_yaml(new_ticker, "tickers")

        saved = mock_save.call_args[0][0]   
        assert len(saved["tickers"]) == 2
        assert saved["tickers"][1]["ticker"] == "TSLA"

class TestRemoveTicker:
    def test_remove_ticker(self, manager):
        fake_data = {"tickers": [ {"ticker": "AAPL", "name": "Apple Inc.", "sector": "Technology"}, \
                                  {"ticker": "TEST", "name": "test test"}]}

        with patch.object(manager, "load_yaml", return_value=fake_data), \
             patch.object(manager, "_save_yaml") as mock_save:
            manager.remove_ticker_yaml("TEST", "tickers")
        saved = mock_save.call_args[0][0]   
        assert len(saved["tickers"]) == 1
        assert saved["tickers"][0]["ticker"] == "AAPL"
        with patch.object(manager, "load_yaml", return_value=saved):
            assert manager.get_ticker("AAPL","tickers") is not None
            assert manager.get_ticker("TEST","tickers") is None
    
    def test_raises_if_key_missing_req_key(self, manager):
        with patch.object(manager, "load_yaml", side_effect=KeyError("missing_key")):
            with pytest.raises(KeyError):
                manager.remove_ticker_yaml("AAPL","missing_key")

    def test_raises_if_ticker_not_found(self, manager):
        fake_data = {"tickers": [{"ticker": "AAPL"}]}
        with patch.object(manager, "load_yaml", return_value=fake_data), \
            patch.object(manager, "_save_yaml"):
            with pytest.raises(KeyError, match="TSLA"):
                manager.remove_ticker_yaml("TSLA", "tickers")