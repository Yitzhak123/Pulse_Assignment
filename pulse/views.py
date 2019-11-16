from django.shortcuts import render
import MySQLdb

# Create your views here.

import pymysql


def connect_to_db():
    db = pymysql.connect("interview.storedot.us", "storedot",
                         "KVzQU-5an@gGa5e", "pulses")
    return db


def show_pulse_graph(request):
    db = connect_to_db()
    cur = db.cursor()
    cur.execute("SELECT series_n, influx, voltage FROM `pulse` ORDER BY `series_n` ASC")
    records = cur.fetchall()
    print("RECORDS:")
    print(records)
    pulse_coordinates_by_series_n = {record[0]: [] for record in records}
    print(pulse_coordinates_by_series_n)
    print("FOR LOOP START:")
    # Every record contains the values of series_n, influx, voltage
    for record in records:
        pulse_coordinates_by_series_n[record[0]].append((record[1], record[2]))
        # pulse_coordinates_by_series_n.append(record)

    print(pulse_coordinates_by_series_n)
    return render(request, 'pulse/show_pulse_graph.html',
                  {'pulse_coordinates_by_series_n': pulse_coordinates_by_series_n})
