from flask_wtf import FlaskForm
from wtforms.fields.numeric import IntegerField
from wtforms.fields.simple import StringField, SubmitField
from wtforms.validators import DataRequired


class CreateItemForm(FlaskForm):
    name = StringField('Item Name', validators=[DataRequired()])
    brand = StringField('Item Brand', validators=[])
    model = StringField('Item Model', validators=[])
    serial_number = StringField('Item Serial Number', validators=[])
    submit = SubmitField('Submit')


class UpdateItemForm(FlaskForm):
    item_id = IntegerField('Item ID', validators=[DataRequired()])
    name = StringField('Item Name', validators=[])
    brand = StringField('Item Brand', validators=[])
    model = StringField('Item Model', validators=[])
    serial_number = StringField('Item Serial Number', validators=[])
    submit = SubmitField('Submit')


class DeleteItemForm(FlaskForm):
    item_id = IntegerField('Item ID', validators=[DataRequired()])
    submit = SubmitField('Submit')
