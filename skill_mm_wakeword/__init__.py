import json
import requests

from ovos_bus_client.message import Message
from ovos_utils.log import LOG
from ovos_workshop.skills import OVOSSkill


class MagicMirrorWakeWord(OVOSSkill):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.configured = False
        self.headers = {}
        self.setup()

    def setup(self):
        if not self.settings.get("url") or not self.settings.get("key"):
            self.speak_dialog("error_setup", data={"fields": "address or key"})
            LOG.warning("MagicMirror address or API key not defined")
        else:
            self.configured = True
            self.headers["Content-Type"] = "application/json"
            self.headers["X-Api-Key"] = self.settings.get("key")
            LOG.info("MagicMirror address: %s", self.settings.get("url"))

    def initialize(self):
        self.add_event("recognizer_loop:record_begin", self.handle_listener_started)
        self.add_event("recognizer_loop:record_end", self.handle_listener_ended)

    def handle_listener_started(
        self, message: Message
    ):  # pylint: disable=unused-argument
        """Handle the record_begin event detection."""
        payload = {"notification": "OVOS_SEND_MESSAGE", "payload": "Listening"}
        try:
            requests.post(
                url=self.settings.get("url") + "/ovos",
                data=json.dumps(payload),
                headers=self.headers,
                verify=self.settings.get("verify", False),
                timeout=self.settings.get("timeout", 10),
            )
        except requests.exceptions.RequestException as err:
            LOG.error(err)

    def handle_listener_ended(
        self, message: Message
    ):  # pylint: disable=unused-argument
        """Handle the record_end event detection."""
        payload = {"notification": "OVOS_DELETE_MESSAGE", "payload": "delete"}
        try:
            requests.post(
                url=self.settings.get("url") + "/ovos",
                data=json.dumps(payload),
                headers=self.headers,
                verify=self.settings.get("verify", False),
                timeout=self.settings.get("timeout", 10),
            )
        except requests.exceptions.RequestException as err:
            LOG.error(err)
