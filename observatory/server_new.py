# Temporary name
from flask import Flask, flash, request, redirect, url_for
import werkzeug
from flask_restful import Api, Resource, reqparse, request
from flask_jsonpify import jsonify
from werkzeug import datastructures, secure_filename
from observatory.sink import Sink
import os
from os.path import expanduser

UPLOAD_FOLDER = expanduser('~') + '\\.observatory\\outputs'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'pkl'])

sink = Sink()
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
api = Api(app)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


class Start(Resource):
    def post(self, run):
        # ? sink.record_start_run ???????
        return 500


class End(Resource):
    def post(self, run):
        # ? sink.record_start_run ???????
        return 500


class Model(Resource):
    def get(self, name):
        # querries.getByName()
        return 500

    def post(self, name):
        # ? sink.record_start_run ???????
        pass

    def delete(self, name):
        return 500


class Version(Resource):

    def get(self, ID):
        return 500

    def delete(self, ID):
        return 500


class Experiment(Resource):

    def get(self, name):
        return 500

    def delete(self, name):
        return 500


class Run(Resource):

    def get(self, ID):
        return 500

    def delete(self, ID):
        return 500


class Metric(Resource):

    def get(self, ID):
        return 500

    def post(self, run):
        parser = reqparse.RequestParser()
        parser.add_argument("model")
        parser.add_argument("run")
        parser.add_argument("name")
        parser.add_argument("value")
        args = parser.parse_args()

        try:
            sink.record_metric(args["model"], run, args["name"], args["value"])
            pass
        except Exception as e:
            return {'status': 'failure'}, 500
        return {'status': 'success'}, 201

    def delete(self, ID):
        return 500


class Setting(Resource):

    def get(self, ID):
        return 500

    def post(self, run):
        parser = reqparse.RequestParser()
        parser.add_argument("model")
        parser.add_argument("version")
        parser.add_argument("experiment")
        parser.add_argument("settings")
        args = parser.parse_args()

        try:
            sink.record_settings(args["model"], args["version"], +
                                 args["experiment"], run, args["settings"])
        except Exception as e:
            return {'status': 'failure'}, 500
        return {'status': 'succes'}, 201

    def delete(self, ID):
        return 500


class Output(Resource):

    def get(self, ID):
        return 500

    def post(self, run):
        if 'file' not in request.files:
            flash('No file part')
            return {'status': 'failure', 'context': 'File was not found'}, 500
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return {'status': 'failure', 'context': 'No valid file name'}, 500
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return {'status': 'succes'}, 201
        else:
            return {'status': 'failure', 'context': 'File type not allowed'}, 500

    def delete(self, ID):
        return 500

api.add_resource(Model, "/api/models/<string:model>")
api.add_resource(Metric, "/api/metrics/<string:run>")
api.add_resource(Setting, "/api/settings/<string:run>")
api.add_resource(Output, "/api/output/<string:run>")
app.run(debug=True)
