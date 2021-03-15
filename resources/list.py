from flask_restful import Resource, reqparse
from modules.list import ToBuyList


class ToBuy(Resource):

    parser = reqparse.RequestParser()

    parser.add_argument('toode', type=str, required=True, help="Toode lisamiseks ei leitud")
    parser.add_argument('hind', type=str, required=False, help="Hind")
    parser.add_argument('kogus', type=int, required=True, help="Kogus")
    parser.add_argument('hind_kogus', type=str, required=False, help="Hind/Kogus")
    parser.add_argument('tahtsus', type=str, required=True, help="tahtsus")



    def get(self,id):
        name = ToBuyList.find_by_id(id)
        if(name):
            return name.json(),200
        return {"message":"Toodet ei ole olemas"}, 400

    def post(self):
        tooted = ToBuy.parser.parse_args()
        #breakpoint()
        data = ToBuyList(**tooted)
        #try:
        data.save_to_db()
        # except:
        #     return {"message":"error posting data"}, 400

        return data.json(), 201

class GetAllToBuy(Resource):
    @classmethod
    def get(cls):
        return {'shopping_list':[x.json() for x in ToBuyList.query.all()]}