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
        self.url = self.settings.get("url")
        self.key = self.settings.get("key")
        self.timeout = self.settings.get("timeout", 10)
        self.verify = self.settings.get("verify", False)

    def setup(self):
        if not self.url or not self.key:
            self.speak_dialog("error_setup", data={"fields": "address or key"})
            LOG.warning("MagicMirror address or API key not defined")
        else:
            self.configured = True
            self.headers["Content-Type"] = "application/json"
            self.headers["X-Api-Key"] = self.key
            LOG.info("MagicMirror address: %s", self.url)

    def initialize(self):
        self.setup()
        self.add_event("recognizer_loop:record_begin", self.handle_listener_started)
        self.add_event("recognizer_loop:record_end", self.handle_listener_ended)

    def handle_listener_started(
        self, message: Message
    ):  # pylint: disable=unused-argument
        """Handle the record_begin event detection."""
        payload = {"notification": "OVOS_SEND_MESSAGE", "payload": "Listening"}
        try:
            requests.post(
                url=self.url + "/ovos",
                data=json.dumps(payload),
                headers=self.headers,
                verify=self.verify,
                timeout=self.timeout,
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
                url=self.url + "/ovos",
                data=json.dumps(payload),
                headers=self.headers,
                verify=self.verify,
                timeout=self.timeout,
            )
        except requests.exceptions.RequestException as err:
            LOG.error(err)
