from openapi_server.db import get_db


def status_get():  # noqa: E501
    """Get list of all sample statuses

     # noqa: E501


    :rtype: List[object]
    """
    db = get_db()
    return [{'id': sample, 'status': db['samples'][sample]['status']} for sample in db['samples'].keys()]
