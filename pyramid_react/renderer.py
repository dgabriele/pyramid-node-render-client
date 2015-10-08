import re
import requests
import requests_unixsocket


class ReactRenderer(object):
    """ Renderer that outsources HTML rendering to react-render-service, which
        can be found here: https://github.com/dgabriele/react-render-service.
    """

    def __init__(self, info):
        # bind can be an http or domain socket.
        # EG: '/tmp/react.sock' or 'localhost:8080'
        self.template = info.name.split('.')[0]
        self.bind = info.settings.get('react.bind')
        if not self.bind:
            raise ValueError('react.bind must be defined in settings')
        if re.match(r'^(.+):(\d+)$', self.bind):
            self.session = requests.Session()
            self.url = 'http://{}/render'.format(self.bind)
        else:
            socket_path = self.bind.rstrip('/').replace('/', '%2F')
            self.session = requests_unixsocket.Session()
            self.url = 'http+unix://{}/render'.format(socket_path)

    def __call__(self, value, system):
        return self.session.post(self.url, json={
            'template': self.template,
            'context': value,
        }).text
