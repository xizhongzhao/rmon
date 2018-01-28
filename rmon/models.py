""" the part of models """
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from redis import StrictRedis,RedisError
from rmon.common.rest import RestException

db = SQLAlchemy()

class Server(db.Model):
    """ the model of redis server """
    __tablename__ = 'redis_server'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64),unique=True)
    description = db.Column(db.String(512))
    host = db.Column(db.String(15))
    port = db.Column(db.Integer,default=6379)
    password = db.Column(db.String())
    updated_at = db.Column(db.DateTime,default=datetime.utcnow)
    created_at = db.Column(db.DateTime,default=datetime.utcnow)

    def __repr__(self):
        return '<Server(name=%s)>' %self.name

    def save(self):
        """ save data to the database """
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """ delete data from the database """
        db.session.delete(self)
        db.session.commit()
    
    def ping(self):
        """ check redis network is connect """
        try:
            return self.redis.ping()
        except RedisError:
            raise RestException(400,'redis server %s can not connected' %self.host)

    def get_metrics(self):
        """ get redis server details """
        try:
            return self.redis.info()
        except RedisError:
            raise RestException(400,'redis server %s can not connected' %self.host)

    @property
    def redis(self):
        return StrictRedis(host=self.host,port=self.port,password=self.password)
