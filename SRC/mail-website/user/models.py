import random
from django.conf import settings
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.core.validators import RegexValidator, ValidationError, EmailValidator
from django.utils.deconstruct import deconstructible
from .managers import CustomUserManager
import re


@deconstructible
class MobileNumberValidator(RegexValidator):
    # A rejection to check user input information
    regex = r"^[0][9]\d{9}$"

    message = _(
        'Enter a valid mobile number. This value may contain only numbers.'
    )
    flags = 0


# create an instance from the class
mobile_number_validation = MobileNumberValidator()


def username_validation(username_str):
    result = re.search('@mail.com$', username_str)
    if result:
        raise ValidationError('username should be without domain')


class Users(AbstractUser):
    username_validator_django = UnicodeUsernameValidator()
    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator_django, username_validation],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    verification_choice = [
        ('Phone', 'Phone'),
        ('Email', 'Email')
    ]
    verification = models.CharField(default='',
                                    max_length=10,
                                    choices=verification_choice
                                    )
    phone = models.CharField(
        max_length=11,
        unique=True,
        verbose_name=_('Phone Number'),
        validators=[mobile_number_validation],
        error_messages={
            'unique': _("A user with that Phone number already exists."),
        },
        help_text=_('Example') + " : 09125573688")

    email = models.EmailField(_('email address'), unique=True, )

    birth_date = models.DateField(null=True, blank=True)
    nationality = models.CharField(max_length=100, null=True, blank=True)
    gender_choices = [
        ('F', 'Female'),
        ('M', 'Male'),
        ('N', 'None'),
    ]
    gender = models.CharField(max_length=10, choices=gender_choices, null=True, blank=True)
    is_active = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def __str__(self):
        return f"{self.username}"

    def get_full_name(self):
        # If the full name is not specified, return username
        if self.first_name == "" and self.last_name == "":
            return self.username
        else:
            return self.first_name + " " + self.last_name

    get_full_name.short_description = 'Name'

    def save(self, *args, **kwargs):
        if not self.is_superuser:
            if '@mail.com' not in self.username:
                self.username += '@mail.com'
        else:
            self.email = f'{self.username}@mail.com'
            self.phone = f'09{random.randint(100000000,999999999)}'
        super(Users, self).save(*args, **kwargs)


class Contact(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='contacts')
    email = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,
                              related_name='contact_email')
    name = models.CharField(max_length=100, default=None)
    birth_date = models.DateField(verbose_name='birth date', null=True, blank=True)
    other_email = models.EmailField(null=True, blank=True, default='')
    phone_number = models.CharField(verbose_name='phone number', max_length=11, validators=[mobile_number_validation],
                                    null=True, blank=True)

    class Meta:
        unique_together = [('owner', 'email')]

    def __str__(self):
        return f"{self.email}"


class CodeRegister(models.Model):
    code = models.IntegerField()
    phone_number = models.CharField(max_length=11, validators=[mobile_number_validation])
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.code}"
