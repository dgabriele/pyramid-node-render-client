import re
import requests
import requests_unixsocket


class Renderer(object):
    """ Renderer that outsources HTML rendering to node via
        pyramid-node-render-service.

        See: https://github.com/dgabriele/react-render-service.
    """

    RE_HTTP_SOCKET = re.compile(r'^(.+):(\d+)$')

    def __init__(self, info):
        # bind can be an http or domain socket.
        # EG: '/tmp/react.sock' or 'localhost:8080'
        self.template = info.name.split('.')[0]
        self.bind = info.settings.get('node-render-client.bind')
        if not self.bind:
            raise ValueError('react.bind must be defined in settings')
        if self.RE_HTTP_SOCKET.match(self.bind):
            self.session = requests.Session()
            self.url = 'http://{}/render'.format(self.bind)
        else:
            socket_path = self.bind.rstrip('/').replace('/', '%2F')
            self.session = requests_unixsocket.Session()
            self.url = 'http+unix://{}/render'.format(socket_path)

    def __call__(self, value, system):
        if hasattr(value, '__json__'):
            context = value.__json__(request=system.get('request'))
        else:
            context = value
        return self.session.post(self.url, json={
            'template': self.template,
            'context': context,
        }).text
