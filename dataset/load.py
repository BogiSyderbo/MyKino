import pandas as pd
import psycopg2
from psycopg2.extras import execute_values

# Connect to the PostgreSQL database
conn = psycopg2.connect(
    dbname='mykino', 
    user='postgres', 
    password='spil3009', 
    host='localhost')

cur = conn.cursor()


# Load the CSV file
df = pd.read_csv('imdb_top_1000.csv')

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


# Insert unique directors
directors = movies_data['Director'].unique()
director_tuple = [(director,) for director in directors]
execute_values(cur, "INSERT INTO directors (name) VALUES %s", director_tuple)
# execute_values(cur, "INSERT INTO directors (name) VALUES %s ON CONFLICT (name) DO NOTHING", [(director,) for director in directors])
# # Insert unique actors
# actors = movies_data[['Star1', 'Star2', 'Star3', 'Star4']]
# execute_values(cur, "INSERT INTO actors (name) VALUES %s ON CONFLICT (name) DO NOTHING", [(actor,) for actor in actors])

# # Insert movies and establish relationships
# for _, row in movies_data.iterrows():
#     cur.execute("SELECT id FROM directors WHERE name = %s", (row['Director'],))
#     director_id = cur.fetchone()[0]
    
#     cur.execute("""
#         INSERT INTO movies (title, genre, year, runtime, rating, votes, revenue, metascore, director_id)
#         VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
#         RETURNING id
#     """, (row['Title'], row['Genre'], row['Year'], row['Runtime'], row['Rating'], row['Votes'], row['Revenue (Millions)'], row['Metascore'], director_id))
    
#     movie_id = cur.fetchone()[0]
    
#     for actor in row[['Star1', 'Star2', 'Star3', 'Star4']]:
#         cur.execute("SELECT id FROM actors WHERE name = %s", (actor,))
#         actor_id = cur.fetchone()[0]
#         cur.execute("INSERT INTO movies_actors (movie_id, actor_id) VALUES (%s, %s) ON CONFLICT DO NOTHING", (movie_id, actor_id))

conn.commit()
cur.close()
conn.close()
