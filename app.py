from modules.list import ToBuyList
import os
import re

from flask import (
                    render_template,
                    Flask,
                    request,
                    redirect,
                    url_for
)
from flask_restful import Api

from modules.shopping import ShoppingList
from resources.shopping import Shopping, ShowAllShoppingLIst
from resources.list import ToBuy, GetAllToBuy
from dataParser import GetData

from db import db
from forms import SearchForms
# from flask_jwt import JWT

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL','sqlite:///util/selver_data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['THREADED'] = True
app.config['PORT'] = 6060
app.secret_key = '4567yt'

api = Api(app)
db.init_app(app)

api.add_resource(ShowAllShoppingLIst,'/fulllist')
api.add_resource(Shopping,'/shopping/<string:_id>')
api.add_resource(ToBuy,'/tobuy')
api.add_resource(GetAllToBuy,'/tobuylist')



@app.route('/', methods=['POST','GET'])
def home():

    toode, hind, kogus, _ , tahtsus, id = GetData().all_data()
    form = SearchForms()
    raw_data = ShoppingList.query

    if(form.lisa_box.data and request.method=="POST"):
        
        x = form.tahtsus.data
        
        hind = raw_data.filter(ShoppingList.toode.like('%' + form.toode_box.data + '%')).first()

        if(hind):
            tooted = {
                    'toode':hind.toode,
                    'hind':str(float(re.findall(r'(\d+.\d+)',hind.hind)[0].replace(',','.')) * float(form.kogus_box.data)) + ' €',
                    'kogus':form.kogus_box.data,
                    'tahtsus':3 if x is None else form.tahtsus.data
                    }

            data = ToBuyList(**tooted)

            try:
                data.save_to_db()
            except:
                return redirect(url_for('home')),404

        return redirect(url_for('home'))

    if(form.kustuta_box.data and request.method=="POST"):
        x = request.form.getlist('optradio')
        for y in x:
            find_me = ToBuyList.find_by_id(y)
            ToBuyList.delete_from_db(find_me)

        return redirect(url_for('home'))
    #breakpoint()
    return render_template('home.html', form=form, toode=zip(toode, kogus, hind, tahtsus, id))

@app.before_first_request
def first_request():
    db.create_all()

if(__name__=="__main__"):
    app.run()
    