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

from marshmallow import (Schema,fields,validate,post_load,validates_schema,ValidationError)

class ServerSchema(Schema):
    """Redis server records 
    """
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True,validate=validate.Length(2,64))
    description = fields.String(validate=validate.Length(0,512))
    host = fields.String(required=True,validate=validate.Regexp(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$'))
    port = fields.Integer(validate=validate.Range(1024,65535))
    password = fields.String()
    updated_at = fields.DateTime(dump_only=True)
    created_at = fields.DateTime(dump_only=True)

    @validates_schema
    def validate_schema(self,data):
        """test if the name redis server
        """
        if 'port' not in data:
            data['port'] = 6379
        instance = self.context.get('instance',None)
        server = Server.query.filter_by(name=data['name']).first()
        if server is None:
            return 
        if instance is not None and server != instance:
            raise ValidationError('Redis server already exist','name')
        if instance is None and server:
            raise validationError('Redis server already exist','name')

        @post_load
        def create_or_update(self,data):
            """data loading server auto_create server object
            """
            instance = self.context.get('instance',None)
            #create redis server
            if instance is None:
                return Server(**data)
            for key in data:
                setattr(instance,key,data[key])
            return instance

