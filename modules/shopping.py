from db import db

class ShoppingList(db.Model):

    __tablename__ = 'Selver'

    #pylint: disable = no-member

    id = db.Column(db.Integer, primary_key=True) 
    toode = db.Column(db.String(50)) 
    hind = db.Column(db.String(20)) 
    hind_kogus = db.Column(db.String(20)) 



    def __init__(self, id: int, toode: str, hind: str, hind_kogus: str) -> None:
        self.id = id
        self.toode = toode
        self.hind = hind
        self.hind_kogus = hind_kogus

    def json(self):
        return {
                'id':self.id,
                'toode':self.toode,
                'hind':self.hind,
                'hind_kogus':self.hind_kogus             
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
    def find_item_by_name(cls, toode):
        return cls.query.filter_by(toode=toode).first()