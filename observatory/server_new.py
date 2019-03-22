# Temporary name
from flask import Flask
import werkzeug
from flask_restful import Api, Resource, reqparse, request
from flask_jsonpify import jsonify
from werkzeug import datastructures, secure_filename
from observatory.sink import Sink

sink = Sink()
app = Flask(__name__)
api = Api(app)


class start(Resource):
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
        parser = reqparse.RequestParser()
        parser.add_argument('file', type=datastructures.FileStorage,
                            location='files')
        parser.add_argument("model")
        args = parser.parse_args()

        print(args['file'])

        try:
            pass
            # sink.record_output(args["model"], run)
        except Exception as e:
            return {'status': 'failure'}, 500
        return {'status': 'succes'}, 201

    def delete(self, ID):
        return 500

api.add_resource(Model, "/api/models/<string:model>")
api.add_resource(Metric, "/api/metrics/<string:run>")
api.add_resource(Setting, "/api/settings/<string:run>")
api.add_resource(Output, "/api/output/<string:run>")
app.run(debug=True)
