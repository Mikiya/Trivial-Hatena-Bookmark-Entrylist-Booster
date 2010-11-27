#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2010  Mikiya Okuno
#
# This file is part of Trivial Hatena Bookmark Entrylist Booster.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Foobar.  If not, see <http://www.gnu.org/licenses/>.

import re
import urllib2
from HTMLParser import HTMLParser
import cgi
import datetime

import wsgiref.handlers
from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import webapp

blog_url = 'http://nippondanji.blogspot.com/'
entry_url = 'http://b.hatena.ne.jp/entrylist?url='\
    + urllib2.quote(blog_url) + '&sort=count'


class BmEntry(db.Model):
    seq = db.IntegerProperty()
    link = db.StringProperty(multiline=False)
    count = db.IntegerProperty()
    title = db.StringProperty(multiline=False)


class ParsedEntry:

    def __init__(self):
        self.link = None
        self.count = None
        self.title = None

    def is_valid(self):
        return self.link and self.count and self.title

class HatenaEntryExtractor(HTMLParser):

    def __init__(self):
        HTMLParser.__init__(self)
        self.entries = []
        self.current_entry = ParsedEntry()
        self.parsing_link = False
        self.parsing_users = False
        self.text = ""

    def handle_starttag(self, tag, attrs):
        if tag == "li":
            attrs = dict(attrs)
            if "class" in attrs and attrs["class"] == "users":
                self.parsing_users = True
                return

        if tag == "a":
            attrs = dict(attrs)
            if "class" in attrs and attrs["class"] == "entry-link" and "title" in attrs:
                self.current_entry = ParsedEntry()
                self.current_entry.title = attrs["title"]
                self.current_entry.link = attrs["href"]
                self.parsing_link = True
            self.text = ""

    def handle_endtag(self, tag):
        if tag == 'li' and self.parsing_users:
            self.parsing_users = False
            self.entries.append(self.current_entry)
            return

        if tag == "a":
            if self.parsing_users:
                users = self.text
                users_re = re.compile('(\d+)\suser')
                m = users_re.match(self.text)
                if m:
                    self.current_entry.count = int(m.groups()[0])
                else:
                    self.current_entry.count = 0

    def handle_data(self, data):
        if self.parsing_users:
            self.text += data


class MainPage(webapp.RequestHandler):

    def get(self):
        self.response.headers['Content-Type'] = 'text/plain; charset=utf-8'

        if(self.request.get('clear')):
          self.clear_data()
          self.response.out.write('Data cleared!\n')

        self.fetch_entry_page(entry_url)
        #fetch_entry_page(entry_url + '&of=20')
        self.response.out.write('OK!')

    def clear_data(self):
        q = db.GqlQuery("SELECT * FROM BmEntry")
        results = q.fetch(1000)
        db.delete(results)

    def fetch_entry_page(self, url):
        page = ''
        try:
            result = urllib2.urlopen(url)
            page = ''.join(result.readlines())
        except Exception:
            self.response.out.write('Failed to fetch data from hatena')
            return

        try:
            page = page.decode('utf-8')
            parser = HatenaEntryExtractor()
            parser.feed(page)
        except Exception:
            self.response.out.write('Failed to parse XML')
            return

        try:
            n = 1
            for item in parser.entries:
                entry = BmEntry(key_name=item.link)
                entry.seq = n
                entry.link = item.link
                entry.count = item.count
                entry.title = re.sub(r'^.+: ', '', item.title)
                entry.put()
                n += 1
        except Exception:
            self.response.out.write('DataStore error')


application = webapp.WSGIApplication([
    ('/fetch', MainPage),
    ],debug=True)


def main():
    wsgiref.handlers.CGIHandler().run(application)

if __name__ == "__main__":
    main()
