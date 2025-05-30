import os
import sys
import traceback
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "lib"))
sys.path.append(os.path.dirname(__file__))

import logging

logging.basicConfig(
    filename=os.path.join(os.path.dirname(__file__), "log/flask_debug.log"),
    level=logging.DEBUG
)

from flask import Flask, request, render_template, redirect, url_for, Response
from model.eshop_word import EshopWord
from model.eshop_logic import EshopLogic
from dao.eshop_dao import EshopDAO
from model.eshop import Eshop
from dotenv import load_dotenv
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))


USERNAME = os.environ.get("ESHOP_ADMIN_USER")
PASSWORD = os.environ.get("ESHOP_ADMIN_PASS")
logging.debug(f"USERNAME from .env = {USERNAME}")
logging.debug(f"PASSWORD from .env = {PASSWORD}")

app = Flask(__name__)

@app.errorhandler(Exception)
def handle_exception(e):
    log_path = os.path.join(os.path.dirname(__file__),"log/flask_error.log")
    with open(log_path, "a") as f:
        f.write(traceback.format_exc())
    return "Internal Server Error", 500

def check_auth(username, password):
    logging.debug(f"check_auth: username={username}, expected={USERNAME}")
    logging.debug(f"check_auth: password={password}, expected={PASSWORD}")
    return username == USERNAME and password == PASSWORD

def authenticate():
    return Response(
        'ログインが必要です', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'}
    )

def requires_auth(f):
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth:
            auth_header = request.headers.get("Authorization")
            if auth_header and auth_header.startswith("Basic "):
                import base64
                encoded_credentials = auth_header.split(" ")[1]
                decoded_credentials = base64.b64decode(encoded_credentials).decode("utf-8")
                username, password = decoded_credentials.split(":", 1)
                auth = type("Auth", (object,), {"username": username, "password": password})()

        logging.debug(f"requires_auth: auth={auth}")
        if not auth or not check_auth(auth.username, auth.password):
            logging.debug("認証失敗: ユーザーが認証されませんでした")
            return authenticate()
        return f(*args, **kwargs)
    decorated.__name__ = f.__name__
    return decorated

@app.route("/eshop_search", methods=["GET", "POST"])
def main():
    if request.method == "GET":
        return render_template("view/umain.html", es=None, searchLocation="", searchShop="")
    logging.debug(">>> main() route accessed")

    searchLocation = request.form.get("searchLocation", "")
    searchShop = request.form.get("searchShop", "")
    logging.debug(f"search_location = {searchLocation}")
    logging.debug(f"search_shop = {searchShop}")

    es = EshopWord(search_location=searchLocation, search_shop=searchShop)
    logic = EshopLogic()
    logic.execute(es)

    logging.debug(f"es.list = {es.list}")
    logging.debug(f"es.total_count = {es.total_count}")

    return render_template("view/umain.html", es=es, searchLocation=searchLocation, searchShop=searchShop)

@app.route("/eshop_manage", methods=["GET", "POST"])
@requires_auth
def manage_main():
    dao = EshopDAO()
    msg = None
    if request.method == "POST":
        location = request.form.get("location", "")
        shop = request.form.get("shop", "")
        detail = request.form.get("detail", "")
        dao.insert_one(Eshop(location=location, shop=shop, detail=detail))
        msg = "1件追加しました"
    eshop_list = dao.find_all()
    return render_template("manage/managemain.html", list=eshop_list, msg=msg)

from flup.server.cgi import WSGIServer

if __name__ == "__eshop_search__":
    WSGIServer(app).run()

