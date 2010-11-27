#!/usr/bin/env python

import cgi
import datetime

import wsgiref.handlers
from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import webapp
from django.utils import simplejson as json

class BmEntry(db.Model):
  seq = db.IntegerProperty()
  link = db.StringProperty(multiline=False)
  count = db.IntegerProperty()
  title = db.StringProperty(multiline=False)


class MainPage(webapp.RequestHandler):
  def get(self):
    self.response.headers["Content-Type"] = 'text/javascript; charset=utf-8'
    max_results = self.request.get('max-results', default_value='10')
    try:
      max_results = int(max_results)
    except Exception:
      self.response.out.write('Invalid parameter')
      return
    jobj = []
    entries = db.GqlQuery("SELECT * "
                            "FROM BmEntry "
                            "ORDER BY count DESC "
                            "LIMIT %d" % max_results)

    for entry in entries:
      jobj.append(
        dict([
          ['link', entry.link],
          ['count', entry.count],
          ['title', entry.title],
        ])
      )

    callback = self.request.get('callback', default_value='')

    self.response.out.write(
      callback
        + '('
        + json.dumps(jobj, ensure_ascii=False)
        + ');'
      )

application = webapp.WSGIApplication([
  ('/', MainPage),
  ('/show', MainPage),
  ], debug=True)


def main():
  wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
  main()
