from flask_wtf import FlaskForm
from wtforms import StringField

class QueryForm(FlaskForm):
    keyword = StringField(name='keyword')

