from django.db import models
from django.core.mail import send_mail
# Create your models here.
#

class Group(models.Model):
    name = models.CharField(max_length=256)
    def __unicode__(self):
        return self.name

class Entrant(models.Model):
    name = models.CharField(max_length=256)
    group = models.ForeignKey(Group)
    email = models.CharField(max_length=256)
    zip = models.CharField(max_length=256, default='', blank=True)
    city = models.CharField(max_length=256, default='', blank=True)
    state = models.CharField(max_length=256, default='', blank=True)
    street = models.CharField(max_length=256, default='', blank=True)
    match = models.ForeignKey('self', null=True, blank=True)
    cantget = models.ManyToManyField('self', null=True, blank=True)
    hint  =  models.TextField(default='', blank=True)

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        needs_confirmation = False
        if not self.id:
            needs_confirmation = True
        super(Entrant, self).save(*args, **kwargs)
        if needs_confirmation:
            send_mail('Secret Santa', 'Just making sure you gave a valid email address. You\'ll get another email telling you about your victim after everyone signs up.'
                    , 'secretsanta@joelsemar.com', [self.email], fail_silently=True) 
