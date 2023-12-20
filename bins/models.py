import uuid

from django.db import models
from datetime import timedelta, datetime

from django.urls import reverse


class Bins(models.Model):
    EXPIRATION_CHOICES = [
        ('1', '1 day'),
        ('7', '7 days'),
        ('30', '30 days'),
        ('0', 'Never'),
    ]

    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    code = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    expiry_policy = models.CharField(max_length=7, choices=EXPIRATION_CHOICES, default='never')
    expires_on = models.DateTimeField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.pk is None:  # if the record is being initialized for first time
            match self.expiry_policy:
                case '1':
                    self.expires_on = datetime.now() + timedelta(days=1)
                case '7':
                    self.expires_on = datetime.now() + timedelta(days=7)
                case '30':
                    self.expires_on = datetime.now() + timedelta(days=30)
                case '0':
                    self.expires_on = datetime.now() + timedelta(weeks=100000)

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Pastebin Entry on {self.created_on.strftime('%Y-%m-%d %H:%M:%S')}"

    def first_20_characters(self):
        return self.code[:20]

    def get_absolute_url(self):
        return reverse('note', args=[self.uuid])

    def is_expired(self):
        import pytz

        is_expired = self.expires_on < datetime.now(pytz.timezone('UTC'))

        return is_expired
