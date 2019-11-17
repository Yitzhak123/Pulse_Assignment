from django.shortcuts import render
from django.http import JsonResponse
import pymysql
import requests
import json
from mysite.settings import API_HOST_OF_STOREDOT, SD_HOST, SD_USER, SD_PASSWORD
import logging


logger = logging.getLogger(__name__)


def connect_to_db():
    db = pymysql.connect(SD_HOST, SD_USER, SD_PASSWORD, "pulses")
    return db


def show_pulse_graph(request):
    db = connect_to_db()
    cur = db.cursor()
    cur.execute("SELECT series_n, influx, voltage FROM `pulse` ORDER BY `series_n` ASC")
    records = cur.fetchall()
    pulse_coordinates_by_series_n = {record[0]: [] for record in records}

    # Every record contains the values of series_n, influx, voltage
    for record in records:
        pulse_coordinates_by_series_n[record[0]].append((record[1], record[2]))

    for pulse_coordinates in pulse_coordinates_by_series_n.values():
        pulse_coordinates.sort()

    return render(request, 'pulse/show_pulse_graph.html',
                  {'pulse_coordinates_by_series_n': pulse_coordinates_by_series_n})


def get_tester_details_of_series_3(request):
    db = connect_to_db()
    cur = db.cursor()
    cur.execute("SELECT test_id FROM `pulse` WHERE series_n=3")
    records = cur.fetchall()
    if not all(record == records[0] for record in records):
        logger.warning("Not all tester for series {} are identical".format(3))

    r = requests.get('{}records/testers/{}'.format(API_HOST_OF_STOREDOT, records[0][0]))
    tester_details = json.loads(r.content)

    return JsonResponse(
        {'name': tester_details['name'],
         'os': tester_details['os'],
         'ver': tester_details['ver']}
    )


def count_testers_running_each_os(request):
    r = requests.get('{}records/testers/'.format(API_HOST_OF_STOREDOT))
    testers = json.loads(r.content)
    tester_list = testers['records']
    os_count_dict = {}

    for t in tester_list:
        if t['os'] in os_count_dict:
            os_count_dict[t['os']] += 1
        else:
            os_count_dict[t['os']] = 1

    return JsonResponse(os_count_dict)
