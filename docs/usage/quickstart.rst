Quickstart
==========
This guide explains how you can start tracking metrics, outputs
and configuration settings of your machine learning models.

Run the server
--------------
After you've installed the server on your machine, use the following steps
to run the server:

 * Start ElasticSearch (usually execute `bin/elasticsearch` from the ElasticSearch folder)
 * Navigate to the folder where you cloned the repository
 * Start the server with `python -m observatory server`

Track metrics from your application
-----------------------------------
To start tracking data from your machine learning code, use the following example.

.. code-block:: python
    :linenos:

    import observatory

    with observatory.start_run('my_model', 1) as run:
        # TODO: Execute your training process.

        # Record metrics like accuracy, precision, r-square, losses, etc.
        run.record_metric('accuracy', 0.97)

        # Record outputs and give them a name for use later when you want
        # to server the model in a docker container.
        run.record_output('output/model.pkl','model.pkl')

        # Record settings so you can keep track of hyperparameters
        # or other things that you use to configure your model.
        run.record_settings(hidden_layers=2, learning_rate=0.01)

A new run is started with `observatory.start_run`, this is a ContextManager scope,
so the data related to the run is kept together during the run.

Within the scope of a run, execute your regular ML code and start tracking metrics,
output and settings.

Using the metrics
-----------------
The metrics are recorded inside ElasticSearch in the `metrics-<model>` index.
There is no dashboard available yet, if you want to visualize the metrics I can
highly recommend using `Kibana <https://elastic.co/products/kibana>`_.