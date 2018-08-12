Installation
============
There are two parts to the Observatory application. There's the server, which
will keep track of your metrics and there's a module that you need to install
in order to send data to the server.

Install the server
----------------------------------
For the server you need to have `ElasticSearch <https://www.elastic.co/products/elasticsearch>`_ available to you.
On a development workstation you can install this product locally. In a production
scenario I highly recommend dedicating a separate machine to ElasticSearch.

Next, execute these steps to install the code needed to run the server:

 * `git clone https://github.com/wmeints/observatory`
 * `cd observatory`
 * `pip install -r requirements.txt`

Install the python module
---------------------------------
With the server running, execute the following steps to install the python module.

 * `git clone https://github.com/wmeints/observatory`
 * `cd observatory`
 * `python setup.py install`

