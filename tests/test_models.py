from rmon.models import Server
from rmon.common.rest import RestException

class TestServer:
    """ test server functions """
    def test_save(self,db):
        """ test Server.save function"""
        assert Server.query.count() == 0
        server = Server(name='test',host='127.0.0.1')
        server.save()
        assert Server.query.count() == 1
        assert Server.query.first() == server

    def test_delete(self,db,server):
        """ test Server.delete function """
        assert Server.query.count() == 1
        server.delete()
        assert Server.query.count() == 0

    def test_ping_success(self,db,server):
        """ test server.ping function success """
        assert server.ping() is True

    def test_ping_failed(self,db):
        """ test server.ping function failed """
        server = Server(name='test',host='127.0.0.1',port=6379)
        try:
            server.ping()
        except RestExcption as e:
            assert e.code == 400
            assert e.message == 'redis server %s can not connected' %server.host
