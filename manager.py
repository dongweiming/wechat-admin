import click
from flask_migrate import Migrate

from views.api import json_api as app
from ext import db

migrate = Migrate(app, db)

from models import *  # noqa


@app.cli.command()
def initdb():
    db.session.commit()
    db.drop_all()
    db.create_all()
    click.echo('Init Finished!')
