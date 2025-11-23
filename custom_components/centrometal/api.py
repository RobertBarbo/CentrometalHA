"""API client for Centrometal portal."""
import logging
import re
import aiohttp
import async_timeout

from .const import LOGIN_PAGE, LOGIN_POST, API_CONTROL, API_STATUS

_LOGGER = logging.getLogger(__name__)


class CentrometalAPI:
    """Centrometal Portal API client."""

    def __init__(self, email: str, password: str, install_id: str):
        """Initialize the API client."""
        self.email = email
        self.password = password
        self.install_id = install_id
        self._session = None
        self._logged_in = False

    async def _get_session(self) -> aiohttp.ClientSession:
        """Get or create aiohttp session."""
        if self._session is None:
            self._session = aiohttp.ClientSession()
        return self._session

    async def login(self) -> bool:
        """Login to portal and get session."""
        try:
            session = await self._get_session()

            # Get CSRF token
            async with async_timeout.timeout(10):
                async with session.get(LOGIN_PAGE) as resp:
                    text = await resp.text()

            match = re.search(r'name="_csrf_token"\s+value="([^"]+)"', text)
            if not match:
                _LOGGER.error("Could not find CSRF token")
                return False

            csrf_token = match.group(1)

            # Login
            login_data = {
                "_csrf_token": csrf_token,
                "_username": self.email,
                "_password": self.password,
            }

            async with async_timeout.timeout(10):
                async with session.post(
                    LOGIN_POST,
                    data=login_data,
                    allow_redirects=False
                ) as resp:
                    if resp.status not in (301, 302, 303, 307, 308):
                        _LOGGER.error("Login failed with status %d", resp.status)
                        return False

            self._logged_in = True
            _LOGGER.info("Successfully logged in to Centrometal portal")
            return True

        except Exception as err:
            _LOGGER.error("Login error: %s", err)
            return False

    async def send_command(self, command: dict) -> bool:
        """Send command to boiler."""
        if not self._logged_in:
            if not await self.login():
                return False

        try:
            session = await self._get_session()

            payload = {
                "messages": {
                    self.install_id: command
                }
            }

            headers = {
                "Content-Type": "application/json;charset=UTF-8",
                "Accept": "application/json, text/plain, */*",
            }

            async with async_timeout.timeout(10):
                async with session.post(
                    API_CONTROL,
                    json=payload,
                    headers=headers
                ) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        if data.get("status") == "success":
                            _LOGGER.debug("Command sent successfully: %s", command)
                            return True
                        else:
                            _LOGGER.warning("Unexpected response: %s", data)
                            return False
                    else:
                        _LOGGER.error("Command failed with status %d", resp.status)
                        return False

        except Exception as err:
            _LOGGER.error("Error sending command: %s", err)
            return False

    async def turn_on(self) -> bool:
        """Turn boiler on."""
        return await self.send_command({"PWR 99": 1})

    async def turn_off(self) -> bool:
        """Turn boiler off."""
        return await self.send_command({"PWR 99": 0})

    async def refresh_status(self) -> bool:
        """Request status refresh."""
        return await self.send_command({"REFRESH": 0})

    async def get_installation_status(self) -> dict:
        """Get installation status from portal (includes PVAL parameters)."""
        if not self._logged_in:
            if not await self.login():
                return {}

        try:
            session = await self._get_session()
            url = API_STATUS.format(install_id=self.install_id)

            async with async_timeout.timeout(10):
                async with session.get(url) as resp:
                    if resp.status == 200:
                        data = await resp.json()

                        # Extract PVAL_* values from params section
                        pval_data = {}
                        params = data.get("params", {})

                        for key, value_obj in params.items():
                            if key.startswith("PVAL_"):
                                # Extract value from {"v": "90", "ut": "..."}
                                if isinstance(value_obj, dict) and "v" in value_obj:
                                    try:
                                        # Convert to appropriate type (int or float)
                                        val = value_obj["v"]
                                        if isinstance(val, str):
                                            # Try float first (handles both int and float)
                                            pval_data[key] = float(val)
                                        else:
                                            pval_data[key] = val
                                    except (ValueError, TypeError):
                                        pval_data[key] = value_obj["v"]

                        _LOGGER.debug("Retrieved %d PVAL parameters from portal", len(pval_data))
                        return pval_data
                    else:
                        _LOGGER.error("Failed to get installation status: %d", resp.status)
                        return {}

        except Exception as err:
            _LOGGER.error("Error getting installation status: %s", err)
            return {}

    async def close(self):
        """Close the session."""
        if self._session:
            await self._session.close()
            self._session = None
        self._logged_in = False
