import datetime
import json
from bson.objectid import ObjectId
from .instance import Config

URI = 'mongodb://{}:{}@{}:{}/{}?authSource={}'.format(Config.MONGODB_USERNAME,
                                                      Config.MONGODB_PASSWORD,
                                                      Config.MONGODB_HOST,
                                                      Config.MONGODB_PORT,
                                                      Config.MONGODB_DB,
                                                      Config.MONGODB_AUTH_DB)


# Here we have extended the 'json-encoder' class to support 'ObjectId' & 'datetime' data types
#    used to store '_id' & 'time-stamp' respectively in MongoDB.  All the response needs to
#    be converted to jason string, to enable the cross-platform data interpretation.
#    We convert the 'ObjectId' & 'datetime' to 'string'.
class JSONEncoder(json.JSONEncoder):
    """ extend json-encoder class """

    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, datetime.datetime):
            return str(o)
        return json.JSONEncoder.default(self, o)
