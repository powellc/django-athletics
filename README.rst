================================
Athletics - a Django application
================================
:Info: See github page at <http://github.com/powellc/django-athletics>
:Author: Colin Powell <colin.powell@me.com>
:License: None, at the moment

Overview
========

A django application for managing sports teams, mostly at schools, though
hooks exist to add other types of groups like clubs in the future. It allows 
for user submitted content, game scheduling amongst other things.

Athletics is meant to be used with a collection of other django apps 
which you can add to your project to manage various sports teams
while abstracting as much of the heavy lifting for all sports as possible.

The way it is setup, adding a lacrosse team should be a fairly straight 
forward matter of creating a lacrosse application.

Dependencies
------------
- `django-schedule <http://github.com/thauber/django-schedule>`_, for schedule games and practices 

Models
------
- `Organization`, a meta class with basics for organizations to tie with games and teams
- `School`, a type of organization with a mascot, multiple sports teams, location, etc
- `Team`, a meta class that has a roster, a coach, and an organization
- `Practice`, bet you can't guess what this is.
- `Game`, another meta class this one to collect general game info, home team, away team, etc
- `Match`, a meta class for sports with matches, such as tennis
- `Tournament`, a meta class for defining basic tournament information


