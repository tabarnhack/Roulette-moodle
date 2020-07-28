import requests
from bs4 import BeautifulSoup
from flask import Flask, request, abort, make_response
from flask_cors import CORS
import urllib.parse as urlparse
from urllib.parse import parse_qs

import re
import codecs

app = Flask(__name__)
cors = CORS(app, supports_credentials=True)

app.config.from_envvar("APP_CFG")

todos = {}

@app.route("/login", methods=["GET"])
def login_get():
    return "You have to use POST method with 'username' and 'password' parameters stored in JSON<br />" + \
        "Example: curl -X POST -d {'username': 'foo', 'password': 'bar} http://&lt;url&gt;/login"


@app.route("/login", methods=["POST"])
def login_post():
    if not request.json:
        abort(400, description="POST parameters are sent via JSON data")

    if "username" not in request.json or "password" not in request.json:
        abort(400, descritpion="Missing parameter (need 'username' and 'password')")

    user = request.json.get('username')
    psw = request.json.get('password')

    session = requests.Session()

    r = session.get(f"{app.config['MOODLE_URL']}/login/index.php")
    soup = BeautifulSoup(r.text, "html.parser")

    payload = {
        'anchor': '',
        'username': user,
        'password': psw,
        'logintoken': soup.find("input", {"name":"logintoken"})["value"]
    }
    
    r = session.post(f"{app.config['MOODLE_URL']}/login/index.php", data=payload)
    if r.history:
        prev_url = r.history[0].headers.get("Location")
    else:
        prev_url = app.config['MOODLE_URL']

    if "MoodleSession" in session.cookies and prev_url != f"{app.config['MOODLE_URL']}/login/index.php":
        res = make_response({"status": "Connected", "cookie": session.cookies.get("MoodleSession")}, r.status_code)
        res.set_cookie("MoodleSession", session.cookies.get("MoodleSession"), secure=True, httponly=True)
    else:
        abort(401, description="The connection was not successful")
    return res


@app.route('/check', methods=['GET'])
def check():
    if "MoodleSession" not in request.cookies:
        abort(401, description="You must first login via /login")

    cookies = {"MoodleSession": request.cookies.get("MoodleSession")}
    r = requests.get(f"{app.config['MOODLE_URL']}/my/", cookies=cookies, allow_redirects=False)

    if r.status_code == 200:
        res = make_response({"status": "Connected"}, 200)
    else:
        abort(401, description="The connection was not successful")
    return res


@app.route('/courses', methods=['GET'])
def courses():
    if "MoodleSession" not in request.cookies:
        abort(401, description="You must first login via /login")

    cookies = {"MoodleSession": request.cookies.get("MoodleSession")}
    r = requests.get(f"{app.config['MOODLE_URL']}/grade/report/overview/", cookies=cookies, allow_redirects=False)

    if r.status_code != 200:
        abort(401, description="You must first login via /login")

    html = r.text

    soup = BeautifulSoup(html, "html.parser")
    table = soup.select("td.cell.c0")

    courses = []
    for course in table:
        ident = course.find('a').get("href")
        content = course.get_text()
        parsed = urlparse.urlparse(ident)
        courses += [{"id": int(urlparse.parse_qs(parsed.query)['id'][0]), "name": content}]

    return {"items": courses}


@app.route('/grades', methods=["GET"])
def grades():
    if "MoodleSession" not in request.cookies:
        abort(401, description="You must first login via /login")

    if "id" not in request.args:
        abort(400, description="'id' parameter missing (id of the course)")

    course_id = request.args.get("id")
    
    cookies = {"MoodleSession": request.cookies.get("MoodleSession")}
    r = requests.get(f"{app.config['MOODLE_URL']}/grade/report/user/?id={course_id}", cookies=cookies)
    html = r.text

    soup = BeautifulSoup(html, "html.parser")

    table = soup.find("table", {"class": "user-grade"})

    maxlevel = 1
    clslevel = re.compile(r"level\d+")
    nums = re.compile(r"\d+$")
    for grade in table.find("tbody").find_all("td", {"class": clslevel}):
        lev = int(nums.findall(list(filter(clslevel.match, grade["class"]))[0])[0])
        if lev > maxlevel:
            maxlevel = lev

    grades = []
    for grade in table.find("tbody").find_all("tr"):
        if not grade.select(f".level{maxlevel}") or len(grade.contents) == 1:
            continue

        name = grade.find("th", {"class": "column-itemname"})
        link = name.find("a")
        if not link:
            continue
        ident = link.get("href")
        parsed = urlparse.urlparse(ident)

        content = name.get_text()
        val = grade.find("td", {"class": "column-grade"}).get_text()
        ranges = grade.find("td", {"class": "column-range"}).get_text()
        grades += [{"id": int(urlparse.parse_qs(parsed.query)['id'][0]), "name": content, "range": ranges, "grade": val}]

    return {"items": grades}

@app.errorhandler(404)
def not_found(error):
    return make_response({"status": "error", "error": "Resource not found"}, 404)

@app.errorhandler(400)
def bad_request(error):
    return make_response({"status": "error", "error": str(error)}, 400)

@app.errorhandler(401)
def bad_request(error):
    return make_response({"status": "error", "error": str(error)}, 401)

if __name__ == "__main__":
    app.run(debug=True)
