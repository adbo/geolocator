import requests

from core.config import Settings
from core.exceptions import IPStackAPIError


settings = Settings()
IPSTACK_API_URL = "https://api.ipstack.com/"


def get_geolocation_data(ip_or_url: str):
    """Fetches geolocation data from the IPStack API."""
    url = f"{IPSTACK_API_URL}{ip_or_url}"
    params = {"access_key": settings.ipstack_api_key}

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        if not data.get("success", True):
            error = data.get("error", {})
            raise IPStackAPIError(
                detail=f"IPStack API Error: {error.get('info', 'Unknown')}",
                error_code=error.get("code"),
                error_type=error.get("type"),
                error_info=error.get("info"),
            )
        return data
    except requests.exceptions.RequestException as e:
        raise IPStackAPIError(detail=f"Error connecting to IPStack API: {e}")
    except ValueError:
        raise IPStackAPIError(detail="Error parsing IPStack API response")
