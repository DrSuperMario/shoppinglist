
from db import db
from flask_restful import Resource
from modules.list import ToBuyList

class GetData(Resource):
    @classmethod
    def all_data(cls):
        toode =  [x.toode for x in ToBuyList.query.all()]
        hind = [x.hind for x in ToBuyList.query.all()]
        hind_kogus = [x.hind_kogus for x in ToBuyList.query.all()]

        return toode, hind, hind_kogus
            