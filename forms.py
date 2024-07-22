from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length, NumberRange

class SpotForm(FlaskForm):
    name = StringField('スポット名', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('説明')
    address = StringField('住所', validators=[DataRequired(), Length(max=200)])
    dog_friendly_rating = IntegerField('ドッグフレンドリー度（1-5）', validators=[DataRequired(), NumberRange(min=1, max=5)])
    submit = SubmitField('追加')

class LoginForm(FlaskForm):
    username = StringField('ユーザー名', validators=[DataRequired()])
    password = PasswordField('パスワード', validators=[DataRequired()])
    submit = SubmitField('ログイン')