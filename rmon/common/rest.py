""" rmon.common.rest """
from collections import Mapping
from flask import request,Response,make_response
from flask.json import dumps
from flask.views import MethodView

class RestException(Exception):
    """ basic class exception """
    def __init__(self,code,message):
        """ initialing  exception
            Args:
                code(int):http status number
                message(str):error message
        """
        self.code = code
        self.message = message
        super(RestException,self).__init__()

class RestView(MethodView):
    """ create view json serial error 
    """
    content_type = 'application/json;charset=utf-8'
    method_decorators = []
    
    def handler_error(self,exception):
        """handler error
        """
        data = {
                'ok':False,
                'message':exception.message
                }
        result = dumps(data) + '\n'
        resp = make_response(result,exception.code)
        resp.header['Content-Type'] = self.content_type
        return resp

    def dispatch_request(self,*args,**kwargs):
        """ rewrite base class function ,for auto_serialiaze
        """
        method = getattr(self,request.method.lower(),None)
        if method is None and request.method == 'HEAD':
            method = getattr(self,'get',None)
        assert method is not None, 'UNimplemented method %r' %request.method
        # head functions is differe
        if isinstance(self.method_decorators,Mapping):
            decorators = self.method_decorators(request.method.lower(),[])
        else:
            decorators = self.method_decorators

        for decorator in decorators:
            method = decorator(method)

        try:
            resp = method(*args,**kwargs)
        except RestException as e:
            resp = self.handler_error(e)

        if isinstance(resp,Response):
            return resp

        data,code,headers = RestView.unpack(resp)

        if code >= 400 and isinstance(data,dict):
            for key in data:
                if isinstance(data[key],list) and len(data[key]) > 0:
                    message = data[key][0]
                else:
                    message = data[key]
            data = { 'ok':False,'message':message }

        result = dumps(data) + '\n'
        response = make_response(result,code)
        response.headers.extend(headers)

        response.headers['Content-Type'] = self.content_type
        return response
    
    @staticmethod
    def unpack(value):
        """ return views return 
        """
        headers = {}
        if not isinstance(value,tuple):
            return value,200,{}
        if len(value) == 3:
            data,code,headers = value
        elif len(value) == 2:
            data,code = value
        return data,code,headers


