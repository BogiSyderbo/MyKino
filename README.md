![](MyKino_ER_model.jpeg)

# MyKino
Mykino is a website running python and flask library. The application can be used for searching and filtering for movies.

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
4. run load.py using command in the dataset folder:
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
