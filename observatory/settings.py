server_url = "http://127.0.0.1:5000/api"


def configure(url, models_path):
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
    global server_url

    server_url = url
