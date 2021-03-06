import os

from flask import send_from_directory, jsonify
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = ['tar', 'zip', 'gz', 'vcf']


def download_file_path_get(file_path):  # noqa: E501
    """download_file_path_get

    Download a result file from given path # noqa: E501

    :param file_path: Path to the file
    :type file_path: str

    :rtype: file
    """
    return send_from_directory(os.path.join(os.getenv('BASE_DIR', os.getcwd()), 'runs'), file_path)


def upload_post(uploaded_file=None, user=None):  # noqa: E501
    """upload_post
    Uploads a file to the server # noqa: E501
    :param uploadedFile: The GSVar file to upload.
    :type uploadedFile: werkzeug.datastructures.FileStorage
    :param user: The user name.
    :type user: str.
    :rtype: None
    """
    file_name = secure_filename(uploaded_file.filename)
    if not any(map(lambda extension: file_name.endswith(extension), ALLOWED_EXTENSIONS)):
        return "File must be one of allowed types.", 400
    abs_folder_path = os.path.join(
        os.getenv('DATA_DIR', os.getcwd()),
        user
    )
    abs_file_path = os.path.join(
        abs_folder_path,
        file_name
    )
    if not os.path.exists(abs_folder_path):
        os.mkdir(abs_folder_path)
    # this will raise a IOError if something goes wrong
    uploaded_file.save(abs_file_path)

    return jsonify({
        'url': file_name
    })
