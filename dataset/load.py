import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
import re

# Connect to the PostgreSQL database -- fill in your username and password
conn = psycopg2.connect(
    dbname='mykino', 
    user='XXXXX', 
    password='XXXXX', 
    host='localhost')

cur = conn.cursor()

# Load the CSV file
df = pd.read_csv('dataset/imdb_top_1000.csv')

# Prepare data
movies_data = df[['Poster_Link', 
                  'Series_Title', 
                  'Released_Year', 
                  'Runtime', 
                  'Genre', 
                  'IMDB_Rating',
                  'Overview', 
                  'Director', 
                  'Star1', 
                  'Star2', 
                  'Star3', 
                  'Star4']].copy()
# change runtime to int using regex
movies_data['Runtime'] = movies_data['Runtime'].apply(lambda x: int(re.findall(r'\d+', x)[0]))

# Insert unique directors
directors = movies_data['Director'].unique()
director_tuple = [(director,) for director in directors]
execute_values(cur, "INSERT INTO directors (name) VALUES %s ON CONFLICT (name) DO NOTHING", [(director,) for director in directors])

# Insert unique actors
actors = pd.unique(movies_data[['Star1', 'Star2', 'Star3', 'Star4']].values.ravel('K'))
execute_values(cur, "INSERT INTO actors (name) VALUES %s ON CONFLICT (name) DO NOTHING", [(actor,) for actor in actors])

# Insert movies
movies_data = movies_data.rename(columns={
    'Poster_Link': 'poster',
    'Series_Title': 'title',
    'Released_Year': 'year',
    'Runtime': 'runtime',
    'Genre': 'genre',
    'IMDB_Rating': 'rating',
    'Overview': 'plot',
})

for _, row in movies_data.iterrows():
    cur.execute("SELECT id FROM directors WHERE name = %s", (row['Director'],))
    director_id = cur.fetchone()[0]
    
    cur.execute("""
        INSERT INTO movies (poster, title, year, runtime, genre, rating, plot, director_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING id
    """, (row['poster'], row['title'], row['year'], row['runtime'], row['genre'], row['rating'], row['plot'], director_id))

# Insert relationships between movies and actors
for _, row in movies_data.iterrows():
    cur.execute("SELECT id FROM movies WHERE title = %s", (row['title'],))
    movie_id = cur.fetchone()[0]
    
    for actor in ['Star1', 'Star2', 'Star3', 'Star4']:
        cur.execute("SELECT id FROM actors WHERE name = %s", (row[actor],))
        actor_id = cur.fetchone()[0]
        
        # Check if the relationship already exists
        cur.execute("""
            SELECT 1 FROM movie_actors 
            WHERE movie_id = %s AND actor_id = %s
        """, (movie_id, actor_id))
        
        if not cur.fetchone():
            # Relationship doesn't exist, insert it
            cur.execute("""
                INSERT INTO movie_actors (movie_id, actor_id)
                VALUES (%s, %s)
            """, (movie_id, actor_id))

conn.commit()
cur.close()
conn.close()
