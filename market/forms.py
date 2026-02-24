from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, Email, ValidationError
from market.models import User


class RegisterForm(FlaskForm):

    username = StringField(
        label='Korisničko ime',
        validators=[
            DataRequired(message="Korisničko ime je obavezno."),
            Length(
                min=2,
                max=30,
                message="Korisničko ime mora imati između 2 i 30 karaktera."
            )
        ]
    )

    email_address = StringField(
        label='Email adresa',
        validators=[
            DataRequired(message="Email adresa je obavezna."),
            Email(message="Unesite ispravnu email adresu.")
        ]
    )

    password1 = PasswordField(
        label='Lozinka',
        validators=[
            DataRequired(message="Lozinka je obavezna."),
            Length(
                min=6,
                message="Lozinka mora imati najmanje 6 karaktera."
            )
        ]
    )

    password2 = PasswordField(
        label='Potvrdite lozinku',
        validators=[
            DataRequired(message="Potvrda lozinke je obavezna."),
            EqualTo(
                'password1',
                message="Lozinke se ne poklapaju."
            )
        ]
    )

    submit = SubmitField(label='Kreiraj nalog')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("Korisničko ime već postoji.")

    def validate_email_address(self, email_address):
        user = User.query.filter_by(email_address=email_address.data).first()
        if user:
            raise ValidationError("Email adresa je već registrovana.")


class LoginForm(FlaskForm):

    username = StringField(
        label='Korisničko ime',
        validators=[
            DataRequired(message="Unesite korisničko ime.")
        ]
    )

    password = PasswordField(
        label='Lozinka',
        validators=[
            DataRequired(message="Unesite lozinku.")
        ]
    )

    submit = SubmitField(label='Prijavi se')