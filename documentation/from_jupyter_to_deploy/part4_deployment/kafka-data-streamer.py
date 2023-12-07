#!/usr/bin/env python
# coding: utf-8

# This is part of the tutorial https://pathway.com/developers/user-guide/from-jupyter-to-deploy

# In[ ]:


# get_ipython().run_cell_magic('capture', '--no-display', '!pip install pathway\n')


# This is a helper notebook to stream data from CSV to Kafka.

# In[1]:


# Download CSV file by running
# wget -nc https://gist.githubusercontent.com/janchorowski/e351af72ecd8d206a34763a428826ab7/raw/ticker.csv'


# In[2]:


import pathway as pw

fname = "ticker.csv"
schema = pw.schema_from_csv(fname)


# In[3]:


print(schema.generate_class(class_name="DataSchema"))


# In[4]:


# The schema definition is autogenerated
class DataSchema(pw.Schema):
    ticker: str
    open: float
    high: float
    low: float
    close: float
    volume: float
    vwap: float
    t: int
    transactions: int
    otc: str


data = pw.demo.replay_csv(fname, schema=DataSchema, input_rate=1000)


# In[5]:


# TODO: please set appropriate values for KAFKA_ENDPOINT, KAFKA_USERNAME, and KAFKA_PASSWORD
rdkafka_producer_settings = {
    "bootstrap.servers": "kafka:9092",
    "security.protocol": "plaintext",
}

pw.io.kafka.write(data, rdkafka_producer_settings, topic_name="ticker")


# In[6]:


pw.run()
