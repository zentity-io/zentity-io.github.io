[Home](/) / Sandbox


# <a name="sandbox"></a>Sandbox

**zentity sandbox** is an Elasticsearch development environment preloaded with
zentity, analysis plugins, data sets, and sample entity models. Download it,
run it, and play with zentity using real data in minutes.

> Questions or feedback? [Submit an issue](https://github.com/zentity-io/zentity-sandbox/issues) on Github.


## <a name="get-started"></a>Get started


**Step 1. Download**

- **Windows**: [sandbox-zentity-{$ sandbox.zentity $}-elasticsearch-{$ sandbox.elasticsearch $}-windows.zip](https://drive.google.com/uc?id=1fk4w-tuU0c0Ktaa0ZW-6T5iv5B5g-zmj) (2.5GB Compressed, 3.5GB Uncompressed)
- **Mac**: [sandbox-zentity-{$ sandbox.zentity $}-elasticsearch-{$ sandbox.elasticsearch $}-mac.tar.gz](https://drive.google.com/uc?id=1lTdF20yrsbMcE4lQ6QydEzXHf5VdqCoA) (2.5GB Compressed, 3.5GB Uncompressed)
- **Linux**: [sandbox-zentity-{$ sandbox.zentity $}-elasticsearch-{$ sandbox.elasticsearch $}-linux.tar.gz](https://drive.google.com/uc?id=1QJOi1fqqQCtq17JYv6UVfCjXTXpjr88_) (2.5GB Compressed, 3.5GB Uncompressed)


**Step 2. Extract**

Extract the contents of the file and navigate into the `./sandbox-zentity-*` directory.


**Step 3. Start Elasticsearch**

Navigate into the `./elasticsearch-*` directory and run:

- Linux/Mac: `./bin/elasticsearch` 
- Windows: `./bin/elasticsearch.bat`

Elasticsearch will be accessible at [`http://localhost:9200`](http://localhost:9200)


**Step 4. Start Kibana**

Navigate into the `./kibana-*` directory and run:

- Linux/Mac: `./bin/kibana`
- Windows: `./bin/kibana.bat`

Kibana will be accessible at [`http://localhost:5601`](http://localhost:5601)


**Step 5. Verify**

Visit this URL: [http://localhost:9200/_zentity?pretty](http://localhost:9200/_zentity?pretty)

You should see this response:

```javascript
{
  "name": "zentity",
  "description": "Real-time entity resolution for Elasticsearch.",
  "website": "http://zentity.io",
  "version": {
    "zentity": "{$ sandbox.zentity $}",
    "elasticsearch": "{$ sandbox.elasticsearch $}"
  }
}
```


**Step 5: Have fun!**

Consider using the [Kibana Console UI](https://www.elastic.co/guide/en/kibana/current/console-kibana.html),
which makes it easy to submit requests to Elasticsearch and read responses.

[http://localhost:5601/app/kibana#/dev_tools/console](http://localhost:5601/app/kibana#/dev_tools/console)


## <a name="whats-included"></a>What's included


### <a name="plugins"></a>Plugins

The sandbox comes with these plugins installed:

- [zentity](/)
- [analysis-icu](https://www.elastic.co/guide/en/elasticsearch/plugins/current/analysis-icu.html)
- [analysis-phonetic](https://www.elastic.co/guide/en/elasticsearch/plugins/current/analysis-phonetic.html)


### <a name="data"></a>Data

The sandbox comes with these data sets loaded into indices:

**LEIE** - List of health care providers who have been excluded from
federally funded health care programs in the United States for a variety of
reasons, including a conviction for Medicare or Medicaid fraud.

  - Index: **[`zentity_sandbox_leie`](https://github.com/zentity-io/zentity-sandbox/blob/master/templates/zentity_sandbox_leie.json)**
  - Source: [https://oig.hhs.gov/exclusions/exclusions_list.asp](https://oig.hhs.gov/exclusions/exclusions_list.asp)

**NPPES** - Registry of National Provider Identifiers (NPIs) issued to health
care providers who are covered by HIPAA in the United States. NPIs are
required in any HIPAA standard transaction.

  - Index: **[`zentity_sandbox_nppes`](https://github.com/zentity-io/zentity-sandbox/blob/master/templates/zentity_sandbox_nppes.json)**
  - Source: [https://download.cms.gov/nppes/NPI_Files.html](https://download.cms.gov/nppes/NPI_Files.html)

**PECOS Enrollment** - List of health care providers in the United States
who are actively enrolled in Medicare.

  - Index: **[`zentity_sandbox_pecos_enrollment`](https://github.com/zentity-io/zentity-sandbox/blob/master/templates/zentity_sandbox_pecos_enrollment.json)**
  - Source: [https://data.cms.gov/Medicare-Enrollment/Base-Provider-Enrollment-File/ykfi-ffzq](https://data.cms.gov/Medicare-Enrollment/Base-Provider-Enrollment-File/ykfi-ffzq)

**Physician Compare** - List of individual eligible professionals in the
United States that includes information on demographics and Medicare quality
program participation.

  - Index: **[`zentity_sandbox_physician_compare`](https://github.com/zentity-io/zentity-sandbox/blob/master/templates/zentity_sandbox_physician_compare.json)**
  - Source: [https://data.cms.gov/Medicare-Enrollment/Base-Provider-Enrollment-File/ykfi-ffzq](https://data.medicare.gov/Physician-Compare/Physician-Compare-National-Downloadable-File/mj5m-pzi6)


### <a name="entity-models"></a>Entity Models

The sandbox comes with these entity models loaded in the `.zentity-models` index:

- **[organization](https://github.com/zentity-io/zentity-sandbox/blob/master/models/organization.json)**
- **[person](https://github.com/zentity-io/zentity-sandbox/blob/master/models/person.json)**

Both entity models represent health care providers. You can use them to discover
more information about a given health care provider in the sample data sets.


## <a name="examples"></a>Examples

Here are some examples you can run in Kibana:

**Blacklist lookup**

Here is an entity that appears in the NPPES registry and LEIE exclusions list
over six hops of queries.

```javascript
POST _zentity/resolution/organization?pretty
{
  "attributes": {
    "id": [ "1497077796" ]
  }
}
```
