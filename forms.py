from flask_wtf import FlaskForm
from wtforms import ( 
                        StringField, 
                        SubmitField,
                        TextAreaField,
                        SelectField
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
