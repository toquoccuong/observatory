server_url = "http://127.0.0.1:5000/api"
state = "local"


def configure(change_state):
    """
    Configures the observatory environment.
    The following settings can be configured:

    Parameters
    ----------
    url : string
        The URL to connect to for tracking session information
    models_path : string
        The path where models should be stored
    """
    global state

    if change_state == 'local' or 'remote':
        state = change_state
