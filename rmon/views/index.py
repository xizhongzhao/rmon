""" rmon.view.index """
from  flask import render_template
from flask.views import MethodView

class IndexView(MethodView):
    """ index view """
    def get(self):
        """ render template """
        return render_template('index.html')
