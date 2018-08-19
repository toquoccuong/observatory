from flask import Flask, send_from_directory, jsonify, request
import os
import subprocess
import platform

from observatory import queries

RELATIVE_STATIC_DIR = os.path.join('clientapp', 'build')

app = Flask(__name__, static_folder='clientapp')

STATIC_DIR = os.path.join(app.root_path, RELATIVE_STATIC_DIR)


@app.route('/api/models')
def serve_models():
    page_index = int(request.args.get("page", default=0))
    return jsonify(queries.find_models(page_index).__dict__)


@app.route('/api/models/<string:model>/versions')
def serve_versions(model):
    page_index = int(request.args.get("page", default=0))
    return jsonify(queries.find_versions(model, page_index).__dict__)


@app.route('/api/models/<string:model>/versions/<int:version>/experiments')
def serve_experiments(model, version):
    page_index = int(request.args.get("page", default=0))
    return jsonify(queries.find_experiments(model, version, page_index).__dict__)


@app.route('/api/models/<string:model>/versions/<int:version>/experiments/<string:experiment>/runs')
def serve_experiments(model, version, experiment):
    page_index = int(request.args.get("page", default=0))
    return jsonify(queries.find_runs(model, version, experiment, page_index).__dict__)


@app.route('/static/<path:path>')
def serve_static_file(path):
    relative_file_path = os.path.join('static', os.path.normpath(path))
    absolute_file_path = os.path.join(STATIC_DIR, relative_file_path)

    if not os.path.exists(absolute_file_path):
        print("Warning! Could not find file", absolute_file_path)
        return jsonify({'message': 'File not found'}), 404

    folder, filename = os.path.split(absolute_file_path)

    return send_from_directory(folder, filename)


@app.route('/')
def serve_index():
    return send_from_directory(STATIC_DIR, 'index.html')


def run_dashboard(host='[::]', port=8000, es_nodes=None):
    """
    Runs the HTTP server for the dashboard.

    The dashboard will serve a single page application that visualizes models, experiments and runs.
    You can use it to explore metrics and download models to your computer as an archive.

    The API of the dashboard uses elasticsearch to find information about the models, experiments and runs.

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

    # Gunicorn is a webserver that has a much better performance than plain Flask.
    # However it is not support on Windows and I want this thing to work on Windows too.
    # So despite that this should be cross-platform, I'm going to find out where I'm running
    # and switch between crappy flask and awesome gunicorn :(
    if platform.system() != 'Windows':
        bind_address = '{}:{}'.format(host, port)

        server_process = subprocess.Popen(
            ['gunicorn', '-b', bind_address, '-w', '10', 'observatory.dashboard:app'],
            env=os.environ.copy(),
            stdout=subprocess.PIPE,
            stdin=subprocess.PIPE,
            cwd=app.root_path, universal_newlines=True)

        exit_code = server_process.wait()

        return exit_code
    else:
        app.run(host, port)
