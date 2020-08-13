import datetime as dt

from django.db import models
from django.utils.translation import ugettext_lazy as _


class User(models.Model):
    email = models.EmailField(_("User's email"), null=False, db_index=True)
    created_ts = models.DateTimeField(_("User created timestamp"), default=dt.datetime.now)

    class Meta:
        db_table = 'users'

    def __str__(self):
        return f'email: {self.email}'

