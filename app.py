from flask import Flask, render_template, request
from models import db, Movie, Actor, Director, User, Review
import pandas as pd
import re

app = Flask(__name__)



@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html')
    
@app.route('/about')
def about():
    return render_template('about.html')





