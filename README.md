# Separser
Dies ist ein kleines Tool um die Werte eines Stiebel-Eltron ISG (Web) auzulesen und in eine Datenbank zu schreiben.

Unterstützt werden derzeit
- SQLite
- InfluxDB

Visualisiert wird es mittels Grafana.


Für den summierten Verbrauch ist noch diese CQ in Grafana einzufügen:

cq_1d   	CREATE CONTINUOUS QUERY cq_1d ON lwzdb BEGIN SELECT max("P HEIZUNG TAG") AS "P HEIZUNG JAHR" INTO lwzdb.awesome_policy.Leistungsaufnahme_Summary FROM lwzdb.awesome_policy.Leistungsaufnahme WHERE time > now() - 365d GROUP BY time(1d) END  
