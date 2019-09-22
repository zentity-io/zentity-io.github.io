[Home](/) / Sandbox


# <a name="sandbox"></a>Sandbox

**zentity sandbox** is an Elasticsearch development environment preloaded with
zentity, analysis plugins, data sets, and sample entity models. Download it,
run it, and play with zentity using real data in minutes.

> Questions or feedback? [Submit an issue](https://github.com/zentity-io/zentity-sandbox/issues) on Github.


## <a name="get-started"></a>Get started


**Step 1. Download**

- **Windows**: [sandbox-zentity-{$ sandbox.zentity $}-elasticsearch-{$ sandbox.elasticsearch $}-windows.zip](https://drive.google.com/uc?id=1m_CtKyn3Ml49ChQ-tSbEdcymsqexVeBj) (2.5GB Compressed, 3.5GB Uncompressed)
- **Mac**: [sandbox-zentity-{$ sandbox.zentity $}-elasticsearch-{$ sandbox.elasticsearch $}-mac.tar.gz](https://drive.google.com/uc?id=1cdXRoA0MbmuwmeiRjbdr86mgRRmbCNkK) (2.5GB Compressed, 3.5GB Uncompressed)
- **Linux**: [sandbox-zentity-{$ sandbox.zentity $}-elasticsearch-{$ sandbox.elasticsearch $}-linux.tar.gz](https://drive.google.com/uc?id=1fwclmqBPjtTBfwt8af95uH5Cf-9TxQl5) (2.5GB Compressed, 3.5GB Uncompressed)


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


### <a name="examples-blacklist-lookup"></a>Blacklist lookup

Here is an entity that appears in the NPPES registry and LEIE exclusions list
over three hops.

**Request**

```javascript
POST _zentity/resolution/organization?pretty&_source=false
{
  "attributes": {
    "id": [ "1497077796" ]
  }
}
```

**Response**

```javascript
{
  "took" : 130,
  "hits" : {
    "total" : 6,
    "hits" : [ {
      "_index" : "zentity_sandbox_leie",
      "_type" : "_doc",
      "_id" : "AmAfGG0Bh4qDFJrXNuqc",
      "_hop" : 0,
      "_query" : 0,
      "_attributes" : {
        "city" : [ "MINNEAPOLIS" ],
        "id" : [ "1497077796" ],
        "name" : [ "CLINICAL SUPPORT SERVICES, LLC" ],
        "postal_code" : [ "55401" ],
        "state" : [ "MN" ],
        "street" : [ "207 5TH AVENUE, N" ]
      }
    }, {
      "_index" : "zentity_sandbox_nppes",
      "_type" : "_doc",
      "_id" : "OpArGG0Bh4qDFJrXHfxg",
      "_hop" : 0,
      "_query" : 1,
      "_attributes" : {
        "city" : [ "CHANHASSEN" ],
        "id" : [ "1497077796" ],
        "name" : [ "COMPLEMENTARY SUPPORT SERVICES" ],
        "phone" : [ "6122035257" ],
        "postal_code" : [ "553177413" ],
        "state" : [ "MN" ],
        "street" : [ "2345 STONE CREEK LN W" ]
      }
    }, {
      "_index" : "zentity_sandbox_leie",
      "_type" : "_doc",
      "_id" : "DWAfGG0Bh4qDFJrXNebG",
      "_hop" : 1,
      "_query" : 0,
      "_attributes" : {
        "city" : [ "MINNEAPOLIS" ],
        "id" : [ "1023093473" ],
        "name" : [ "COMPLEMENTARY SUPPORT SERVICES" ],
        "postal_code" : [ "55423" ],
        "state" : [ "MN" ],
        "street" : [ "6701 PENN AVENUE, S, STE 301" ]
      }
    }, {
      "_index" : "zentity_sandbox_nppes",
      "_type" : "_doc",
      "_id" : "t2UiGG0Bh4qDFJrX9KFU",
      "_hop" : 2,
      "_query" : 1,
      "_attributes" : {
        "city" : [ "RICHFIELD" ],
        "id" : [ "1023093473" ],
        "name" : [ "COMPLEMENTARY SUPPORT SERVICES" ],
        "phone" : [ "9526088403" ],
        "postal_code" : [ "554232093" ],
        "state" : [ "MN" ],
        "street" : [ "6701 PENN AVE S" ]
      }
    }, {
      "_index" : "zentity_sandbox_nppes",
      "_type" : "_doc",
      "_id" : "F28kGG0Bh4qDFJrX1qdK",
      "_hop" : 2,
      "_query" : 1,
      "_attributes" : {
        "city" : [ "RICHFIELD" ],
        "id" : [ "1174537823" ],
        "name" : [ "COMPLEMENTARY SUPPORT SERVICES" ],
        "phone" : [ "9528951730" ],
        "postal_code" : [ "554232093" ],
        "state" : [ "MN" ],
        "street" : [ "6701 PENN AVE S" ]
      }
    }, {
      "_index" : "zentity_sandbox_leie",
      "_type" : "_doc",
      "_id" : "iWAfGG0Bh4qDFJrXNeLB",
      "_hop" : 3,
      "_query" : 0,
      "_attributes" : {
        "city" : [ "MINNEAPOLIS" ],
        "id" : [ "1174537823" ],
        "name" : [ "CSS METRO, LLC" ],
        "postal_code" : [ "55401" ],
        "state" : [ "MN" ],
        "street" : [ "207 5TH AVENUE, N" ]
      }
    } ]
  }
}
```


#### <a name="examples-blacklist-lookup-explanation"></a>Why did they match?

You can learn why each document matched using the `_explanation` parameter.
This will include an explanation for each matching document.

**Request**

```javascript
POST _zentity/resolution/organization?pretty&_source=false&_explanation=true
{
  "attributes": {
    "id": [ "1497077796" ]
  }
}
```

**Response**

```javascript
{
  "took" : 159,
  "hits" : {
    "total" : 6,
    "hits" : [ {
      "_index" : "zentity_sandbox_leie",
      "_type" : "_doc",
      "_id" : "AmAfGG0Bh4qDFJrXNuqc",
      "_hop" : 0,
      "_query" : 0,
      "_attributes" : {
        "city" : [ "MINNEAPOLIS" ],
        "id" : [ "1497077796" ],
        "name" : [ "CLINICAL SUPPORT SERVICES, LLC" ],
        "postal_code" : [ "55401" ],
        "state" : [ "MN" ],
        "street" : [ "207 5TH AVENUE, N" ]
      },
      "_explanation" : {
        "resolvers" : {
          "id" : {
            "attributes" : [ "id" ]
          }
        },
        "matches" : [ {
          "attribute" : "id",
          "target_field" : "npi",
          "target_value" : "1497077796",
          "input_value" : "1497077796",
          "input_matcher" : "term",
          "input_matcher_params" : { }
        } ]
      }
    }, {
      "_index" : "zentity_sandbox_nppes",
      "_type" : "_doc",
      "_id" : "OpArGG0Bh4qDFJrXHfxg",
      "_hop" : 0,
      "_query" : 1,
      "_attributes" : {
        "city" : [ "CHANHASSEN" ],
        "id" : [ "1497077796" ],
        "name" : [ "COMPLEMENTARY SUPPORT SERVICES" ],
        "phone" : [ "6122035257" ],
        "postal_code" : [ "553177413" ],
        "state" : [ "MN" ],
        "street" : [ "2345 STONE CREEK LN W" ]
      },
      "_explanation" : {
        "resolvers" : {
          "id" : {
            "attributes" : [ "id" ]
          }
        },
        "matches" : [ {
          "attribute" : "id",
          "target_field" : "number",
          "target_value" : "1497077796",
          "input_value" : "1497077796",
          "input_matcher" : "term",
          "input_matcher_params" : { }
        } ]
      }
    }, {
      "_index" : "zentity_sandbox_leie",
      "_type" : "_doc",
      "_id" : "DWAfGG0Bh4qDFJrXNebG",
      "_hop" : 1,
      "_query" : 0,
      "_attributes" : {
        "city" : [ "MINNEAPOLIS" ],
        "id" : [ "1023093473" ],
        "name" : [ "COMPLEMENTARY SUPPORT SERVICES" ],
        "postal_code" : [ "55423" ],
        "state" : [ "MN" ],
        "street" : [ "6701 PENN AVENUE, S, STE 301" ]
      },
      "_explanation" : {
        "resolvers" : {
          "name_city_state" : {
            "attributes" : [ "city", "name", "state" ]
          }
        },
        "matches" : [ {
          "attribute" : "city",
          "target_field" : "city",
          "target_value" : "MINNEAPOLIS",
          "input_value" : "MINNEAPOLIS",
          "input_matcher" : "match_fuzzy",
          "input_matcher_params" : {
            "fuzziness" : "1"
          }
        }, {
          "attribute" : "name",
          "target_field" : "busname.phonetic",
          "target_value" : "COMPLEMENTARY SUPPORT SERVICES",
          "input_value" : "COMPLEMENTARY SUPPORT SERVICES",
          "input_matcher" : "match",
          "input_matcher_params" : { }
        }, {
          "attribute" : "name",
          "target_field" : "busname",
          "target_value" : "COMPLEMENTARY SUPPORT SERVICES",
          "input_value" : "COMPLEMENTARY SUPPORT SERVICES",
          "input_matcher" : "match_fuzzy_and_initials",
          "input_matcher_params" : {
            "fuzziness" : "1"
          }
        }, {
          "attribute" : "state",
          "target_field" : "state",
          "target_value" : "MN",
          "input_value" : "MN",
          "input_matcher" : "term",
          "input_matcher_params" : { }
        } ]
      }
    }, {
      "_index" : "zentity_sandbox_nppes",
      "_type" : "_doc",
      "_id" : "t2UiGG0Bh4qDFJrX9KFU",
      "_hop" : 2,
      "_query" : 1,
      "_attributes" : {
        "city" : [ "RICHFIELD" ],
        "id" : [ "1023093473" ],
        "name" : [ "COMPLEMENTARY SUPPORT SERVICES" ],
        "phone" : [ "9526088403" ],
        "postal_code" : [ "554232093" ],
        "state" : [ "MN" ],
        "street" : [ "6701 PENN AVE S" ]
      },
      "_explanation" : {
        "resolvers" : {
          "id" : {
            "attributes" : [ "id" ]
          },
          "name_postal_code" : {
            "attributes" : [ "name", "postal_code" ]
          }
        },
        "matches" : [ {
          "attribute" : "id",
          "target_field" : "number",
          "target_value" : "1023093473",
          "input_value" : "1023093473",
          "input_matcher" : "term",
          "input_matcher_params" : { }
        }, {
          "attribute" : "name",
          "target_field" : "basic.organization_name.phonetic",
          "target_value" : "COMPLEMENTARY SUPPORT SERVICES",
          "input_value" : "COMPLEMENTARY SUPPORT SERVICES",
          "input_matcher" : "match",
          "input_matcher_params" : { }
        }, {
          "attribute" : "name",
          "target_field" : "basic.organization_name",
          "target_value" : "COMPLEMENTARY SUPPORT SERVICES",
          "input_value" : "COMPLEMENTARY SUPPORT SERVICES",
          "input_matcher" : "match_fuzzy_and_initials",
          "input_matcher_params" : {
            "fuzziness" : "1"
          }
        }, {
          "attribute" : "postal_code",
          "target_field" : "addresses.location.postal_code",
          "target_value" : "554232093",
          "input_value" : "55423",
          "input_matcher" : "match_fuzzy",
          "input_matcher_params" : {
            "fuzziness" : "1"
          }
        }, {
          "attribute" : "state",
          "target_field" : "addresses.location.state",
          "target_value" : "MN",
          "input_value" : "MN",
          "input_matcher" : "term",
          "input_matcher_params" : { }
        } ]
      }
    }, {
      "_index" : "zentity_sandbox_nppes",
      "_type" : "_doc",
      "_id" : "F28kGG0Bh4qDFJrX1qdK",
      "_hop" : 2,
      "_query" : 1,
      "_attributes" : {
        "city" : [ "RICHFIELD" ],
        "id" : [ "1174537823" ],
        "name" : [ "COMPLEMENTARY SUPPORT SERVICES" ],
        "phone" : [ "9528951730" ],
        "postal_code" : [ "554232093" ],
        "state" : [ "MN" ],
        "street" : [ "6701 PENN AVE S" ]
      },
      "_explanation" : {
        "resolvers" : {
          "name_postal_code" : {
            "attributes" : [ "name", "postal_code" ]
          }
        },
        "matches" : [ {
          "attribute" : "name",
          "target_field" : "basic.organization_name.phonetic",
          "target_value" : "COMPLEMENTARY SUPPORT SERVICES",
          "input_value" : "COMPLEMENTARY SUPPORT SERVICES",
          "input_matcher" : "match",
          "input_matcher_params" : { }
        }, {
          "attribute" : "name",
          "target_field" : "basic.organization_name",
          "target_value" : "COMPLEMENTARY SUPPORT SERVICES",
          "input_value" : "COMPLEMENTARY SUPPORT SERVICES",
          "input_matcher" : "match_fuzzy_and_initials",
          "input_matcher_params" : {
            "fuzziness" : "1"
          }
        }, {
          "attribute" : "postal_code",
          "target_field" : "addresses.location.postal_code",
          "target_value" : "554232093",
          "input_value" : "55423",
          "input_matcher" : "match_fuzzy",
          "input_matcher_params" : {
            "fuzziness" : "1"
          }
        }, {
          "attribute" : "state",
          "target_field" : "addresses.location.state",
          "target_value" : "MN",
          "input_value" : "MN",
          "input_matcher" : "term",
          "input_matcher_params" : { }
        } ]
      }
    }, {
      "_index" : "zentity_sandbox_leie",
      "_type" : "_doc",
      "_id" : "iWAfGG0Bh4qDFJrXNeLB",
      "_hop" : 3,
      "_query" : 0,
      "_attributes" : {
        "city" : [ "MINNEAPOLIS" ],
        "id" : [ "1174537823" ],
        "name" : [ "CSS METRO, LLC" ],
        "postal_code" : [ "55401" ],
        "state" : [ "MN" ],
        "street" : [ "207 5TH AVENUE, N" ]
      },
      "_explanation" : {
        "resolvers" : {
          "id" : {
            "attributes" : [ "id" ]
          }
        },
        "matches" : [ {
          "attribute" : "city",
          "target_field" : "city",
          "target_value" : "MINNEAPOLIS",
          "input_value" : "MINNEAPOLIS",
          "input_matcher" : "match_fuzzy",
          "input_matcher_params" : {
            "fuzziness" : "1"
          }
        }, {
          "attribute" : "id",
          "target_field" : "npi",
          "target_value" : "1174537823",
          "input_value" : "1174537823",
          "input_matcher" : "term",
          "input_matcher_params" : { }
        }, {
          "attribute" : "postal_code",
          "target_field" : "zip",
          "target_value" : "55401",
          "input_value" : "55401",
          "input_matcher" : "match_fuzzy",
          "input_matcher_params" : {
            "fuzziness" : "1"
          }
        }, {
          "attribute" : "state",
          "target_field" : "state",
          "target_value" : "MN",
          "input_value" : "MN",
          "input_matcher" : "term",
          "input_matcher_params" : { }
        }, {
          "attribute" : "street",
          "target_field" : "address",
          "target_value" : "207 5TH AVENUE, N",
          "input_value" : "207 5TH AVENUE, N",
          "input_matcher" : "match_fuzzy",
          "input_matcher_params" : {
            "fuzziness" : "1"
          }
        } ]
      }
    } ]
  }
}
```


#### <a name="examples-blacklist-lookup-queries"></a>What queries were made?

You can see the queries that zentity submitted using the `queries` parameter.

**Request**

```javascript
POST _zentity/resolution/organization?pretty&_source=false&queries=true
{
  "attributes": {
    "id": [ "1497077796" ]
  }
}
```

**Response**

```javascript
{
  "took" : 123,
  "hits" : {
    "total" : 6,
    "hits" : [ {
      "_index" : "zentity_sandbox_leie",
      "_type" : "_doc",
      "_id" : "AmAfGG0Bh4qDFJrXNuqc",
      "_hop" : 0,
      "_query" : 0,
      "_attributes" : {
        "city" : [ "MINNEAPOLIS" ],
        "id" : [ "1497077796" ],
        "name" : [ "CLINICAL SUPPORT SERVICES, LLC" ],
        "postal_code" : [ "55401" ],
        "state" : [ "MN" ],
        "street" : [ "207 5TH AVENUE, N" ]
      }
    }, {
      "_index" : "zentity_sandbox_nppes",
      "_type" : "_doc",
      "_id" : "OpArGG0Bh4qDFJrXHfxg",
      "_hop" : 0,
      "_query" : 1,
      "_attributes" : {
        "city" : [ "CHANHASSEN" ],
        "id" : [ "1497077796" ],
        "name" : [ "COMPLEMENTARY SUPPORT SERVICES" ],
        "phone" : [ "6122035257" ],
        "postal_code" : [ "553177413" ],
        "state" : [ "MN" ],
        "street" : [ "2345 STONE CREEK LN W" ]
      }
    }, {
      "_index" : "zentity_sandbox_leie",
      "_type" : "_doc",
      "_id" : "DWAfGG0Bh4qDFJrXNebG",
      "_hop" : 1,
      "_query" : 0,
      "_attributes" : {
        "city" : [ "MINNEAPOLIS" ],
        "id" : [ "1023093473" ],
        "name" : [ "COMPLEMENTARY SUPPORT SERVICES" ],
        "postal_code" : [ "55423" ],
        "state" : [ "MN" ],
        "street" : [ "6701 PENN AVENUE, S, STE 301" ]
      }
    }, {
      "_index" : "zentity_sandbox_nppes",
      "_type" : "_doc",
      "_id" : "t2UiGG0Bh4qDFJrX9KFU",
      "_hop" : 2,
      "_query" : 1,
      "_attributes" : {
        "city" : [ "RICHFIELD" ],
        "id" : [ "1023093473" ],
        "name" : [ "COMPLEMENTARY SUPPORT SERVICES" ],
        "phone" : [ "9526088403" ],
        "postal_code" : [ "554232093" ],
        "state" : [ "MN" ],
        "street" : [ "6701 PENN AVE S" ]
      }
    }, {
      "_index" : "zentity_sandbox_nppes",
      "_type" : "_doc",
      "_id" : "F28kGG0Bh4qDFJrX1qdK",
      "_hop" : 2,
      "_query" : 1,
      "_attributes" : {
        "city" : [ "RICHFIELD" ],
        "id" : [ "1174537823" ],
        "name" : [ "COMPLEMENTARY SUPPORT SERVICES" ],
        "phone" : [ "9528951730" ],
        "postal_code" : [ "554232093" ],
        "state" : [ "MN" ],
        "street" : [ "6701 PENN AVE S" ]
      }
    }, {
      "_index" : "zentity_sandbox_leie",
      "_type" : "_doc",
      "_id" : "iWAfGG0Bh4qDFJrXNeLB",
      "_hop" : 3,
      "_query" : 0,
      "_attributes" : {
        "city" : [ "MINNEAPOLIS" ],
        "id" : [ "1174537823" ],
        "name" : [ "CSS METRO, LLC" ],
        "postal_code" : [ "55401" ],
        "state" : [ "MN" ],
        "street" : [ "207 5TH AVENUE, N" ]
      }
    } ]
  },
  "queries" : [ [ {
    "_hop" : 0,
    "_query" : 0,
    "_index" : "zentity_sandbox_leie",
    "filters" : {
      "attributes" : {
        "tree" : {
          "0" : {
            "id" : { }
          }
        },
        "resolvers" : {
          "id" : {
            "attributes" : [ "id" ]
          }
        }
      },
      "terms" : null
    },
    "search" : {
      "request" : {
        "_source" : true,
        "query" : {
          "term" : {
            "npi" : "1497077796"
          }
        },
        "size" : 1000
      },
      "response" : {
        "took" : 1,
        "timed_out" : false,
        "_shards" : {
          "total" : 1,
          "successful" : 1,
          "skipped" : 0,
          "failed" : 0
        },
        "hits" : {
          "total" : {
            "value" : 1,
            "relation" : "eq"
          },
          "max_score" : 10.78556
        }
      }
    }
  }, {
    "_hop" : 0,
    "_query" : 1,
    "_index" : "zentity_sandbox_nppes",
    "filters" : {
      "attributes" : {
        "tree" : {
          "0" : {
            "id" : { }
          }
        },
        "resolvers" : {
          "id" : {
            "attributes" : [ "id" ]
          }
        }
      },
      "terms" : null
    },
    "search" : {
      "request" : {
        "_source" : true,
        "query" : {
          "term" : {
            "number" : "1497077796"
          }
        },
        "size" : 1000
      },
      "response" : {
        "took" : 2,
        "timed_out" : false,
        "_shards" : {
          "total" : 1,
          "successful" : 1,
          "skipped" : 0,
          "failed" : 0
        },
        "hits" : {
          "total" : {
            "value" : 1,
            "relation" : "eq"
          },
          "max_score" : 15.217276
        }
      }
    }
  }, {
    "_hop" : 0,
    "_query" : 2,
    "_index" : "zentity_sandbox_pecos_enrollment",
    "filters" : {
      "attributes" : {
        "tree" : {
          "0" : {
            "id" : { }
          }
        },
        "resolvers" : {
          "id" : {
            "attributes" : [ "id" ]
          }
        }
      },
      "terms" : null
    },
    "search" : {
      "request" : {
        "_source" : true,
        "query" : {
          "term" : {
            "npi" : "1497077796"
          }
        },
        "size" : 1000
      },
      "response" : {
        "took" : 2,
        "timed_out" : false,
        "_shards" : {
          "total" : 1,
          "successful" : 1,
          "skipped" : 0,
          "failed" : 0
        },
        "hits" : {
          "total" : {
            "value" : 0,
            "relation" : "eq"
          },
          "max_score" : null
        }
      }
    }
  }, {
    "_hop" : 0,
    "_query" : 3,
    "_index" : "zentity_sandbox_physician_compare",
    "filters" : {
      "attributes" : {
        "tree" : {
          "0" : {
            "id" : { }
          }
        },
        "resolvers" : {
          "id" : {
            "attributes" : [ "id" ]
          }
        }
      },
      "terms" : null
    },
    "search" : {
      "request" : {
        "_source" : true,
        "query" : {
          "term" : {
            "npi" : "1497077796"
          }
        },
        "size" : 1000
      },
      "response" : {
        "took" : 0,
        "timed_out" : false,
        "_shards" : {
          "total" : 1,
          "successful" : 1,
          "skipped" : 0,
          "failed" : 0
        },
        "hits" : {
          "total" : {
            "value" : 0,
            "relation" : "eq"
          },
          "max_score" : null
        }
      }
    }
  }, {
    "_hop" : 1,
    "_query" : 0,
    "_index" : "zentity_sandbox_leie",
    "filters" : {
      "attributes" : {
        "tree" : {
          "0" : {
            "id" : { },
            "name" : {
              "city" : {
                "state" : { }
              },
              "postal_code" : { },
              "street" : { }
            }
          }
        },
        "resolvers" : {
          "id" : {
            "attributes" : [ "id" ]
          },
          "name_city_state" : {
            "attributes" : [ "city", "name", "state" ]
          },
          "name_postal_code" : {
            "attributes" : [ "name", "postal_code" ]
          },
          "name_street" : {
            "attributes" : [ "name", "street" ]
          }
        }
      },
      "terms" : null
    },
    "search" : {
      "request" : {
        "_source" : true,
        "query" : {
          "bool" : {
            "must_not" : {
              "ids" : {
                "values" : [ "AmAfGG0Bh4qDFJrXNuqc" ]
              }
            },
            "filter" : {
              "bool" : {
                "should" : [ {
                  "term" : {
                    "npi" : "1497077796"
                  }
                }, {
                  "bool" : {
                    "filter" : [ {
                      "bool" : {
                        "should" : [ {
                          "bool" : {
                            "should" : [ {
                              "bool" : {
                                "filter" : [ {
                                  "match" : {
                                    "busname" : {
                                      "query" : "CLINICAL SUPPORT SERVICES, LLC",
                                      "fuzziness" : "1"
                                    }
                                  }
                                }, {
                                  "match" : {
                                    "busname.initials" : {
                                      "query" : "CLINICAL SUPPORT SERVICES, LLC",
                                      "fuzziness" : "auto"
                                    }
                                  }
                                } ]
                              }
                            }, {
                              "bool" : {
                                "filter" : [ {
                                  "match" : {
                                    "busname" : {
                                      "query" : "COMPLEMENTARY SUPPORT SERVICES",
                                      "fuzziness" : "1"
                                    }
                                  }
                                }, {
                                  "match" : {
                                    "busname.initials" : {
                                      "query" : "COMPLEMENTARY SUPPORT SERVICES",
                                      "fuzziness" : "auto"
                                    }
                                  }
                                } ]
                              }
                            } ]
                          }
                        }, {
                          "bool" : {
                            "should" : [ {
                              "match" : {
                                "busname.phonetic" : "CLINICAL SUPPORT SERVICES, LLC"
                              }
                            }, {
                              "match" : {
                                "busname.phonetic" : "COMPLEMENTARY SUPPORT SERVICES"
                              }
                            } ]
                          }
                        } ]
                      }
                    }, {
                      "bool" : {
                        "should" : [ {
                          "bool" : {
                            "filter" : [ {
                              "bool" : {
                                "should" : [ {
                                  "match" : {
                                    "city" : {
                                      "query" : "CHANHASSEN",
                                      "fuzziness" : "1"
                                    }
                                  }
                                }, {
                                  "match" : {
                                    "city" : {
                                      "query" : "MINNEAPOLIS",
                                      "fuzziness" : "1"
                                    }
                                  }
                                } ]
                              }
                            }, {
                              "term" : {
                                "state" : "MN"
                              }
                            } ]
                          }
                        }, {
                          "bool" : {
                            "should" : [ {
                              "match" : {
                                "zip" : {
                                  "query" : "553177413",
                                  "fuzziness" : "1"
                                }
                              }
                            }, {
                              "match" : {
                                "zip" : {
                                  "query" : "55401",
                                  "fuzziness" : "1"
                                }
                              }
                            } ]
                          }
                        }, {
                          "bool" : {
                            "should" : [ {
                              "match" : {
                                "address" : {
                                  "query" : "207 5TH AVENUE, N",
                                  "fuzziness" : "1"
                                }
                              }
                            }, {
                              "match" : {
                                "address" : {
                                  "query" : "2345 STONE CREEK LN W",
                                  "fuzziness" : "1"
                                }
                              }
                            } ]
                          }
                        } ]
                      }
                    } ]
                  }
                } ]
              }
            }
          }
        },
        "size" : 1000
      },
      "response" : {
        "took" : 8,
        "timed_out" : false,
        "_shards" : {
          "total" : 1,
          "successful" : 1,
          "skipped" : 0,
          "failed" : 0
        },
        "hits" : {
          "total" : {
            "value" : 1,
            "relation" : "eq"
          },
          "max_score" : 0.0
        }
      }
    }
  }, {
    "_hop" : 1,
    "_query" : 1,
    "_index" : "zentity_sandbox_nppes",
    "filters" : {
      "attributes" : {
        "tree" : {
          "0" : {
            "id" : { },
            "name" : {
              "city" : {
                "state" : { }
              },
              "phone" : { },
              "postal_code" : { },
              "street" : { }
            }
          }
        },
        "resolvers" : {
          "id" : {
            "attributes" : [ "id" ]
          },
          "name_city_state" : {
            "attributes" : [ "city", "name", "state" ]
          },
          "name_phone" : {
            "attributes" : [ "name", "phone" ]
          },
          "name_postal_code" : {
            "attributes" : [ "name", "postal_code" ]
          },
          "name_street" : {
            "attributes" : [ "name", "street" ]
          }
        }
      },
      "terms" : null
    },
    "search" : {
      "request" : {
        "_source" : true,
        "query" : {
          "bool" : {
            "must_not" : {
              "ids" : {
                "values" : [ "OpArGG0Bh4qDFJrXHfxg" ]
              }
            },
            "filter" : {
              "bool" : {
                "should" : [ {
                  "term" : {
                    "number" : "1497077796"
                  }
                }, {
                  "bool" : {
                    "filter" : [ {
                      "bool" : {
                        "should" : [ {
                          "bool" : {
                            "should" : [ {
                              "bool" : {
                                "filter" : [ {
                                  "match" : {
                                    "basic.organization_name" : {
                                      "query" : "CLINICAL SUPPORT SERVICES, LLC",
                                      "fuzziness" : "1"
                                    }
                                  }
                                }, {
                                  "match" : {
                                    "basic.organization_name.initials" : {
                                      "query" : "CLINICAL SUPPORT SERVICES, LLC",
                                      "fuzziness" : "auto"
                                    }
                                  }
                                } ]
                              }
                            }, {
                              "bool" : {
                                "filter" : [ {
                                  "match" : {
                                    "basic.organization_name" : {
                                      "query" : "COMPLEMENTARY SUPPORT SERVICES",
                                      "fuzziness" : "1"
                                    }
                                  }
                                }, {
                                  "match" : {
                                    "basic.organization_name.initials" : {
                                      "query" : "COMPLEMENTARY SUPPORT SERVICES",
                                      "fuzziness" : "auto"
                                    }
                                  }
                                } ]
                              }
                            } ]
                          }
                        }, {
                          "bool" : {
                            "should" : [ {
                              "match" : {
                                "basic.organization_name.phonetic" : "CLINICAL SUPPORT SERVICES, LLC"
                              }
                            }, {
                              "match" : {
                                "basic.organization_name.phonetic" : "COMPLEMENTARY SUPPORT SERVICES"
                              }
                            } ]
                          }
                        } ]
                      }
                    }, {
                      "bool" : {
                        "should" : [ {
                          "bool" : {
                            "filter" : [ {
                              "bool" : {
                                "should" : [ {
                                  "match" : {
                                    "addresses.location.city" : {
                                      "query" : "CHANHASSEN",
                                      "fuzziness" : "1"
                                    }
                                  }
                                }, {
                                  "match" : {
                                    "addresses.location.city" : {
                                      "query" : "MINNEAPOLIS",
                                      "fuzziness" : "1"
                                    }
                                  }
                                } ]
                              }
                            }, {
                              "term" : {
                                "addresses.location.state" : "MN"
                              }
                            } ]
                          }
                        }, {
                          "match" : {
                            "addresses.location.telephone_number" : {
                              "query" : "6122035257",
                              "fuzziness" : "1"
                            }
                          }
                        }, {
                          "bool" : {
                            "should" : [ {
                              "match" : {
                                "addresses.location.postal_code" : {
                                  "query" : "553177413",
                                  "fuzziness" : "1"
                                }
                              }
                            }, {
                              "match" : {
                                "addresses.location.postal_code" : {
                                  "query" : "55401",
                                  "fuzziness" : "1"
                                }
                              }
                            } ]
                          }
                        }, {
                          "bool" : {
                            "should" : [ {
                              "match" : {
                                "addresses.location.address_1" : {
                                  "query" : "207 5TH AVENUE, N",
                                  "fuzziness" : "1"
                                }
                              }
                            }, {
                              "match" : {
                                "addresses.location.address_1" : {
                                  "query" : "2345 STONE CREEK LN W",
                                  "fuzziness" : "1"
                                }
                              }
                            } ]
                          }
                        } ]
                      }
                    } ]
                  }
                } ]
              }
            }
          }
        },
        "size" : 1000
      },
      "response" : {
        "took" : 9,
        "timed_out" : false,
        "_shards" : {
          "total" : 1,
          "successful" : 1,
          "skipped" : 0,
          "failed" : 0
        },
        "hits" : {
          "total" : {
            "value" : 0,
            "relation" : "eq"
          },
          "max_score" : null
        }
      }
    }
  }, {
    "_hop" : 1,
    "_query" : 2,
    "_index" : "zentity_sandbox_pecos_enrollment",
    "filters" : {
      "attributes" : {
        "tree" : {
          "0" : {
            "id" : { }
          }
        },
        "resolvers" : {
          "id" : {
            "attributes" : [ "id" ]
          }
        }
      },
      "terms" : null
    },
    "search" : {
      "request" : {
        "_source" : true,
        "query" : {
          "term" : {
            "npi" : "1497077796"
          }
        },
        "size" : 1000
      },
      "response" : {
        "took" : 0,
        "timed_out" : false,
        "_shards" : {
          "total" : 1,
          "successful" : 1,
          "skipped" : 0,
          "failed" : 0
        },
        "hits" : {
          "total" : {
            "value" : 0,
            "relation" : "eq"
          },
          "max_score" : null
        }
      }
    }
  }, {
    "_hop" : 1,
    "_query" : 3,
    "_index" : "zentity_sandbox_physician_compare",
    "filters" : {
      "attributes" : {
        "tree" : {
          "0" : {
            "id" : { },
            "name" : {
              "city" : {
                "state" : { }
              },
              "phone" : { },
              "postal_code" : { },
              "street" : { }
            }
          }
        },
        "resolvers" : {
          "id" : {
            "attributes" : [ "id" ]
          },
          "name_city_state" : {
            "attributes" : [ "city", "name", "state" ]
          },
          "name_phone" : {
            "attributes" : [ "name", "phone" ]
          },
          "name_postal_code" : {
            "attributes" : [ "name", "postal_code" ]
          },
          "name_street" : {
            "attributes" : [ "name", "street" ]
          }
        }
      },
      "terms" : null
    },
    "search" : {
      "request" : {
        "_source" : true,
        "query" : {
          "bool" : {
            "should" : [ {
              "term" : {
                "npi" : "1497077796"
              }
            }, {
              "bool" : {
                "filter" : [ {
                  "bool" : {
                    "should" : [ {
                      "bool" : {
                        "should" : [ {
                          "bool" : {
                            "filter" : [ {
                              "match" : {
                                "org_nm" : {
                                  "query" : "CLINICAL SUPPORT SERVICES, LLC",
                                  "fuzziness" : "1"
                                }
                              }
                            }, {
                              "match" : {
                                "org_nm.initials" : {
                                  "query" : "CLINICAL SUPPORT SERVICES, LLC",
                                  "fuzziness" : "auto"
                                }
                              }
                            } ]
                          }
                        }, {
                          "bool" : {
                            "filter" : [ {
                              "match" : {
                                "org_nm" : {
                                  "query" : "COMPLEMENTARY SUPPORT SERVICES",
                                  "fuzziness" : "1"
                                }
                              }
                            }, {
                              "match" : {
                                "org_nm.initials" : {
                                  "query" : "COMPLEMENTARY SUPPORT SERVICES",
                                  "fuzziness" : "auto"
                                }
                              }
                            } ]
                          }
                        } ]
                      }
                    }, {
                      "bool" : {
                        "should" : [ {
                          "match" : {
                            "org_nm.phonetic" : "CLINICAL SUPPORT SERVICES, LLC"
                          }
                        }, {
                          "match" : {
                            "org_nm.phonetic" : "COMPLEMENTARY SUPPORT SERVICES"
                          }
                        } ]
                      }
                    } ]
                  }
                }, {
                  "bool" : {
                    "should" : [ {
                      "bool" : {
                        "filter" : [ {
                          "bool" : {
                            "should" : [ {
                              "match" : {
                                "cty" : {
                                  "query" : "CHANHASSEN",
                                  "fuzziness" : "1"
                                }
                              }
                            }, {
                              "match" : {
                                "cty" : {
                                  "query" : "MINNEAPOLIS",
                                  "fuzziness" : "1"
                                }
                              }
                            } ]
                          }
                        }, {
                          "term" : {
                            "st" : "MN"
                          }
                        } ]
                      }
                    }, {
                      "match" : {
                        "phn_numbr" : {
                          "query" : "6122035257",
                          "fuzziness" : "1"
                        }
                      }
                    }, {
                      "bool" : {
                        "should" : [ {
                          "match" : {
                            "zip" : {
                              "query" : "553177413",
                              "fuzziness" : "1"
                            }
                          }
                        }, {
                          "match" : {
                            "zip" : {
                              "query" : "55401",
                              "fuzziness" : "1"
                            }
                          }
                        } ]
                      }
                    }, {
                      "bool" : {
                        "should" : [ {
                          "match" : {
                            "adr_ln_1" : {
                              "query" : "207 5TH AVENUE, N",
                              "fuzziness" : "1"
                            }
                          }
                        }, {
                          "match" : {
                            "adr_ln_1" : {
                              "query" : "2345 STONE CREEK LN W",
                              "fuzziness" : "1"
                            }
                          }
                        } ]
                      }
                    } ]
                  }
                } ]
              }
            } ]
          }
        },
        "size" : 1000
      },
      "response" : {
        "took" : 5,
        "timed_out" : false,
        "_shards" : {
          "total" : 1,
          "successful" : 1,
          "skipped" : 0,
          "failed" : 0
        },
        "hits" : {
          "total" : {
            "value" : 0,
            "relation" : "eq"
          },
          "max_score" : null
        }
      }
    }
  }, {
    "_hop" : 2,
    "_query" : 0,
    "_index" : "zentity_sandbox_leie",
    "filters" : {
      "attributes" : {
        "tree" : {
          "0" : {
            "id" : { },
            "name" : {
              "city" : {
                "state" : { }
              },
              "postal_code" : { },
              "street" : { }
            }
          }
        },
        "resolvers" : {
          "id" : {
            "attributes" : [ "id" ]
          },
          "name_city_state" : {
            "attributes" : [ "city", "name", "state" ]
          },
          "name_postal_code" : {
            "attributes" : [ "name", "postal_code" ]
          },
          "name_street" : {
            "attributes" : [ "name", "street" ]
          }
        }
      },
      "terms" : null
    },
    "search" : {
      "request" : {
        "_source" : true,
        "query" : {
          "bool" : {
            "must_not" : {
              "ids" : {
                "values" : [ "AmAfGG0Bh4qDFJrXNuqc", "DWAfGG0Bh4qDFJrXNebG" ]
              }
            },
            "filter" : {
              "bool" : {
                "should" : [ {
                  "bool" : {
                    "should" : [ {
                      "term" : {
                        "npi" : "1023093473"
                      }
                    }, {
                      "term" : {
                        "npi" : "1497077796"
                      }
                    } ]
                  }
                }, {
                  "bool" : {
                    "filter" : [ {
                      "bool" : {
                        "should" : [ {
                          "bool" : {
                            "should" : [ {
                              "bool" : {
                                "filter" : [ {
                                  "match" : {
                                    "busname" : {
                                      "query" : "CLINICAL SUPPORT SERVICES, LLC",
                                      "fuzziness" : "1"
                                    }
                                  }
                                }, {
                                  "match" : {
                                    "busname.initials" : {
                                      "query" : "CLINICAL SUPPORT SERVICES, LLC",
                                      "fuzziness" : "auto"
                                    }
                                  }
                                } ]
                              }
                            }, {
                              "bool" : {
                                "filter" : [ {
                                  "match" : {
                                    "busname" : {
                                      "query" : "COMPLEMENTARY SUPPORT SERVICES",
                                      "fuzziness" : "1"
                                    }
                                  }
                                }, {
                                  "match" : {
                                    "busname.initials" : {
                                      "query" : "COMPLEMENTARY SUPPORT SERVICES",
                                      "fuzziness" : "auto"
                                    }
                                  }
                                } ]
                              }
                            } ]
                          }
                        }, {
                          "bool" : {
                            "should" : [ {
                              "match" : {
                                "busname.phonetic" : "CLINICAL SUPPORT SERVICES, LLC"
                              }
                            }, {
                              "match" : {
                                "busname.phonetic" : "COMPLEMENTARY SUPPORT SERVICES"
                              }
                            } ]
                          }
                        } ]
                      }
                    }, {
                      "bool" : {
                        "should" : [ {
                          "bool" : {
                            "filter" : [ {
                              "bool" : {
                                "should" : [ {
                                  "match" : {
                                    "city" : {
                                      "query" : "CHANHASSEN",
                                      "fuzziness" : "1"
                                    }
                                  }
                                }, {
                                  "match" : {
                                    "city" : {
                                      "query" : "MINNEAPOLIS",
                                      "fuzziness" : "1"
                                    }
                                  }
                                } ]
                              }
                            }, {
                              "term" : {
                                "state" : "MN"
                              }
                            } ]
                          }
                        }, {
                          "bool" : {
                            "should" : [ {
                              "match" : {
                                "zip" : {
                                  "query" : "553177413",
                                  "fuzziness" : "1"
                                }
                              }
                            }, {
                              "match" : {
                                "zip" : {
                                  "query" : "55401",
                                  "fuzziness" : "1"
                                }
                              }
                            }, {
                              "match" : {
                                "zip" : {
                                  "query" : "55423",
                                  "fuzziness" : "1"
                                }
                              }
                            } ]
                          }
                        }, {
                          "bool" : {
                            "should" : [ {
                              "match" : {
                                "address" : {
                                  "query" : "207 5TH AVENUE, N",
                                  "fuzziness" : "1"
                                }
                              }
                            }, {
                              "match" : {
                                "address" : {
                                  "query" : "2345 STONE CREEK LN W",
                                  "fuzziness" : "1"
                                }
                              }
                            }, {
                              "match" : {
                                "address" : {
                                  "query" : "6701 PENN AVENUE, S, STE 301",
                                  "fuzziness" : "1"
                                }
                              }
                            } ]
                          }
                        } ]
                      }
                    } ]
                  }
                } ]
              }
            }
          }
        },
        "size" : 1000
      },
      "response" : {
        "took" : 5,
        "timed_out" : false,
        "_shards" : {
          "total" : 1,
          "successful" : 1,
          "skipped" : 0,
          "failed" : 0
        },
        "hits" : {
          "total" : {
            "value" : 0,
            "relation" : "eq"
          },
          "max_score" : null
        }
      }
    }
  }, {
    "_hop" : 2,
    "_query" : 1,
    "_index" : "zentity_sandbox_nppes",
    "filters" : {
      "attributes" : {
        "tree" : {
          "0" : {
            "id" : { },
            "name" : {
              "city" : {
                "state" : { }
              },
              "phone" : { },
              "postal_code" : { },
              "street" : { }
            }
          }
        },
        "resolvers" : {
          "id" : {
            "attributes" : [ "id" ]
          },
          "name_city_state" : {
            "attributes" : [ "city", "name", "state" ]
          },
          "name_phone" : {
            "attributes" : [ "name", "phone" ]
          },
          "name_postal_code" : {
            "attributes" : [ "name", "postal_code" ]
          },
          "name_street" : {
            "attributes" : [ "name", "street" ]
          }
        }
      },
      "terms" : null
    },
    "search" : {
      "request" : {
        "_source" : true,
        "query" : {
          "bool" : {
            "must_not" : {
              "ids" : {
                "values" : [ "OpArGG0Bh4qDFJrXHfxg" ]
              }
            },
            "filter" : {
              "bool" : {
                "should" : [ {
                  "bool" : {
                    "should" : [ {
                      "term" : {
                        "number" : "1023093473"
                      }
                    }, {
                      "term" : {
                        "number" : "1497077796"
                      }
                    } ]
                  }
                }, {
                  "bool" : {
                    "filter" : [ {
                      "bool" : {
                        "should" : [ {
                          "bool" : {
                            "should" : [ {
                              "bool" : {
                                "filter" : [ {
                                  "match" : {
                                    "basic.organization_name" : {
                                      "query" : "CLINICAL SUPPORT SERVICES, LLC",
                                      "fuzziness" : "1"
                                    }
                                  }
                                }, {
                                  "match" : {
                                    "basic.organization_name.initials" : {
                                      "query" : "CLINICAL SUPPORT SERVICES, LLC",
                                      "fuzziness" : "auto"
                                    }
                                  }
                                } ]
                              }
                            }, {
                              "bool" : {
                                "filter" : [ {
                                  "match" : {
                                    "basic.organization_name" : {
                                      "query" : "COMPLEMENTARY SUPPORT SERVICES",
                                      "fuzziness" : "1"
                                    }
                                  }
                                }, {
                                  "match" : {
                                    "basic.organization_name.initials" : {
                                      "query" : "COMPLEMENTARY SUPPORT SERVICES",
                                      "fuzziness" : "auto"
                                    }
                                  }
                                } ]
                              }
                            } ]
                          }
                        }, {
                          "bool" : {
                            "should" : [ {
                              "match" : {
                                "basic.organization_name.phonetic" : "CLINICAL SUPPORT SERVICES, LLC"
                              }
                            }, {
                              "match" : {
                                "basic.organization_name.phonetic" : "COMPLEMENTARY SUPPORT SERVICES"
                              }
                            } ]
                          }
                        } ]
                      }
                    }, {
                      "bool" : {
                        "should" : [ {
                          "bool" : {
                            "filter" : [ {
                              "bool" : {
                                "should" : [ {
                                  "match" : {
                                    "addresses.location.city" : {
                                      "query" : "CHANHASSEN",
                                      "fuzziness" : "1"
                                    }
                                  }
                                }, {
                                  "match" : {
                                    "addresses.location.city" : {
                                      "query" : "MINNEAPOLIS",
                                      "fuzziness" : "1"
                                    }
                                  }
                                } ]
                              }
                            }, {
                              "term" : {
                                "addresses.location.state" : "MN"
                              }
                            } ]
                          }
                        }, {
                          "match" : {
                            "addresses.location.telephone_number" : {
                              "query" : "6122035257",
                              "fuzziness" : "1"
                            }
                          }
                        }, {
                          "bool" : {
                            "should" : [ {
                              "match" : {
                                "addresses.location.postal_code" : {
                                  "query" : "553177413",
                                  "fuzziness" : "1"
                                }
                              }
                            }, {
                              "match" : {
                                "addresses.location.postal_code" : {
                                  "query" : "55401",
                                  "fuzziness" : "1"
                                }
                              }
                            }, {
                              "match" : {
                                "addresses.location.postal_code" : {
                                  "query" : "55423",
                                  "fuzziness" : "1"
                                }
                              }
                            } ]
                          }
                        }, {
                          "bool" : {
                            "should" : [ {
                              "match" : {
                                "addresses.location.address_1" : {
                                  "query" : "207 5TH AVENUE, N",
                                  "fuzziness" : "1"
                                }
                              }
                            }, {
                              "match" : {
                                "addresses.location.address_1" : {
                                  "query" : "2345 STONE CREEK LN W",
                                  "fuzziness" : "1"
                                }
                              }
                            }, {
                              "match" : {
                                "addresses.location.address_1" : {
                                  "query" : "6701 PENN AVENUE, S, STE 301",
                                  "fuzziness" : "1"
                                }
                              }
                            } ]
                          }
                        } ]
                      }
                    } ]
                  }
                } ]
              }
            }
          }
        },
        "size" : 1000
      },
      "response" : {
        "took" : 12,
        "timed_out" : false,
        "_shards" : {
          "total" : 1,
          "successful" : 1,
          "skipped" : 0,
          "failed" : 0
        },
        "hits" : {
          "total" : {
            "value" : 2,
            "relation" : "eq"
          },
          "max_score" : 0.0
        }
      }
    }
  }, {
    "_hop" : 2,
    "_query" : 2,
    "_index" : "zentity_sandbox_pecos_enrollment",
    "filters" : {
      "attributes" : {
        "tree" : {
          "0" : {
            "id" : { }
          }
        },
        "resolvers" : {
          "id" : {
            "attributes" : [ "id" ]
          }
        }
      },
      "terms" : null
    },
    "search" : {
      "request" : {
        "_source" : true,
        "query" : {
          "bool" : {
            "should" : [ {
              "term" : {
                "npi" : "1023093473"
              }
            }, {
              "term" : {
                "npi" : "1497077796"
              }
            } ]
          }
        },
        "size" : 1000
      },
      "response" : {
        "took" : 0,
        "timed_out" : false,
        "_shards" : {
          "total" : 1,
          "successful" : 1,
          "skipped" : 0,
          "failed" : 0
        },
        "hits" : {
          "total" : {
            "value" : 0,
            "relation" : "eq"
          },
          "max_score" : null
        }
      }
    }
  }, {
    "_hop" : 2,
    "_query" : 3,
    "_index" : "zentity_sandbox_physician_compare",
    "filters" : {
      "attributes" : {
        "tree" : {
          "0" : {
            "id" : { },
            "name" : {
              "city" : {
                "state" : { }
              },
              "phone" : { },
              "postal_code" : { },
              "street" : { }
            }
          }
        },
        "resolvers" : {
          "id" : {
            "attributes" : [ "id" ]
          },
          "name_city_state" : {
            "attributes" : [ "city", "name", "state" ]
          },
          "name_phone" : {
            "attributes" : [ "name", "phone" ]
          },
          "name_postal_code" : {
            "attributes" : [ "name", "postal_code" ]
          },
          "name_street" : {
            "attributes" : [ "name", "street" ]
          }
        }
      },
      "terms" : null
    },
    "search" : {
      "request" : {
        "_source" : true,
        "query" : {
          "bool" : {
            "should" : [ {
              "bool" : {
                "should" : [ {
                  "term" : {
                    "npi" : "1023093473"
                  }
                }, {
                  "term" : {
                    "npi" : "1497077796"
                  }
                } ]
              }
            }, {
              "bool" : {
                "filter" : [ {
                  "bool" : {
                    "should" : [ {
                      "bool" : {
                        "should" : [ {
                          "bool" : {
                            "filter" : [ {
                              "match" : {
                                "org_nm" : {
                                  "query" : "CLINICAL SUPPORT SERVICES, LLC",
                                  "fuzziness" : "1"
                                }
                              }
                            }, {
                              "match" : {
                                "org_nm.initials" : {
                                  "query" : "CLINICAL SUPPORT SERVICES, LLC",
                                  "fuzziness" : "auto"
                                }
                              }
                            } ]
                          }
                        }, {
                          "bool" : {
                            "filter" : [ {
                              "match" : {
                                "org_nm" : {
                                  "query" : "COMPLEMENTARY SUPPORT SERVICES",
                                  "fuzziness" : "1"
                                }
                              }
                            }, {
                              "match" : {
                                "org_nm.initials" : {
                                  "query" : "COMPLEMENTARY SUPPORT SERVICES",
                                  "fuzziness" : "auto"
                                }
                              }
                            } ]
                          }
                        } ]
                      }
                    }, {
                      "bool" : {
                        "should" : [ {
                          "match" : {
                            "org_nm.phonetic" : "CLINICAL SUPPORT SERVICES, LLC"
                          }
                        }, {
                          "match" : {
                            "org_nm.phonetic" : "COMPLEMENTARY SUPPORT SERVICES"
                          }
                        } ]
                      }
                    } ]
                  }
                }, {
                  "bool" : {
                    "should" : [ {
                      "bool" : {
                        "filter" : [ {
                          "bool" : {
                            "should" : [ {
                              "match" : {
                                "cty" : {
                                  "query" : "CHANHASSEN",
                                  "fuzziness" : "1"
                                }
                              }
                            }, {
                              "match" : {
                                "cty" : {
                                  "query" : "MINNEAPOLIS",
                                  "fuzziness" : "1"
                                }
                              }
                            } ]
                          }
                        }, {
                          "term" : {
                            "st" : "MN"
                          }
                        } ]
                      }
                    }, {
                      "match" : {
                        "phn_numbr" : {
                          "query" : "6122035257",
                          "fuzziness" : "1"
                        }
                      }
                    }, {
                      "bool" : {
                        "should" : [ {
                          "match" : {
                            "zip" : {
                              "query" : "553177413",
                              "fuzziness" : "1"
                            }
                          }
                        }, {
                          "match" : {
                            "zip" : {
                              "query" : "55401",
                              "fuzziness" : "1"
                            }
                          }
                        }, {
                          "match" : {
                            "zip" : {
                              "query" : "55423",
                              "fuzziness" : "1"
                            }
                          }
                        } ]
                      }
                    }, {
                      "bool" : {
                        "should" : [ {
                          "match" : {
                            "adr_ln_1" : {
                              "query" : "207 5TH AVENUE, N",
                              "fuzziness" : "1"
                            }
                          }
                        }, {
                          "match" : {
                            "adr_ln_1" : {
                              "query" : "2345 STONE CREEK LN W",
                              "fuzziness" : "1"
                            }
                          }
                        }, {
                          "match" : {
                            "adr_ln_1" : {
                              "query" : "6701 PENN AVENUE, S, STE 301",
                              "fuzziness" : "1"
                            }
                          }
                        } ]
                      }
                    } ]
                  }
                } ]
              }
            } ]
          }
        },
        "size" : 1000
      },
      "response" : {
        "took" : 5,
        "timed_out" : false,
        "_shards" : {
          "total" : 1,
          "successful" : 1,
          "skipped" : 0,
          "failed" : 0
        },
        "hits" : {
          "total" : {
            "value" : 0,
            "relation" : "eq"
          },
          "max_score" : null
        }
      }
    }
  }, {
    "_hop" : 3,
    "_query" : 0,
    "_index" : "zentity_sandbox_leie",
    "filters" : {
      "attributes" : {
        "tree" : {
          "0" : {
            "id" : { },
            "name" : {
              "city" : {
                "state" : { }
              },
              "postal_code" : { },
              "street" : { }
            }
          }
        },
        "resolvers" : {
          "id" : {
            "attributes" : [ "id" ]
          },
          "name_city_state" : {
            "attributes" : [ "city", "name", "state" ]
          },
          "name_postal_code" : {
            "attributes" : [ "name", "postal_code" ]
          },
          "name_street" : {
            "attributes" : [ "name", "street" ]
          }
        }
      },
      "terms" : null
    },
    "search" : {
      "request" : {
        "_source" : true,
        "query" : {
          "bool" : {
            "must_not" : {
              "ids" : {
                "values" : [ "AmAfGG0Bh4qDFJrXNuqc", "DWAfGG0Bh4qDFJrXNebG" ]
              }
            },
            "filter" : {
              "bool" : {
                "should" : [ {
                  "bool" : {
                    "should" : [ {
                      "term" : {
                        "npi" : "1023093473"
                      }
                    }, {
                      "term" : {
                        "npi" : "1174537823"
                      }
                    }, {
                      "term" : {
                        "npi" : "1497077796"
                      }
                    } ]
                  }
                }, {
                  "bool" : {
                    "filter" : [ {
                      "bool" : {
                        "should" : [ {
                          "bool" : {
                            "should" : [ {
                              "bool" : {
                                "filter" : [ {
                                  "match" : {
                                    "busname" : {
                                      "query" : "CLINICAL SUPPORT SERVICES, LLC",
                                      "fuzziness" : "1"
                                    }
                                  }
                                }, {
                                  "match" : {
                                    "busname.initials" : {
                                      "query" : "CLINICAL SUPPORT SERVICES, LLC",
                                      "fuzziness" : "auto"
                                    }
                                  }
                                } ]
                              }
                            }, {
                              "bool" : {
                                "filter" : [ {
                                  "match" : {
                                    "busname" : {
                                      "query" : "COMPLEMENTARY SUPPORT SERVICES",
                                      "fuzziness" : "1"
                                    }
                                  }
                                }, {
                                  "match" : {
                                    "busname.initials" : {
                                      "query" : "COMPLEMENTARY SUPPORT SERVICES",
                                      "fuzziness" : "auto"
                                    }
                                  }
                                } ]
                              }
                            } ]
                          }
                        }, {
                          "bool" : {
                            "should" : [ {
                              "match" : {
                                "busname.phonetic" : "CLINICAL SUPPORT SERVICES, LLC"
                              }
                            }, {
                              "match" : {
                                "busname.phonetic" : "COMPLEMENTARY SUPPORT SERVICES"
                              }
                            } ]
                          }
                        } ]
                      }
                    }, {
                      "bool" : {
                        "should" : [ {
                          "bool" : {
                            "filter" : [ {
                              "bool" : {
                                "should" : [ {
                                  "match" : {
                                    "city" : {
                                      "query" : "CHANHASSEN",
                                      "fuzziness" : "1"
                                    }
                                  }
                                }, {
                                  "match" : {
                                    "city" : {
                                      "query" : "MINNEAPOLIS",
                                      "fuzziness" : "1"
                                    }
                                  }
                                }, {
                                  "match" : {
                                    "city" : {
                                      "query" : "RICHFIELD",
                                      "fuzziness" : "1"
                                    }
                                  }
                                } ]
                              }
                            }, {
                              "term" : {
                                "state" : "MN"
                              }
                            } ]
                          }
                        }, {
                          "bool" : {
                            "should" : [ {
                              "match" : {
                                "zip" : {
                                  "query" : "553177413",
                                  "fuzziness" : "1"
                                }
                              }
                            }, {
                              "match" : {
                                "zip" : {
                                  "query" : "55401",
                                  "fuzziness" : "1"
                                }
                              }
                            }, {
                              "match" : {
                                "zip" : {
                                  "query" : "55423",
                                  "fuzziness" : "1"
                                }
                              }
                            }, {
                              "match" : {
                                "zip" : {
                                  "query" : "554232093",
                                  "fuzziness" : "1"
                                }
                              }
                            } ]
                          }
                        }, {
                          "bool" : {
                            "should" : [ {
                              "match" : {
                                "address" : {
                                  "query" : "207 5TH AVENUE, N",
                                  "fuzziness" : "1"
                                }
                              }
                            }, {
                              "match" : {
                                "address" : {
                                  "query" : "2345 STONE CREEK LN W",
                                  "fuzziness" : "1"
                                }
                              }
                            }, {
                              "match" : {
                                "address" : {
                                  "query" : "6701 PENN AVE S",
                                  "fuzziness" : "1"
                                }
                              }
                            }, {
                              "match" : {
                                "address" : {
                                  "query" : "6701 PENN AVENUE, S, STE 301",
                                  "fuzziness" : "1"
                                }
                              }
                            } ]
                          }
                        } ]
                      }
                    } ]
                  }
                } ]
              }
            }
          }
        },
        "size" : 1000
      },
      "response" : {
        "took" : 8,
        "timed_out" : false,
        "_shards" : {
          "total" : 1,
          "successful" : 1,
          "skipped" : 0,
          "failed" : 0
        },
        "hits" : {
          "total" : {
            "value" : 1,
            "relation" : "eq"
          },
          "max_score" : 0.0
        }
      }
    }
  }, {
    "_hop" : 3,
    "_query" : 1,
    "_index" : "zentity_sandbox_nppes",
    "filters" : {
      "attributes" : {
        "tree" : {
          "0" : {
            "id" : { },
            "name" : {
              "city" : {
                "state" : { }
              },
              "phone" : { },
              "postal_code" : { },
              "street" : { }
            }
          }
        },
        "resolvers" : {
          "id" : {
            "attributes" : [ "id" ]
          },
          "name_city_state" : {
            "attributes" : [ "city", "name", "state" ]
          },
          "name_phone" : {
            "attributes" : [ "name", "phone" ]
          },
          "name_postal_code" : {
            "attributes" : [ "name", "postal_code" ]
          },
          "name_street" : {
            "attributes" : [ "name", "street" ]
          }
        }
      },
      "terms" : null
    },
    "search" : {
      "request" : {
        "_source" : true,
        "query" : {
          "bool" : {
            "must_not" : {
              "ids" : {
                "values" : [ "F28kGG0Bh4qDFJrX1qdK", "OpArGG0Bh4qDFJrXHfxg", "t2UiGG0Bh4qDFJrX9KFU" ]
              }
            },
            "filter" : {
              "bool" : {
                "should" : [ {
                  "bool" : {
                    "should" : [ {
                      "term" : {
                        "number" : "1023093473"
                      }
                    }, {
                      "term" : {
                        "number" : "1174537823"
                      }
                    }, {
                      "term" : {
                        "number" : "1497077796"
                      }
                    } ]
                  }
                }, {
                  "bool" : {
                    "filter" : [ {
                      "bool" : {
                        "should" : [ {
                          "bool" : {
                            "should" : [ {
                              "bool" : {
                                "filter" : [ {
                                  "match" : {
                                    "basic.organization_name" : {
                                      "query" : "CLINICAL SUPPORT SERVICES, LLC",
                                      "fuzziness" : "1"
                                    }
                                  }
                                }, {
                                  "match" : {
                                    "basic.organization_name.initials" : {
                                      "query" : "CLINICAL SUPPORT SERVICES, LLC",
                                      "fuzziness" : "auto"
                                    }
                                  }
                                } ]
                              }
                            }, {
                              "bool" : {
                                "filter" : [ {
                                  "match" : {
                                    "basic.organization_name" : {
                                      "query" : "COMPLEMENTARY SUPPORT SERVICES",
                                      "fuzziness" : "1"
                                    }
                                  }
                                }, {
                                  "match" : {
                                    "basic.organization_name.initials" : {
                                      "query" : "COMPLEMENTARY SUPPORT SERVICES",
                                      "fuzziness" : "auto"
                                    }
                                  }
                                } ]
                              }
                            } ]
                          }
                        }, {
                          "bool" : {
                            "should" : [ {
                              "match" : {
                                "basic.organization_name.phonetic" : "CLINICAL SUPPORT SERVICES, LLC"
                              }
                            }, {
                              "match" : {
                                "basic.organization_name.phonetic" : "COMPLEMENTARY SUPPORT SERVICES"
                              }
                            } ]
                          }
                        } ]
                      }
                    }, {
                      "bool" : {
                        "should" : [ {
                          "bool" : {
                            "filter" : [ {
                              "bool" : {
                                "should" : [ {
                                  "match" : {
                                    "addresses.location.city" : {
                                      "query" : "CHANHASSEN",
                                      "fuzziness" : "1"
                                    }
                                  }
                                }, {
                                  "match" : {
                                    "addresses.location.city" : {
                                      "query" : "MINNEAPOLIS",
                                      "fuzziness" : "1"
                                    }
                                  }
                                }, {
                                  "match" : {
                                    "addresses.location.city" : {
                                      "query" : "RICHFIELD",
                                      "fuzziness" : "1"
                                    }
                                  }
                                } ]
                              }
                            }, {
                              "term" : {
                                "addresses.location.state" : "MN"
                              }
                            } ]
                          }
                        }, {
                          "bool" : {
                            "should" : [ {
                              "match" : {
                                "addresses.location.telephone_number" : {
                                  "query" : "6122035257",
                                  "fuzziness" : "1"
                                }
                              }
                            }, {
                              "match" : {
                                "addresses.location.telephone_number" : {
                                  "query" : "9526088403",
                                  "fuzziness" : "1"
                                }
                              }
                            }, {
                              "match" : {
                                "addresses.location.telephone_number" : {
                                  "query" : "9528951730",
                                  "fuzziness" : "1"
                                }
                              }
                            } ]
                          }
                        }, {
                          "bool" : {
                            "should" : [ {
                              "match" : {
                                "addresses.location.postal_code" : {
                                  "query" : "553177413",
                                  "fuzziness" : "1"
                                }
                              }
                            }, {
                              "match" : {
                                "addresses.location.postal_code" : {
                                  "query" : "55401",
                                  "fuzziness" : "1"
                                }
                              }
                            }, {
                              "match" : {
                                "addresses.location.postal_code" : {
                                  "query" : "55423",
                                  "fuzziness" : "1"
                                }
                              }
                            }, {
                              "match" : {
                                "addresses.location.postal_code" : {
                                  "query" : "554232093",
                                  "fuzziness" : "1"
                                }
                              }
                            } ]
                          }
                        }, {
                          "bool" : {
                            "should" : [ {
                              "match" : {
                                "addresses.location.address_1" : {
                                  "query" : "207 5TH AVENUE, N",
                                  "fuzziness" : "1"
                                }
                              }
                            }, {
                              "match" : {
                                "addresses.location.address_1" : {
                                  "query" : "2345 STONE CREEK LN W",
                                  "fuzziness" : "1"
                                }
                              }
                            }, {
                              "match" : {
                                "addresses.location.address_1" : {
                                  "query" : "6701 PENN AVE S",
                                  "fuzziness" : "1"
                                }
                              }
                            }, {
                              "match" : {
                                "addresses.location.address_1" : {
                                  "query" : "6701 PENN AVENUE, S, STE 301",
                                  "fuzziness" : "1"
                                }
                              }
                            } ]
                          }
                        } ]
                      }
                    } ]
                  }
                } ]
              }
            }
          }
        },
        "size" : 1000
      },
      "response" : {
        "took" : 12,
        "timed_out" : false,
        "_shards" : {
          "total" : 1,
          "successful" : 1,
          "skipped" : 0,
          "failed" : 0
        },
        "hits" : {
          "total" : {
            "value" : 0,
            "relation" : "eq"
          },
          "max_score" : null
        }
      }
    }
  }, {
    "_hop" : 3,
    "_query" : 2,
    "_index" : "zentity_sandbox_pecos_enrollment",
    "filters" : {
      "attributes" : {
        "tree" : {
          "0" : {
            "id" : { }
          }
        },
        "resolvers" : {
          "id" : {
            "attributes" : [ "id" ]
          }
        }
      },
      "terms" : null
    },
    "search" : {
      "request" : {
        "_source" : true,
        "query" : {
          "bool" : {
            "should" : [ {
              "term" : {
                "npi" : "1023093473"
              }
            }, {
              "term" : {
                "npi" : "1174537823"
              }
            }, {
              "term" : {
                "npi" : "1497077796"
              }
            } ]
          }
        },
        "size" : 1000
      },
      "response" : {
        "took" : 0,
        "timed_out" : false,
        "_shards" : {
          "total" : 1,
          "successful" : 1,
          "skipped" : 0,
          "failed" : 0
        },
        "hits" : {
          "total" : {
            "value" : 0,
            "relation" : "eq"
          },
          "max_score" : null
        }
      }
    }
  }, {
    "_hop" : 3,
    "_query" : 3,
    "_index" : "zentity_sandbox_physician_compare",
    "filters" : {
      "attributes" : {
        "tree" : {
          "0" : {
            "id" : { },
            "name" : {
              "city" : {
                "state" : { }
              },
              "phone" : { },
              "postal_code" : { },
              "street" : { }
            }
          }
        },
        "resolvers" : {
          "id" : {
            "attributes" : [ "id" ]
          },
          "name_city_state" : {
            "attributes" : [ "city", "name", "state" ]
          },
          "name_phone" : {
            "attributes" : [ "name", "phone" ]
          },
          "name_postal_code" : {
            "attributes" : [ "name", "postal_code" ]
          },
          "name_street" : {
            "attributes" : [ "name", "street" ]
          }
        }
      },
      "terms" : null
    },
    "search" : {
      "request" : {
        "_source" : true,
        "query" : {
          "bool" : {
            "should" : [ {
              "bool" : {
                "should" : [ {
                  "term" : {
                    "npi" : "1023093473"
                  }
                }, {
                  "term" : {
                    "npi" : "1174537823"
                  }
                }, {
                  "term" : {
                    "npi" : "1497077796"
                  }
                } ]
              }
            }, {
              "bool" : {
                "filter" : [ {
                  "bool" : {
                    "should" : [ {
                      "bool" : {
                        "should" : [ {
                          "bool" : {
                            "filter" : [ {
                              "match" : {
                                "org_nm" : {
                                  "query" : "CLINICAL SUPPORT SERVICES, LLC",
                                  "fuzziness" : "1"
                                }
                              }
                            }, {
                              "match" : {
                                "org_nm.initials" : {
                                  "query" : "CLINICAL SUPPORT SERVICES, LLC",
                                  "fuzziness" : "auto"
                                }
                              }
                            } ]
                          }
                        }, {
                          "bool" : {
                            "filter" : [ {
                              "match" : {
                                "org_nm" : {
                                  "query" : "COMPLEMENTARY SUPPORT SERVICES",
                                  "fuzziness" : "1"
                                }
                              }
                            }, {
                              "match" : {
                                "org_nm.initials" : {
                                  "query" : "COMPLEMENTARY SUPPORT SERVICES",
                                  "fuzziness" : "auto"
                                }
                              }
                            } ]
                          }
                        } ]
                      }
                    }, {
                      "bool" : {
                        "should" : [ {
                          "match" : {
                            "org_nm.phonetic" : "CLINICAL SUPPORT SERVICES, LLC"
                          }
                        }, {
                          "match" : {
                            "org_nm.phonetic" : "COMPLEMENTARY SUPPORT SERVICES"
                          }
                        } ]
                      }
                    } ]
                  }
                }, {
                  "bool" : {
                    "should" : [ {
                      "bool" : {
                        "filter" : [ {
                          "bool" : {
                            "should" : [ {
                              "match" : {
                                "cty" : {
                                  "query" : "CHANHASSEN",
                                  "fuzziness" : "1"
                                }
                              }
                            }, {
                              "match" : {
                                "cty" : {
                                  "query" : "MINNEAPOLIS",
                                  "fuzziness" : "1"
                                }
                              }
                            }, {
                              "match" : {
                                "cty" : {
                                  "query" : "RICHFIELD",
                                  "fuzziness" : "1"
                                }
                              }
                            } ]
                          }
                        }, {
                          "term" : {
                            "st" : "MN"
                          }
                        } ]
                      }
                    }, {
                      "bool" : {
                        "should" : [ {
                          "match" : {
                            "phn_numbr" : {
                              "query" : "6122035257",
                              "fuzziness" : "1"
                            }
                          }
                        }, {
                          "match" : {
                            "phn_numbr" : {
                              "query" : "9526088403",
                              "fuzziness" : "1"
                            }
                          }
                        }, {
                          "match" : {
                            "phn_numbr" : {
                              "query" : "9528951730",
                              "fuzziness" : "1"
                            }
                          }
                        } ]
                      }
                    }, {
                      "bool" : {
                        "should" : [ {
                          "match" : {
                            "zip" : {
                              "query" : "553177413",
                              "fuzziness" : "1"
                            }
                          }
                        }, {
                          "match" : {
                            "zip" : {
                              "query" : "55401",
                              "fuzziness" : "1"
                            }
                          }
                        }, {
                          "match" : {
                            "zip" : {
                              "query" : "55423",
                              "fuzziness" : "1"
                            }
                          }
                        }, {
                          "match" : {
                            "zip" : {
                              "query" : "554232093",
                              "fuzziness" : "1"
                            }
                          }
                        } ]
                      }
                    }, {
                      "bool" : {
                        "should" : [ {
                          "match" : {
                            "adr_ln_1" : {
                              "query" : "207 5TH AVENUE, N",
                              "fuzziness" : "1"
                            }
                          }
                        }, {
                          "match" : {
                            "adr_ln_1" : {
                              "query" : "2345 STONE CREEK LN W",
                              "fuzziness" : "1"
                            }
                          }
                        }, {
                          "match" : {
                            "adr_ln_1" : {
                              "query" : "6701 PENN AVE S",
                              "fuzziness" : "1"
                            }
                          }
                        }, {
                          "match" : {
                            "adr_ln_1" : {
                              "query" : "6701 PENN AVENUE, S, STE 301",
                              "fuzziness" : "1"
                            }
                          }
                        } ]
                      }
                    } ]
                  }
                } ]
              }
            } ]
          }
        },
        "size" : 1000
      },
      "response" : {
        "took" : 6,
        "timed_out" : false,
        "_shards" : {
          "total" : 1,
          "successful" : 1,
          "skipped" : 0,
          "failed" : 0
        },
        "hits" : {
          "total" : {
            "value" : 0,
            "relation" : "eq"
          },
          "max_score" : null
        }
      }
    }
  }, {
    "_hop" : 4,
    "_query" : 0,
    "_index" : "zentity_sandbox_leie",
    "filters" : {
      "attributes" : {
        "tree" : {
          "0" : {
            "id" : { },
            "name" : {
              "city" : {
                "state" : { }
              },
              "postal_code" : { },
              "street" : { }
            }
          }
        },
        "resolvers" : {
          "id" : {
            "attributes" : [ "id" ]
          },
          "name_city_state" : {
            "attributes" : [ "city", "name", "state" ]
          },
          "name_postal_code" : {
            "attributes" : [ "name", "postal_code" ]
          },
          "name_street" : {
            "attributes" : [ "name", "street" ]
          }
        }
      },
      "terms" : null
    },
    "search" : {
      "request" : {
        "_source" : true,
        "query" : {
          "bool" : {
            "must_not" : {
              "ids" : {
                "values" : [ "AmAfGG0Bh4qDFJrXNuqc", "DWAfGG0Bh4qDFJrXNebG", "iWAfGG0Bh4qDFJrXNeLB" ]
              }
            },
            "filter" : {
              "bool" : {
                "should" : [ {
                  "bool" : {
                    "should" : [ {
                      "term" : {
                        "npi" : "1023093473"
                      }
                    }, {
                      "term" : {
                        "npi" : "1174537823"
                      }
                    }, {
                      "term" : {
                        "npi" : "1497077796"
                      }
                    } ]
                  }
                }, {
                  "bool" : {
                    "filter" : [ {
                      "bool" : {
                        "should" : [ {
                          "bool" : {
                            "should" : [ {
                              "bool" : {
                                "filter" : [ {
                                  "match" : {
                                    "busname" : {
                                      "query" : "CLINICAL SUPPORT SERVICES, LLC",
                                      "fuzziness" : "1"
                                    }
                                  }
                                }, {
                                  "match" : {
                                    "busname.initials" : {
                                      "query" : "CLINICAL SUPPORT SERVICES, LLC",
                                      "fuzziness" : "auto"
                                    }
                                  }
                                } ]
                              }
                            }, {
                              "bool" : {
                                "filter" : [ {
                                  "match" : {
                                    "busname" : {
                                      "query" : "COMPLEMENTARY SUPPORT SERVICES",
                                      "fuzziness" : "1"
                                    }
                                  }
                                }, {
                                  "match" : {
                                    "busname.initials" : {
                                      "query" : "COMPLEMENTARY SUPPORT SERVICES",
                                      "fuzziness" : "auto"
                                    }
                                  }
                                } ]
                              }
                            }, {
                              "bool" : {
                                "filter" : [ {
                                  "match" : {
                                    "busname" : {
                                      "query" : "CSS METRO, LLC",
                                      "fuzziness" : "1"
                                    }
                                  }
                                }, {
                                  "match" : {
                                    "busname.initials" : {
                                      "query" : "CSS METRO, LLC",
                                      "fuzziness" : "auto"
                                    }
                                  }
                                } ]
                              }
                            } ]
                          }
                        }, {
                          "bool" : {
                            "should" : [ {
                              "match" : {
                                "busname.phonetic" : "CLINICAL SUPPORT SERVICES, LLC"
                              }
                            }, {
                              "match" : {
                                "busname.phonetic" : "COMPLEMENTARY SUPPORT SERVICES"
                              }
                            }, {
                              "match" : {
                                "busname.phonetic" : "CSS METRO, LLC"
                              }
                            } ]
                          }
                        } ]
                      }
                    }, {
                      "bool" : {
                        "should" : [ {
                          "bool" : {
                            "filter" : [ {
                              "bool" : {
                                "should" : [ {
                                  "match" : {
                                    "city" : {
                                      "query" : "CHANHASSEN",
                                      "fuzziness" : "1"
                                    }
                                  }
                                }, {
                                  "match" : {
                                    "city" : {
                                      "query" : "MINNEAPOLIS",
                                      "fuzziness" : "1"
                                    }
                                  }
                                }, {
                                  "match" : {
                                    "city" : {
                                      "query" : "RICHFIELD",
                                      "fuzziness" : "1"
                                    }
                                  }
                                } ]
                              }
                            }, {
                              "term" : {
                                "state" : "MN"
                              }
                            } ]
                          }
                        }, {
                          "bool" : {
                            "should" : [ {
                              "match" : {
                                "zip" : {
                                  "query" : "553177413",
                                  "fuzziness" : "1"
                                }
                              }
                            }, {
                              "match" : {
                                "zip" : {
                                  "query" : "55401",
                                  "fuzziness" : "1"
                                }
                              }
                            }, {
                              "match" : {
                                "zip" : {
                                  "query" : "55423",
                                  "fuzziness" : "1"
                                }
                              }
                            }, {
                              "match" : {
                                "zip" : {
                                  "query" : "554232093",
                                  "fuzziness" : "1"
                                }
                              }
                            } ]
                          }
                        }, {
                          "bool" : {
                            "should" : [ {
                              "match" : {
                                "address" : {
                                  "query" : "207 5TH AVENUE, N",
                                  "fuzziness" : "1"
                                }
                              }
                            }, {
                              "match" : {
                                "address" : {
                                  "query" : "2345 STONE CREEK LN W",
                                  "fuzziness" : "1"
                                }
                              }
                            }, {
                              "match" : {
                                "address" : {
                                  "query" : "6701 PENN AVE S",
                                  "fuzziness" : "1"
                                }
                              }
                            }, {
                              "match" : {
                                "address" : {
                                  "query" : "6701 PENN AVENUE, S, STE 301",
                                  "fuzziness" : "1"
                                }
                              }
                            } ]
                          }
                        } ]
                      }
                    } ]
                  }
                } ]
              }
            }
          }
        },
        "size" : 1000
      },
      "response" : {
        "took" : 7,
        "timed_out" : false,
        "_shards" : {
          "total" : 1,
          "successful" : 1,
          "skipped" : 0,
          "failed" : 0
        },
        "hits" : {
          "total" : {
            "value" : 0,
            "relation" : "eq"
          },
          "max_score" : null
        }
      }
    }
  }, {
    "_hop" : 4,
    "_query" : 1,
    "_index" : "zentity_sandbox_nppes",
    "filters" : {
      "attributes" : {
        "tree" : {
          "0" : {
            "id" : { },
            "name" : {
              "city" : {
                "state" : { }
              },
              "phone" : { },
              "postal_code" : { },
              "street" : { }
            }
          }
        },
        "resolvers" : {
          "id" : {
            "attributes" : [ "id" ]
          },
          "name_city_state" : {
            "attributes" : [ "city", "name", "state" ]
          },
          "name_phone" : {
            "attributes" : [ "name", "phone" ]
          },
          "name_postal_code" : {
            "attributes" : [ "name", "postal_code" ]
          },
          "name_street" : {
            "attributes" : [ "name", "street" ]
          }
        }
      },
      "terms" : null
    },
    "search" : {
      "request" : {
        "_source" : true,
        "query" : {
          "bool" : {
            "must_not" : {
              "ids" : {
                "values" : [ "F28kGG0Bh4qDFJrX1qdK", "OpArGG0Bh4qDFJrXHfxg", "t2UiGG0Bh4qDFJrX9KFU" ]
              }
            },
            "filter" : {
              "bool" : {
                "should" : [ {
                  "bool" : {
                    "should" : [ {
                      "term" : {
                        "number" : "1023093473"
                      }
                    }, {
                      "term" : {
                        "number" : "1174537823"
                      }
                    }, {
                      "term" : {
                        "number" : "1497077796"
                      }
                    } ]
                  }
                }, {
                  "bool" : {
                    "filter" : [ {
                      "bool" : {
                        "should" : [ {
                          "bool" : {
                            "should" : [ {
                              "bool" : {
                                "filter" : [ {
                                  "match" : {
                                    "basic.organization_name" : {
                                      "query" : "CLINICAL SUPPORT SERVICES, LLC",
                                      "fuzziness" : "1"
                                    }
                                  }
                                }, {
                                  "match" : {
                                    "basic.organization_name.initials" : {
                                      "query" : "CLINICAL SUPPORT SERVICES, LLC",
                                      "fuzziness" : "auto"
                                    }
                                  }
                                } ]
                              }
                            }, {
                              "bool" : {
                                "filter" : [ {
                                  "match" : {
                                    "basic.organization_name" : {
                                      "query" : "COMPLEMENTARY SUPPORT SERVICES",
                                      "fuzziness" : "1"
                                    }
                                  }
                                }, {
                                  "match" : {
                                    "basic.organization_name.initials" : {
                                      "query" : "COMPLEMENTARY SUPPORT SERVICES",
                                      "fuzziness" : "auto"
                                    }
                                  }
                                } ]
                              }
                            }, {
                              "bool" : {
                                "filter" : [ {
                                  "match" : {
                                    "basic.organization_name" : {
                                      "query" : "CSS METRO, LLC",
                                      "fuzziness" : "1"
                                    }
                                  }
                                }, {
                                  "match" : {
                                    "basic.organization_name.initials" : {
                                      "query" : "CSS METRO, LLC",
                                      "fuzziness" : "auto"
                                    }
                                  }
                                } ]
                              }
                            } ]
                          }
                        }, {
                          "bool" : {
                            "should" : [ {
                              "match" : {
                                "basic.organization_name.phonetic" : "CLINICAL SUPPORT SERVICES, LLC"
                              }
                            }, {
                              "match" : {
                                "basic.organization_name.phonetic" : "COMPLEMENTARY SUPPORT SERVICES"
                              }
                            }, {
                              "match" : {
                                "basic.organization_name.phonetic" : "CSS METRO, LLC"
                              }
                            } ]
                          }
                        } ]
                      }
                    }, {
                      "bool" : {
                        "should" : [ {
                          "bool" : {
                            "filter" : [ {
                              "bool" : {
                                "should" : [ {
                                  "match" : {
                                    "addresses.location.city" : {
                                      "query" : "CHANHASSEN",
                                      "fuzziness" : "1"
                                    }
                                  }
                                }, {
                                  "match" : {
                                    "addresses.location.city" : {
                                      "query" : "MINNEAPOLIS",
                                      "fuzziness" : "1"
                                    }
                                  }
                                }, {
                                  "match" : {
                                    "addresses.location.city" : {
                                      "query" : "RICHFIELD",
                                      "fuzziness" : "1"
                                    }
                                  }
                                } ]
                              }
                            }, {
                              "term" : {
                                "addresses.location.state" : "MN"
                              }
                            } ]
                          }
                        }, {
                          "bool" : {
                            "should" : [ {
                              "match" : {
                                "addresses.location.telephone_number" : {
                                  "query" : "6122035257",
                                  "fuzziness" : "1"
                                }
                              }
                            }, {
                              "match" : {
                                "addresses.location.telephone_number" : {
                                  "query" : "9526088403",
                                  "fuzziness" : "1"
                                }
                              }
                            }, {
                              "match" : {
                                "addresses.location.telephone_number" : {
                                  "query" : "9528951730",
                                  "fuzziness" : "1"
                                }
                              }
                            } ]
                          }
                        }, {
                          "bool" : {
                            "should" : [ {
                              "match" : {
                                "addresses.location.postal_code" : {
                                  "query" : "553177413",
                                  "fuzziness" : "1"
                                }
                              }
                            }, {
                              "match" : {
                                "addresses.location.postal_code" : {
                                  "query" : "55401",
                                  "fuzziness" : "1"
                                }
                              }
                            }, {
                              "match" : {
                                "addresses.location.postal_code" : {
                                  "query" : "55423",
                                  "fuzziness" : "1"
                                }
                              }
                            }, {
                              "match" : {
                                "addresses.location.postal_code" : {
                                  "query" : "554232093",
                                  "fuzziness" : "1"
                                }
                              }
                            } ]
                          }
                        }, {
                          "bool" : {
                            "should" : [ {
                              "match" : {
                                "addresses.location.address_1" : {
                                  "query" : "207 5TH AVENUE, N",
                                  "fuzziness" : "1"
                                }
                              }
                            }, {
                              "match" : {
                                "addresses.location.address_1" : {
                                  "query" : "2345 STONE CREEK LN W",
                                  "fuzziness" : "1"
                                }
                              }
                            }, {
                              "match" : {
                                "addresses.location.address_1" : {
                                  "query" : "6701 PENN AVE S",
                                  "fuzziness" : "1"
                                }
                              }
                            }, {
                              "match" : {
                                "addresses.location.address_1" : {
                                  "query" : "6701 PENN AVENUE, S, STE 301",
                                  "fuzziness" : "1"
                                }
                              }
                            } ]
                          }
                        } ]
                      }
                    } ]
                  }
                } ]
              }
            }
          }
        },
        "size" : 1000
      },
      "response" : {
        "took" : 10,
        "timed_out" : false,
        "_shards" : {
          "total" : 1,
          "successful" : 1,
          "skipped" : 0,
          "failed" : 0
        },
        "hits" : {
          "total" : {
            "value" : 0,
            "relation" : "eq"
          },
          "max_score" : null
        }
      }
    }
  }, {
    "_hop" : 4,
    "_query" : 2,
    "_index" : "zentity_sandbox_pecos_enrollment",
    "filters" : {
      "attributes" : {
        "tree" : {
          "0" : {
            "id" : { }
          }
        },
        "resolvers" : {
          "id" : {
            "attributes" : [ "id" ]
          }
        }
      },
      "terms" : null
    },
    "search" : {
      "request" : {
        "_source" : true,
        "query" : {
          "bool" : {
            "should" : [ {
              "term" : {
                "npi" : "1023093473"
              }
            }, {
              "term" : {
                "npi" : "1174537823"
              }
            }, {
              "term" : {
                "npi" : "1497077796"
              }
            } ]
          }
        },
        "size" : 1000
      },
      "response" : {
        "took" : 0,
        "timed_out" : false,
        "_shards" : {
          "total" : 1,
          "successful" : 1,
          "skipped" : 0,
          "failed" : 0
        },
        "hits" : {
          "total" : {
            "value" : 0,
            "relation" : "eq"
          },
          "max_score" : null
        }
      }
    }
  }, {
    "_hop" : 4,
    "_query" : 3,
    "_index" : "zentity_sandbox_physician_compare",
    "filters" : {
      "attributes" : {
        "tree" : {
          "0" : {
            "id" : { },
            "name" : {
              "city" : {
                "state" : { }
              },
              "phone" : { },
              "postal_code" : { },
              "street" : { }
            }
          }
        },
        "resolvers" : {
          "id" : {
            "attributes" : [ "id" ]
          },
          "name_city_state" : {
            "attributes" : [ "city", "name", "state" ]
          },
          "name_phone" : {
            "attributes" : [ "name", "phone" ]
          },
          "name_postal_code" : {
            "attributes" : [ "name", "postal_code" ]
          },
          "name_street" : {
            "attributes" : [ "name", "street" ]
          }
        }
      },
      "terms" : null
    },
    "search" : {
      "request" : {
        "_source" : true,
        "query" : {
          "bool" : {
            "should" : [ {
              "bool" : {
                "should" : [ {
                  "term" : {
                    "npi" : "1023093473"
                  }
                }, {
                  "term" : {
                    "npi" : "1174537823"
                  }
                }, {
                  "term" : {
                    "npi" : "1497077796"
                  }
                } ]
              }
            }, {
              "bool" : {
                "filter" : [ {
                  "bool" : {
                    "should" : [ {
                      "bool" : {
                        "should" : [ {
                          "bool" : {
                            "filter" : [ {
                              "match" : {
                                "org_nm" : {
                                  "query" : "CLINICAL SUPPORT SERVICES, LLC",
                                  "fuzziness" : "1"
                                }
                              }
                            }, {
                              "match" : {
                                "org_nm.initials" : {
                                  "query" : "CLINICAL SUPPORT SERVICES, LLC",
                                  "fuzziness" : "auto"
                                }
                              }
                            } ]
                          }
                        }, {
                          "bool" : {
                            "filter" : [ {
                              "match" : {
                                "org_nm" : {
                                  "query" : "COMPLEMENTARY SUPPORT SERVICES",
                                  "fuzziness" : "1"
                                }
                              }
                            }, {
                              "match" : {
                                "org_nm.initials" : {
                                  "query" : "COMPLEMENTARY SUPPORT SERVICES",
                                  "fuzziness" : "auto"
                                }
                              }
                            } ]
                          }
                        }, {
                          "bool" : {
                            "filter" : [ {
                              "match" : {
                                "org_nm" : {
                                  "query" : "CSS METRO, LLC",
                                  "fuzziness" : "1"
                                }
                              }
                            }, {
                              "match" : {
                                "org_nm.initials" : {
                                  "query" : "CSS METRO, LLC",
                                  "fuzziness" : "auto"
                                }
                              }
                            } ]
                          }
                        } ]
                      }
                    }, {
                      "bool" : {
                        "should" : [ {
                          "match" : {
                            "org_nm.phonetic" : "CLINICAL SUPPORT SERVICES, LLC"
                          }
                        }, {
                          "match" : {
                            "org_nm.phonetic" : "COMPLEMENTARY SUPPORT SERVICES"
                          }
                        }, {
                          "match" : {
                            "org_nm.phonetic" : "CSS METRO, LLC"
                          }
                        } ]
                      }
                    } ]
                  }
                }, {
                  "bool" : {
                    "should" : [ {
                      "bool" : {
                        "filter" : [ {
                          "bool" : {
                            "should" : [ {
                              "match" : {
                                "cty" : {
                                  "query" : "CHANHASSEN",
                                  "fuzziness" : "1"
                                }
                              }
                            }, {
                              "match" : {
                                "cty" : {
                                  "query" : "MINNEAPOLIS",
                                  "fuzziness" : "1"
                                }
                              }
                            }, {
                              "match" : {
                                "cty" : {
                                  "query" : "RICHFIELD",
                                  "fuzziness" : "1"
                                }
                              }
                            } ]
                          }
                        }, {
                          "term" : {
                            "st" : "MN"
                          }
                        } ]
                      }
                    }, {
                      "bool" : {
                        "should" : [ {
                          "match" : {
                            "phn_numbr" : {
                              "query" : "6122035257",
                              "fuzziness" : "1"
                            }
                          }
                        }, {
                          "match" : {
                            "phn_numbr" : {
                              "query" : "9526088403",
                              "fuzziness" : "1"
                            }
                          }
                        }, {
                          "match" : {
                            "phn_numbr" : {
                              "query" : "9528951730",
                              "fuzziness" : "1"
                            }
                          }
                        } ]
                      }
                    }, {
                      "bool" : {
                        "should" : [ {
                          "match" : {
                            "zip" : {
                              "query" : "553177413",
                              "fuzziness" : "1"
                            }
                          }
                        }, {
                          "match" : {
                            "zip" : {
                              "query" : "55401",
                              "fuzziness" : "1"
                            }
                          }
                        }, {
                          "match" : {
                            "zip" : {
                              "query" : "55423",
                              "fuzziness" : "1"
                            }
                          }
                        }, {
                          "match" : {
                            "zip" : {
                              "query" : "554232093",
                              "fuzziness" : "1"
                            }
                          }
                        } ]
                      }
                    }, {
                      "bool" : {
                        "should" : [ {
                          "match" : {
                            "adr_ln_1" : {
                              "query" : "207 5TH AVENUE, N",
                              "fuzziness" : "1"
                            }
                          }
                        }, {
                          "match" : {
                            "adr_ln_1" : {
                              "query" : "2345 STONE CREEK LN W",
                              "fuzziness" : "1"
                            }
                          }
                        }, {
                          "match" : {
                            "adr_ln_1" : {
                              "query" : "6701 PENN AVE S",
                              "fuzziness" : "1"
                            }
                          }
                        }, {
                          "match" : {
                            "adr_ln_1" : {
                              "query" : "6701 PENN AVENUE, S, STE 301",
                              "fuzziness" : "1"
                            }
                          }
                        } ]
                      }
                    } ]
                  }
                } ]
              }
            } ]
          }
        },
        "size" : 1000
      },
      "response" : {
        "took" : 7,
        "timed_out" : false,
        "_shards" : {
          "total" : 1,
          "successful" : 1,
          "skipped" : 0,
          "failed" : 0
        },
        "hits" : {
          "total" : {
            "value" : 0,
            "relation" : "eq"
          },
          "max_score" : null
        }
      }
    }
  } ] ]
}
```