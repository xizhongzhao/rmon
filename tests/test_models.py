from rmon.models import Server

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
