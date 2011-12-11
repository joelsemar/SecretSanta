from django.db import models
from django.core.mail import send_mail
# Create your models here.
#
class Entrant(models.Model):
    name = models.CharField(max_length=256)
    email = models.CharField(max_length=256)
    zip = models.CharField(max_length=256, default='')
    city = models.CharField(max_length=256, default='')
    state = models.CharField(max_length=256, default='')
    street = models.CharField(max_length=256, default='')
    match = models.ForeignKey('self', null=True)
    hint  =  models.TextField(default='')


    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        super(Entrant, self).save(*args, **kwargs)
        send_mail('Secret Santa', 'Just making sure you gave a valid email address. You\'ll get another email telling you about your victim after everyone signs up.'
                  , 'secretsanta@joelsemar.com', [self.email], fail_silently=True) 
