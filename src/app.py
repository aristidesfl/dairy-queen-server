import sys
import pandas as pd
import datetime
import time
import itertools
import json
import urllib
import re
import flask

sys.path.append('./dairy_queen')
import double_dip

app = flask.Flask(__name__)


@app.route('/', methods=['GET','POST'])
def guacamole():

    days_from_now = 0  # deprecated since Kimono stopped allowing ondemand APIs
    ads_mins = flask.request.form.get('ads_mins', default=15, type=int)
    trailers_mins = flask.request.form.get('trailers_mins', default=15, type=int)
    max_waiting_mins = flask.request.form.get('max_waiting_mins', default=45, type=int)
    acceptable_overlap_mins = flask.request.form.get('acceptable_overlap_mins', default=10, type=int)  # 0
    movies_to_exclude = flask.request.form.get('movies_to_exclude', default='Spectre, Star Wars')  # ['Spectre', 'Star Wars']  #set to None to disable
    movies_to_exclude = [movie.strip() for movie in movies_to_exclude.split(',')]
    interesting_movies = flask.request.form.get('interesting_movies', default=None)    # set to None to disable
    if interesting_movies:
        interesting_movies = [movie.strip() for movie in interesting_movies.split(',')]
    all_interesting_movies_must_be_in_dip = flask.request.form.get('all_interesting_movies_must_be_in_dip', default=False, type=bool)  # False  # consider any dip that has at least one of the interesting movies

    print days_from_now
    print ads_mins
    print trailers_mins
    print max_waiting_mins
    print acceptable_overlap_mins
    print movies_to_exclude
    print interesting_movies
    print all_interesting_movies_must_be_in_dip


    # hit kimono-made Cinestar showtimes API
    api_endpoint = 'http://www.kimonolabs.com/api/9q0fwoh2?apikey=2GuGNJHoWhVjhlu4yTXWyyTi8a1o8ybM&kimmodify=1'
    api_endpoint = api_endpoint + '&date=' + str(days_from_now) # the data parameter is currently inoperative
    results = json.load(urllib.urlopen(api_endpoint))

    if not results['results']:
        print " _Error:_ Either there are no showings for your day, or you've hit the API too many times. Try changing `days_from_now` and re-running?"
        print results

    kino_program = double_dip.make_showtimes(results,
                                             ads_mins=ads_mins,
                                             trailers_mins=trailers_mins)

    double_dips = \
    double_dip.find_all_double_dips(kino_program,
                                    max_waiting_mins=max_waiting_mins,
                                    acceptable_overlap_mins=acceptable_overlap_mins,
                                    movies_to_exclude=movies_to_exclude,
                                    interesting_movies=interesting_movies,
                                    all_interesting_movies_must_be_in_dip=all_interesting_movies_must_be_in_dip)

    double_dips = [dip.split(' -> ') for dip in double_dips]

    return flask.json.jsonify(double_dips=double_dips)

if __name__ == '__main__':
    app.run(debug=True)
