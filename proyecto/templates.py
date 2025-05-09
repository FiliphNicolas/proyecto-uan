import os
from flask import Flask

def init_app(app):
    template_dir = os.path.abspath('templates')
    app.template_folder = template_dir
