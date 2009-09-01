from django.conf import settings
from django.conf.urls.defaults import *
from athletics import views
from athletics.models import *
from tagging.views import tagged_object_list


# custom views vendors
urlpatterns = patterns('athletics.views',
    url(r'^$', view=views.team_index, name="team_index"),
    
)