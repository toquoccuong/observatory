import os
import platform
import subprocess
import time

from flask import Flask, jsonify, request, send_from_directory
from werkzeug.utils import secure_filename
from observatory import queries, sink, archive, settings

RELATIVE_STATIC_DIR = os.path.join('clientapp', 'build')

app = Flask(__name__, static_folder='clientapp')

STATIC_DIR = os.path.join(app.root_path, RELATIVE_STATIC_DIR)


def with_generic_errorhandling(handler):
    """
    This generates a functions that generates a default error response when
    the handler unsuccesfully handles the request.

    Parameters:
    -----------
    handler : object
        The function that handles the request

    Returns:
    --------
    object
        A function that produces a standard HTTP 500 error response when the incoming request
        could not be handled by the provided request handler.
    """

    try:
        return handler()
    except Exception as ex:
        print("Failed to handle request", ex)
        return jsonify({'status': 'failed', 'message': 'Failed to process request'}), 500


def with_default_accepted_response(handler):
    """
    Generates a function that will produce a default accepted 
    response when the handler succesfully runs.

    Parameters:
    -----------
    handler : object
        The function that handles the request.

    Returns:
    --------
    object
        A function that produces a default HTTP 201 response when the 
        request handler succesfully handled the incoming request.
    """
    def request_handler():
        handler()
        return jsonify({'status': 'success'}), 201

    return request_handler


@app.route('/api/models')
def serve_models():
    """
    Serves a list of versions for a particular model

    Returns:
    --------
    object
        The response containing a paged list of versions
        The response contains the following properties:

         - data : list of experiments
         - page_index : int
         - page_size : int
         - total_items : int

        Each element in the data property will contain the following properties:

         - model : str
         - date_created : str
    """
    def models_handler():
        page_index = int(request.args.get("page", default=0))
        return jsonify(queries.find_models(page_index).__dict__)

    return with_generic_errorhandling(models_handler)


@app.route('/api/models/<string:model>/versions')
def serve_versions(model):
    """
    Serves a list of versions for a particular model

    Parameters:
    -----------
    model : str
        The name of the model

    Returns:
    --------
    object
        The response containing a paged list of versions
        The response contains the following properties:

         - data : list of experiments
         - page_index : int
         - page_size : int
         - total_items : int

        Each element in the data property will contain the following properties:

         - model : str
         - version : int
         - date_created : str
    """
    def versions_handler():
        page_index = int(request.args.get("page", default=0))
        return jsonify(queries.find_versions(model, page_index).__dict__)

    return with_generic_errorhandling(versions_handler)


@app.route('/api/models/<string:model>/versions/<int:version>/experiments')
def serve_experiments(model, version):
    """
    Serves a list of experiments for a specific model version

    Parameters:
    -----------
    model : str
        The name of the model
    version : int
        The version number of the model

    Returns
    -------
    object
        The response containing a paged list of experiments.
        The response contains the following properties:

         - data : list of experiments
         - page_index : int
         - page_size : int
         - total_items : int

        Each element in the data property will contain the following properties:

         - model : str
         - version : int
         - experiment : str
         - date_created : str
    """
    def experiments_handler():
        page_index = int(request.args.get("page", default=0))
        return jsonify(queries.find_experiments(model, version, page_index).__dict__)

    return with_generic_errorhandling(experiments_handler)


@app.route('/api/models/<string:model>/versions/<int:version>/experiments/<string:experiment>/runs')
def serve_runs(model, version, experiment):
    """
    Serves a list of all runs for a given experiment

    Parameters:
    -----------
    model : str
        The name of the model
    version : int
        The version of the model
    experiment : str
        The name of the experiment

    Returns:
    --------
    object
        The response containing a paged list of experiments.
            The response contains the following properties:

            - data : list of runs
            - page_index : number
            - page_size : number
            - total_items : number

            Each element in the data property will contain the following properties:

            - model : str
            - version : int
            - run_id : str
            - date_created : str
    """
    def runs_handler():
        page_index = int(request.args.get("page", default=0))
        return jsonify(queries.find_runs(model, version, experiment, page_index).__dict__)

    return with_generic_errorhandling(runs_handler)


@app.route('/api/models/<string:model>/versions/<int:version>/experiments/<string:experiment>/runs/<string:run_id>/archive', methods=['GET'])
def serve_model_data(model, version, experiment, run_id):
    """
    Allows clients to download all assets of a specific model.

    The download is a tar.gz archive that the client needs to extract in order to use the model data.
    By default the downloaded tarball contains the outputs, settings and some metadata about the model.

    Parameters:
    -----------
    model : str
        The name of the model
    version : int
        The version of the model
    experiment : str
        The name of the experiment
    run_id : str
        The ID of the run

    Returns:
    --------
    obj
        The HTTP response containing the model data.
    """

    if not queries.model_data_available(model, version, experiment, run_id):
        return jsonify({ 'message': 'Model data unavailable. Please record outputs and/or settings for your model.'}), 404

    archive_file = archive.create(settings.base_path, model, version, experiment, run_id)
    folder, filename = os.path.split(archive_file)

    return send_from_directory(folder, filename)


@app.route('/api/models/<string:model>/versions/<int:version>/experiments/<string:experiment>/runs', methods=['POST'])
def record_run_start(model, version, experiment):
    """
    Records the start of a new training session.
    This handler expects a JSON payload as the body of the HTTP request with a single field `run_id`

    Parameters:
    -----------
    model : str 
        The name of the model
    version : int
        The version of the model
    experiment : str
        The name of the experiment

    Returns:
    --------
    object
        The HTTP response with status 201 when the session start was sucessfully recorded.
        Otherwise sends 500 response with a generic error message.
    """
    def handle_run_start():
        request_content = request.get_json()

        print('Request payload', request_content)

        sink.record_session_start(
            model, version, experiment,
            request_content['run_id'], int(time.time()))

    return with_generic_errorhandling(with_default_accepted_response(handle_run_start))


@app.route('/api/models/<string:model>/versions/<int:version>/experiments/<string:experiment>/runs/<string:run_id>', methods=['PUT'])
def record_run_completion(model, version, experiment, run_id):
    """
    Records the end of a training session.
    This handler expects a JSON payload as the body of the HTTP request with a single field `status`

    Parameters:
    -----------
    model : str 
        The name of the model
    version : int
        The version of the model
    experiment : str
        The name of the experiment

    Returns:
    --------
    object
        Returns a HTTP response with status 201 when the metric is succesfully recorded.
        Otherwise returns a HTTP response with status 500.
    """
    def handle_run_completion():
        request_content = request.get_json()

        sink.record_session_end(model, version, experiment,
                                run_id, request_content['status'], int(time.time()))

    return with_generic_errorhandling(with_default_accepted_response(handle_run_completion))


@app.route('/api/models/<string:model>/versions/<int:version>/experiments/<string:experiment>/runs/<string:run_id>/metrics', methods=['POST'])
def record_metric(model, version, experiment, run_id):
    """
    Records metrics

    Parameters:
    -----------
    model : str
        The name of the model
    version : int
        The version of the model
    experiment : str
        The name of the experiment
    run_id : str
        The identifier for the run

    Returns:
    --------
    object
        Returns a HTTP response with status 201 when the metric is succesfully recorded.
        Otherwise returns a HTTP response with status 500.
    """
    def tracking_handler():
        request_content = request.get_json()

        metric_name = request_content['name']
        metric_value = request_content['value']

        sink.record_metric(model, version, experiment, run_id, int(
            time.time()), metric_name, metric_value)

    return with_generic_errorhandling(with_default_accepted_response(tracking_handler))


@app.route('/api/models/<string:model>/versions/<int:version>/experiments/<string:experiment>/runs/<string:run_id>/outputs/<filename>', methods=['PUT'])
def record_output(model, version, experiment, run_id, filename):
    """
    Records the output of an experiment run.

    Parameters:
    -----------
    model : str
        The name of the model
    version : int
        The version of the model
    experiment : str
        The name of the experiment
    run_id : str
        The identifier for the run

    Returns:
    --------
    object
        Returns a HTTP response with status 201 when the output is succesfully recorded.
        Otherwise returns a HTTP response with status 500.
    """

    def tracking_handler():
        if 'file' not in request.files:
            return jsonify({'message': 'Missing file in request'}), 400

        file = request.files['file']

        if file.filename == '':
            return jsonify({'message': 'Invalid filename'}), 400

        filename = secure_filename(file.filename)

        sink.record_output(model, version, experiment, run_id, filename, file)

    return with_generic_errorhandling(with_default_accepted_response(tracking_handler))


@app.route('/api/models/<string:model>/versions/<int:version>/experiments/<string:experiment>/runs/<string:run_id>/settings', methods=['POST'])
def record_settings(model, version, experiment, run_id):
    """
    Records settings for an experiment run.

    Parameters:
    -----------
    model : str
        The name of the model
    version : int
        The version of the model
    experiment : str
        The name of the experiment
    run_id : str
        The identifier for the run

    Returns:
    --------
    object
        Returns a HTTP response with status 201 when the settings is succesfully recorded.
        Otherwise returns a HTTP response with status 500.
    """
    def tracking_handler():
        request_content = request.get_json()
        sink.record_settings(model, version, experiment,
                             run_id, request_content)

    return with_generic_errorhandling(with_default_accepted_response(tracking_handler))


@app.route('/static/<path:path>')
def serve_static_file(path):
    """
    Serves static resources from the application
    """
    relative_file_path = os.path.join('static', os.path.normpath(path))
    absolute_file_path = os.path.join(STATIC_DIR, relative_file_path)

    if not os.path.exists(absolute_file_path):
        print("Warning! Could not find file", absolute_file_path)
        return jsonify({'message': 'File not found'}), 404

    folder, filename = os.path.split(absolute_file_path)

    return send_from_directory(folder, filename)


@app.route('/')
def serve_index():
    """
    Serves the index.html file from the root of the website
    """
    return send_from_directory(STATIC_DIR, 'index.html')


def run_server(host='[::]', port=8000, es_nodes=None):
    """
    Runs the HTTP server for tracking and the dashboard.

    The dashboard will serve a single page application that visualizes models, experiments and runs.
    You can use it to explore metrics and download models to your computer as an archive.

    The API of the dashboard uses elasticsearch to track and find information about the models, experiments and runs.

    Parameters
    ----------
    host : str
        The hostname to bind on, default '[::]'
    port : int
        The port to bind on, default 8000
    es_nodes: [string]
        The list of elasticsearch nodes to connect to

    Returns
    -------
    int
        The exit code for the server process.
    """
    if es_nodes is None:
        es_nodes = ['localhost']

    queries.configure(es_nodes)
    sink.configure(es_nodes)

    # Gunicorn is a webserver that has a much better performance than plain Flask.
    # However it is not support on Windows and I want this thing to work on Windows too.
    # So despite that this should be cross-platform, I'm going to find out where I'm running
    # and switch between crappy flask and awesome gunicorn :(
    if platform.system() != 'Windows':
        bind_address = '{}:{}'.format(host, port)

        server_process = subprocess.Popen(
            ['gunicorn', '-b', bind_address, '-w',
                '10', 'observatory.dashboard:app'],
            env=os.environ.copy(),
            stdout=subprocess.PIPE,
            stdin=subprocess.PIPE,
            cwd=app.root_path, universal_newlines=True)

        exit_code = server_process.wait()

        return exit_code
    else:
        app.run(host, port)
