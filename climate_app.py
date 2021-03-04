import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii-Copy1.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to the table
Measurement = Base.classes.measurement
Station = Base.classes.station


#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start> and /api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return date and precipitation values"""
    # Query date and precipitation
    precip = session.query(Measurement.date, Measurement.prcp).all()

    session.close()

    return jsonify(precip)

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return stations"""
    # Query station names
    stations = session.query(Station.station, Station.name).all()

    session.close()

    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return dates and temperatures from most active station from the past year"""
    # Query data within parameters
    stations = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date > '2016-08-23', Measurement.station == 'USC00519281').all()

    session.close()

    return jsonify(stations)

@app.route("/api/v1.0/<start>")
def one_date(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Get query information"""
    # Query
    start_results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date >= start).all()

    session.close()
    return jsonify(start_results)















if __name__ == "__main__":
    app.run(debug=True)