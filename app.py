import os

from flask import (
                    render_template,
                    Flask,
                    request
)
from flask_restful import Api

from resources.shopping import Shopping, ShowAllShoppingLIst
from data.dataParser import ParseJsonToHTML

from db import db
from forms import SearchForms
# from flask_jwt import JWT

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL','sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['THREADED'] = True
app.config['PORT'] = 6060
app.secret_key = '4567yt'

api = Api(app)
db.init_app(app)

api.add_resource(ShowAllShoppingLIst,'/shoppinglist')
api.add_resource(Shopping,'/shopping/<string:_id>')


@app.route('/', methods=['POST','GET'])
def home():
    data = ParseJsonToHTML().convert()
    form = SearchForms()
    #breakpoint()
    return render_template('home.html', form=form)

if(__name__=="__main__"):

    with app.app_context():
        db.create_all()
    
    app.run()
    