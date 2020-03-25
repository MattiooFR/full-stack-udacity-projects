#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for, abort, jsonify, session
from werkzeug.datastructures import MultiDict
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import logging
from logging import Formatter, FileHandler
from forms import *

import sys

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)

moment = Moment(app)
app.config.from_object('config')

db = SQLAlchemy(app)
migrate = Migrate(app, db)

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#


class Venue(db.Model):  # Venue database model
    __tablename__ = 'venues'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120), nullable=False)
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String(120))

    shows = db.relationship(
        'Show',
        backref='venue',
        lazy=True)

    def __repr__(self):
        return f'<Todo {self.id} {self.name} {self.city}>'


class Artist(db.Model):  # Artist database model
    __tablename__ = 'artists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120), nullable=False)
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String(120))

    shows = db.relationship(
        'Show',
        backref='artist',
        lazy=True)

    def __repr__(self):
        return f'<Todo {self.id} {self.name} {self.city}>'


class Show(db.Model):  # Show database model
    __tablename__ = 'shows'

    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime, nullable=False)
    artist_id = db.Column(
        db.Integer,
        db.ForeignKey(
            'artists.id'),
        nullable=False)
    venue_id = db.Column(
        db.Integer,
        db.ForeignKey(
            'venues.id'),
        nullable=False)

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#


def format_datetime(value, format='medium'):
    date = dateutil.parser.parse(value)
    if format == 'full':
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format)


app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#


@app.route('/')
def index():
    return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
    venues = Venue.query.order_by(Venue.state, Venue.city).all()

    # build the num_upcoming_shows attribute
    data = []
    for venue in venues:
        venue_data = {
            'id': venue.id,
            'name': venue.name,
            'num_upcoming_shows': len(
                list(
                    filter(
                        lambda x: x.start_time > datetime.today(),
                        venue.shows)))}

        temp = {}
        temp['city'] = venue.city
        temp['state'] = venue.state
        temp['venues'] = [venue_data]

        print(temp)

        # algorithm to merge venues that are from the same city and state
        for d in data:
            print(d)
            if d['city'] == temp['city'] and d['state'] == temp['state']:
                d['venues'].append(venue_data)
                break
        else:
            data.append(temp)

    return render_template('pages/venues.html', areas=data)


@app.route('/venues/search', methods=['POST'])
def search_venues():
    # use ilike method to search incomplete venues
    search_term = request.form.get('search_term')
    venues = Venue.query.filter(
        Venue.name.ilike(
            '%{}%'.format(search_term))).all()

    data = []
    for venue in venues:
        temp = {}
        temp['id'] = venue.id
        temp['name'] = venue.name
        temp['num_upcoming_shows'] = len(venue.shows)
        data.append(temp)

    response = {}
    response['count'] = len(data)
    response['data'] = data

    return render_template(
        'pages/search_venues.html',
        results=response,
        search_term=request.form.get(
            'search_term',
            ''))


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    venue = Venue.query.filter_by(id=venue_id).first_or_404()

    # Filter the shows between past and upcoming
    past_shows = Show.query.join(Artist, Show.artist_id == Artist.id)\
        .filter(Show.venue_id == venue_id)\
        .filter(Show.start_time < datetime.now())\
        .add_columns(Artist.id, Artist.name, Artist.image_link, Show.start_time)\
        .all()
    upcoming_shows = Show.query.join(Artist, Show.artist_id == Artist.id)\
        .filter(Show.venue_id == venue_id)\
        .filter(Show.start_time >= datetime.now())\
        .add_columns(Artist.id, Artist.name, Artist.image_link, Show.start_time)\
        .all()

    # return a populated show dict from a show object with start_time in
    # proper format

    def get_show(show):
        return {
            'artist_id': show[1],
            'artist_name': show[2],
            'artist_image_link': show[3],
            'start_time': show[4].strftime('%Y-%m-%d %H:%M:%S')
        }

    past_shows = list(map(get_show, past_shows))
    upcoming_shows = list(map(get_show, upcoming_shows))

    # populate the venue data dict that we need to send to the view
    data = {
        'id': venue.id,
        'name': venue.name,
        'city': venue.city,
        'state': venue.state,
        'address': venue.address,
        'phone': venue.phone,
        'genres': venue.genres.split(','),
        'image_link': venue.image_link,
        'facebook_link': venue.facebook_link,
        'website': venue.website,
        'seeking_talent': venue.seeking_talent,
        'seeking_description': venue.seeking_description,
        'past_shows': past_shows,
        'upcoming_shows': upcoming_shows,
        'past_shows_count': len(past_shows),
        'upcoming_shows_count': len(upcoming_shows)
    }

    return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------


@app.route('/venues/create', methods=['POST', 'GET'])
def create_venue_form():
    form = VenueForm()

    # I merged the two route so if a validate error happen all the values are not erased
    if request.method == 'GET':
        formdata = session.get('formdata', None)
        print(formdata)
        if formdata:
            form = VenueForm(MultiDict(formdata))
            form.validate()
            session.pop('formdata')
        return render_template('forms/new_venue.html', form=form)

    # flash error depending on WTForm validator's error
    if not form.validate():
        session['formdata'] = request.form
        for item, error in form.errors.items():
            flash(item.title() + ': ' + error[0])
        return redirect(url_for('create_venue_form'))

    error = False

    # get the value from the form, build the query to create a Venue and commit
    try:
        form_values = request.form

        venue = Venue()
        venue.name = form_values.get('name')
        venue.city = form_values.get('city')
        venue.state = form_values.get('state')
        venue.address = form_values.get('address')
        venue.phone = form_values.get('phone')
        venue.genres = ','.join(form_values.getlist('genres'))
        venue.facebook_link = form_values.get('facebook_link')
        db.session.add(venue)
        db.session.commit()

    # if error we rollback the commit
    except BaseException:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()

        # we flash an error if the creation of a Venue didn't work
        if error:
            flash(
                'An error occurred. Venue ' +
                form_values.get('name') +
                ' could not be listed.')
        else:
            flash(
                'Venue ' +
                form_values.get('name') +
                ' was successfully listed!')

    return render_template('pages/home.html')


@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    # TODO: Complete this endpoint for taking a venue_id, and using
    # SQLAlchemy ORM to delete a record. Handle cases where the session commit
    # could fail.

    # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
    # clicking that button delete it from the db then redirect the user to the
    # homepage
    return None

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
    return render_template('pages/artists.html', artists=Artist.query.all())


@app.route('/artists/search', methods=['POST'])
def search_artists():
    # we use ilike to get database rows of the incomplete artist name
    search = request.form.get('search_term')
    data = Artist.query.filter(Artist.name.ilike("%{}%".format(search))).all()
    response = {}
    response['count'] = len(data)
    response['data'] = data

    return render_template(
        'pages/search_artists.html',
        results=response,
        search_term=request.form.get(
            'search_term',
            ''))


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    artist = Artist.query.get(artist_id)

    # filter the shows between past and upcoming shows
    past_shows = Show.query.join(Venue, Show.venue_id == Venue.id)\
        .filter(Show.artist_id == artist_id)\
        .filter(Show.start_time < datetime.now())\
        .add_columns(Venue.id, Venue.name, Venue.image_link, Show.start_time)\
        .all()

    upcoming_shows = Show.query.join(Venue, Show.venue_id == Venue.id)\
        .filter(Show.artist_id == artist_id)\
        .filter(Show.start_time >= datetime.now())\
        .add_columns(Venue.id, Venue.name, Venue.image_link, Show.start_time)\
        .all()

    def get_show(show):
        return {
            'venue_id': show[1],
            'venue_name': show[2],
            'venue_image_link': show[3],
            'start_time': show[4].strftime('%Y-%m-%d %H:%M:%S')
        }

    past_shows = list(map(get_show, past_shows))
    upcoming_shows = list(map(get_show, upcoming_shows))

    data = {
        'id': artist.id,
        'name': artist.name,
        'city': artist.city,
        'state': artist.state,
        'phone': artist.phone,
        'genres': artist.genres.split(','),
        'image_link': artist.image_link,
        'facebook_link': artist.facebook_link,
        'website': artist.website,
        'seeking_venue': artist.seeking_venue,
        'seeking_description': artist.seeking_description,
        'past_shows': past_shows,
        'upcoming_shows': upcoming_shows,
        'past_shows_count': len(past_shows),
        'upcoming_shows_count': len(upcoming_shows)
    }

    return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
# update the artist
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    artist = Artist.query.get(artist_id)
    form = ArtistForm(obj=artist)

    # How can I populate the SelectMultipleField for genres ?

    return render_template('forms/edit_artist.html', form=form, artist=artist)


@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    error = False
    try:
        artist = Artist.query.get(artist_id)
        form_values = request.form

        artist.name = form_values.get('name')
        artist.city = form_values.get('city')
        artist.state = form_values.get('state')
        artist.phone = form_values.get('phone')
        artist.genres = form_values.get('genres')
        artist.facebook_link = form_values.get('facebook_link')

        db.session.commit()
    except BaseException:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
        if error:
            return redirect(url_for('server_error'))
        else:
            return redirect(url_for('show_artist', artist_id=artist_id))


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    venue = Venue.query.get(venue_id)
    form = VenueForm(obj=venue)

    # How can I populate the SelectMultipleField for genres ?

    return render_template('forms/edit_venue.html', form=form, venue=venue)


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    venue = Venue.query.get(venue_id)

    error = False
    try:
        form_values = request.form

        venue.name = form_values.get('name')
        venue.city = form_values.get('city')
        venue.state = form_values.get('state')
        venue.address = form_values.get('address')
        venue.phone = form_values.get('phone')
        venue.genres = ','.join(form_values.getlist('genres'))
        venue.facebook_link = form_values.get('facebook_link')
        db.session.add(venue)
        db.session.commit()
    except BaseException:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
        if error:
            flash(
                'An error occurred. Venue ' +
                request.form['name'] +
                ' could not be updated.')
        else:
            flash(
                'Venue ' +
                request.form['name'] +
                ' was successfully updated!')
    return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------


@app.route('/artists/create', methods=['POST', 'GET'])
def create_artist_form():
    form = ArtistForm()

    # I merged the two route so if a validate error happen all the values are not erased
    if request.method == 'GET':
        formdata = session.get('formdata', None)
        print(formdata)
        if formdata:
            form = ArtistForm(MultiDict(formdata))
            form.validate()
            session.pop('formdata')
        return render_template('forms/new_artist.html', form=form)

    # Flash error from WTForm validators
    if not form.validate():
        session['formdata'] = request.form
        for item, error in form.errors.items():
            flash(item.title() + ': ' + error[0])
        return redirect(url_for('create_artist_form'))

    error = False
    # create a Artist database object to create a new artist value
    try:
        form_values = request.form

        artist = Artist()
        artist.name = form_values.get('name')
        artist.city = form_values.get('city')
        artist.state = form_values.get('state')
        artist.phone = form_values.get('phone')
        artist.genres = ','.join(form_values.getlist('genres'))
        artist.facebook_link = form_values.get('facebook_link')
        db.session.add(artist)
        db.session.commit()
    # if an eror happen we rollback the database to prevent any issue
    except BaseException:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    # if an error happened while creating an Artist we flash it
    finally:
        db.session.close()
        if error:
            flash(
                'An error occurred. Artist ' +
                form_values.get('name') +
                ' could not be listed.')
        else:
            flash(
                'Artist ' +
                form_values.get('name') +
                ' was successfully listed!')

    return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
    shows = Show.query.join(Venue, Show.venue_id == Venue.id)\
        .join(Artist, Show.artist_id == Artist.id)\
        .order_by(Show.start_time)\
        .add_columns(Venue.id, Venue.name, Artist.id, Artist.name, Artist.image_link, Show.start_time)\
        .all()

    data = []
    # we display only the shows that are upcoming

    for show in shows:
        if show.start_time >= datetime.today():
            data.append({
                'venue_id': show[1],
                'venue_name': show[2],
                'artist_id': show[3],
                'artist_name': show[4],
                'artist_image_link': show[5],
                'start_time': show[6].isoformat()
            })

    return render_template('pages/shows.html', shows=data)


@app.route('/shows/create')
def create_shows():
    # renders form. do not touch.
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)


@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    error = False
    try:
        show = Show()
        show.artist_id = request.form['artist_id']
        show.venue_id = request.form['venue_id']
        show.start_time = request.form['start_time']
        db.session.add(show)
        db.session.commit()
    except BaseException:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    if error:
        flash('An error occurred. Requested show could not be listed.')
    else:
        flash('Requested show was successfully listed')
    return render_template('pages/home.html')


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
