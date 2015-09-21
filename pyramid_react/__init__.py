from .client import ReactClient
from .util import transform_directory


def includeme(config):
    settings = config.get_settings()

    src_dir = settings['react.src-dir']
    dst_dir = settings['react.dst-dir']

    # generate JS files from new or updated JSX files.
    transform_directory(src_dir, dst_dir)

    client = ReactClient(dst_dir,
                         http_socket=settings.get('react.http-socket'),
                         unix_socket=settings.get('react.unix-socket'))

    config.add_request_method(client, 'react', reify=True)
