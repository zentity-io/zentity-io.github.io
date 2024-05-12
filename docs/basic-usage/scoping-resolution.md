[Home](/) / [Documentation](/docs) / [Basic Usage](/docs/basic-usage) / Scoping Resolution


#### <a name="contents"></a>Basic Usage Tutorials 📖

This tutorial is part of a series to help you learn and perform the basic
functions of zentity. Each tutorial adds a little more sophistication to the
prior tutorials, so you can start simple and learn the more advanced features
over time.

1. [Exact Name Matching](/docs/basic-usage/exact-name-matching)
2. [Robust Name Matching](/docs/basic-usage/robust-name-matching)
3. [Multiple Attribute Resolution](/docs/basic-usage/multiple-attribute-resolution)
4. [Multiple Resolver Resolution](/docs/basic-usage/multiple-resolver-resolution)
5. [Cross Index Resolution](/docs/basic-usage/cross-index-resolution)
6. **Scoping Resolution** *&#8592; You are here.*

---


# <a name="scoping-resolution"></a>Scoping Resolution

A resolution job will attempt to run every resolver for every index in the
entity model, unless otherwise instructed. If you use the same entity model for
multiple applications, then you might need only some of the resolvers or indices
for each application. You can limit the scope of a resolution job to the
resolvers and indices that apply to a given use case. This will prevent
unnecessary searches, omit unnecessary results, optimize the performance of your
resolution jobs, and minimize the load on your cluster.

This tutorial shows how you can scope a resolution job to prevent unnecessary
searches.

Let's dive in.

> **Before you start**
> 
> You must install [Elasticsearch](https://www.elastic.co/downloads/elasticsearch),
> [Kibana](https://www.elastic.co/downloads/kibana), and [zentity](/docs/installation)
> to complete this tutorial. This tutorial was tested with
> [zentity-{$ tutorial.zentity $}-elasticsearch-{$ tutorial.elasticsearch $}](/releases#zentity-{$ tutorial.zentity $}).
> 
> **Quick start**
> 
> You can use the [zentity sandbox](/sandbox) which has the required software
> and data for these tutorials. This will let you skip many of the setup steps.


## <a name="prepare"></a>1. Prepare for the tutorial


### <a name="install-required-plugins"></a>1.1 Install the required plugins

> **Note:** Skip this step if you're using the [zentity sandbox](/sandbox).

This tutorial uses the [phonetic analysis plugin](https://www.elastic.co/guide/en/elasticsearch/plugins/current/analysis-phonetic.html)
and [ICU analysis plugin](https://www.elastic.co/guide/en/elasticsearch/plugins/current/analysis-icu.html)
for Elasticsearch. You will need to stop Elasticsearch, install these plugin,
and start Elasticsearch. You can learn more about Elasticsearch plugin management
[here](https://www.elastic.co/guide/en/elasticsearch/plugins/current/plugin-management.html).

For Linux (in the `$ES_HOME` directory of a .tar.gz installation):

```sh
sudo bin/elasticsearch-plugin install analysis-phonetic
sudo bin/elasticsearch-plugin install analysis-icu
```

For Windows (in the `$ES_HOME` directory of a .zip installation):

```sh
bin/elasticsearch-plugin.bat install analysis-phonetic
bin/elasticsearch-plugin.bat install analysis-icu
```


### <a name="open-kibana-console-ui"></a>1.2 Open the Kibana Console UI

The [Kibana Console UI](https://www.elastic.co/guide/en/kibana/current/console-kibana.html)
makes it easy to submit requests to Elasticsearch and read responses.


### <a name="delete-old-tutorial-indices"></a>1.3 Delete any old tutorial indices

> **Note:** Skip this step if you're using the [zentity sandbox](/sandbox).

Let's start from scratch. Delete any tutorial indices you might have created
from other tutorials.

```javascript
DELETE zentity_tutorial_5_*
```


### <a name="create-tutorial-index"></a>1.4 Create the tutorial index

> **Note:** Skip this step if you're using the [zentity sandbox](/sandbox).

Now create the indices for this tutorial. This is the same data used in the
prior tutorial on [cross index resolution](/docs/basic-usage/cross-index-resolution).

**Index A**

```javascript
PUT zentity_tutorial_5_cross_index_resolution_a
{
  "settings": {
    "index": {
      "number_of_shards": 1,
      "number_of_replicas": 0,
      "analysis" : {
        "filter" : {
          "street_suffix_map" : {
            "pattern" : "(st)",
            "type" : "pattern_replace",
            "replacement" : "street"
          },
          "phonetic" : {
            "type" : "phonetic",
            "encoder" : "nysiis"
          },
          "punct_white" : {
            "pattern" : "\\p{Punct}",
            "type" : "pattern_replace",
            "replacement" : " "
          },
          "remove_non_digits" : {
            "pattern" : "[^\\d]",
            "type" : "pattern_replace",
            "replacement" : ""
          }
        },
        "analyzer" : {
          "name_clean" : {
            "filter" : [
              "icu_normalizer",
              "icu_folding",
              "punct_white"
            ],
            "tokenizer" : "standard"
          },
          "name_phonetic" : {
            "filter" : [
              "icu_normalizer",
              "icu_folding",
              "punct_white",
              "phonetic"
            ],
            "tokenizer" : "standard"
          },
          "street_clean" : {
            "filter" : [
              "icu_normalizer",
              "icu_folding",
              "punct_white",
              "trim"
            ],
            "tokenizer" : "keyword"
          },
          "phone_clean" : {
            "filter" : [
              "remove_non_digits"
            ],
            "tokenizer" : "keyword"
          }
        }
      }
    }
  },
  "mappings": {
    "properties": {
      "id_a": {
        "type": "keyword"
      },
      "first_name_a": {
        "type": "text",
        "fields": {
          "clean": {
            "type": "text",
            "analyzer": "name_clean"
          },
          "phonetic": {
            "type": "text",
            "analyzer": "name_phonetic"
          }
        }
      },
      "last_name_a": {
        "type": "text",
        "fields": {
          "clean": {
            "type": "text",
            "analyzer": "name_clean"
          },
          "phonetic": {
            "type": "text",
            "analyzer": "name_phonetic"
          }
        }
      },
      "street_a": {
        "type": "text",
        "fields": {
          "clean": {
            "type": "text",
            "analyzer": "street_clean"
          }
        }
      },
      "city_a": {
        "type": "text",
        "fields": {
          "clean": {
            "type": "text",
            "analyzer": "name_clean"
          }
        }
      },
      "state_a": {
        "type": "text",
        "fields": {
          "keyword": {
            "type": "keyword"
          }
        }
      },
      "phone_a": {
        "type": "text",
        "fields": {
          "clean": {
            "type": "text",
            "analyzer": "phone_clean"
          }
        }
      },
      "email_a": {
        "type": "text",
        "fields": {
          "keyword": {
            "type": "keyword"
          }
        }
      }
    }
  }
}
```

**Index B**

<span class="code-overflow"></span>
```javascript
PUT zentity_tutorial_5_cross_index_resolution_b
{
  "settings": {
    "index": {
      "number_of_shards": 1,
      "number_of_replicas": 0,
      "analysis" : {
        "filter" : {
          "street_suffix_map" : {
            "pattern" : "(st)",
            "type" : "pattern_replace",
            "replacement" : "street"
          },
          "phonetic" : {
            "type" : "phonetic",
            "encoder" : "nysiis"
          },
          "punct_white" : {
            "pattern" : "\\p{Punct}",
            "type" : "pattern_replace",
            "replacement" : " "
          },
          "remove_non_digits" : {
            "pattern" : "[^\\d]",
            "type" : "pattern_replace",
            "replacement" : ""
          }
        },
        "analyzer" : {
          "name_clean" : {
            "filter" : [
              "icu_normalizer",
              "icu_folding",
              "punct_white"
            ],
            "tokenizer" : "standard"
          },
          "name_phonetic" : {
            "filter" : [
              "icu_normalizer",
              "icu_folding",
              "punct_white",
              "phonetic"
            ],
            "tokenizer" : "standard"
          },
          "street_clean" : {
            "filter" : [
              "icu_normalizer",
              "icu_folding",
              "punct_white",
              "trim"
            ],
            "tokenizer" : "keyword"
          },
          "phone_clean" : {
            "filter" : [
              "remove_non_digits"
            ],
            "tokenizer" : "keyword"
          }
        }
      }
    }
  },
  "mappings": {
    "properties": {
      "id_b": {
        "type": "keyword"
      },
      "first_name_b": {
        "type": "text",
        "fields": {
          "clean": {
            "type": "text",
            "analyzer": "name_clean"
          },
          "phonetic": {
            "type": "text",
            "analyzer": "name_phonetic"
          }
        }
      },
      "last_name_b": {
        "type": "text",
        "fields": {
          "clean": {
            "type": "text",
            "analyzer": "name_clean"
          },
          "phonetic": {
            "type": "text",
            "analyzer": "name_phonetic"
          }
        }
      },
      "street_b": {
        "type": "text",
        "fields": {
          "clean": {
            "type": "text",
            "analyzer": "street_clean"
          }
        }
      },
      "city_b": {
        "type": "text",
        "fields": {
          "clean": {
            "type": "text",
            "analyzer": "name_clean"
          }
        }
      },
      "state_b": {
        "type": "text",
        "fields": {
          "keyword": {
            "type": "keyword"
          }
        }
      },
      "phone_b": {
        "type": "text",
        "fields": {
          "clean": {
            "type": "text",
            "analyzer": "phone_clean"
          }
        }
      },
      "email_b": {
        "type": "text",
        "fields": {
          "keyword": {
            "type": "keyword"
          }
        }
      }
    }
  }
}
```


### <a name="load-tutorial-data"></a>1.5 Load the tutorial data

> **Note:** Skip this step if you're using the [zentity sandbox](/sandbox).

Add the tutorial data to the index. This is the same data used in the prior
tutorial on [cross index resolution](/docs/basic-usage/cross-index-resolution).

```javascript
POST _bulk?refresh
{"index": {"_id": "1", "_index": "zentity_tutorial_5_cross_index_resolution_a"}}
{"city_a": "Washington", "email_a": "allie@example.net", "first_name_a": "Allie", "id_a": "1", "last_name_a": "Jones", "phone_a": "202-555-1234", "state_a": "DC", "street_a": "123 Main St"}
{"index": {"_id": "2", "_index": "zentity_tutorial_5_cross_index_resolution_b"}}
{"city_b": "Washington", "email_b": "", "first_name_b": "Alicia", "id_b": "2", "last_name_b": "Johnson", "phone_b": "202-123-4567", "state_b": "DC", "street_b": "300 Main St"}
{"index": {"_id": "3", "_index": "zentity_tutorial_5_cross_index_resolution_a"}}
{"city_a": "Washington", "email_a": "", "first_name_a": "Allie", "id_a": "3", "last_name_a": "Jones", "phone_a": "", "state_a": "DC", "street_a": "123 Main St"}
{"index": {"_id": "4", "_index": "zentity_tutorial_5_cross_index_resolution_b"}}
{"city_b": "", "email_b": "", "first_name_b": "Ally", "id_b": "4", "last_name_b": "Joans", "phone_b": "202-555-1234", "state_b": "", "street_b": ""}
{"index": {"_id": "5", "_index": "zentity_tutorial_5_cross_index_resolution_a"}}
{"city_a": "Arlington", "email_a": "ej@example.net", "first_name_a": "Eli", "id_a": "5", "last_name_a": "Jonas", "phone_a": "", "state_a": "VA", "street_a": "500 23rd Street"}
{"index": {"_id": "6", "_index": "zentity_tutorial_5_cross_index_resolution_b"}}
{"city_b": "Washington", "email_b": "allie@example.net", "first_name_b": "Allison", "id_b": "6", "last_name_b": "Jones", "phone_b": "202-555-1234", "state_b": "DC", "street_b": "123 Main St"}
{"index": {"_id": "7", "_index": "zentity_tutorial_5_cross_index_resolution_a"}}
{"city_a": "Washington", "email_a": "", "first_name_a": "Allison", "id_a": "7", "last_name_a": "Smith", "phone_a": "+1 (202) 555 1234", "state_a": "DC", "street_a": "555 Broad St"}
{"index": {"_id": "8", "_index": "zentity_tutorial_5_cross_index_resolution_b"}}
{"city_b": "Washington", "email_b": "alan.smith@example.net", "first_name_b": "Alan", "id_b": "8", "last_name_b": "Smith", "phone_b": "202-000-5555", "state_b": "DC", "street_b": "555 Broad St"}
{"index": {"_id": "9", "_index": "zentity_tutorial_5_cross_index_resolution_a"}}
{"city_a": "Washington", "email_a": "alan.smith@example.net", "first_name_a": "Alan", "id_a": "9", "last_name_a": "Smith", "phone_a": "2020005555", "state_a": "DC", "street_a": "555 Broad St"}
{"index": {"_id": "10", "_index": "zentity_tutorial_5_cross_index_resolution_b"}}
{"city_b": "Washington", "email_b": "", "first_name_b": "Alison", "id_b": "10", "last_name_b": "Smith", "phone_b": "202-555-9876", "state_b": "DC", "street_b": "555 Broad St"}
{"index": {"_id": "11", "_index": "zentity_tutorial_5_cross_index_resolution_a"}}
{"city_a": "", "email_a": "allie@example.net", "first_name_a": "Alison", "id_a": "11", "last_name_a": "Jones-Smith", "phone_a": "2025559867", "state_a": "", "street_a": ""}
{"index": {"_id": "12", "_index": "zentity_tutorial_5_cross_index_resolution_b"}}
{"city_b": "Washington", "email_b": "allison.j.smith@corp.example.net", "first_name_b": "Allison", "id_b": "12", "last_name_b": "Jones-Smith", "phone_b": "", "state_b": "DC", "street_b": "555 Broad St"}
{"index": {"_id": "13", "_index": "zentity_tutorial_5_cross_index_resolution_a"}}
{"city_a": "Arlington", "email_a": "allison.j.smith@corp.example.net", "first_name_a": "Allison", "id_a": "13", "last_name_a": "Jones Smith", "phone_a": "703-555-5555", "state_a": "VA", "street_a": "1 Corporate Way"}
{"index": {"_id": "14", "_index": "zentity_tutorial_5_cross_index_resolution_b"}}
{"city_b": "Arlington", "email_b": "elise.jonas@corp.example.net", "first_name_b": "Elise", "id_b": "14", "last_name_b": "Jonas", "phone_b": "703-555-5555", "state_b": "VA", "street_b": "1 Corporate Way"}
```

Here's what the tutorial data looks like.

**Index A**

|id_a|first_name_a|last_name_a|street_a|city_a|state_a|phone_a|email_a|
|:---|:---|:---|:---|:---|:---|:---|:---|
|1|Allie|Jones|123 Main St|Washington|DC|202-555-1234|allie@example.net|
|3|Allie|Jones|123 Main St|Washington|DC|||
|5|Eli|Jonas|500 23rd Street|Arlington|VA||ej@example.net|
|7|Allison|Smith|555 Broad St|Washington|DC|+1 (202) 555 1234||
|9|Alan|Smith|555 Broad St|Washington|DC|2020005555|alan.smith@example.net|
|11|Alison|Jones-Smith||||2025559867|allie@example.net|
|13|Allison|Jones Smith|1 Corporate Way|Arlington|VA|703-555-5555|allison.j.smith@corp.example.net|

**Index B**

|id_b|first_name_b|last_name_b|street_b|city_b|state_b|phone_b|email_b|
|:---|:---|:---|:---|:---|:---|:---|:---|
|2|Alicia|Johnson|300 Main St|Washington|DC|202-123-4567||
|4|Ally|Joans||||202-555-1234||
|6|Allison|Jones|123 Main St|Washington|DC|202-555-1234|allie@example.net|
|8|Alan|Smith|555 Broad St|Washington|DC|202-000-5555|alan.smith@example.net|
|10|Alison|Smith|555 Broad St|Washington|DC|202-555-9876||
|12|Allison|Jones-Smith|555 Broad St|Washington|DC||allison.j.smith@corp.example.net|
|14|Elise|Jonas|1 Corporate Way|Arlington|VA|703-555-5555|elise.jonas@corp.example.net|


## <a name="create-entity-model"></a>2. Create the entity model

> **Note:** Skip this step if you're using the [zentity sandbox](/sandbox).

Let's use the [Models API](/docs/rest-apis/models-api) to create the entity
model below. This is the same model used in the prior tutorial on
[cross index resolution](/docs/basic-usage/cross-index-resolution). This
tutorial will show how to omit some of the resolvers and indices during a
resolution job.

**Request**

```javascript
PUT _zentity/models/zentity_tutorial_5_person
{
  "attributes": {
    "first_name": {
      "type": "string"
    },
    "last_name": {
      "type": "string"
    },
    "street": {
      "type": "string"
    },
    "city": {
      "type": "string"
    },
    "state": {
      "type": "string"
    },
    "phone": {
      "type": "string"
    },
    "email": {
      "type": "string"
    }
  },
  "resolvers": {
    "name_street_city_state": {
      "attributes": [ "first_name", "last_name", "street", "city", "state" ]
    },
    "name_phone": {
      "attributes": [ "first_name", "last_name", "phone" ]
    },
    "name_email": {
      "attributes": [ "first_name", "last_name", "email" ]
    },
    "email_phone": {
      "attributes": [ "email", "phone" ]
    }
  },
  "matchers": {
    "simple": {
      "clause": {
        "match": {
          "{{ field }}": "{{ value }}"
        }
      }
    },
    "fuzzy": {
      "clause": {
        "match": {
          "{{ field }}": {
            "query": "{{ value }}",
            "fuzziness": "1"
          }
        }
      }
    },
    "exact": {
      "clause": {
        "term": {
          "{{ field }}": "{{ value }}"
        }
      }
    }
  },
  "indices": {
    "zentity_tutorial_5_cross_index_resolution_a": {
      "fields": {
        "first_name_a.clean": {
          "attribute": "first_name",
          "matcher": "fuzzy"
        },
        "first_name_a.phonetic": {
          "attribute": "first_name",
          "matcher": "simple"
        },
        "last_name_a.clean": {
          "attribute": "last_name",
          "matcher": "fuzzy"
        },
        "last_name_a.phonetic": {
          "attribute": "last_name",
          "matcher": "simple"
        },
        "street_a.clean": {
          "attribute": "street",
          "matcher": "fuzzy"
        },
        "city_a.clean": {
          "attribute": "city",
          "matcher": "fuzzy"
        },
        "state_a.keyword": {
          "attribute": "state",
          "matcher": "exact"
        },
        "phone_a.clean": {
          "attribute": "phone",
          "matcher": "fuzzy"
        },
        "email_a.keyword": {
          "attribute": "email",
          "matcher": "exact"
        }
      }
    },
    "zentity_tutorial_5_cross_index_resolution_b": {
      "fields": {
        "first_name_b.clean": {
          "attribute": "first_name",
          "matcher": "fuzzy"
        },
        "first_name_b.phonetic": {
          "attribute": "first_name",
          "matcher": "simple"
        },
        "last_name_b.clean": {
          "attribute": "last_name",
          "matcher": "fuzzy"
        },
        "last_name_b.phonetic": {
          "attribute": "last_name",
          "matcher": "simple"
        },
        "street_b.clean": {
          "attribute": "street",
          "matcher": "fuzzy"
        },
        "city_b.clean": {
          "attribute": "city",
          "matcher": "fuzzy"
        },
        "state_b.keyword": {
          "attribute": "state",
          "matcher": "exact"
        },
        "phone_b.clean": {
          "attribute": "phone",
          "matcher": "fuzzy"
        },
        "email_b.keyword": {
          "attribute": "email",
          "matcher": "exact"
        }
      }
    }
  }
}
```


## <a name="resolve-entity"></a>3. Resolve an entity


## <a name="resolve-entity-scope-indices"></a>3.1 Control the scope of indices

Let's use the [Resolution API](/docs/rest-apis/resolution-api) to resolve a
person with a known first name, last name, and phone number. These are the same
attributes used in the prior tutorial on [cross index resolution](/docs/basic-usage/cross-index-resolution),
which returned nine results. This time, we are going to control the scope of the
indices searched during the resolution job. Let's limit the job to the
`"zentity_tutorial_5_cross_index_resolution_a"` index.

**Request**

```javascript
POST _zentity/resolution/zentity_tutorial_5_person?pretty&_source=false
{
  "attributes": {
    "first_name": [ "Allie" ],
    "last_name": [ "Jones" ],
    "phone": [ "202-555-1234" ]
  },
  "scope": {
    "include": {
      "indices": [
        "zentity_tutorial_5_cross_index_resolution_a"
      ]
    }
  }
}
```

**Response**

```javascript
{
  "took" : 7,
  "hits" : {
    "total" : 2,
    "hits" : [ {
      "_index" : "zentity_tutorial_5_cross_index_resolution_a",
      "_id" : "1",
      "_hop" : 0,
      "_query" : 0,
      "_attributes" : {
        "city" : [ "Washington" ],
        "email" : [ "allie@example.net" ],
        "first_name" : [ "Allie" ],
        "last_name" : [ "Jones" ],
        "phone" : [ "202-555-1234" ],
        "state" : [ "DC" ],
        "street" : [ "123 Main St" ]
      }
    }, {
      "_index" : "zentity_tutorial_5_cross_index_resolution_a",
      "_id" : "3",
      "_hop" : 1,
      "_query" : 0,
      "_attributes" : {
        "city" : [ "Washington" ],
        "email" : [ "" ],
        "first_name" : [ "Allie" ],
        "last_name" : [ "Jones" ],
        "phone" : [ "" ],
        "state" : [ "DC" ],
        "street" : [ "123 Main St" ]
      }
    } ]
  }
}
```

As expected, we retrieved results only from `"zentity_tutorial_5_cross_index_resolution_a"`.
There are only two results, which is less than the nine results of the prior
tutorial on [cross index resolution](/docs/basic-usage/cross-index-resolution)
because some of those matches required searching both indices.


## <a name="resolve-entity-scope-resolvers"></a>3.2 Control the scope of resolvers

Let's use the [Resolution API](/docs/rest-apis/resolution-api) to resolve a
person with a known first name, last name, and phone number. These are the same
attributes used in the prior tutorial on [cross index resolution](/docs/basic-usage/cross-index-resolution),
which returned nine results. This time, we are going to control the scope of the
resolvers searched during the resolution job. Let's exclude only the
`"name_street_city_state"` resolver. Let's also search across both indices.

**Request**

```javascript
POST _zentity/resolution/zentity_tutorial_5_person?pretty&_source=false
{
  "attributes": {
    "first_name": [ "Allie" ],
    "last_name": [ "Jones" ],
    "phone": [ "202-555-1234" ]
  },
  "scope": {
    "include": {
      "indices": [
        "zentity_tutorial_5_cross_index_resolution_a",
        "zentity_tutorial_5_cross_index_resolution_b"
      ]
    },
    "exclude": {
      "resolvers": [
        "name_street_city_state"
      ]
    }
  }
}
```

**Response**

```javascript
{
  "took" : 42,
  "hits" : {
    "total" : 6,
    "hits" : [ {
      "_index" : "zentity_tutorial_5_cross_index_resolution_a",
      "_id" : "1",
      "_hop" : 0,
      "_query" : 0,
      "_attributes" : {
        "city" : [ "Washington" ],
        "email" : [ "allie@example.net" ],
        "first_name" : [ "Allie" ],
        "last_name" : [ "Jones" ],
        "phone" : [ "202-555-1234" ],
        "state" : [ "DC" ],
        "street" : [ "123 Main St" ]
      }
    }, {
      "_index" : "zentity_tutorial_5_cross_index_resolution_b",
      "_id" : "4",
      "_hop" : 0,
      "_query" : 1,
      "_attributes" : {
        "city" : [ "" ],
        "email" : [ "" ],
        "first_name" : [ "Ally" ],
        "last_name" : [ "Joans" ],
        "phone" : [ "202-555-1234" ],
        "state" : [ "" ],
        "street" : [ "" ]
      }
    }, {
      "_index" : "zentity_tutorial_5_cross_index_resolution_b",
      "_id" : "6",
      "_hop" : 1,
      "_query" : 1,
      "_attributes" : {
        "city" : [ "Washington" ],
        "email" : [ "allie@example.net" ],
        "first_name" : [ "Allison" ],
        "last_name" : [ "Jones" ],
        "phone" : [ "202-555-1234" ],
        "state" : [ "DC" ],
        "street" : [ "123 Main St" ]
      }
    }, {
      "_index" : "zentity_tutorial_5_cross_index_resolution_a",
      "_id" : "11",
      "_hop" : 2,
      "_query" : 0,
      "_attributes" : {
        "city" : [ "" ],
        "email" : [ "allie@example.net" ],
        "first_name" : [ "Alison" ],
        "last_name" : [ "Jones-Smith" ],
        "phone" : [ "2025559867" ],
        "state" : [ "" ],
        "street" : [ "" ]
      }
    }, {
      "_index" : "zentity_tutorial_5_cross_index_resolution_a",
      "_id" : "7",
      "_hop" : 3,
      "_query" : 0,
      "_attributes" : {
        "city" : [ "Washington" ],
        "email" : [ "" ],
        "first_name" : [ "Allison" ],
        "last_name" : [ "Smith" ],
        "phone" : [ "+1 (202) 555 1234" ],
        "state" : [ "DC" ],
        "street" : [ "555 Broad St" ]
      }
    }, {
      "_index" : "zentity_tutorial_5_cross_index_resolution_b",
      "_id" : "10",
      "_hop" : 3,
      "_query" : 1,
      "_attributes" : {
        "city" : [ "Washington" ],
        "email" : [ "" ],
        "first_name" : [ "Alison" ],
        "last_name" : [ "Smith" ],
        "phone" : [ "202-555-9876" ],
        "state" : [ "DC" ],
        "street" : [ "555 Broad St" ]
      }
    } ]
  }
}
```

This time we retrieved six results total from two indices, which is less than
the nine results of the prior tutorial on [cross index resolution](/docs/basic-usage/cross-index-resolution)
because some of those matches required using the `"name_street_city_state"`
resolver that we excluded in this job.

> **Tip**
> 
> If you want to include all indices in your resolution job, then you can omit
> `"scope.include.indices"` altogether as we did in prior tutorials. But when
> you begin to use the same entity model for different applications, then you
> might not need to search every index in every application. As a best pratice,
> use `"scope.include.indices"` to prevent unnecessary searches and results.
> Conversely, as a best pratice, use `"scope.exclude.resolvers"` and
> `"scope.exclude.attributes"` to exclude unnecessary details about the entity.
> You can be more liberal with your use of resolvers and attributes, because
> they will only be used for the indices that support them.


## <a name="conclusion"></a>Conclusion

Congratulations! You learned how to resolve an entity using a controlled scope
of indices and resolvers. This is an important concept to understand and
implement when you use zentity in production.


&nbsp;

----

#### Continue Reading

|&#8249;|[Cross Index Resolution](/docs/basic-usage/cross-index-resolution)|[Advanced Usage](/docs/advanced-usage)|&#8250;|
|:---|:---|---:|---:|
|    |    |    |    |
