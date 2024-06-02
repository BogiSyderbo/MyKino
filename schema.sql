-- Table to store actors
CREATE TABLE actors (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

-- Table to store directors
CREATE TABLE directors (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

-- Table to store movies
CREATE TABLE movies (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    director_id INTEGER REFERENCES directors(id),
    release_year INTEGER
);

-- Table to store the association between movies and actors
CREATE TABLE movie_actors (
    movie_id INTEGER REFERENCES movies(id),
    actor_id INTEGER REFERENCES actors(id),
    PRIMARY KEY (movie_id, actor_id)
);

-- Table to store users
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL
);

-- Table to store watchlist
CREATE TABLE watchlist (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    movie_id INTEGER REFERENCES movies(id),
);
