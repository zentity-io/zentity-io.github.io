[Home](/) / [Documentation](/docs) / [Basic Usage](/docs/basic-usage) / Cross Index Resolution


#### <a name="contents"></a>Basic Usage Tutorials 📖

This tutorial is part of a series to help you learn and perform the basic
functions of zentity. Each tutorial adds a little more sophistication to the
prior tutorials, so you can start simple and learn the more advanced features
over time.

1. [Exact Name Matching](/docs/basic-usage/exact-name-matching)
2. [Robust Name Matching](/docs/basic-usage/robust-name-matching)
3. [Multiple Attribute Resolution](/docs/basic-usage/multiple-attribute-resolution)
4. [Multiple Resolver Resolution](/docs/basic-usage/multiple-resolver-resolution)
5. **Cross Index Resolution** *&#8592; You are here.*
6. [Scoping Resolution](/docs/basic-usage/scoping-resolution)

---


# <a name="cross-index-resolution"></a>Cross Index Resolution

Many applications of entity resolution require matching records that are
scattered across multiple data sets. One application might be to profile
everything known about a customer, patient, or employee across different
business systems. Another might be to see if a person or organization is present
in one or more blacklists.

This tutorial adds more sophistication to the prior tutorial on
[multiple resolver resolution](/docs/basic-usage/multiple-resolver-resolution).
This time you will map **multiple combinations of attributes**
(i.e. "resolvers") to **multiple fields** of **multiple indices**.


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

Now create the indices for this tutorial.

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

Add the tutorial data to the index.

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
model below. We'll review each part of the model in depth.

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


### <a name="review-attributes"></a>2.1 Review the attributes

We defined five attributes as shown in this section:

```javascript
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
  }
}
```


### <a name="review-resolvers"></a>2.2 Review the resolvers

We defined four resolvers as shown in this section:

```javascript
{
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
  }
}
```


### <a name="review-matchers"></a>2.3 Review the matchers

We defined three matchers called `"simple"`, `"fuzzy"`, and `"exact"` as shown
in this section:

```javascript
{
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
  }
}
```


### <a name="review-indices"></a>2.4 Review the indices

We defined a two indices as shown in this section:

```javascript
{
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


### <a name="resolve-entity-basic"></a>3.1 Run a basic resolution job

Let's use the [Resolution API](/docs/rest-apis/resolution-api) to resolve a
person with a known first name, last name, and phone number.

**Request**

```javascript
POST _zentity/resolution/zentity_tutorial_5_person?pretty&_source=false
{
  "attributes": {
    "first_name": [ "Allie" ],
    "last_name": [ "Jones" ],
    "phone": [ "202-555-1234" ]
  }
}
```

**Response**

```javascript
{
  "took" : 64,
  "hits" : {
    "total" : 9,
    "hits" : [ {
      "_index" : "zentity_tutorial_5_cross_index_resolution_a",
      "_type" : "_doc",
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
      "_type" : "_doc",
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
      "_index" : "zentity_tutorial_5_cross_index_resolution_a",
      "_type" : "_doc",
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
    }, {
      "_index" : "zentity_tutorial_5_cross_index_resolution_b",
      "_type" : "_doc",
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
      "_type" : "_doc",
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
      "_type" : "_doc",
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
      "_type" : "_doc",
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
    }, {
      "_index" : "zentity_tutorial_5_cross_index_resolution_b",
      "_type" : "_doc",
      "_id" : "12",
      "_hop" : 4,
      "_query" : 1,
      "_attributes" : {
        "city" : [ "Washington" ],
        "email" : [ "allison.j.smith@corp.example.net" ],
        "first_name" : [ "Allison" ],
        "last_name" : [ "Jones-Smith" ],
        "phone" : [ "" ],
        "state" : [ "DC" ],
        "street" : [ "555 Broad St" ]
      }
    }, {
      "_index" : "zentity_tutorial_5_cross_index_resolution_a",
      "_type" : "_doc",
      "_id" : "13",
      "_hop" : 5,
      "_query" : 0,
      "_attributes" : {
        "city" : [ "Arlington" ],
        "email" : [ "allison.j.smith@corp.example.net" ],
        "first_name" : [ "Allison" ],
        "last_name" : [ "Jones Smith" ],
        "phone" : [ "703-555-5555" ],
        "state" : [ "VA" ],
        "street" : [ "1 Corporate Way" ]
      }
    } ]
  }
}
```

As expected, we retrieved the same results as the prior tutorial on
[multiple resolver resolution](/docs/basic-usage/multiple-resolver-resolution)
even though the documents were separated into two indices. These are shown in
the `"_index"`, `"_hop"`, and `"_query"` fields.


### <a name="resolve-entity-source"></a>3.2 Show the `"_source"`

We can include the original values of each document as they exist in
Elasticsearch.

Let's run the job again, and now let's include the [`"_source"`](/docs/entity-resolution/output-specification/#hits.hits._source)
field of each document. The [`"_source"`](https://www.elastic.co/guide/en/elasticsearch/reference/current/mapping-source-field.html)
field is the original JSON document that's stored in an Elasticsearch index.

**Request**

```javascript
POST _zentity/resolution/zentity_tutorial_5_person?pretty&_source=true
{
  "attributes": {
    "first_name": [ "Allie" ],
    "last_name": [ "Jones" ],
    "phone": [ "202-555-1234" ]
  }
}
```

**Response**

```javascript
{
  "took" : 62,
  "hits" : {
    "total" : 9,
    "hits" : [ {
      "_index" : "zentity_tutorial_5_cross_index_resolution_a",
      "_type" : "_doc",
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
      },
      "_source" : {
        "city_a" : "Washington",
        "email_a" : "allie@example.net",
        "first_name_a" : "Allie",
        "id_a" : "1",
        "last_name_a" : "Jones",
        "phone_a" : "202-555-1234",
        "state_a" : "DC",
        "street_a" : "123 Main St"
      }
    }, {
      "_index" : "zentity_tutorial_5_cross_index_resolution_b",
      "_type" : "_doc",
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
      },
      "_source" : {
        "city_b" : "",
        "email_b" : "",
        "first_name_b" : "Ally",
        "id_b" : "4",
        "last_name_b" : "Joans",
        "phone_b" : "202-555-1234",
        "state_b" : "",
        "street_b" : ""
      }
    }, {
      "_index" : "zentity_tutorial_5_cross_index_resolution_a",
      "_type" : "_doc",
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
      },
      "_source" : {
        "city_a" : "Washington",
        "email_a" : "",
        "first_name_a" : "Allie",
        "id_a" : "3",
        "last_name_a" : "Jones",
        "phone_a" : "",
        "state_a" : "DC",
        "street_a" : "123 Main St"
      }
    }, {
      "_index" : "zentity_tutorial_5_cross_index_resolution_b",
      "_type" : "_doc",
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
      },
      "_source" : {
        "city_b" : "Washington",
        "email_b" : "allie@example.net",
        "first_name_b" : "Allison",
        "id_b" : "6",
        "last_name_b" : "Jones",
        "phone_b" : "202-555-1234",
        "state_b" : "DC",
        "street_b" : "123 Main St"
      }
    }, {
      "_index" : "zentity_tutorial_5_cross_index_resolution_a",
      "_type" : "_doc",
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
      },
      "_source" : {
        "city_a" : "",
        "email_a" : "allie@example.net",
        "first_name_a" : "Alison",
        "id_a" : "11",
        "last_name_a" : "Jones-Smith",
        "phone_a" : "2025559867",
        "state_a" : "",
        "street_a" : ""
      }
    }, {
      "_index" : "zentity_tutorial_5_cross_index_resolution_a",
      "_type" : "_doc",
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
      },
      "_source" : {
        "city_a" : "Washington",
        "email_a" : "",
        "first_name_a" : "Allison",
        "id_a" : "7",
        "last_name_a" : "Smith",
        "phone_a" : "+1 (202) 555 1234",
        "state_a" : "DC",
        "street_a" : "555 Broad St"
      }
    }, {
      "_index" : "zentity_tutorial_5_cross_index_resolution_b",
      "_type" : "_doc",
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
      },
      "_source" : {
        "city_b" : "Washington",
        "email_b" : "",
        "first_name_b" : "Alison",
        "id_b" : "10",
        "last_name_b" : "Smith",
        "phone_b" : "202-555-9876",
        "state_b" : "DC",
        "street_b" : "555 Broad St"
      }
    }, {
      "_index" : "zentity_tutorial_5_cross_index_resolution_b",
      "_type" : "_doc",
      "_id" : "12",
      "_hop" : 4,
      "_query" : 1,
      "_attributes" : {
        "city" : [ "Washington" ],
        "email" : [ "allison.j.smith@corp.example.net" ],
        "first_name" : [ "Allison" ],
        "last_name" : [ "Jones-Smith" ],
        "phone" : [ "" ],
        "state" : [ "DC" ],
        "street" : [ "555 Broad St" ]
      },
      "_source" : {
        "city_b" : "Washington",
        "email_b" : "allison.j.smith@corp.example.net",
        "first_name_b" : "Allison",
        "id_b" : "12",
        "last_name_b" : "Jones-Smith",
        "phone_b" : "",
        "state_b" : "DC",
        "street_b" : "555 Broad St"
      }
    }, {
      "_index" : "zentity_tutorial_5_cross_index_resolution_a",
      "_type" : "_doc",
      "_id" : "13",
      "_hop" : 5,
      "_query" : 0,
      "_attributes" : {
        "city" : [ "Arlington" ],
        "email" : [ "allison.j.smith@corp.example.net" ],
        "first_name" : [ "Allison" ],
        "last_name" : [ "Jones Smith" ],
        "phone" : [ "703-555-5555" ],
        "state" : [ "VA" ],
        "street" : [ "1 Corporate Way" ]
      },
      "_source" : {
        "city_a" : "Arlington",
        "email_a" : "allison.j.smith@corp.example.net",
        "first_name_a" : "Allison",
        "id_a" : "13",
        "last_name_a" : "Jones Smith",
        "phone_a" : "703-555-5555",
        "state_a" : "VA",
        "street_a" : "1 Corporate Way"
      }
    } ]
  }
}
```

Notice how the `"_attributes"` of each result have the same field names
regardless of which index the documents came from. The `"_source"` fields show
the original names of the fields as they exist in the indices. This mapping of
the source field names to the canonical attribute names allows you to access
their under as a common schema. This makes it much easier to analyze the values
of the entity.


### <a name="resolve-entity-explanation"></a>3.3 Show the `"_explanation"`

We can learn how the documents matched, too.

Let's run the job again, and now let's include the [`"_explanation"`](/docs/entity-resolution/output-specification/#hits.hits._explanation)
field to see exactly why each document matched. The `"_explanation"` field tells
us which resolvers caused a document to match, and more specifically, which
input value matched which indexed value using which matcher and any parameters.

**Request**

```javascript
POST _zentity/resolution/zentity_tutorial_5_person?pretty&_source=true&_explanation=true
{
  "attributes": {
    "first_name": [ "Allie" ],
    "last_name": [ "Jones" ],
    "phone": [ "202-555-1234" ]
  }
}
```

**Response**

```javascript
{
  "took" : 77,
  "hits" : {
    "total" : 9,
    "hits" : [ {
      "_index" : "zentity_tutorial_5_cross_index_resolution_a",
      "_type" : "_doc",
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
      },
      "_explanation" : {
        "resolvers" : {
          "name_phone" : {
            "attributes" : [ "first_name", "last_name", "phone" ]
          }
        },
        "matches" : [ {
          "attribute" : "first_name",
          "target_field" : "first_name_a.clean",
          "target_value" : "Allie",
          "input_value" : "Allie",
          "input_matcher" : "fuzzy",
          "input_matcher_params" : { }
        }, {
          "attribute" : "first_name",
          "target_field" : "first_name_a.phonetic",
          "target_value" : "Allie",
          "input_value" : "Allie",
          "input_matcher" : "simple",
          "input_matcher_params" : { }
        }, {
          "attribute" : "last_name",
          "target_field" : "last_name_a.clean",
          "target_value" : "Jones",
          "input_value" : "Jones",
          "input_matcher" : "fuzzy",
          "input_matcher_params" : { }
        }, {
          "attribute" : "last_name",
          "target_field" : "last_name_a.phonetic",
          "target_value" : "Jones",
          "input_value" : "Jones",
          "input_matcher" : "simple",
          "input_matcher_params" : { }
        }, {
          "attribute" : "phone",
          "target_field" : "phone_a.clean",
          "target_value" : "202-555-1234",
          "input_value" : "202-555-1234",
          "input_matcher" : "fuzzy",
          "input_matcher_params" : { }
        } ]
      },
      "_source" : {
        "city_a" : "Washington",
        "email_a" : "allie@example.net",
        "first_name_a" : "Allie",
        "id_a" : "1",
        "last_name_a" : "Jones",
        "phone_a" : "202-555-1234",
        "state_a" : "DC",
        "street_a" : "123 Main St"
      }
    }, {
      "_index" : "zentity_tutorial_5_cross_index_resolution_b",
      "_type" : "_doc",
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
      },
      "_explanation" : {
        "resolvers" : {
          "name_phone" : {
            "attributes" : [ "first_name", "last_name", "phone" ]
          }
        },
        "matches" : [ {
          "attribute" : "first_name",
          "target_field" : "first_name_b.phonetic",
          "target_value" : "Ally",
          "input_value" : "Allie",
          "input_matcher" : "simple",
          "input_matcher_params" : { }
        }, {
          "attribute" : "last_name",
          "target_field" : "last_name_b.phonetic",
          "target_value" : "Joans",
          "input_value" : "Jones",
          "input_matcher" : "simple",
          "input_matcher_params" : { }
        }, {
          "attribute" : "phone",
          "target_field" : "phone_b.clean",
          "target_value" : "202-555-1234",
          "input_value" : "202-555-1234",
          "input_matcher" : "fuzzy",
          "input_matcher_params" : { }
        } ]
      },
      "_source" : {
        "city_b" : "",
        "email_b" : "",
        "first_name_b" : "Ally",
        "id_b" : "4",
        "last_name_b" : "Joans",
        "phone_b" : "202-555-1234",
        "state_b" : "",
        "street_b" : ""
      }
    }, {
      "_index" : "zentity_tutorial_5_cross_index_resolution_a",
      "_type" : "_doc",
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
      },
      "_explanation" : {
        "resolvers" : {
          "name_street_city_state" : {
            "attributes" : [ "city", "first_name", "last_name", "state", "street" ]
          }
        },
        "matches" : [ {
          "attribute" : "city",
          "target_field" : "city_a.clean",
          "target_value" : "Washington",
          "input_value" : "Washington",
          "input_matcher" : "fuzzy",
          "input_matcher_params" : { }
        }, {
          "attribute" : "first_name",
          "target_field" : "first_name_a.clean",
          "target_value" : "Allie",
          "input_value" : "Allie",
          "input_matcher" : "fuzzy",
          "input_matcher_params" : { }
        }, {
          "attribute" : "first_name",
          "target_field" : "first_name_a.phonetic",
          "target_value" : "Allie",
          "input_value" : "Allie",
          "input_matcher" : "simple",
          "input_matcher_params" : { }
        }, {
          "attribute" : "first_name",
          "target_field" : "first_name_a.phonetic",
          "target_value" : "Allie",
          "input_value" : "Ally",
          "input_matcher" : "simple",
          "input_matcher_params" : { }
        }, {
          "attribute" : "last_name",
          "target_field" : "last_name_a.clean",
          "target_value" : "Jones",
          "input_value" : "Jones",
          "input_matcher" : "fuzzy",
          "input_matcher_params" : { }
        }, {
          "attribute" : "last_name",
          "target_field" : "last_name_a.phonetic",
          "target_value" : "Jones",
          "input_value" : "Joans",
          "input_matcher" : "simple",
          "input_matcher_params" : { }
        }, {
          "attribute" : "last_name",
          "target_field" : "last_name_a.phonetic",
          "target_value" : "Jones",
          "input_value" : "Jones",
          "input_matcher" : "simple",
          "input_matcher_params" : { }
        }, {
          "attribute" : "state",
          "target_field" : "state_a.keyword",
          "target_value" : "DC",
          "input_value" : "DC",
          "input_matcher" : "exact",
          "input_matcher_params" : { }
        }, {
          "attribute" : "street",
          "target_field" : "street_a.clean",
          "target_value" : "123 Main St",
          "input_value" : "123 Main St",
          "input_matcher" : "fuzzy",
          "input_matcher_params" : { }
        } ]
      },
      "_source" : {
        "city_a" : "Washington",
        "email_a" : "",
        "first_name_a" : "Allie",
        "id_a" : "3",
        "last_name_a" : "Jones",
        "phone_a" : "",
        "state_a" : "DC",
        "street_a" : "123 Main St"
      }
    }, {
      "_index" : "zentity_tutorial_5_cross_index_resolution_b",
      "_type" : "_doc",
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
      },
      "_explanation" : {
        "resolvers" : {
          "email_phone" : {
            "attributes" : [ "email", "phone" ]
          }
        },
        "matches" : [ {
          "attribute" : "city",
          "target_field" : "city_b.clean",
          "target_value" : "Washington",
          "input_value" : "Washington",
          "input_matcher" : "fuzzy",
          "input_matcher_params" : { }
        }, {
          "attribute" : "email",
          "target_field" : "email_b.keyword",
          "target_value" : "allie@example.net",
          "input_value" : "allie@example.net",
          "input_matcher" : "exact",
          "input_matcher_params" : { }
        }, {
          "attribute" : "last_name",
          "target_field" : "last_name_b.clean",
          "target_value" : "Jones",
          "input_value" : "Jones",
          "input_matcher" : "fuzzy",
          "input_matcher_params" : { }
        }, {
          "attribute" : "last_name",
          "target_field" : "last_name_b.phonetic",
          "target_value" : "Jones",
          "input_value" : "Joans",
          "input_matcher" : "simple",
          "input_matcher_params" : { }
        }, {
          "attribute" : "last_name",
          "target_field" : "last_name_b.phonetic",
          "target_value" : "Jones",
          "input_value" : "Jones",
          "input_matcher" : "simple",
          "input_matcher_params" : { }
        }, {
          "attribute" : "phone",
          "target_field" : "phone_b.clean",
          "target_value" : "202-555-1234",
          "input_value" : "202-555-1234",
          "input_matcher" : "fuzzy",
          "input_matcher_params" : { }
        }, {
          "attribute" : "state",
          "target_field" : "state_b.keyword",
          "target_value" : "DC",
          "input_value" : "DC",
          "input_matcher" : "exact",
          "input_matcher_params" : { }
        }, {
          "attribute" : "street",
          "target_field" : "street_b.clean",
          "target_value" : "123 Main St",
          "input_value" : "123 Main St",
          "input_matcher" : "fuzzy",
          "input_matcher_params" : { }
        } ]
      },
      "_source" : {
        "city_b" : "Washington",
        "email_b" : "allie@example.net",
        "first_name_b" : "Allison",
        "id_b" : "6",
        "last_name_b" : "Jones",
        "phone_b" : "202-555-1234",
        "state_b" : "DC",
        "street_b" : "123 Main St"
      }
    }, {
      "_index" : "zentity_tutorial_5_cross_index_resolution_a",
      "_type" : "_doc",
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
      },
      "_explanation" : {
        "resolvers" : {
          "name_email" : {
            "attributes" : [ "email", "first_name", "last_name" ]
          }
        },
        "matches" : [ {
          "attribute" : "email",
          "target_field" : "email_a.keyword",
          "target_value" : "allie@example.net",
          "input_value" : "allie@example.net",
          "input_matcher" : "exact",
          "input_matcher_params" : { }
        }, {
          "attribute" : "first_name",
          "target_field" : "first_name_a.clean",
          "target_value" : "Alison",
          "input_value" : "Allison",
          "input_matcher" : "fuzzy",
          "input_matcher_params" : { }
        }, {
          "attribute" : "first_name",
          "target_field" : "first_name_a.phonetic",
          "target_value" : "Alison",
          "input_value" : "Allison",
          "input_matcher" : "simple",
          "input_matcher_params" : { }
        }, {
          "attribute" : "last_name",
          "target_field" : "last_name_a.clean",
          "target_value" : "Jones-Smith",
          "input_value" : "Jones",
          "input_matcher" : "fuzzy",
          "input_matcher_params" : { }
        }, {
          "attribute" : "last_name",
          "target_field" : "last_name_a.phonetic",
          "target_value" : "Jones-Smith",
          "input_value" : "Joans",
          "input_matcher" : "simple",
          "input_matcher_params" : { }
        }, {
          "attribute" : "last_name",
          "target_field" : "last_name_a.phonetic",
          "target_value" : "Jones-Smith",
          "input_value" : "Jones",
          "input_matcher" : "simple",
          "input_matcher_params" : { }
        } ]
      },
      "_source" : {
        "city_a" : "",
        "email_a" : "allie@example.net",
        "first_name_a" : "Alison",
        "id_a" : "11",
        "last_name_a" : "Jones-Smith",
        "phone_a" : "2025559867",
        "state_a" : "",
        "street_a" : ""
      }
    }, {
      "_index" : "zentity_tutorial_5_cross_index_resolution_a",
      "_type" : "_doc",
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
      },
      "_explanation" : {
        "resolvers" : {
          "name_phone" : {
            "attributes" : [ "first_name", "last_name", "phone" ]
          }
        },
        "matches" : [ {
          "attribute" : "city",
          "target_field" : "city_a.clean",
          "target_value" : "Washington",
          "input_value" : "Washington",
          "input_matcher" : "fuzzy",
          "input_matcher_params" : { }
        }, {
          "attribute" : "first_name",
          "target_field" : "first_name_a.clean",
          "target_value" : "Allison",
          "input_value" : "Alison",
          "input_matcher" : "fuzzy",
          "input_matcher_params" : { }
        }, {
          "attribute" : "first_name",
          "target_field" : "first_name_a.clean",
          "target_value" : "Allison",
          "input_value" : "Allison",
          "input_matcher" : "fuzzy",
          "input_matcher_params" : { }
        }, {
          "attribute" : "first_name",
          "target_field" : "first_name_a.phonetic",
          "target_value" : "Allison",
          "input_value" : "Alison",
          "input_matcher" : "simple",
          "input_matcher_params" : { }
        }, {
          "attribute" : "first_name",
          "target_field" : "first_name_a.phonetic",
          "target_value" : "Allison",
          "input_value" : "Allison",
          "input_matcher" : "simple",
          "input_matcher_params" : { }
        }, {
          "attribute" : "last_name",
          "target_field" : "last_name_a.clean",
          "target_value" : "Smith",
          "input_value" : "Jones-Smith",
          "input_matcher" : "fuzzy",
          "input_matcher_params" : { }
        }, {
          "attribute" : "last_name",
          "target_field" : "last_name_a.phonetic",
          "target_value" : "Smith",
          "input_value" : "Jones-Smith",
          "input_matcher" : "simple",
          "input_matcher_params" : { }
        }, {
          "attribute" : "phone",
          "target_field" : "phone_a.clean",
          "target_value" : "+1 (202) 555 1234",
          "input_value" : "202-555-1234",
          "input_matcher" : "fuzzy",
          "input_matcher_params" : { }
        }, {
          "attribute" : "state",
          "target_field" : "state_a.keyword",
          "target_value" : "DC",
          "input_value" : "DC",
          "input_matcher" : "exact",
          "input_matcher_params" : { }
        } ]
      },
      "_source" : {
        "city_a" : "Washington",
        "email_a" : "",
        "first_name_a" : "Allison",
        "id_a" : "7",
        "last_name_a" : "Smith",
        "phone_a" : "+1 (202) 555 1234",
        "state_a" : "DC",
        "street_a" : "555 Broad St"
      }
    }, {
      "_index" : "zentity_tutorial_5_cross_index_resolution_b",
      "_type" : "_doc",
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
      },
      "_explanation" : {
        "resolvers" : {
          "name_phone" : {
            "attributes" : [ "first_name", "last_name", "phone" ]
          }
        },
        "matches" : [ {
          "attribute" : "city",
          "target_field" : "city_b.clean",
          "target_value" : "Washington",
          "input_value" : "Washington",
          "input_matcher" : "fuzzy",
          "input_matcher_params" : { }
        }, {
          "attribute" : "first_name",
          "target_field" : "first_name_b.clean",
          "target_value" : "Alison",
          "input_value" : "Alison",
          "input_matcher" : "fuzzy",
          "input_matcher_params" : { }
        }, {
          "attribute" : "first_name",
          "target_field" : "first_name_b.clean",
          "target_value" : "Alison",
          "input_value" : "Allison",
          "input_matcher" : "fuzzy",
          "input_matcher_params" : { }
        }, {
          "attribute" : "first_name",
          "target_field" : "first_name_b.phonetic",
          "target_value" : "Alison",
          "input_value" : "Alison",
          "input_matcher" : "simple",
          "input_matcher_params" : { }
        }, {
          "attribute" : "first_name",
          "target_field" : "first_name_b.phonetic",
          "target_value" : "Alison",
          "input_value" : "Allison",
          "input_matcher" : "simple",
          "input_matcher_params" : { }
        }, {
          "attribute" : "last_name",
          "target_field" : "last_name_b.clean",
          "target_value" : "Smith",
          "input_value" : "Jones-Smith",
          "input_matcher" : "fuzzy",
          "input_matcher_params" : { }
        }, {
          "attribute" : "last_name",
          "target_field" : "last_name_b.phonetic",
          "target_value" : "Smith",
          "input_value" : "Jones-Smith",
          "input_matcher" : "simple",
          "input_matcher_params" : { }
        }, {
          "attribute" : "phone",
          "target_field" : "phone_b.clean",
          "target_value" : "202-555-9876",
          "input_value" : "2025559867",
          "input_matcher" : "fuzzy",
          "input_matcher_params" : { }
        }, {
          "attribute" : "state",
          "target_field" : "state_b.keyword",
          "target_value" : "DC",
          "input_value" : "DC",
          "input_matcher" : "exact",
          "input_matcher_params" : { }
        } ]
      },
      "_source" : {
        "city_b" : "Washington",
        "email_b" : "",
        "first_name_b" : "Alison",
        "id_b" : "10",
        "last_name_b" : "Smith",
        "phone_b" : "202-555-9876",
        "state_b" : "DC",
        "street_b" : "555 Broad St"
      }
    }, {
      "_index" : "zentity_tutorial_5_cross_index_resolution_b",
      "_type" : "_doc",
      "_id" : "12",
      "_hop" : 4,
      "_query" : 1,
      "_attributes" : {
        "city" : [ "Washington" ],
        "email" : [ "allison.j.smith@corp.example.net" ],
        "first_name" : [ "Allison" ],
        "last_name" : [ "Jones-Smith" ],
        "phone" : [ "" ],
        "state" : [ "DC" ],
        "street" : [ "555 Broad St" ]
      },
      "_explanation" : {
        "resolvers" : {
          "name_street_city_state" : {
            "attributes" : [ "city", "first_name", "last_name", "state", "street" ]
          }
        },
        "matches" : [ {
          "attribute" : "city",
          "target_field" : "city_b.clean",
          "target_value" : "Washington",
          "input_value" : "Washington",
          "input_matcher" : "fuzzy",
          "input_matcher_params" : { }
        }, {
          "attribute" : "first_name",
          "target_field" : "first_name_b.clean",
          "target_value" : "Allison",
          "input_value" : "Alison",
          "input_matcher" : "fuzzy",
          "input_matcher_params" : { }
        }, {
          "attribute" : "first_name",
          "target_field" : "first_name_b.clean",
          "target_value" : "Allison",
          "input_value" : "Allison",
          "input_matcher" : "fuzzy",
          "input_matcher_params" : { }
        }, {
          "attribute" : "first_name",
          "target_field" : "first_name_b.phonetic",
          "target_value" : "Allison",
          "input_value" : "Alison",
          "input_matcher" : "simple",
          "input_matcher_params" : { }
        }, {
          "attribute" : "first_name",
          "target_field" : "first_name_b.phonetic",
          "target_value" : "Allison",
          "input_value" : "Allison",
          "input_matcher" : "simple",
          "input_matcher_params" : { }
        }, {
          "attribute" : "last_name",
          "target_field" : "last_name_b.clean",
          "target_value" : "Jones-Smith",
          "input_value" : "Jones",
          "input_matcher" : "fuzzy",
          "input_matcher_params" : { }
        }, {
          "attribute" : "last_name",
          "target_field" : "last_name_b.clean",
          "target_value" : "Jones-Smith",
          "input_value" : "Jones-Smith",
          "input_matcher" : "fuzzy",
          "input_matcher_params" : { }
        }, {
          "attribute" : "last_name",
          "target_field" : "last_name_b.clean",
          "target_value" : "Jones-Smith",
          "input_value" : "Smith",
          "input_matcher" : "fuzzy",
          "input_matcher_params" : { }
        }, {
          "attribute" : "last_name",
          "target_field" : "last_name_b.phonetic",
          "target_value" : "Jones-Smith",
          "input_value" : "Joans",
          "input_matcher" : "simple",
          "input_matcher_params" : { }
        }, {
          "attribute" : "last_name",
          "target_field" : "last_name_b.phonetic",
          "target_value" : "Jones-Smith",
          "input_value" : "Jones",
          "input_matcher" : "simple",
          "input_matcher_params" : { }
        }, {
          "attribute" : "last_name",
          "target_field" : "last_name_b.phonetic",
          "target_value" : "Jones-Smith",
          "input_value" : "Jones-Smith",
          "input_matcher" : "simple",
          "input_matcher_params" : { }
        }, {
          "attribute" : "last_name",
          "target_field" : "last_name_b.phonetic",
          "target_value" : "Jones-Smith",
          "input_value" : "Smith",
          "input_matcher" : "simple",
          "input_matcher_params" : { }
        }, {
          "attribute" : "state",
          "target_field" : "state_b.keyword",
          "target_value" : "DC",
          "input_value" : "DC",
          "input_matcher" : "exact",
          "input_matcher_params" : { }
        }, {
          "attribute" : "street",
          "target_field" : "street_b.clean",
          "target_value" : "555 Broad St",
          "input_value" : "555 Broad St",
          "input_matcher" : "fuzzy",
          "input_matcher_params" : { }
        } ]
      },
      "_source" : {
        "city_b" : "Washington",
        "email_b" : "allison.j.smith@corp.example.net",
        "first_name_b" : "Allison",
        "id_b" : "12",
        "last_name_b" : "Jones-Smith",
        "phone_b" : "",
        "state_b" : "DC",
        "street_b" : "555 Broad St"
      }
    }, {
      "_index" : "zentity_tutorial_5_cross_index_resolution_a",
      "_type" : "_doc",
      "_id" : "13",
      "_hop" : 5,
      "_query" : 0,
      "_attributes" : {
        "city" : [ "Arlington" ],
        "email" : [ "allison.j.smith@corp.example.net" ],
        "first_name" : [ "Allison" ],
        "last_name" : [ "Jones Smith" ],
        "phone" : [ "703-555-5555" ],
        "state" : [ "VA" ],
        "street" : [ "1 Corporate Way" ]
      },
      "_explanation" : {
        "resolvers" : {
          "name_email" : {
            "attributes" : [ "email", "first_name", "last_name" ]
          }
        },
        "matches" : [ {
          "attribute" : "email",
          "target_field" : "email_a.keyword",
          "target_value" : "allison.j.smith@corp.example.net",
          "input_value" : "allison.j.smith@corp.example.net",
          "input_matcher" : "exact",
          "input_matcher_params" : { }
        }, {
          "attribute" : "first_name",
          "target_field" : "first_name_a.clean",
          "target_value" : "Allison",
          "input_value" : "Alison",
          "input_matcher" : "fuzzy",
          "input_matcher_params" : { }
        }, {
          "attribute" : "first_name",
          "target_field" : "first_name_a.clean",
          "target_value" : "Allison",
          "input_value" : "Allison",
          "input_matcher" : "fuzzy",
          "input_matcher_params" : { }
        }, {
          "attribute" : "first_name",
          "target_field" : "first_name_a.phonetic",
          "target_value" : "Allison",
          "input_value" : "Alison",
          "input_matcher" : "simple",
          "input_matcher_params" : { }
        }, {
          "attribute" : "first_name",
          "target_field" : "first_name_a.phonetic",
          "target_value" : "Allison",
          "input_value" : "Allison",
          "input_matcher" : "simple",
          "input_matcher_params" : { }
        }, {
          "attribute" : "last_name",
          "target_field" : "last_name_a.clean",
          "target_value" : "Jones Smith",
          "input_value" : "Jones",
          "input_matcher" : "fuzzy",
          "input_matcher_params" : { }
        }, {
          "attribute" : "last_name",
          "target_field" : "last_name_a.clean",
          "target_value" : "Jones Smith",
          "input_value" : "Jones-Smith",
          "input_matcher" : "fuzzy",
          "input_matcher_params" : { }
        }, {
          "attribute" : "last_name",
          "target_field" : "last_name_a.clean",
          "target_value" : "Jones Smith",
          "input_value" : "Smith",
          "input_matcher" : "fuzzy",
          "input_matcher_params" : { }
        }, {
          "attribute" : "last_name",
          "target_field" : "last_name_a.phonetic",
          "target_value" : "Jones Smith",
          "input_value" : "Joans",
          "input_matcher" : "simple",
          "input_matcher_params" : { }
        }, {
          "attribute" : "last_name",
          "target_field" : "last_name_a.phonetic",
          "target_value" : "Jones Smith",
          "input_value" : "Jones",
          "input_matcher" : "simple",
          "input_matcher_params" : { }
        }, {
          "attribute" : "last_name",
          "target_field" : "last_name_a.phonetic",
          "target_value" : "Jones Smith",
          "input_value" : "Jones-Smith",
          "input_matcher" : "simple",
          "input_matcher_params" : { }
        }, {
          "attribute" : "last_name",
          "target_field" : "last_name_a.phonetic",
          "target_value" : "Jones Smith",
          "input_value" : "Smith",
          "input_matcher" : "simple",
          "input_matcher_params" : { }
        } ]
      },
      "_source" : {
        "city_a" : "Arlington",
        "email_a" : "allison.j.smith@corp.example.net",
        "first_name_a" : "Allison",
        "id_a" : "13",
        "last_name_a" : "Jones Smith",
        "phone_a" : "703-555-5555",
        "state_a" : "VA",
        "street_a" : "1 Corporate Way"
      }
    } ]
  }
}
```


## <a name="conclusion"></a>Conclusion

Congratulations! You learned how to resolve an entity using multiple
combinations of attributes mapped to multiple fields across multiple indices.

The next tutorial will introduce [scoping resolution](/docs/basic-usage/scoping-resolution).
You will **limit the scope** of an entity resolution job to specific resolvers
and indices to prevent unnecessary searches under particular circumstances.


&nbsp;

----

#### Continue Reading

|&#8249;|[Multiple Resolver Resolution](/docs/basic-usage/multiple-resolver-resolution)|[Scoping Resolution](/docs/basic-usage/scoping-resolution)|&#8250;|
|:---|:---|---:|---:|
|    |    |    |    |
