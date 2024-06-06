![](MyKino_ER_model.jpeg)

# MyKino
Mykino is a website running python and flask library. The application can be used for searching and filtering for movies.
Click on a movie poster to see information about a movie. Click links for actors or directors to see film they are involved with.
Use the search bar to search for movies, actors or directors.
On the home page you can filter movies by genre. Click the "Mykino" text to get back to the home page.
## Requirements:
Run the code below to install the necessary modules.
    
    $ pip install -r requirements.txt


## Database init
0. make a database using the command:
```
    createdb -U {user} mykino
```
2. set the database username and password in load.py and app.py
3. run schema.sql in your database
4. run load.py using command:
```
    $ python3 load.py
```
Example on how to run sql files: 
```
    psql -d{database} -U{user} -W -f schema.sql
```
#### notes
For Ubuntu add host (-h127.0.0.1) to psql: 
```
    psql -d{database} -U{user} -h127.0.0.1 -W -f schema.sql
```
schema_drop.sql can be used to drop the schema.
