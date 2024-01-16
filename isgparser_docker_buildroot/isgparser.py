# -*- coding: utf-8 -*-
from selib import parser, database_influx, database_sqlite, isgweather
import time
from configparser import ConfigParser
from datetime import datetime
import os.path
from os import environ
import sqlite3 as lite



def sqlite_parser():
    if not os.path.isfile(dbname):
        print("Database " + dbname + " is not accessible. Creating one")
        con = lite.connect(database=dbname)
        cur = con.cursor()
        database_sqlite.initdb(con, cur)
    else:
        print("Opening database " + dbname)
        con = lite.connect(database=dbname)
        cur = con.cursor()
        database_sqlite.selectdb(con, cur)
    try:
        while True:
                jetzt = datetime.strftime(datetime.now(), format('%Y-%m-%d %H:%M:%S'))
                values = parser.parsehtml(timestamp=jetzt, webpw=webpw, webuser=webuser, baseurl=baseurl, dbtype='sqlite')
                database_sqlite.inserttemps(con, cur,
                                            var_we=values['anlage_values_we'][0],
                                            var_rt=values['anlage_values_rt'][0],
                                            var_hz=values['anlage_values_hz'][0],
                                            var_lf=values['anlage_values_lf'][0],
                                            var_ww=values['anlage_values_ww'][0],
                                            var_pz=values['wp_values_pz'][0],
                                            var_wm=values['wp_values_wm'][0],
                                            var_la=values['wp_values_la'][0],
                                            var_lz=values['wp_values_lz'][0],
                                            var_z=jetzt)
                print("Datenpunkt geschrieben. Timestamp: {0}".format(jetzt))
                time.sleep(float(interval))
    except KeyboardInterrupt:
        print('interrupted!')
    finally:
        con.close()
        print("Connection closed.")


def influx_parser():
    while True:
        # Get Values from LWZ
        values = parser.parsehtml('', baseurl, webuser, webpw, dbtype=dbtype)
        points = []
        jetzt = time.strftime('%Y-%m-%dT%H:%M:%SZ')
        for category in list(values.keys()):
            if len(values[category]) > 0:
                json_body = [
                    {
                        "measurement": category,
                        "tags": {
                            "Kategorie": category
                        },
                        "time": jetzt,
                        "fields": values[category]
                    }
                ]
                points += json_body
        database_influx.main(host=dbhost, port=dbport, dbname=dbname, json_body=points, influxpw=dbpw, influxuser=dbuser)

        # Get Values from WeatherUnderground
        # Todo: Run this in parallel to utilize retry logic
        # currently retry is ignored
        if wu_enabled:
            try:          
                values_wu = isgweather.get_weather(wu_url, wu_apikey, wu_stationid)
                points_wu = []
                for category in list(values_wu.keys()):
                    if len(values_wu[category]) > 0:
                        json_body_wu = [
                            {
                                "measurement": category,
                                "tags": {
                                    "Kategorie": category
                                },
                                "time": jetzt,
                                "fields": values_wu[category]
                            }
                        ]
                        points_wu += json_body_wu
                database_influx.main(host=dbhost, port=dbport, dbname=dbname, json_body=points_wu, influxpw=dbpw, influxuser=dbuser)
            except:
                print("Something is wrong with the WU API")
        
        time.sleep(float(interval))

if __name__ == '__main__':
    try:
        config = ConfigParser()
        config.read('config.cfg')

        baseurl = config.get('web', 'baseurl')
        webuser = config.get('web', 'webuser')
        webpw = config.get('web', 'webpw')
        dbname = config.get('db', 'dbname')
        dbtype = config.get('db', 'dbtype')
        dbport = config.get('db', 'dbport')
        dbhost = config.get('db', 'dbhost')
        interval = config.get('general', 'interval')
        wu_url = config.get('weather', 'wu_url')
        wu_apikey = config.get('weather', 'wu_apikey')
        wu_stationid = config.get('weather', 'wu_stationid')
        wu_enabled = config.get('weather', 'wu_enabled')
    except:
        print("INFO: Keine Config gefunden. Versuche mit ENV.")
        baseurl = os.environ.get('SE_BASEURL','http://servicewelt')
        webuser = os.environ.get('SE_WEBUSER','admin')
        webpw = os.environ.get('SE_WEBPW','password')
        dbname = os.environ.get('SE_DBNAME','isg')
        dbtype = os.environ.get('SE_DBTYPE','influxdb')
        dbport = os.environ.get('SE_DBPORT','8086')
        dbhost = os.environ.get('SE_DBHOST','localhost')
        dbuser = os.environ.get('SE_DBUSER','isgparser')
        dbpw = os.environ.get('SE_DBPW','PASSWORD')
        interval = os.environ.get('SE_INTERVAL','300')
        wu_url = os.environ.get('SE_WU_URL','api.weather.com/v2/pws/observations/current')
        wu_apikey = os.environ.get('SE_WU_APIKEY','XXXXXXXXXXXX')
        wu_stationid = os.environ.get('SE_WU_STATIONID','XXXXXXXXXXXX')
        wu_enabled = os.environ.get('SE_WU_ENABLED','false')
    else:
        print("ERROR: Keine Config gefunden")
        exit(1)

    if dbtype == 'influxdb':
        time.sleep(15)
        influx_parser()
    else:
        sqlite_parser()


