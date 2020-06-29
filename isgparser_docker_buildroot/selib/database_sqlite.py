# -*- coding: utf-8 -*-
from datetime import datetime
import sqlite3 as lite

jetzt = datetime.strftime(datetime.now(), format('%Y-%m-%d %H:%M:%S'))



def initdb(con, cur):
    cur.execute('DROP TABLE IF EXISTS RAUMTEMPERATUR')
    cur.execute('DROP TABLE IF EXISTS ENERGIEMANAGEMENT')
    cur.execute('DROP TABLE IF EXISTS WAERMEERZEUGER')
    cur.execute('DROP TABLE IF EXISTS HEIZEN')
    cur.execute('DROP TABLE IF EXISTS LUEFTEN')
    cur.execute('DROP TABLE IF EXISTS WARMWASSER')
    cur.execute('DROP TABLE IF EXISTS PROZESSWERTE')
    cur.execute('DROP TABLE IF EXISTS WAERMEMENGEN')
    cur.execute('DROP TABLE IF EXISTS LEISTUNGSAUFNAHME')
    cur.execute('DROP TABLE IF EXISTS LAUFZEITEN')
    cur.execute('DROP TABLE IF EXISTS ZEIT')

    cur.execute('CREATE TABLE ENERGIEMANAGEMENT(Id integer Primary Key autoincrement,  \
                WERT	 int default null, \
                inserted DATETIME)')

    cur.execute('CREATE TABLE RAUMTEMPERATUR(Id integer Primary Key autoincrement,  \
                RAUMISTTEMP_HK1 double, \
                RAUMSOLLTEMP_HK1 double, \
                RAUMFEUCHTE_HK1 double, \
                RAUMISTTEMP_HK2	 double, \
                RAUMSOLLTEMP_HK2	 double, \
                RAUMFEUCHTE_HK2	 double, \
                inserted DATETIME)')

    cur.execute('CREATE TABLE WAERMEERZEUGER(Id integer Primary Key autoincrement,  \
                HEIZSTUFE	 double, \
                inserted DATETIME)')

    cur.execute('CREATE TABLE HEIZEN(Id integer Primary Key autoincrement,  \
                AUSSENTEMPERATUR double, \
                ISTWERT_HK1 double, \
                SOLLWERT_HK1 double, \
                ISTWERT_HK2 double, \
                SOLLWERT_HK2 double, \
                VORLAUFTEMPERATUR double, \
                RUECKLAUFTEMPERATUR double, \
                DRUCK_HEIZKREIS double, \
                VOLUMENSTROM double, \
                inserted DATETIME)')

    cur.execute('CREATE TABLE WARMWASSER(Id integer Primary Key autoincrement,  \
                WW_ISTTEMP double, \
                WW_SOLLTEMP double, \
                inserted DATETIME)')

    cur.execute('CREATE TABLE LUEFTEN(Id integer Primary Key autoincrement,  \
                ZL_IST_LUEFTERDREHZAHL double, \
                ZL_SOLL_VOLUMENSTROM double, \
                AL_IST_LUEFTERDREHZAHL double, \
                AL_SOLL_VOLUMENSTROM double, \
                inserted DATETIME)')

    cur.execute('CREATE TABLE PROZESSWERTE(Id integer Primary Key autoincrement,  \
                HEISSGASTEMPERATUR double, \
                HOCHDRUCK double, \
                NIEDERDRUCK double, \
                VERDAMPFERTEMP double, \
                VERFLUESSIGERTEMP double, \
                FL_IST_LUEFTERDREHZAHL double, \
                FL_SOLL_VOLUMENSTROM	 double, \
                inserted DATETIME)')

    cur.execute('CREATE TABLE WAERMEMENGEN(Id integer Primary Key autoincrement,  \
                WM_HEIZEN_TAG double, \
                WM_HEIZEN_SUMME double, \
                WM_WW_TAG double, \
                WM_WW_SUMME double, \
                WM_NE_HEIZEN_SUMME double, \
                WM_NE_WW_SUMME double, \
                WM_WRG_TAG double, \
                WM_WRG_SUMME double, \
                inserted DATETIME)')

    cur.execute('CREATE TABLE LEISTUNGSAUFNAHME(Id integer Primary Key autoincrement,  \
                P_HEIZUNG_TAG double, \
                P_HEIZUNG_SUMME  double, \
                P_WW_TAG double, \
                P_WW_SUMME double, \
                inserted DATETIME)')

    cur.execute('CREATE TABLE LAUFZEITEN(Id integer Primary Key autoincrement,  \
                VERDICHTER_HEIZEN int, \
                VERDICHTER_WW  int, \
                ELEKTR_NE_HEIZEN int, \
                ELEKTR_NE_WW int, \
                inserted DATETIME)')
    cur.execute('CREATE TABLE ZEIT(Id integer Primary Key autoincrement,  \
                inserted DATETIME)')
    return True


def inserttemps(con, cur, var_rt, var_we, var_hz, var_lf, var_ww, var_pz, var_wm, var_la, var_lz, var_z):
#def inserttemps(cur, var_rt, var_em, var_we, var_hz, var_lf, var_ww, var_pz, var_wm, var_la, var_lz, var_z):
    cur.execute('''INSERT INTO RAUMTEMPERATUR (RAUMISTTEMP_HK1, RAUMSOLLTEMP_HK1, RAUMFEUCHTE_HK1, RAUMISTTEMP_HK2,
                RAUMSOLLTEMP_HK2, RAUMFEUCHTE_HK2, inserted)  values (?,?,?,?,?,?,?)''',        var_rt)
    # cur.execute('''INSERT INTO ENERGIEMANAGEMENT (WERT, inserted) values (?,?)''', var_em)
    cur.execute('''INSERT INTO WAERMEERZEUGER (HEIZSTUFE, inserted) values (?,?)''', var_we)
    cur.execute('''INSERT INTO HEIZEN (AUSSENTEMPERATUR, ISTWERT_HK1, SOLLWERT_HK1, ISTWERT_HK2, SOLLWERT_HK2,
                VORLAUFTEMPERATUR, RUECKLAUFTEMPERATUR, DRUCK_HEIZKREIS,
                VOLUMENSTROM, inserted) values (?,?,?,?,?,?,?,?,?,?)''',        var_hz)
    cur.execute('''INSERT INTO LUEFTEN (ZL_IST_LUEFTERDREHZAHL, ZL_SOLL_VOLUMENSTROM, AL_IST_LUEFTERDREHZAHL,
                AL_SOLL_VOLUMENSTROM, inserted  ) values (?,?,?,?,?)''',        var_lf)
    cur.execute('''INSERT INTO WARMWASSER (WW_ISTTEMP, WW_SOLLTEMP, inserted) values (?,?,?)''', var_ww)
    cur.execute('''INSERT INTO PROZESSWERTE (HEISSGASTEMPERATUR, HOCHDRUCK, NIEDERDRUCK, VERDAMPFERTEMP,
                VERFLUESSIGERTEMP, FL_IST_LUEFTERDREHZAHL,
                FL_SOLL_VOLUMENSTROM	, inserted) values (?,?,?,?,?,?,?,?)''',        var_pz)
    cur.execute('''INSERT INTO WAERMEMENGEN (WM_HEIZEN_TAG, WM_HEIZEN_SUMME, WM_WW_TAG, WM_WW_SUMME,
                WM_NE_HEIZEN_SUMME, WM_NE_WW_SUMME, WM_WRG_TAG,
                WM_WRG_SUMME, inserted) values (?,?,?,?,?,?,?,?,?)''',        var_wm)
    cur.execute('''INSERT INTO LEISTUNGSAUFNAHME (P_HEIZUNG_TAG, P_HEIZUNG_SUMME,
                P_WW_TAG, P_WW_SUMME, inserted) values (?,?,?,?,?)''',        var_la)
    cur.execute('''INSERT INTO LAUFZEITEN (VERDICHTER_HEIZEN ,  VERDICHTER_WW ,  ELEKTR_NE_HEIZEN ,
                ELEKTR_NE_WW ,  inserted) values (?,?,?,?,?)''',        var_lz)
    cur.execute('''INSERT INTO ZEIT (inserted) values (?)''',        (var_z,))
    con.commit()
    return True


def selectdb(con, cur):
    cur.execute('SELECT 1 from HEIZEN where 1=0')
    cur.execute('SELECT 1 from RAUMTEMPERATUR where 1=0')
    cur.execute('SELECT 1 from WAERMEERZEUGER where 1=0')
    cur.execute('SELECT 1 from LUEFTEN where 1=0')
    cur.execute('SELECT 1 from WARMWASSER where 1=0')
    cur.execute('SELECT 1 from WAERMEMENGEN where 1=0')
    cur.execute('SELECT 1 from LEISTUNGSAUFNAHME where 1=0')
    cur.execute('SELECT 1 from LAUFZEITEN where 1=0')
    cur.execute('SELECT 1 from ZEIT where 1=0')

    data = cur.fetchall()
    print(data)
