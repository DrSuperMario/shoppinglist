from datetime import datetime

from flask_restful import Resource, reqparse

from modules.shopping import ShoppingList


class Shopping(Resource):

    parser = reqparse.RequestParser()

    parser.add_argument('toode' , type=str, required=True, help='Item name must be added')
    parser.add_argument('hind', type=int, required=False, help='Quantity is defaulted to one if not added')
    parser.add_argument('hind_kogus', type=str, required=False, help="item description, not required")

    def get(self, _id):
        _id = ShoppingList.find_item_by_id(_id)
        if(_id):
            return _id.json()
        return {"Message":"Item not found on the list"}, 404

    def post(self, _id):
        items = Shopping.parser.parse_args()
        items['dateAdded'] = datetime.strftime(datetime.now(), "%d-%m-%y %H:%M")

        item = ShoppingList(_id, **items)
        #breakpoint()
        
        try:
            item.save_to_db()
        
        except:
            return {"Message":"error occured while saving"},404

        return item.json(),201


class ShowAllShoppingLIst(Resource):

    def get(self):
        return {'shopping':[x.json() for x in ShoppingList.query.all()]}