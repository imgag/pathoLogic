import os
import connexion
import six

from flask import send_from_directory

from openapi_server import util

def download_file_path_get(file_path):  # noqa: E501
    """download_file_path_get

    Download a result file from given path # noqa: E501

    :param file_path: Path to the file
    :type file_path: str

    :rtype: file
    """
    return send_from_directory(os.path.join(os.getenv('BASE_DIR', os.getcwd()), 'runs'), file_path)
