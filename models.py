# ----------------------------------------------------------------------------#
# Imports
# ----------------------------------------------------------------------------#

import json
import sys
import dateutil.parser
import babel
from flask import Flask
from flask_migrate import Migrate
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler

from sqlalchemy import func

from forms import *

# ----------------------------------------------------------------------------#
# App Config.
# ----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
# app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# ----------------------------------------------------------------------------#
# Models.
# ----------------------------------------------------------------------------#


class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String), nullable=False)
    seeking_talent = db.Column(db.Boolean)
    seeking_description = db.Column(db.String(500))
    shows = db.relationship('Show', backref='Venue', lazy='dynamic',cascade="all, delete-orphan")

    @property
    def upcoming_shows(self):

        shows_list = self.shows
        upcoming_shows = [show for show in shows_list if show.start_time >= datetime.now()]
        upcoming_shows_list = []
        for show in upcoming_shows:
            show_dict = {
                'artist_id': show.artist_id,
                'artist_name': show.artist.name,
                'artist_image_link': show.artist.image_link,
                'start_time': str(show.start_time),
            }
            upcoming_shows_list.append(show_dict)
        return upcoming_shows_list

    @property
    def num_upcoming_shows(self):

        upcoming_shows = self.upcoming_shows
        return len(upcoming_shows)

    @property
    def past_shows(self):


        past_shows = [show for show in self.shows if show.start_time < datetime.now()]
        past_shows_list = []
        for show in past_shows:
            show_dict = {
                'artist_id': show.artist_id,
                'artist_name': show.artist.name,
                'artist_image_link': show.artist.image_link,
                'start_time': str(show.start_time),
            }
            past_shows_list.append(show_dict)
        return past_shows_list

    @property
    def num_past_shows(self):
        """
        Returns number of past shows
        """
        return len(self.past_shows)

    def __repr__(self):
        return f'<Venue: id: {self.id} name: {self.name}>'


class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String), nullable=False)
    website = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean)
    seeking_description = db.Column(db.String(500))
    shows = db.relationship('Show', backref='Artist', lazy='dynamic',cascade="all, delete-orphan")

    @property
    def upcoming_shows(self):


        upcoming_shows = [show for show in self.shows if show.start_time > datetime.now()]
        upcoming_show_list = []
        for show in upcoming_shows:
            show_dict = {
                'venue_id': show.venue_id,
                'venue_name': show.venue.name,
                'venue_image_link': show.venue.image_link,
                'start_time': str(show.start_time),
            }
            upcoming_show_list.append(show_dict)
        return upcoming_show_list

    @property
    def past_shows(self):


        past_shows = [show for show in self.shows if show.start_time < datetime.now()]
        past_shows_list = []
        for show in past_shows:
            show_dict = {
                'venue_id': show.venue_id,
                'venue_name': show.venue.name,
                'venue_image_link': show.venue.image_link,
                'start_time': str(show.start_time),
            }
            past_shows_list.append(show_dict)
        return past_shows_list

    @property
    def past_shows_count(self):

        return len(self.past_shows)

    @property
    def num_upcoming_shows(self):

        return len(self.upcoming_shows)


class Show(db.Model):
    __tablename__ = 'Show'
    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)

    venue = db.relationship('Venue')
    artist = db.relationship('Artist')

