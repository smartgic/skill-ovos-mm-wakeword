from mycroft import MycroftSkill
import json
import requests

__author__ = 'smartgic'


class MagicMirrorWakeWord(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

        # By default the skill requires configuration
        self.configured = False
        self.headers = {}

    def _setup(self):
        self.url = self.settings.get('url')
        self.key = self.settings.get('key')
        self.verify = self.settings.get('verify')

        if not self.url or not self.key:
            self.speak_dialog('error.setup',
                              data={"field": "address or api key"})
            self.log.warning('MagicMirror URL not defined')
        else:
            self.configured = True
            self.headers['X-Api-Key'] = self.key
            self.log.info('MagicMirror URL: {}'.format(self.url))

    # See https://bit.ly/37pwxIC (Mycroft documentation about skill lifecycle)
    def initialize(self):
        # Callback when setting changes are detected from home.mycroft.ai
        self.settings_change_callback = self.on_websettings_changed
        self.on_websettings_changed()

    # What to do in case of setting changes detected
    def on_websettings_changed(self):
        self._setup()
        self._run()

    def _run(self):
        # Run only when the skill is properly configured
        if self.configured:
            try:
                # Catch event
                self.add_event('recognizer_loop:record_begin',
                               self._handle_listener_started)
                self.add_event('recognizer_loop:record_end',
                               self._handle_listener_ended)
            except Exception:
                self.log.error('Cannot initialize MagicMirror skill')
                self.speak_dialog('error.initialize')

    def _handle_listener_started(self):
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
    return MagicMirrorWakeWord()
