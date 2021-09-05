#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# dependencies
import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect
from flask import Flask, jsonify


# In[ ]:


# create engine
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine,reflect = True)


# In[ ]:


# save references to each table
stations = Base.classes.station
measurements = Base.classes.measurement


# In[ ]:


# create session (link) from Python to the DB
session = Session(engine)


# In[ ]:


# create an app
app = Flask(__name__)

# create a home page
@app.route("/")
def home():
    return (
        "Welcome to the Hawaii Climate API!<br/>"
        "Available Routes:<br/>"
        "/api/v1.0/precipitation<br/>"
        "/api/v1.0/stations<br/>"
        "/api.v1.0/tobs<br/>"      
    )


# convert precip query results to a data dictionary
# use date as the key and prcp as the value
# return the json representation of the dictionary
@app.route("/api/v1.0/precipitation")
def precip():
    lastDate = dt.date(2017,8,23)
    oneYear = lastDate - dt.timedelta(days = 365)
    precipitation = session.query(measurements.date, measurements.prcp).filter(measurements.date >= oneYear).all()
    
    precip = {date: prcp for date,prcp in precipitation}
    return jsonify(precip)


# return a JSON list of stations from the dataset
@app.route("/api/v1.0/stations")
def stationList():
    allStations = session.query(stations.station).all()
    
    results = list(np.ravel(allStations))
    return jsonify(results)


# query the dates and temperature observations of the most active station for the last year of data
# return a JSON list of temperature observations (TOBS) for the previous year
@app.route("/api.v1.0/tobs")
def tobs():
    lastDate = dt.date(2017,8,23)
    oneYear = lastDate - dt.timedelta(days = 365)
    mostActiveStation = session.query(measurements.tobs).filter(measurements.station == 'USC00519281').    filter(measurements.date >= oneYear).all()
    
    temps = list(np.ravel(mostActiveStation))
    return jsonify(temps)
    


# In[ ]:


if __name__ == "__main__":
    app.run(debug=True)


# In[ ]:





# In[ ]:




