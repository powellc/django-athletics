from django.shortcuts import get_list_or_404, render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import Http404
from django.contrib.auth.decorators import login_required
from athletics.models import Team
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify
from tagging.models import Tag, TaggedItem
from django.conf import settings


import datetime

def team_index(request):
    teams=Team.public_objects.all()
    return render_to_response('athletics/team_index.html', locals(),
                              context_instance=RequestContext(request))


