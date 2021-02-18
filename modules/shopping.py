from db import db

class ShoppingList(db.Model):

    __tablename__ = 'shopping_list'

    id = db.Column(db.Integer, primary_key=True)
    itemName = db.Column(db.String(20))
    itemQuantity = db.Column(db.Integer)
    itemDescription = db.Column(db.String(100))
    itemCost = db.Column(db.String(10))
    dateAdded = db.Column(db.String(20))


    def __init__(self, id, itemName, itemQuantity, itemDescription, itemCost, dateAdded):
        self.id = id
        self.itemName = itemName
        self.itemQuantity = itemQuantity
        self.itemDescription = itemDescription
        self.itemCost = itemCost
        self.dateAdded = dateAdded


    def json(self):
        return {
            'id':self.id,
            'itemName':self.itemName,
            'itemQuantity':self.itemQuantity,
            'itemDescription':self.itemDescription,
            'itemCost':self.itemCost,
            'dateAdded':self.dateAdded
        }
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_b(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_item_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_item_by_name(cls, itemName):
        return cls.query.filter_by(itemName=itemName).first()