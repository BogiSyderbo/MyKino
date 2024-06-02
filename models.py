# watchlist_table

class Movie(db.Model):
    id = primary_key=True

class Actor(db.Model):
    id = primary_key=True

class Director(db.Model):
    id = primary_key=True

class User(db.Model):
    id = primary_key=True
    
class Review(db.Model):
    id = primary_key=True
    rating 
    review_text 
    #movie_id = ForeignKey('movie.id')
    #user_id = ForeignKey('user.id')
