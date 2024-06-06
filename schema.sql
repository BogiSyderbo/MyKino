-- Table to store actors
CREATE TABLE IF NOT EXISTS actors (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL
);


-- Table to store directors
CREATE TABLE IF NOT EXISTS directors (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL
);

-- Table to store movies
CREATE TABLE IF NOT EXISTS movies (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    genre VARCHAR(255),
    year INT,
    runtime INT,
    rating FLOAT,
    poster VARCHAR(255), -- URL to the poster image
    plot TEXT,
    director_id INTEGER REFERENCES directors(id),
    release_year INTEGER
);

-- Table to store the association between movies and actors
CREATE TABLE IF NOT EXISTS movie_actors (
    movie_id INTEGER REFERENCES movies(id),
    actor_id INTEGER REFERENCES actors(id),
    PRIMARY KEY (movie_id, actor_id)
);




