from db import db
from datetime import datetime

class ToBuyList(db.Model):

    __tablename__='things_to_buy'

    #pylint: disable = no-member

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    toode = db.Column(db.String(50), nullable=False)
    hind = db.Column(db.String(20), nullable=True)
    kogus = db.Column(db.Integer, nullable=False)
    hind_kogus = db.Column(db.String(20), nullable=True)
    date = db.Column(db.String(30), nullable=False)

    #things = db.relationship('Selver', lazy='dynamic')


    def __init__(self, toode: str, hind: str=None, kogus: int=None, hind_kogus: str=None) -> None:
        self.toode = toode
        self.hind = hind
        self.kogus = kogus
        self.hind_kogus = hind_kogus
        self.date = datetime.now()

    def json(self):
        return {
                'toode':self.toode,
                'hind':self.hind,
                'kogus':self.kogus,
                'hind_kogus':self.hind_kogus,
                'kuupaev':self.date
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls,id=id):
        return cls.query.filter_by(id=id).first()
    

    @classmethod
    def find_by_name(cls, toode=toode):
        return cls.query.filter_by(toode=toode).first()

    @classmethod
    def find_by_date(cls, date=date):
        return cls.query.filter_by(date=date).first()



