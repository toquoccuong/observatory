server_url = "localhost:5001"


def configure(url):
    """
    Configures the observatory environment.
    The following settings can be configured:

    Parameters
    ----------
    url : string
        The URL to connect to for tracking session information
    """
    global server_url

    server_url = url