server_url = "http://localhost:5001"
base_path = './models'


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
    global base_path

    server_url = url
    base_path = models_path
