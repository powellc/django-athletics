================================
Athletics - a Django application
================================
:Info: See github page at <http://github.com/powellc/django-athletics>
:Author: Colin Powell <colin.powell@me.com>


Overview
========

A django application for managing a variety of sports teams, leagues, 
schools and organizations. It allows for user submitted content, 
game scheduling amongst other things.

The schedule portion of the application is actually handled with the 
django-schedule application, while each game can be associated with an 
event, and a league or school (top levels app models) can contain 
numerous calendars for each team it reprsents.

There are also some blog-like features built in to allow an arbitrary 
user of the system to keep updates on their team. Blogs are given 
priority based on the level of the user, whether a player, parent, coach 
or team administrator.    
