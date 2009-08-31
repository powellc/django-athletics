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

class Sport(StandardMetadata):
    """Sport model.
       A farily simple model to handle categorizing of schools and leagues into sports."""
    name=models.CharField(_('name'), max_length=100)
    slug=models.SlugField(_('slug'), unique=True) 


     
class Organization(StandardMetadata)
    """Organization model.
       A meta model for Schools or Leagues that contains basic info every organization needs:

       name, slug, website, description, admins."""

    name=models.CharField(_('name'), max_length=100)
    slug=models.SlugField(_('slug'), unique=True)
    administrators=models.ManyToManyField(User, null=True, blank=True, related_name='')
    description=models.TextField()
    public=models.BooleanField(_('public'), default=False)
    teams=models.ManyToManyField(Team, null=True, blank=True)
    objects=models.Manager()
    public_objects=PublicManager()
    
    class Meta:
        abstract=True
        
class School(Organization)
    """School model.

       Inherits from Organization, it represents a school, complete with mascots and everything."""

    mascot=models.CharField(_('mascot'), help_text="Please use the plural form of the mascot." )
    phone=PhoneNumberField(_('phone'), blank=True, null=True)
    website=models.URLField(_('website'), blank=True, null=True)
    address=models.CharField(_('address'), max_length=255)
    town=models.CharField(_('town'), max_length=100)
    state=USStateField(_('state'))
    zipcode=ZipCodeField(_('zip'), max_length=5)
    lat_long=models.CharField(_('coordinates'), max_length=255, blank=True)

    objects=models.Manager()
    public_objects=PublicManager()
    
    class Meta:
        verbose_name = _('school')
        verbose_name_plural = _('schools')
        get_latest_by='created'

    def save(self):
        if not self.lat_long:
            location = "%s +%s +%s +%s" % (self.address, self.town, self.state, self.zipcode)
            self.lat_long = get_lat_long(location)
            if not self.lat_long:
                location = "%s +%s +%s" % (self.town, self.state, self.zipcode)
                self.lat_long = get_lat_long(location)
        
        super(School, self).save()    

    def __unicode__(self):
        return self.name
        
    def get_absolute_url(self):
        args=[self.slug]
        return reverse('school_detail', args=args)

class League(Organization)
    """League model.

       Inherits from Organization, it represents a league, such as a private soccer league, or a little league."""

    phone=PhoneNumberField(_('phone'), blank=True, null=True)
    website=models.URLField(_('website'), blank=True, null=True)
    address=models.CharField(_('address'), max_length=255)
    town=models.CharField(_('town'), max_length=100)
    state=USStateField(_('state'))
    zipcode=ZipCodeField(_('zip'), max_length=5)

    objects=models.Manager()
    public_objects=PublicManager()
    
    class Meta:
        verbose_name = _('league')
        verbose_name_plural = _('leagues')
        get_latest_by='created'

    def __unicode__(self):
        return self.name
        
    def get_absolute_url(self):
        args=[self.slug]
        return reverse('league_detail', args=args)

class Coach(StandardMetadata)
    firstname=models.CharField(_('first name'))
    lastname=models.CharField(_('last name'))
    nickname=models.CharField(_('nickname'), blank=True, null=True) 
    slug=models.SlugField(_('slug'), unique=True)
    user=ForeignKey(User, blank=True, null=True)
    bio=models.TextField(_('bio'), blank=True, null=True)

    objects=models.Manager()
    public_objects=PublicManager()

    class Meta:
        verbose_name = _('coach')
        verbose_name_plural = _('coaches')
        get_latest_by='created'

    def __unicode__(self):
        return u'%s %s' % self.firstname, self.lastname
        
    def get_absolute_url(self):
        args=[self.slug]
        return reverse('coach_detail', args=args)

class Player(StandardMetadata)
    firstname=models.CharField(_('first name'))
    lastname=models.CharField(_('last name'))
    slug=models.SlugField(_('slug'), unique=True)
    nickname=models.CharField(_('nickname'), blank=True, null=True) 
    dob=models.DateField(_('date of birth'))
    bio=models.TextField(_('bio'), blank=True, null=True)
    public=models.BooleanField(_('public'), default=False)
    user=ForeignKey(User, blank=True, null=True)

    objects=models.Manager()
    public_objects=PublicManager()

    class Meta:
        verbose_name = _('player')
        verbose_name_plural = _('players')
        get_latest_by='created'

    def __unicode__(self):
        return u'%s %s' % self.firstname, self.lastname
        
    def get_absolute_url(self):
        args=[self.slug]
        return reverse('player_detail', args=args)

class Team(StandardMetadata):
    sport=models.ForeignKey(Sport)
    year=models.PositiveIntegerField(_('year'), max_length=4)
    coach=models.ForeignKey(Coach)
    asst_coach=models.ForeignKey(Coach, blank=True, null=True)
    roster=models.ManyToManyField(Player, blank=True, null=Trues)

    objects=models.Manager()
    public_objects=PublicManager()
    
    class Meta:
        verbose_name = _('team')
        verbose_name_plural = _('teams')
        get_latest_by='created'

    def __unicode__(self):
        return self.name
        
    def get_absolute_url(self):
        args=[self.slug]
        return reverse('team_detail', args=args)

class Location(StandardMetadata):

class Game(Event):
    home_team=models.ForeignKey(Team, blank=True, null=True)
    away_team=models.ForeignKey(Team, blank=True, null=True)
    home_team_one_off=models.CharField(_('one-off home team', blank=True, null=True, max_length=100)
    away_team_one_off=models.CharField(_('one-off away team', blank=True, null=True, max_length=100)
    location=

    class Meta:
        verbose_name = _('team')
        verbose_name_plural = _('teams')
        get_latest_by='created'

    def __unicode__(self):
        return self.name
        
    def get_absolute_url(self):
        args=[self.slug]
        return reverse('team_detail', args=args)
