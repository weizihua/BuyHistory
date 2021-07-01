# -*- coding: utf-8 -*-
"""Public forms."""
from flask_wtf import FlaskForm
from werkzeug.utils import validate_arguments
from wtforms import RadioField, StringField, SubmitField
from wtforms.validators import URL, DataRequired, Length, ValidationError


class QueryForm(FlaskForm):
    """Login form."""

    address = StringField(
        "address", validators=[DataRequired(), Length(max=2047), URL()]
    )
    range = RadioField("range", choices=["7", "31", "90", "365"])
    submit = SubmitField()

    def validate_address(self, field):
        """Validate the form."""
        if "amazon" not in field.data:
            raise ValidationError("Please query an Amazon products address!")
