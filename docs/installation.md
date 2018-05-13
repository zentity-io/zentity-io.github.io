[Home](/) / [Documentation](/docs) / Installation


# Installation


## Step 1. Install Elasticsearch

Download: [https://www.elastic.co/downloads/elasticsearch](https://www.elastic.co/downloads/elasticsearch)


## Step 2. Install zentity

Once you have installed Elasticsearch, you can install zentity from a remote URL or a local file.


### Install from remote URL

1. Browse the **[releases](/releases)**.
2. Find a release that matches your version of Elasticsearch. Copy the name of the .zip file.
3. Install the plugin using the `elasticsearch-plugin` script that comes with Elasticsearch.

Example:

`elasticsearch-plugin install https://zentity.io/releases/zentity-0.5.0-beta.2-elasticsearch-6.2.4.zip`


### Install from local file

1. Browse the **[releases](/releases)**.
2. Find a release that matches your version of Elasticsearch. Download the .zip file.
4. Install the plugin using the `elasticsearch-plugin` script that comes with Elasticsearch.

Example:

`elasticsearch-plugin install file:///path/to/zentity-0.5.0-beta.2-elasticsearch-6.2.4.zip`


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
    "zentity": "0.5.0-beta.2,
    "elasticsearch": "6.2.4"
  }
}
```

## Installation on Elastic Cloud

[Elastic Cloud](https://www.elastic.co/cloud) is a hosted Elasticsearch service offered by Elastic,
the creators of Elasticsearch and the Elastic Stack. Elastic Cloud supports the usage of custom
Elasticsearch plugins such as zentity.

To install zentity on an Elastic Cloud cluster:

1. Browse the **[releases](/releases)** and download one of the .zip files.
2. Sign into Elastic Cloud and navigate to the [plugins tab](https://cloud.elastic.co/#plugins).
3. Select "This is an installable plugin. (Compiled, not the plugin's source code)".
4. Name the plugin "zentity".
5. Specify the version of your Elasticsearch cluster.
6. Upload the .zip file.
7. Create or restart your cluster. If creating a cluster, select "zentity" under the list of custom plugins.

If you will be creating indices and performing entity resolution with data that has names of people or
companies or other fields that often have data quality challenges, consider also selecting
[analysis-icu](https://www.elastic.co/guide/en/elasticsearch/plugins/current/analysis-icu.html)
and [analysis-phonetic](https://www.elastic.co/guide/en/elasticsearch/plugins/current/analysis-phonetic.html)
from the list of plugins, which can help you index cleaner representations of that data.



&nbsp;

----

#### Continue Reading

|&#8249;|[Contents](/docs)|[Basic Usage](/docs/basic-usage)|&#8250;|
|:---|:---|---:|---:|
|    |    |    |    |
