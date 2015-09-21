import os
import re

import requests
import requests_unixsocket


class ReactClient(object):
    """ Server-side React rendering client.
    """

    def __init__(self, component_dir, http_socket=None, unix_socket=None):
        self.component_dir = component_dir
        if not (http_socket or unix_socket):
            raise ValueError('http_socket or unix_socket must be defined')
        if http_socket:
            self._setup_http_socket(http_socket)
        elif unix_socket:
            self._setup_unix_socket(unix_socket)

    def _setup_http_socket(self, http_socket):
        self.session = requests.Session()
        if not re.match('https?://'):
            http_socket = 'http://' + http_socket
        self.render_endpoint = http_socket.rstrip('/') + '/render'

    def _setup_unix_socket(self, unix_socket):
        self.session = requests_unixsocket.Session()
        self.render_endpoint = 'http+unix://{unix_socket}/render'.format(
            unix_socket=unix_socket.rstrip('/').replace('/', '%2F'))

    def render(self, component, props=None):
        component_path = os.path.join(self.component_dir, component) + '.js'
        return self.session.post(self.render_endpoint, json={
            'c': component_path,
            'p': props,
        }).text
