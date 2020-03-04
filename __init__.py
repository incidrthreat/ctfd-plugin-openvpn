#from flask import render_template, Blueprint
#from CTFd.models import db, Users
#from sqlalchemy.sql import or_
#from jinja2 import Template
#import sys

# The load method is the entry point of our plugin, as described in the docs

def load(app):
    print("OpenVPN-Cfg plugin is ready!")