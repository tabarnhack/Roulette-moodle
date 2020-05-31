import requests
from bs4 import BeautifulSoup
from flask import Flask, request, abort, make_response
from flask_cors import CORS

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


@app.route('/grade', methods=["GET"])
def grade():
    if "MoodleSession" not in request.cookies:
        abort(401, description="You must first login via /login")

    if "id" not in request.args:
        abort(400, description="'id' parameter missing (id of the course)")

    course_id = request.args.get("id")
    
    cookies = {"MoodleSession": request.cookies.get("MoodleSession")}
    r = requests.get(f"{app.config['MOODLE_URL']}/grade/report/user/index.php?id={course_id}", cookies=cookies)
    html = r.text

    soup = BeautifulSoup(html, "html.parser")
    table_text = soup.find("table", {"class": "user-grade"}).text

    table = soup.find("table", {"class": "user-grade"})

    headers = [header["class"][-1].split('-')[-1] for header in table.select("thead tr th")]

    results = [{headers[headers.index(cell["class"][-1].split('-')[-1])]: cell.text for cell in row.find_all(["th", "td"])} for row in table.select("tbody tr")[1:-1]]

    return {"items": results}

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
