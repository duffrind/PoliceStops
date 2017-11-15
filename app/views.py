import flask
from flask import render_template, request
from app import app
import viz
import psycopg2
import os
from urllib import parse

parse.uses_netloc.append("postgres")
url = parse.urlparse(os.environ["DATABASE_URL"])

conn = psycopg2.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
)

#conn = psycopg2.connect(dbname='Open_Policing')
cur = conn.cursor()

def generateQuery(stop_date_MIN, stop_date_MAX, driver_gender, driver_age_MIN, driver_age_MAX, \
driver_race_TUPLE, violation_TUPLE, search_conducted, search_type_TUPLE, stop_outcome_TUPLE, \
officer_gender,  officer_age_MIN,  officer_age_MAX,  officer_race_TUPLE,  officer_rank_TUPLE,  out_of_state):
    add_where = True
    query = 'select county_name, count(*) from fl_stops'
    if stop_date_MIN is not None and len(stop_date_MIN) > 0:
        query = query + " where stop_date >= TO_DATE('" + str(stop_date_MIN) + "', 'YYYY-MM-DD')"
        add_where = False
    if stop_date_MAX is not None and len(stop_date_MAX) > 0:
        if add_where:
            query = query + ' where'
            add_where = False
        else:
            query = query + ' AND'
        query = query + " stop_date <= TO_DATE('" + str(stop_date_MAX) + "', 'YYYY-MM-DD')"
    if driver_gender is not None and len(driver_gender) > 0:
        if add_where:
            query = query + ' where'
            add_where = False
        else:
            query = query + ' AND'
        query = query + " driver_gender = '" + driver_gender + "'"
    if driver_age_MIN is not None:
        if add_where:
            query = query + ' where'
            add_where = False
        else:
            query = query + ' AND'
        query = query + ' driver_age >= ' + str(driver_age_MIN)
    if driver_age_MAX is not None:
        if add_where:
            query = query + ' where'
            add_where = False
        else:
            query = query + ' AND'
        query = query + ' driver_age <= ' + str(driver_age_MAX)
    if len(driver_race_TUPLE) > 0:
        if add_where:
            query = query + ' where'
            add_where = False
        else:
            query = query + ' AND'
        query = query + " driver_race IN (" + ','.join(["'" + x + "'" for x in driver_race_TUPLE]) + ")"
    if len(violation_TUPLE) > 0:
        if add_where:
            query = query + ' where'
            add_where = False
        else:
            query = query + ' AND'
        query = query + " violation SIMILAR TO '%(" + '|'.join(violation_TUPLE) + ")%'"
    if search_conducted is not None and len(search_conducted) > 0:
        if add_where:
            query = query + ' where'
            add_where = False
        else:
            query = query + ' AND'
        query = query + " search_conducted = '" + str(search_conducted) + "'"
    if len(search_type_TUPLE) > 0:
        if add_where:
            query = query + ' where'
            add_where = False
        else:
            query = query + ' AND'
        query = query + " search_type IN (" + ','.join(["'" + x + "'" for x in search_type_TUPLE]) + ")"
    if len(stop_outcome_TUPLE) > 0:
        if add_where:
            query = query + ' where'
            add_where = False
        else:
            query = query + ' AND'
        query = query + " stop_outcome IN (" + ','.join(["'" + x + "'" for x in stop_outcome_TUPLE]) + ")"
    if officer_gender is not None and len(officer_gender) > 0:
        if add_where:
            query = query + ' where'
            add_where = False
        else:
            query = query + ' AND'
        query = query + " officer_gender = '" + officer_gender + "'"
    if officer_age_MIN is not None:
        if add_where:
            query = query + ' where'
            add_where = False
        else:
            query = query + ' AND'
        query = query + ' officer_age >= ' + str(officer_age_MIN)
    if officer_age_MAX is not None:
        if add_where:
            query = query + ' where'
            add_where = False
        else:
            query = query + ' AND'
        query = query + ' officer_age <= ' + str(officer_age_MAX)
    if len(officer_race_TUPLE) > 0:
        if add_where:
            query = query + ' where'
            add_where = False
        else:
            query = query + ' AND'
        query = query + " officer_race IN (" + ','.join(["'" + x + "'" for x in officer_race_TUPLE]) + ")"
    if len(officer_rank_TUPLE) > 0:
        if add_where:
            query = query + ' where'
            add_where = False
        else:
            query = query + ' AND'
        query = query + " officer_rank IN (" + ','.join(["'" + x + "'" for x in officer_rank_TUPLE]) +  ")"
    if out_of_state is not None and len(out_of_state) > 0:
        if add_where:
            query = query + ' where'
            add_where = False
        else:
            query = query + ' AND'
        query = query + " out_of_state = '" + str(out_of_state) + "'"
    query = query + ' group by county_name order by county_name;'
    #print(query)
    cur.execute(query)
    counties_counts = cur.fetchall()
    counties_dict = dict(counties_counts)
    return counties_dict

@app.route('/')
@app.route('/index')
def index():
    stop_date_MIN = request.args.get('stop_date_MIN', default=None, type=str)
    stop_date_MAX = request.args.get('stop_date_MAX', default=None, type=str)
    driver_gender = request.args.get('driver_gender', default=None, type=str)
    driver_age_MIN = request.args.get('driver_age_MIN', default=None, type=int)
    driver_age_MAX = request.args.get('driver_age_MAX', default=None, type=int)
    driver_race_TUPLE = request.args.getlist('driver_race_TUPLE', type=str)
    violation_TUPLE = request.args.getlist('violation_TUPLE', type=str)
    search_conducted = request.args.get('search_conducted', default=None, type=str)
    search_type_TUPLE = request.args.getlist('search_type', type=str)
    stop_outcome_TUPLE = request.args.getlist('stop_outcome_TUPLE', type=str)
    officer_gender = request.args.get('officer_gender', default=None, type=str)
    officer_age_MIN = request.args.get('officer_age_MIN', default=None, type=int)
    officer_age_MAX = request.args.get('officer_age_MAX', default=None, type=int)
    officer_race_TUPLE = request.args.getlist('officer_race_TUPLE', type=str)
    officer_rank_TUPLE = request.args.getlist('officer_rank_TUPLE', type=str)
    out_of_state = request.args.get('out_of_state', default=None, type=str)
    count_dict = generateQuery(stop_date_MIN, stop_date_MAX, driver_gender, driver_age_MIN, driver_age_MAX, \
    driver_race_TUPLE, violation_TUPLE, search_conducted, search_type_TUPLE, stop_outcome_TUPLE, \
    officer_gender,  officer_age_MIN,  officer_age_MAX,  officer_race_TUPLE,  officer_rank_TUPLE,  out_of_state)
    viz.generate(count_dict)#viz.generate(count_dict)
    #return str(stop_date_MIN) + str(stop_date_MAX) + str(driver_gender) + str(driver_age_MIN) + str(driver_age_MAX) + \
    #    str(driver_race_TUPLE) + str(violation_TUPLE) + str(search_conducted) + str(search_type_TUPLE) + \
    #    str(stop_outcome_TUPLE) + str(officer_gender) + str(officer_age_MIN) + str(officer_age_MAX) + \
    #    str(officer_race_TUPLE) + str(officer_rank_TUPLE) + str(out_of_state)
    return render_template('index.html')

#@app.route('/results/map.html')
#def show_map():
#    return flask.send_file('/Users/duffrind/ncf/data/project1/police-traffic-stop-explorer/PoliceStops/app/results/map.html')
