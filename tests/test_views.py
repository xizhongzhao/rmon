import json
from flask import url_for
from rmon.models import Server

class TestServerList:
    """test redis server list api
    """
    endpoint = 'api.server_list'

