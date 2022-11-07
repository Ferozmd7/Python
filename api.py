import gitlab
import os
from pathlib import Path
import git
from git import Repo
import shutil
import subprocess
from os import environ
from os import environ as env
from flask import Flask, request, render_template,send_file
from jinja2 import Template
from jinja2 import Environment, FileSystemLoader
from flask import Flask, jsonify, request

from flask_autoindex import AutoIndex


ppath = "/home/feroz/test/templates/" # update your own parent directory here

app = Flask(__name__)
AutoIndex(app, browse_root=ppath)

@app.route('/', methods = ['GET', 'POST'])
def home():
    if(request.method == 'GET'):

        msg = "use curl http://localhost:5000/help"
        return jsonify({'msg': msg})


@app.route('/help', methods = ['GET', 'POST'])
def help():
    if(request.method == 'GET'):
        data = " with rendering [ wget -O http://localhost:5000/{folder}/{file_name}/{user}/{pass} ]"
        data1 = " with render [ wget http://localhost/{folder}/{file_name} ]"
        return jsonify({'command': data},{'command': data1})
        
        
@app.route('/<path:req_path>')
def without_render(req_path):
    BASE_DIR = '/home/feroz/test/templates/'
    subprocess.call(["git", "pull","--recurse-submodules","git@gitlab:ferozmohammad/test.git"],cwd=BASE_DIR)
    # Joining the base and the requested path
    abs_path = os.path.join(BASE_DIR, req_path)
    if os.path.isfile(abs_path):
       return send_file(abs_path)

@app.route('/<path:req_path>/<name>/<ps>', methods=['POST','GET'])
def with_render(req_path,name,ps):
    BASE_DIR = '/home/feroz/test/templates/'
    subprocess.call(["git", "pull","--recurse-submodules","git@gitlab:ferozmohammad/test.git"],cwd=BASE_DIR)
    # Joining the base and the requested path
    abs_path = os.path.join(BASE_DIR, req_path)
    env = Environment( loader = FileSystemLoader('templates'))
    myTemplate = env.get_template(req_path)
    return myTemplate.render(name=name,ps=ps)

     
    if os.path.isfile(abs_path):
       return send_file(abs_path)
    

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=5000)

