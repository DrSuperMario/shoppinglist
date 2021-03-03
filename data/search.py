from db import db


class InitDB(db.Model):

    __tablename__="Selver Items and Prices"

    @classmethod
    def find_by_name(cls,name):
        return cls.query().filter_by(index=name).first()

    @classmethod
    def get_all_items(cls):
        return cls.query.all()    