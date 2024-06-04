from flask import Flask, render_template
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import psycopg2
import os.path

app = Flask(__name__)

app.config['SECRET_KEY'] = 'fc089b9218301ad987914c53481bff04'


# set your own database
db = "dbname='mykino' user='postgres' host='127.0.0.1' password = 'spil3009'"
conn = psycopg2.connect(db)

bcrypt = Bcrypt(app)
# Function to create tables from schema.sql

@app.route('/')
def index():
    cur = conn.cursor()
    cur.execute('SELECT id, title, poster FROM movies')
    movies = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('index.html', movies=movies)


@app.route('/movie/<int:movie_id>')
def movie(movie_id):
    cur = conn.cursor()
    cur.execute('SELECT title, genre, year, runtime, rating, poster, plot FROM movies WHERE id = %s', (movie_id,))
    movie = cur.fetchone()
    cur.execute('SELECT actors.id, actors.name FROM actors JOIN movie_actors ON actors.id = movie_actors.actor_id WHERE movie_actors.movie_id = %s', (movie_id,))
    actors = cur.fetchall()
    cur.execute('SELECT directors.id, directors.name FROM directors JOIN movies ON directors.id = movies.director_id WHERE movies.id = %s', (movie_id,))
    director = cur.fetchone()
    cur.close()
    conn.close()
    return render_template('movie.html', movie=movie, actors=actors, director=director)

@app.route('/actor/<int:actor_id>')
def actor(actor_id):
    cur = conn.cursor()
    cur.execute('SELECT name FROM actors WHERE id = %s', (actor_id,))
    actor = cur.fetchone()
    cur.execute('SELECT movies.id, movies.title, movies.poster FROM movies JOIN movie_actors ON movies.id = movie_actors.movie_id WHERE movie_actors.actor_id = %s', (actor_id,))
    movies = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('actor.html', actor=actor, movies=movies)

@app.route('/director/<int:director_id>')
def director(director_id):
    cur = conn.cursor()
    cur.execute('SELECT name FROM directors WHERE id = %s', (director_id,))
    director = cur.fetchone()
    cur.execute('SELECT id, title, poster FROM movies WHERE director_id = %s', (director_id,))
    movies = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('director.html', director=director, movies=movies)

if __name__ == "__main__":
    app.run(debug=True)
