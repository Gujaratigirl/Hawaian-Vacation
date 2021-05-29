#Dependancies
import numpy as np
from numpy.lib import twodim_base
from numpy.lib.polynomial import RankWarning

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt



from flask import Flask, jsonify
from sqlalchemy.sql.operators import startswith_op

#Set up
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
Base.prepare(engine, reflect=True)

# Save reference to the table
Measure = Base.classes.measurement
Stations = Base.classes.station



# Create an app
app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

# Define static routes
@app.route("/")
def home():
    return (
        f"Welcome to the 'Pick Your Vacation Date' page!<br/><br/>"
        f"Going to Hawaii!  Wonderful!  Let's take a look at some rain and temperature!<br/><br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/><br/>"

        f"To get all results from a start date <br/>"
        f"Insert a date into *start with format *YYYY-MM-DD* <br/>"
        f"Range of dates 2010-01-01 through 2017-08-23 <br/>"
        f"/api/v1.0/start<br/>"
        f"Example: <br>"
        f"/api/v1.0/2010-01-01<br/><br/>"
        
        f"To get all results for a range of dates <br/>"
        f"Insert a date into *start and *end with format *YYYY-MM-DD* <br/>"
        f"Range of dates 2010-01-01 through 2017-08-23 <br/>"
        f"/api/v1.0/start/end<br/>"
        f"Example: <br>"
        f"/api/v1.0/2010-01-01/2017-08-23<br/>"
        
    )

@app.route("/api/v1.0/precipitation")
def precip():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all dates and precipitation """
    # Query all prcp
    results = session.query(Measure.date, Measure.prcp).all()

    session.close()

# Create a dictionary from the row data and append to a list of all_rain
    all_rain= []
    for date, prcp in results:
        rain_dict = {}
        rain_dict["date"] = date
        rain_dict["prcp"] = prcp
        all_rain.append(rain_dict)
    
    return jsonify(all_rain)

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all stations"""
    # Query all stations
    results = session.query(Stations.station).all()

    session.close()

   # Create a dictionary from the row data and append to a list of all_stations
    all_stations= []
    for station in results:
        station_dict = {}
        station_dict["stations"] = station
        all_stations.append(station_dict)

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    max_date_scalar = session.query(func.max(Measure.date)).scalar()
    max_date_scalar

    max_date =dt.datetime.strptime(max_date_scalar, '%Y-%m-%d')
    max_date

    one_year = dt.timedelta(weeks = 52)
    one_year_before = max_date - one_year
    one_year_before



    """Return a list of station=USC00519281, date and temp for the last year of data """
    # Query all tobs
    results = session.query(Measure.station, Measure.date, Measure.prcp, Measure.tobs).filter(Measure.station == 'USC00519281').filter(Measure.date >= one_year_before).all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_tobs
    all_tobs= []
    for station, date, prcp, tobs in results:
        tobs_dict = {}
        tobs_dict["station"] = station
        tobs_dict["date"] = date
        tobs_dict["prcp"] = prcp
        tobs_dict["tobs"] = date
        
        all_tobs.append(tobs_dict)

    return jsonify(all_tobs)

2020-10-10

# @app.route("/api/v1.0/working/<start>")
# def start_date(start):
#     # Create our session (link) from Python to the DB
#     session = Session(engine)

#     search_term = start.replace(" ", "").lower() #this is a value
#     date_present = session.query(Measure.date, Measure.date == search_term).all() #this is a list or dict??

#     #return(search_term)
#     return jsonify(date_present)

#     # for data in date_present:
#     #     if data == 'true':
#     #         #date_found = 'Yes' 
#     #         return(data)
#     #         #return(date_found)


#     # # Query all tobs
#     # if search_term == date_present:
#     #     results = session.query(Measure.station, Measure.date, Measure.prcp, Measure.tobs).filter(Measure.date >= search_term).all()

#     session.close()

#     #     # Create a dictionary from the row data and append to a list of all_tobs
#     #     all_tobs= []
#     #     for station, date, prcp, tobs in results:
#     #         tobs_dict = {}
#     #         tobs_dict["station"] = station
#     #         tobs_dict["date"] = date
#     #         tobs_dict["prcp"] = prcp
#     #         tobs_dict["tobs"] = date
        
#     #         all_tobs.append(tobs_dict)

#     #     return jsonify(all_tobs)


#     # return jsonify({"error": f"Date Range not found.  Please try again with format *YYYY-MM-DD* and range of dates 2010-01-01 through 2017-08-23 "}), 404    



# @app.route("/api/v1.0/test/<start>")
# def working_start_date(start):
#     # Create our session (link) from Python to the DB
#     session = Session(engine)

#     search_term = start.replace(" ", "").lower() #this is a value
#     #date_present = session.query(Measure.date, Measure.date == search_term).all() #this is a list or dict??

#     #return(search_term)
#     #return jsonify(date_present)

#     # for data in date_present:
#     #     if data == 'true':
#     #         #date_found = 'Yes' 
#     #         return(data)
#     #         #return(date_found)


#     # Query all tobs
#     #if search_term == date_present:
#     results = session.query(Measure.station, Measure.date, Measure.prcp, Measure.tobs).filter(Measure.date >= search_term).all()
#     #tmin = session.query(Measure.station, Measure.date, func.min(Measure.tobs)).all()
#     #tavg = session.query(Measure.station, Measure.date, func.avg(Measure.tobs)).all()
#     #tmax = session.query(Measure.station, Measure.date, func.max(Measure.tobs)).all()

#     session.close()

#         # Create a dictionary from the row data and append to a list of all_tobs
#     all_tobs= []


    
#     for station, date, prcp, tobs in results:
#         tobs_dict = {}
#         tobs_dict["station"] = station
#         tobs_dict["date"] = date
#         tobs_dict["prcp"] = prcp
#         tobs_dict["tobs"] = date
    
#         all_tobs.append(tobs_dict)

#     return jsonify(all_tobs)


#     return jsonify({"error": f"Date Range not found.  Please try again with format *YYYY-MM-DD* and range of dates 2010-01-01 through 2017-08-23 "}), 404    

@app.route("/api/v1.0/<start>")
def working2_start_date(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    search_term = start.replace(" ", "").lower() 

    tmin = session.query(Measure.station, Measure.date, func.min(Measure.tobs)).filter(Measure.date >= search_term).all()
    tavg = session.query(Measure.station, Measure.date, func.avg(Measure.tobs)).filter(Measure.date >= search_term).all()
    tmax = session.query(Measure.station, Measure.date, func.max(Measure.tobs)).filter(Measure.date >= search_term).all()

    session.close()

    all_agg= [tmin, tavg, tmax]

    return jsonify(all_agg)
    
@app.route("/api/v1.0/<start>/<end>")
def start_end_date(start,end):
    # Create our session (link) from Python to the DB
    session = Session(engine)


    start_term = start.replace(" ", "").lower() 
    end_term = end.replace(" ", "").lower()

    tmin = session.query(Measure.station, Measure.date, func.min(Measure.tobs)).filter(Measure.date <= end_term).filter(Measure.date >= start_term).all()
    tavg = session.query(Measure.station, Measure.date, func.avg(Measure.tobs)).filter(Measure.date <= end_term).filter(Measure.date >= start_term).all()
    tmax = session.query(Measure.station, Measure.date, func.max(Measure.tobs)).filter(Measure.date <= end_term).filter(Measure.date >= start_term).all()

    session.close()
 
    all_agg= [tmin, tavg, tmax]

    return jsonify(all_agg)



if __name__ == "__main__":
    app.run(debug=True)

