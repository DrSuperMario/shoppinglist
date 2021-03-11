from flask_wtf import FlaskForm
from sqlalchemy.sql.selectable import HasPrefixes
from wtforms import ( 
                        StringField, 
                        SubmitField,
                        TextAreaField,
                        SelectField,
                        HiddenField,
                        BooleanField,
                     
                    )
import pandas as pd


csv_file = pd.read_csv('selver_data.csv')
csv_file.drop(['Unnamed: 0'], axis=1, inplace=True)

class SearchForms(FlaskForm):


    toode_box = StringField('toode')
    toode_test_box = SelectField('Otsi toodet',choices=[i for i in csv_file['Toode']])
    kogus_box = StringField('kogus')
    kirjeldus_box = TextAreaField('kirjeldus')
    lisa_box = SubmitField('lisa toode')
    kustuta_box = SubmitField('kustuta toode')
    kustuta_link = HiddenField('kustuta')
    toode_check = BooleanField('Checkboxs')

