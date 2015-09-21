import logging
import os
import glob

from pathlib import PurePath
from os.path import getmtime

from react import jsx


log = logging.getLogger(__name__)


def transform_directory(src_dir, dst_dir):
    """ Transform all JSX files in src_dir to JS files in dst_dir. Only
        transform JSX files that are new or have been modified.
    """
    transformer = jsx.JSXTransformer()
    for jsx_filename in glob.glob(os.path.join(src_dir, '*.jsx')):
        src_path = PurePath(jsx_filename)
        dst_path = PurePath(dst_dir, src_path.stem + '.js')
        src_path_str = str(src_path)
        dst_path_str = str(dst_path)
        is_new = (not os.path.exists(dst_path_str))
        if is_new or (getmtime(src_path_str) > getmtime(dst_path_str)):
            log.debug('Transforming JSX: {}'.format(src_path_str))
            transformer.transform(src_path_str, js_path=dst_path_str)
