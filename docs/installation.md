[Home](/#/) / [Documentation](/#/docs) / Installation


# Installation


## Step 1. Install Elasticsearch

Download: [https://www.elastic.co/downloads/elasticsearch](https://www.elastic.co/downloads/elasticsearch)


## Step 2. Install zentity

Once you have installed Elasticsearch, you can install zentity from a remote URL or a local file.


### Install from remote URL

1. Browse the **[releases](/#/releases)**.
2. Find a release that matches your version of Elasticsearch. Copy the name of the .zip file.
3. Install the plugin using the `elasticsearch-plugin` script that comes with Elasticsearch.

Example:

`elasticsearch-plugin install https://zentity.io/releases/zentity-0.1.1-beta.2-elasticsearch-6.2.3.zip`


### Install from local file

1. Browse the **[releases](/#/releases)**.
2. Find a release that matches your version of Elasticsearch. Download the .zip file.
4. Install the plugin using the `elasticsearch-plugin` script that comes with Elasticsearch.

Example:

`elasticsearch-plugin install file:///path/to/zentity-0.1.1-beta.2-elasticsearch-6.2.3.zip`


## Step 3. Verify installation

**Example request:**

`GET http://localhost:9200/_zentity`

**Example response:**

```javascript
{
  "name": "zentity",
  "description": "Real-time entity resolution for Elasticsearch.",
  "website": "http://zentity.io",
  "version": {
    "zentity": "0.1.1-beta.2",
    "elasticsearch": "6.2.3"
  }
}
```


&nbsp;

----

#### Continue Reading

|&#8249;|[Contents](/#/docs)|[Basic Usage](/#/docs/basic-usage)|&#8250;|
|:---|:---|---:|---:|
|    |    |    |    |
