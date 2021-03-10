from modules.list import ToBuyList
import os

from flask import (
                    render_template,
                    Flask,
                    request,
                    redirect,
                    url_for
)
from flask_restful import Api

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
    toode, hind, kogus, _ = GetData().all_data()
    #breakpoint()
    form = SearchForms()
    if(form.is_submitted and request.method=="POST"):
        tooted = {'toode':form.toode_box.data,'kogus':form.kogus_box.data}
        data = ToBuyList(**tooted)
        data.save_to_db()
        return redirect(url_for('home'))

    return render_template('home.html', form=form, toode=zip(toode, kogus, hind))

@app.before_first_request
def first_request():
    db.create_all()

if(__name__=="__main__"):
    app.run()
    