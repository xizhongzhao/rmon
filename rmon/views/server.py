from flask import request,g

from rmon.common.rest import RestView
from rmon.models import Server,ServerSchema

class ServerList(RestView):
    """Redis server list
    """
    def get(self):
        """ get redis list
        """
        servers = Server.query.all()
        return ServerSchema().dump(servers,many=True).data

    def post(self):
        """create redis server
        """
        data = request.get_json()
        server,errors = ServerSchema().load(data)
        if errors:
            return errors,400
        server.ping()
        server.save()
        return {'ok':True},201
