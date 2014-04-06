from flask import Flask, redirect
app = Flask(__name__)

import pprint
import pytumblr
from cStringIO import StringIO
from pymongo import MongoClient
from bson.binary import Binary
from pytumblr.helpers import validate_params, validate_blogname
from pytumblr.request import TumblrRequest
import datetime
import time

mongo_client = MongoClient()
db = mongo_client.pix
coll = db.pictures
tclient = pytumblr.TumblrRestClient(
  '8ZSmieaZyMRctFmzsGCawM7LeO4CGp0nmHHuh80eE1zS5BhQzD',
  '3PjroUjOTMXMZCsusRk0k04kOEIwbVW4DcDwsBI2an3d3DRquh',
  '8emSmQ98bCuTSchGpNfwV0AbY0t5DQ7BjGxANImWTmID422qhV',
  'd9KYyL99stpokakHNu2DIKbKKDUkc3jkwBrpphl6WpuQZIdNEm'
)
blogname = "qrscanner.tumblr.com"

@app.route('/')
def hello_world():
    return redirect("http://%s" % (blogname)

@app.route('/qr/<when>')
def qr(when):
    print "trying to get" + when
    if datetime.datetime.now() - datetime.datetime.strptime(when, "%Y-%m-%d-%H-%M-%S") < datetime.timedelta(seconds=4):
        time.sleep(4000)
    try:
        rec = coll.find({"time" : when})[0]
    except IndexError:
        return "hello"
    if rec.has_key("tumblr_id"):
        return redirect("http://%s/%s" % (blogname, rec["tumblr_id"]))

    params = {"type": "photo"}
    url = "/v2/blog/%s/post" % blogname
    params.update({'api_key': tclient.request.consumer.key})
    files = [('data', str(rec["time"]) + ".jpg", str(rec["picture"]))]
    response = tclient.request.post(url, params, files)
    rec["tumblr_id"] =  response["id"]
    coll.save(rec)
    return redirect("http://%s/%s" % (blogname, rec["tumblr_id"]))




if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)