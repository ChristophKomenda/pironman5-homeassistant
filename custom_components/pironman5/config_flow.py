import logging

import aiohttp
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_HOST, CONF_PORT

from .const import API_PATH, DEFAULT_HOST, DEFAULT_PORT, DOMAIN


_LOGGER = logging.getLogger(__name__)


class Pironman5ConfigFlow(
    config_entries.ConfigFlow,
    domain=DOMAIN,
):
    VERSION = 1

    async def async_step_user(
        self,
        user_input=None,
    ):
        errors = {}

        if user_input is not None:
            host = user_input[CONF_HOST]
            port = user_input[CONF_PORT]

            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(
                        f"http://{host}:{port}{API_PATH}/get-device-info",
                        timeout=aiohttp.ClientTimeout(total=5),
                    ) as response:
                        response.raise_for_status()
                        result = await response.json()

                if not result.get("status"):
                    raise ValueError(
                        "Pironman API returned status=false"
                    )

                device_info = result.get(
                    "data",
                    {},
                )

                device_name = device_info.get(
                    "name",
                    "Pironman 5",
                )

                await self.async_set_unique_id(host)
                self._abort_if_unique_id_configured()

                return self.async_create_entry(
                    title=device_name,
                    data=user_input,
                )

            except (
                aiohttp.ClientError,
                TimeoutError,
                ValueError,
            ) as err:
                _LOGGER.debug(
                    "Unable to connect to Pironman API: %s",
                    err,
                )
                errors["base"] = "cannot_connect"

            except Exception:
                _LOGGER.exception(
                    "Unexpected error while configuring Pironman 5"
                )
                errors["base"] = "unknown"

        schema = vol.Schema(
            {
                vol.Required(
                    CONF_HOST,
                    default=DEFAULT_HOST,
                ): str,
                vol.Required(
                    CONF_PORT,
                    default=DEFAULT_PORT,
                ): vol.All(
                    int,
                    vol.Range(
                        min=1,
                        max=65535,
                    ),
                ),
            }
        )

        return self.async_show_form(
            step_id="user",
            data_schema=schema,
            errors=errors,
        )
