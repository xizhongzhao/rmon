""" rmon.common.rest """

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
