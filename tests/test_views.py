import json
from flask import url_for
from rmon.models import Server

class TestServerList:
    """test redis server list api
    """
    endpoint = 'api.server_list'
    def test_get_servers(self,server,client):
        """ get redis serverlist 
        """
        resp = client.get(url_for(self.endpoint))
        #RestView view base class set http head content-type is json
        assert resp.header['Content-Type'] == 'application/json;charset=utf-8'
        assert resp.status_code == 200
        servers = resp.json
        assert len(servers) == 1

        h = servers[0]
        assert h['name'] == server.name
        assert h['description'] == server.description
        assert h['host'] == server.host
        assert h['port'] == server.port
        assert 'updated_at' in h
        assert 'created_at' in h

    def test_create_server_success(self,db,client):
        """test create redis server success
        """
        pass
    
    def test_create_server_failed_with_invalid_host(self,db,client):
        """
        """
        pass

    def test_create_server_failed_with_duplciate_server(self,server,client):
        """
        """
        pass
