"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file creates your application.
"""

from app import app, db
from flask import render_template, request, jsonify, send_from_directory
import os
from flask_wtf.csrf import generate_csrf
from app.forms import MovieForm
from app.models import Movie



###
# Routing for your application.
###

@app.route('/')
def index():
    return jsonify(message="This is the beginning of our API")


###
# The functions below should be applicable to all Flask apps.
###
def form_errors(form):
    error_messages = []
    """Collects form errors"""
    for field, errors in form.errors.items():
        for error in errors:
            message = u"Error in the %s field - %s" % (
                    getattr(form, field).label.text,
                    error
                )
            error_messages.append(message)

    return error_messages



@app.route('/api/v1/movies', methods=['POST'])
def add_movie():
    form = MovieForm()

    if form.validate_on_submit():
        # Save the movie to the database
        movie = Movie(title=form.title.data, poster=form.poster.data.filename, description=form.description.data)
        db.session.add(movie)
        db.session.commit()

        # Save the movie poster file to the uploads folder
        if not os.path.exists('app/static/uploads'):
            os.makedirs('app/static/uploads')
        form.poster.data.save(f'app/static/uploads/{form.poster.data.filename}')

        # Return a JSON response with the movie details
        return jsonify({
            'message': 'Movie successfully added',
            'title': movie.title,
            'poster': form.poster.data.filename,
            'description': movie.description
        }), 201
    else:
        # Return a JSON response with the form errors
        return jsonify({'errors': form_errors(form)}), 400

# Here we define a function to collect form errors from Flask-WTF
# which we can later use

@app.route('/api/v1/movies')
def get_movies():
    movies = Movie.query.all()
    movie_list = []
    for movie in movies:
        movie_dict = {
            'id': movie.id,
            'title': movie.title,
            'description': movie.description,
            'poster': f'/api/v1/posters/{movie.poster}'

        }
        movie_list.append(movie_dict)
    return jsonify({'movies': movie_list})

@app.route('/api/v1/posters/<filename>')
def get_poster(filename):
    return send_from_directory(os.path.join(app.root_path, 'static', 'uploads'), filename)




@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404

@app.route('/api/v1/csrf-token', methods=['GET'])
def get_csrf():
 return jsonify({'csrf_token': generate_csrf()})
