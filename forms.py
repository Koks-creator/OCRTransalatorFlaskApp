from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileAllowed


class ImageForm(FlaskForm):
    image = FileField("", validators=[FileAllowed(['jpg', 'png']), DataRequired()])
    lang_select = SelectField("Languages", choices=[
        ('en', 'English'),
        ('de', 'German'),
        ('fr', 'French'),
        ('hi', 'Hindi'),
        ('pl', 'Polish'),
        ('sp', 'Spanish'),
    ], render_kw={'style': 'width: 300px;'})
    submit = SubmitField("Send", render_kw={'class': 'btn btn-outline',
                                            'style': 'width: 300px; height: 50px; background-color: #d5bdaf;'},)
