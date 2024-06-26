from flask import Flask, render_template, redirect, url_for, session, request
from forms import SearchForm
import psycopg2
import psycopg2.extras
import re  


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

def get_db_connection():
    conn = psycopg2.connect(
    dbname='mykino', 
    user='xxxxxx', 
    password='xxxxxxx', 
    host='localhost')
    return conn

@app.route('/')
def home():
    conn = get_db_connection()
    # using DictCursor to access elements using dicts instead of tuples

    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    cur.execute("SELECT DISTINCT genre FROM movies;")
    genres = [row['genre'] for row in cur.fetchall()]

    unique_genres = set()
    # REGEX HERE!
    for genre in genres:
        unique_genres.update(re.findall(r'\b\w+(?:-\w+)?\b', genre))


    filter_genre = request.args.get('genre')

    sql_query = "SELECT * FROM movies"
    if filter_genre:
        sql_query += f" WHERE genre LIKE '%{filter_genre}%'"

    cur.execute(sql_query)
    movies = cur.fetchall()

    cur.close()
    conn.close()

    form = SearchForm()  

    return render_template('home.html', movies=movies, genres=unique_genres, form=form)


@app.route('/movie/<int:movie_id>')
def movie_detail(movie_id):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute('SELECT * FROM movies WHERE id = %s;', (movie_id,))
    movie = cur.fetchone()

    cur.execute('''
        SELECT a.id, a.name FROM actors a
        JOIN movie_actors ma ON a.id = ma.actor_id
        WHERE ma.movie_id = %s;
    ''', (movie_id,))
    actors = cur.fetchall()

    cur.execute('SELECT * FROM directors WHERE id = %s;', (movie['director_id'],))
    director = cur.fetchone()

    cur.close()
    conn.close()
    form = SearchForm()
    return render_template('movie_detail.html', movie=movie, actors=actors, director=director, form=form)

@app.route('/search', methods=['GET', 'POST'])
def search():
    form = SearchForm()
    results = {}
    query = ""
    if form.validate_on_submit():
        query = form.search.data
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute('SELECT * FROM movies WHERE title ILIKE %s;', (f'%{query}%',))
        results['movies'] = cur.fetchall()

        cur.execute('SELECT * FROM directors WHERE name ILIKE %s;', (f'%{query}%',))
        results['directors'] = cur.fetchall()

        cur.execute('SELECT * FROM actors WHERE name ILIKE %s;', (f'%{query}%',))
        results['actors'] = cur.fetchall()

        cur.close()
        conn.close()
    return render_template('search_results.html', results=results, query=query, form=form)

@app.route('/director/<int:director_id>')
def director_movies(director_id):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute('SELECT * FROM directors WHERE id = %s;', (director_id,))
    director = cur.fetchone()

    cur.execute('SELECT * FROM movies WHERE director_id = %s;', (director_id,))
    movies = cur.fetchall()

    cur.close()
    conn.close()
    form = SearchForm()
    return render_template('director_movies.html', director=director, movies=movies, form=form)

@app.route('/actor/<int:actor_id>')
def actor_movies(actor_id):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute('SELECT * FROM actors WHERE id = %s;', (actor_id,))
    actor = cur.fetchone()

    cur.execute('''
        SELECT m.* FROM movies m
        JOIN movie_actors ma ON m.id = ma.movie_id
        WHERE ma.actor_id = %s;
    ''', (actor_id,))
    movies = cur.fetchall()

    cur.close()
    conn.close()
    form = SearchForm()
    return render_template('actor_movies.html', actor=actor, movies=movies, form=form)

@app.route('/about')
def about():
    form = SearchForm()
    return render_template('about.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)
