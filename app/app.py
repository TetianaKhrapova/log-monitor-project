

#A tiny Flask app which log  different levels and "syntetic error" endpoint to test alerts.
 
from flask import Flask
import logging, time


app = Flask(_name_)
handler = logging.FileHandler( ' /var/log/sample_app/app.log')
handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s'))
logger =logging.getLogger('sample_app')
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)


@app.route('/')
def hello():
    logger.info("Helllo endpoint hit")
    return "OK\n"


@app.route('/error')
def err():
   logger.error("Syntetic Error: SOmthing went wrong")
   return "error triggered\n", 500


if _name_ == '_main_':
   app.run(host='0.0.0.0', port=8000)

