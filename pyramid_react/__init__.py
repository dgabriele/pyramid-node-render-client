
from .client import ReactClient


def includeme(config):
    settings = config.get_settings()

    client = ReactClient.from_settings(settings)

    # transform each JSX file on the path
    client.transform_path(settings['react.path'])

    def react(req):
        return client

    config.add_request_method(react, reify=True)
