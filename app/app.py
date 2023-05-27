

import pandas as pd
import time
import redis
from flask import Flask, render_template
import os
from dotenv import load_dotenv

load_dotenv() 
cache = redis.Redis(host=os.getenv('REDIS_HOST'), port=6379,  password=os.getenv('REDIS_PASSWORD'))
app = Flask(__name__, static_folder='static')


# Function to load the Titanic dataset and display the first 5 rows
def load_titanic_data():
    file_path = 'titanic.csv'
    df = pd.read_csv(file_path)
    return df.head().to_html()

# Titanic page route
@app.route('/titanic')
def titanic():
    table_html = load_titanic_data()
    return render_template('titanic.html', table_html=table_html)

#get hit count
def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)

@app.route('/')
def hello():
    count = get_hit_count()
    return render_template('hello.html', name= "BIPM", count = count)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)

    ##end#end