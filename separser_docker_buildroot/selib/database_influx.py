# -*- coding: utf-8 -*-
from influxdb import InfluxDBClient


def main(host, port, dbname, json_body):
    """

    :rtype: object
    """
    query = 'select VORLAUFTEMPERATUR from "LWZ Logging";'

    client = InfluxDBClient(host, port, dbname)

    # Script for creating DB 
    # print("Create database: " + dbname)
    # client.create_database(dbname)
    #
    # print("Create a retention policy")
    # client.create_retention_policy('awesome_policy', '3d', 3, database=dbname, default=True)

    #print("Write points: {0}".format(json_body))
    client.write_points(json_body, database=dbname)

    # Query DB
    #print("Queying data: " + query)
    #result = client.query(query, database=dbname)
    #print("Result: {0}".format(result))

    # Script for dropping DB
    #client.drop_database(dbname)

