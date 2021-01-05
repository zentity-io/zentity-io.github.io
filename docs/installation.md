[Home](/) / [Documentation](/docs) / Installation


# <a name="installation"></a>Installation


## <a name="install-elasticsearch"></a>Step 1. Install Elasticsearch

Download and install: [https://www.elastic.co/downloads/elasticsearch](https://www.elastic.co/downloads/elasticsearch)


## <a name="install-zentity"></a>Step 2. Install zentity

Once you have installed Elasticsearch, you can install zentity from a remote URL
or a local file.


### <a name="install-zentity-remote-url"></a>Install from remote URL

1. Browse the [releases](/releases).
2. Find a release that matches your version of Elasticsearch. Copy the name of the .zip file.
3. Install the plugin using the `elasticsearch-plugin` script that comes with Elasticsearch.

Example:

`elasticsearch-plugin install https://zentity.io/releases/zentity-{$ latest.zentity $}-elasticsearch-{$ latest.elasticsearch $}.zip`


### <a name="install-zentity-local-file"></a>Install from local file

1. Browse the [releases](/releases).
2. Find a release that matches your version of Elasticsearch. Download the .zip file.
4. Install the plugin using the `elasticsearch-plugin` script that comes with Elasticsearch.

Example:

`elasticsearch-plugin install file:///path/to/zentity-{$ latest.zentity $}-elasticsearch-{$ latest.elasticsearch $}.zip`


## <a name="verify-installation"></a>Step 3. Verify installation

**Example Request**

`GET http://localhost:9200/_zentity`

**Example Response**

```javascript
{
  "name": "zentity",
  "description": "Real-time entity resolution for Elasticsearch.",
  "website": "http://zentity.io",
  "version": {
    "zentity": "{$ latest.zentity $}",
    "elasticsearch": "{$ latest.elasticsearch $}"
  }
}
```

## <a name="run-setup"></a>Step 4. Invoke the Setup API (Optional)

The [Setup API](/docs/rest-apis/setup-api) creates the `.zentity-models` index.
This is optional to invoke because zentity will create the index if it doesn't
already exist upon invoking the [Models API](/docs/rest-apis/models-api).

**Example Request**

`POST http://localhost:9200/_zentity/_setup`

**Example Response**

```javascript
{
  "acknowledged": true
}
```

## <a name="installation-elasticsearch-service"></a>Installation on Elasticsearch Service

[Elasticsearch Service](https://www.elastic.co/products/elasticsearch/service)
is a hosted service offered by Elastic, the creators of Elasticsearch and the
Elastic Stack. Elasticsearch Service supports the usage of custom Elasticsearch
plugins such as zentity.

To install zentity on an Elasticsearch Service deployment:

1. Browse the [releases](/releases) and download one of the .zip files.
2. [Sign in](https://cloud.elastic.co/) to Elasticsearch Service.
3. Navigate to the [Extensions](https://cloud.elastic.co/extensions) tab.
4. Click the "Create Extension" button.
5. Name the extension "zentity" or anything else.
6. Specify the version of your Elasticsearch deployment.
7. Under plugin type, select "An installable plugin (Compiled, no source code)".
8. Click the "Create plugin" button.
9. Upload the .zip file under the "Plugin file" section.
10. Create or restart your deployment. If creating a deployment, select the zentity extension under the list of custom plugins.

If you will be creating indices and performing entity resolution with data that
has names of people or companies or other fields that often have data quality
challenges, consider also selecting [analysis-icu](https://www.elastic.co/guide/en/elasticsearch/plugins/current/analysis-icu.html)
and [analysis-phonetic](https://www.elastic.co/guide/en/elasticsearch/plugins/current/analysis-phonetic.html)
from the list of plugins, which can help you index cleaner representations of
that data.

> **Important**
>
> Amazon's Elasticsearch Service does not let you install community plugins.
> You will need to use the official Elasticsearch Service offered by Elastic.
> You can [compare the services](https://www.elastic.co/aws-elasticsearch-service#aws-elasticsearch-service:-amazon-vs.-elastic)
> and then learn [how to migrate from AWS to Elastic](https://www.elastic.co/blog/migrating-from-aws-elasticsearch-to-elasticsearch-service-on-elastic-cloud).


## <a name="sandbox"></a>Sandbox

Just learning? Want to learn faster? Download and run the **[zentity sandbox](/sandbox)**
development environment, which bundles Elasticsearch with zentity, analysis
plugins, real data, and sample entity models.


&nbsp;

----

#### Continue Reading

|&#8249;|[Contents](/docs)|[Basic Usage](/docs/basic-usage)|&#8250;|
|:---|:---|---:|---:|
|    |    |    |    |
