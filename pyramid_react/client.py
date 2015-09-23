import os
import re
import glob
import logging

import requests
import requests_unixsocket


class ReactClient(object):
    """ Server-side React rendering client.
    """

    @classmethod
    def from_settings(cls, settings):
        return cls(http=settings.get('react.http'),
                   socket=settings.get('react.socket'))

    def __init__(self, http=None, socket=None):
        self.log = logging.getLogger(self.__class__.__name__)
        if not (http or socket):
            raise ValueError('http or socket must be defined')
        if http:
            self._init_http(http)
        elif socket:
            self._init_socket(socket)

    def _init_http(self, socket_str):
        self.session = requests.Session()
        if not socket_str.startswith('http://'):
            socket_str = 'http://' + socket_str
        self.render_endpoint = socket_str.rstrip('/') + '/render'
        self.transform_endpoint = socket_str.rstrip('/') + '/transform'

    def _init_socket(self, socket_str):
        self.session = requests_unixsocket.Session()
        self.render_endpoint = 'http+unix://{socket_str}/render'.format(
            socket_str=socket_str.rstrip('/').replace('/', '%2F'))
        self.transform_endpoint = 'http+unix://{socket_str}/transform'.format(
            socket_str=socket_str.rstrip('/').replace('/', '%2F'))

    def transform(self, component_name, file_path):
        return self.session.post(self.transform_endpoint, json={
            'component_name': component_name,
            'file_path': file_path,
        }).ok

    def transform_path(self, path):
        dir_names = path.split()
        re_jsx = re.compile(r'(?P<stem>[\w+\.\-]+)\.jsx$')
        for dir_name in dir_names:
            jsx_dir = os.path.join(dir_name, '*.jsx')
            for jsx_fpath in glob.glob(jsx_dir):
                match = re_jsx.search(jsx_fpath)
                self.transform(match.group('stem'), jsx_fpath)

    def render(self, component_name, props=None):
        return self.session.post(self.render_endpoint, json={
            'component_name': component_name,
            'props': props,
        }).json()
