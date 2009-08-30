from datetime import datetime
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from tagging.fields import TagField
from django.contrib.localflavor.us.models import PhoneNumberField, USStateField 

from schedule.models import Event
import tagging
import urllib
import settings

def get_lat_long(location):
    key = settings.GOOGLE_API_KEY_CFM
    output = "csv"
    location = urllib.quote_plus(location)
    request = "http://maps.google.com/maps/geo?q=%s&output=%s&key=%s" % (location, output, key)
    data = urllib.urlopen(request).read()
    dlist = data.split(',')
    if dlist[0] == '200':
        return "%s, %s" % (dlist[2], dlist[3])
    else:
        return ''


class StandardMetadata(models.Model):
    """
    A basic (abstract) model for metadata.
    
	Subclass new models from 'StandardMetadata' instead of 'models.Model'.
    """
    created = models.DateTimeField(default=datetime.now, editable=False)
    updated = models.DateTimeField(default=datetime.now, editable=False)
    
    class Meta:
        abstract = True
    
    def save(self, *args, **kwargs):
        self.updated = datetime.now()
        super(StandardMetadata, self).save(*args, **kwargs)

class PublicManager(models.Manager):
    def get_query_set(self):
        return super(PublicManager, self).get_query_set().filter(public=True)

class ZipCodeField(models.CharField):
    def __unicode__(self):
        return self.rjust(5, '0')

class Vendor(StandardMetadata):
    """Vendor model."""
    name=models.CharField(_('title'), max_length=100)
    slug=models.SlugField(_('slug'), unique=True)
    owner=models.ForeignKey(User, related_name='vendor_owner')
    email=models.EmailField(_('email'), unique=True)
    phone=PhoneNumberField(_('phone'), blank=True, null=True)
    website=models.URLField(_('website'), blank=True, null=True)
    address=models.CharField(_('address'), max_length=255)
    town=models.CharField(_('town'), max_length=100)
    state=USStateField(_('state'))
    zipcode=ZipCodeField(_('zip'), max_length=5)
    description=models.TextField()
    products=TagField()
    markets=models.ManyToManyField(Event, null=True, blank=True)
    public=models.BooleanField(_('public'), default=False)
    #organic=models.BooleanField(_('certified organic'), default=False)
    lat_long=models.CharField(_('coordinates'), max_length=255)
    
    objects=models.Manager()
    public_objects=PublicManager()
    
    class Meta:
        verbose_name = _('vendor')
        verbose_name_plural = _('vendors')
        ordering = ('name',)
        get_latest_by='created'
        
    def save(self):
        if not self.lat_long:
            location = "%s +%s +%s +%s" % (self.address, self.town, self.state, self.zipcode)
            self.lat_long = get_lat_long(location)
            if not self.lat_long:
                location = "%s +%s +%s" % (self.town, self.state, self.zipcode)
                self.lat_long = get_lat_long(location)
        
        super(Vendor, self).save()
        
    def __unicode__(self):
        return u'%s in %s' % (self.name, self.town)
        
    def get_absolute_url(self):
        args=[self.slug]
        return reverse('vendor_detail', args=args)
        
    def get_previous_vendor(self):
        return self.get_previous_by_name(public=True)

    def get_next_vendor(self):
        return self.get_next_by_name(public=True)
