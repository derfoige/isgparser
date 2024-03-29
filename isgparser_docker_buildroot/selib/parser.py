# -*- coding: utf-8 -*-

import urllib.request, urllib.error, urllib.parse, time
from bs4 import BeautifulSoup
from .urlret import retry


@retry(urllib.error.URLError, tries=1000, delay=10)
def parsehtml(timestamp, baseurl, webuser, webpw, dbtype):
    """

    :rtype: dict

    """

    anlage_url = baseurl + '/?s=1,0'
    wp_url = baseurl + '/?s=1,1'
    payload = {'make': 'send', 'user': webuser, 'pass': webpw}
    logindata = urllib.parse.urlencode(payload).encode('utf-8')

    '''
    Scrapen der Daten aus dem Anlagen-Tab
    '''
    request = urllib.request.Request(anlage_url, logindata)
    result = urllib.request.urlopen(request)
    soup = BeautifulSoup(result, 'html.parser')

    '''
    Tabelle 0 holen: Raumtemperatur
    '''
    js = soup.findAll('table')[0]
    raumtemperatur = {}
    for row in js.findAll('tr'):
        cells = row.findAll('td')
        if len(cells) > 0:
            key = cells[0].find(text=True)
            value = cells[1].find(text=True)
            raumtemperatur[key] = float(''.join((ch if ch in '0123456789.-,' else '') for ch in value.replace(',','.')))
    anlage_values_rt = [(raumtemperatur['RAUMISTTEMP. HK1'],
                         raumtemperatur['RAUMSOLLTEMP. HK1'],
                         raumtemperatur['RAUMFEUCHTE HK1'],
                         raumtemperatur['RAUMISTTEMP. HK2'],
                         raumtemperatur['RAUMSOLLTEMP. HK2'],
                         raumtemperatur['RAUMFEUCHTE HK2'],
                         timestamp)]

    '''
    Tabelle 1 holen: Heizen
    '''
    js = soup.findAll('table')[1]
    heizen = {}
    for row in js.findAll('tr'):
        cells = row.findAll('td')
        if len(cells) > 0:
            key = cells[0].find(text=True)
            value = cells[1].find(text=True)
            heizen[key] = float(''.join((ch if ch in '0123456789.-,' else '') for ch in value.replace(',','.')))
    anlage_values_hz = [(heizen['AUSSENTEMPERATUR'],
                         heizen['ISTWERT HK1'],
                         heizen['SOLLWERT HK1'],
                         heizen['ISTWERT HK2'],
                         heizen['SOLLWERT HK2'],
                         heizen['VORLAUFTEMP.'],
                         heizen['R\xdcCKLAUFTEMP.'],
                         heizen['DRUCK HEIZKREIS'],
                         heizen['VOLUMENSTROM'],
                         timestamp)]

    '''
    Tabelle 2 holen: Warmwasser
    '''
    js = soup.findAll('table')[2]
    warmwasser = {}
    for row in js.findAll('tr'):
        cells = row.findAll('td')
        if len(cells) > 0:
            key = cells[0].find(text=True)
            value = cells[1].find(text=True)
            warmwasser[key] = float(''.join((ch if ch in '0123456789.-,' else '') for ch in value.replace(',','.')))
    anlage_values_ww = [(warmwasser['WW-ISTTEMP.'],
                         warmwasser['WW-SOLLTEMP.'],
                         timestamp)]

    '''
    Tabelle 3 holen: Lüften
    '''
    js = soup.findAll('table')[3]
    lueften = {}
    for row in js.findAll('tr'):
        cells = row.findAll('td')
        if len(cells) > 0:
            key = cells[0].find(text=True)
            value = cells[1].find(text=True)
            lueften[key] = float(''.join((ch if ch in '0123456789.-,' else '') for ch in value.replace(',','.')))
    anlage_values_lf = [(lueften['ZULUFT IST L\xdcFTERDREHZAHL'],
                     lueften['ZULUFT SOLL VOLUMENSTROM'],
                     lueften['ABLUFT IST L\xdcFTERDREHZAHL'],
                     lueften['ABLUFT SOLL VOLUMENSTROM'],
                     timestamp)]


    '''
    Tabelle 4 holen: Wärmeerzeuger
    '''
    js = soup.findAll('table')[4]
    waermeerzeuger = {}
    for row in js.findAll('tr'):
        cells = row.findAll('td')
        if len(cells) > 0:
            key = cells[0].find(text=True)
            value = cells[1].find(text=True)
            waermeerzeuger[key] = float(''.join((ch if ch in '0123456789.-,' else '') for ch in value.replace(',','.')))
    anlage_values_we = [(waermeerzeuger['HEIZSTUFE'],
                         timestamp)]

    '''
    Tabelle 5 holen: Energiemanagement
    '''
    js = soup.findAll('table')[5]
    energiemanagement = {}
    for row in js.findAll('tr'):
        cells = row.findAll('td')
        if len(cells) > 0:
            key = cells[0].find(text=True)
            value = cells[1].find(text=True)
            energiemanagement[key] = 0

    '''
    Scrapen der Daten aus dem Wärmepumpen-Tab
    '''
    request = urllib.request.Request(wp_url, logindata)
    result = urllib.request.urlopen(request)
    soup = BeautifulSoup(result, 'html.parser')

    '''
    Tabelle 1 holen: Prozesswerte
    '''
    js = soup.findAll('table')[0]
    prozesswerte = {}
    for row in js.findAll('tr'):
        cells = row.findAll('td')
        if len(cells) > 0:
            key = cells[0].find(text=True)
            value = cells[1].find(text=True)
            prozesswerte[key] = float(''.join((ch if ch in '0123456789.-,' else '') for ch in value.replace(',','.')))
    wp_values_pz = [(prozesswerte['HEISSGASTEMP.'],
                    prozesswerte['HOCHDRUCK'],
                    prozesswerte['NIEDERDRUCK'],
                    prozesswerte['VERDAMPFERTEMP.'],
                    prozesswerte['VERFL\xdcSSIGERTEMP.'],
                    prozesswerte['FORTLUFT IST L\xdcFTERDREHZAHL'],
                    prozesswerte['FORTLUFT SOLL VOLUMENSTROM'],
                    timestamp)]

    '''
    Tabelle 2 holen: Waermemengen
    '''
    js = soup.findAll('table')[1]
    waermemengen = {}
    for row in js.findAll('tr'):
        cells = row.findAll('td')
        if len(cells) > 0:
            key = cells[0].find(text=True)
            value = cells[1].find(text=True)
            waermemengen[key] = float(''.join((ch if ch in '0123456789.-,' else '') for ch in value.replace(',','.')))
    wp_values_wm = [(waermemengen['WM HEIZEN TAG'],
                 waermemengen['WM HEIZEN SUMME'],
                 waermemengen['WM WW TAG'],
                 waermemengen['WM WW SUMME'],
                 waermemengen['WM NE HEIZEN SUMME'],
                 waermemengen['WM NE WW SUMME'],
                 waermemengen['WM WRG TAG'],
                 waermemengen['WM WRG SUMME'],
                 timestamp)]


    '''
    Tabelle 3 holen: Leistungsaufnahme
    '''
    js = soup.findAll('table')[2]
    leistungsaufnahme = {}
    for row in js.findAll('tr'):
        cells = row.findAll('td')
        if len(cells) > 0:
            key = cells[0].find(text=True)
            value = cells[1].find(text=True)
            leistungsaufnahme[key] = float(''.join((ch if ch in '0123456789.-,' else '') for ch in value.replace(',','.')))
    wp_values_la = [(leistungsaufnahme['P HEIZUNG TAG'],
                 leistungsaufnahme['P HEIZUNG SUMME'],
                 leistungsaufnahme['P WW TAG'],
                 leistungsaufnahme['P WW SUMME'],
                 timestamp)]


    '''
    Tabelle 4 holen: Laufzeiten
    '''
    js = soup.findAll('table')[3]
    laufzeiten = {}
    for row in js.findAll('tr'):
        cells = row.findAll('td')
        if len(cells) > 0:
            key = cells[0].find(text=True)
            value = cells[1].find(text=True)
            laufzeiten[key] = int(''.join((ch if ch in '0123456789.-,' else '') for ch in value.replace(',','.')))
    wp_values_lz = [(laufzeiten['VERDICHTER HEIZEN'],
                     laufzeiten['VERDICHTER WW'],
                     laufzeiten['ELEKTR. NE HEIZEN'],
                     laufzeiten['ELEKTR. NE WW'],
                     timestamp)]

    if dbtype == 'influxdb':
        ergebnis = {'Raumtemperatur': raumtemperatur, 'Energiemanagement': energiemanagement,
                    'Waermeerzeuger': waermeerzeuger, 'Heizen': heizen, 'Wamwasser': warmwasser,
                    'Lueften': lueften, 'Prozesswerte': prozesswerte, 'Leistungsaufnahme': leistungsaufnahme,
                    'Waermemengen': waermemengen, 'Laufzeiten': laufzeiten}
    else:
        ergebnis = {'anlage_values_rt': anlage_values_rt, 'anlage_values_we': anlage_values_we,
                    'anlage_values_hz': anlage_values_hz, 'anlage_values_ww': anlage_values_ww,
                    'anlage_values_lf': anlage_values_lf,
                    'wp_values_pz': wp_values_pz, 'wp_values_wm': wp_values_wm,
                    'wp_values_la': wp_values_la, 'wp_values_lz': wp_values_lz}

    return ergebnis
