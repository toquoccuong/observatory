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
app.secret_key = '?secret?'  # this has to change, and be secret
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
api = Api(app)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


class Start(Resource):
    """
    This class is used to group all logic related to the start of a Run

    Arguments:
        Resource flask_restful.Resource -- Represents an abstract RESTful resource

    This class is used to group all logic related to the start of a Run
    """

    def post(self, run):
        """
        This method handles the Post method

        Arguments:
            run {str} -- The ID of a run

        Returns:
            HTTP request -- When the function finishes it wil return a http status.
        """
        # ? sink.record_start_run ???????
        return 500


class End(Resource):
    """
    This class is used to group all logic related to the end of a Run

    Arguments:
        Resource flask_restful.Resource -- Represents an abstract RESTful resource

    """
    def post(self, run):
        """
        This method handles the Post method

        Arguments:
            run {str} -- The ID of a run

        Returns:
            HTTP request -- When the function finishes it wil return a http status.
        """
        # ? sink.record_start_run ???????
        return 500


class Model(Resource):
    """
    This class is used to group all logic related to the Model

    This class only has a get and delete method, because adding just a model
    never happens.

    Arguments:
        Resource flask_restful.Resource -- Represents an abstract RESTful resource

    """
    def get(self, name):
        """
        This method handles the Get method
        It gets all data related to a single model

        Arguments:
            name {str} -- The name of the model

        Returns:
            HTTP request -- When the function finishes it wil return a http status.
        """
        # querries.getByName()
        return 500

    def delete(self, name):
        """
        This method handles the Delete method

        Arguments:
            name {str} -- The name of the model

        Returns:
            HTTP request -- When the function finishes it wil return a http status.
        """
        return 500


class Version(Resource):
    """
    This class is used to group all logic related to the Version

    This class only has a get and delete method, because adding just a Version
    never happens.

    Arguments:
        Resource flask_restful.Resource -- Represents an abstract RESTful resource

    """
    def get(self, ID):
        """
        This method handles the Get method

        Arguments:
            ID {str} -- The version ID

        Returns:
            HTTP request -- When the function finishes it wil return a http status.
        """
        return 500

    def delete(self, ID):
        """
        This method handles the Delete method

        Arguments:
            ID {str} -- The version ID

        Returns:
            HTTP request -- When the function finishes it wil return a http status.
        """
        return 500


class Experiment(Resource):
    """
    This class is used to group all logic related to the Experiment

    This class only has a get and delete method, because adding just an Experiment
    never happens.

    Arguments:
        Resource flask_restful.Resource -- Represents an abstract RESTful resource

    """

    def get(self, name):
        return 500

    def delete(self, name):
        return 500


class Run(Resource):
    """
    This class is used to group all logic related to the Run

    This class only has a get and delete method, because adding just a Run
    never happens.

    Arguments:
        Resource flask_restful.Resource -- Represents an abstract RESTful resource

    """

    def get(self, ID):
        return 500

    def delete(self, ID):
        return 500


class Metric(Resource):
    """
    This class is used to group all logic related to the Metrics of a Run

    This class has no PUT method because updating data never happens

    Arguments:
        Resource flask_restful.Resource -- Represents an abstract RESTful resource

    """

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
    """
    This class is used to group all logic related to the Settings of a Run

    This class has no PUT method because updating data never happens

    Arguments:
        Resource flask_restful.Resource -- Represents an abstract RESTful resource

    """

    def get(self, ID):
        return 500

    def post(self, run):
        parser = reqparse.RequestParser()
        parser.add_argument("model")
        parser.add_argument("version")
        parser.add_argument("experiment")
        parser.add_argument("settings")
        args = parser.parse_args()

        sink.record_settings(args["model"], args["version"], args["experiment"], run, args["settings"])
        return {'status': 'succes'}, 201

    def delete(self, ID):
        return 500


class Output(Resource):
    """
    This class is used to group all logic related to the Output of a Run

    This class has no PUT method because updating data never happens

    Arguments:
        Resource flask_restful.Resource -- Represents an abstract RESTful resource

    """

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
api.add_resource(Version, "/api/versions/<string:id>")
api.add_resource(Experiment, "/api/experiments/<string:name>")
api.add_resource(Metric, "/api/metrics/<string:run>")
api.add_resource(Setting, "/api/settings/<string:run>")
api.add_resource(Output, "/api/output/<string:run>")
app.run(debug=True)
