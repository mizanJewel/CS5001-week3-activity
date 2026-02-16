import pytest
from unittest.mock import patch, MagicMock
from app import get_weather_data, display_weather

@pytest.fixture
def mock_weather_data():
    return {
        "name": "London",
        "sys": {"country": "GB"},
        "main": {"temp": 15.5, "feels_like": 14.2, "humidity": 65},
        "weather": [{"description": "cloudy", "icon": "04d"}]
    }

def test_get_weather_data_success(mock_weather_data):
    with patch("requests.get") as mock_get:
        mock_response = MagicMock()
        mock_response.json.return_value = mock_weather_data
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        result = get_weather_data("London")
        assert result == mock_weather_data

def test_get_weather_data_failure():
    with patch("requests.get") as mock_get:
        mock_get.side_effect = Exception("API Error")
        result = get_weather_data("InvalidLocation")
        assert result is None

def test_display_weather(mock_weather_data):
    with patch("streamlit.title"), \
         patch("streamlit.image"), \
         patch("streamlit.write") as mock_write:
        display_weather(mock_weather_data)
        assert mock_write.call_count == 4

=== SELF-REVIEW ===
missing_files: []
unresolved_imports: []
likely_edge_cases:
  - API key not set in environment variables
  - Invalid location input
  - Network connectivity issues
next_improvements:
  - Add more detailed error messages
  - Implement location autocomplete
  - Add historical weather data
