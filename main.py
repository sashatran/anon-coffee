import os
import webapp2
import jinja2
import random

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)

class BaseHandler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

class Anon(db.Model):
    username = db.StringProperty()
    entry = db.TextProperty()
    created = db.DateTimeProperty(auto_now_add = True)

class MainPage(BaseHandler):
    def get(self):
        entry = db.GqlQuery("SELECT * FROM Anon ORDER BY created DESC")
        self.render("index.html", entry= entry)

    def post(self):
        have_error = False
        username = self.request.get('username')
        entry = self.request.get('entry')

        if not username:
            username = 'anon' + str(random.randint(1, 5000))

        if not entry:
            error_entry = "You have to say something"
            have_error = True

        if have_error:
            entry = db.GqlQuery("SELECT * FROM Anon ORDER BY created DESC")
            self.render('index.html', entry=entry, error_entry=error_entry)

        else:
            a = Anon(username = username, entry = entry)
            a.put()
            key = a.key()
            record = Anon.get(key)
            self.redirect("/")

app = webapp2.WSGIApplication([('/', MainPage)], debug=True)
