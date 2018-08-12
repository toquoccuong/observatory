# Observatory
Welcome to the observatory, a solution for tracking your machine learning models.

When working a machine learning model you will find yourself changing hyper parameters, 
code, settings and data all the time. You may even end up choosing a different model alltogether.

Because of the high number of changes it is quite hard to keep track of what you have tried before.
Questions like:

 - Which model is the best for us?
 - How long did it take to train this model last time?
 - Which hyper parameters did I use?
 
 Are quite hard to answer if you're not careful. 
 
 Observatory is a simple solution that allows you to keep track of outputs, 
 metrics and configuration settings of your models.
 
 
## Get started
There are two parts to the Observatory application. There's the server, which
will keep track of your metrics and there's a module that you need to install 
in order to send data to the server.

### Step 1: Install and run the server
For the server you need to have [ElasticSearch](https://www.elastic.co/products/elasticsearch) available to you. 
On a development workstation you can install this product locally. In a production
scenario I highly recommend dedicating a separate machine to ElasticSearch.

Also, make sure that you have python 3.6 or higher installed on your machine.

Next, execute these steps to run the server:

 * `git clone https://github.com/wmeints/observatory`
 * `cd observatory`
 * `pip install -r requirements.txt`
 * `python -m observatory --port 5001 --es-node localhost`
 
### Step 2: Install the python module
With the server running, execute the following steps to install the python module.

 * `git clone https://github.com/wmeints/observatory`
 * `cd observatory`
 * `python setup.py install`
 
### Step 3: Write code
Time to start tracking some metrics! Using the following code you can start tracking your model.

```python
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
```

## Using the metrics gathered by this tool
All metrics and other data is recorded in ElasticSearch indices.
Every model gets its own index `metrics-<model-name>`. This index has two
types of documents:

 - metric - A series of metric values for each experiment/run
 - run - A series of runs that you've executed with timings, etc.

Right now, the observatory tool doesn't contain a dashboard. 
I am planning on building one, but meanwhile I can highly recommend using
[Kibana](https://www.elastic.co/products/kibana). This dashboard tool makes it really easy to visualize all the aspects
of your model.

## Development
Feel free to fork this repository and send me pull requests.
I personally recommend using PyCharm and/or Visual Studio Code for writing code.