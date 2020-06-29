# -*- coding: utf-8 -*-
from selib import parser, database_influx, database_sqlite
import time
from configparser import ConfigParser
from datetime import datetime
import os.path
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
        database_influx.main(host=dbhost, port=dbport, dbname=dbname, json_body=points)
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
    except:
        print("ERROR: Fehler beim einlesen der Config")
        exit(1)

    if dbtype == 'influxdb':
        time.sleep(15)
        influx_parser()
    else:
        sqlite_parser()


