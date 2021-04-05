"""MagicMirror wake word entrypoint skill
"""
from mycroft import MycroftSkill
import json
import requests

__author__ = 'smartgic'


class MagicMirrorWakeWord(MycroftSkill):
    """This is the place where all the magic happens for the MagicMirror
    wake word skill.
    """

    def __init__(self):
        MycroftSkill.__init__(self)

        # Initialize variables with empty or None values.
        self.configured = False
        self.headers = {}

    def _setup(self):
        """Provision initialized variables and retrieve configuration
        from home.mycroft.ai.
        """
        self.url = self.settings.get('url')
        self.key = self.settings.get('key')
        self.verify = self.settings.get('verify')

        # Make sure the requirements are fulfill.
        if not self.url or not self.key:
            self.speak_dialog('error.setup',
                              data={"field": "address or api key"})
            self.log.warning('MagicMirror address or API key not defined')
        else:
            self.configured = True

            # Construct the headers dict.
            self.headers['Content-Type'] = 'application/json'
            self.headers['X-Api-Key'] = self.key

            self.log.info('MagicMirror address: {}'.format(self.url))

    def initialize(self):
        """The initialize method is called after the Skill is fully
        constructed and registered with the system. It is used to perform
        any final setup for the Skill including accessing Skill settings.
        https://tinyurl.com/4pevkdhj
        """
        self.settings_change_callback = self.on_websettings_changed
        self.on_websettings_changed()

    def on_websettings_changed(self):
        """Each Mycroft device will check for updates to a users settings
        regularly, and write these to the Skills settings.json.
        https://tinyurl.com/f2bkymw
        """
        self._setup()
        self._run()

    def _run(self):
        """Based on event, functions will be called to send different
        notifications.
        """
        if self.configured:
            try:
                # Catch events
                self.add_event('recognizer_loop:record_begin',
                               self._handle_listener_started)
                self.add_event('recognizer_loop:record_end',
                               self._handle_listener_ended)
            except Exception:
                self.log.error('Cannot initialize MagicMirror skill')
                self.speak_dialog('error.initialize')

    def _handle_listener_started(self):
        """Handle the record_begin event detection.
        """
        payload = {"notification": "MYCROFT_SEND_MESSAGE",
                   "payload": "Listening"}
        try:
            requests.post(url=self.url + '/mycroft',
                          data=json.dumps(payload),
                          headers=self.headers,
                          verify=self.verify)
        except requests.exceptions.RequestException as err:
            return err

    def _handle_listener_ended(self):
        """Handle the record_end event detection.
        """
        payload = {"notification": "MYCROFT_DELETE_MESSAGE",
                   "payload": "delete"}
        try:
            requests.post(url=self.url + '/mycroft',
                          data=json.dumps(payload),
                          headers=self.headers,
                          verify=self.verify)
        except requests.exceptions.RequestException as err:
            return err


def create_skill():
    """Main function to register the skill
    """
    return MagicMirrorWakeWord()
