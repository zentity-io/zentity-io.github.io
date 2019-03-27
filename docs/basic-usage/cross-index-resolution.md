[Home](/) / [Documentation](/docs) / [Basic Usage](/docs/basic-usage) / Cross Index Resolution


#### <a name="contents"></a>Basic Usage Tutorials

This tutorial is part of a series to help you learn and perform the basic functions of zentity. Each tutorial adds a little more
sophistication to the prior tutorials, so you can start simple and learn the more advanced features over time.

1. [Exact Name Matching](/docs/basic-usage/exact-name-matching)
2. [Robust Name Matching](/docs/basic-usage/robust-name-matching)
3. [Multiple Attribute Resolution](/docs/basic-usage/multiple-attribute-resolution)
4. [Multiple Resolver Resolution](/docs/basic-usage/multiple-resolver-resolution)
5. **Cross Index Resolution** *&#8592; You are here.*

---


# <a name="cross-index-resolution"></a>Cross Index Resolution

This tutorial shows how you can ...

Let's dive in.

> **Important**
> 
> You must install [Elasticsearch](https://www.elastic.co/downloads/elasticsearch), [Kibana](https://www.elastic.co/downloads/kibana), and [zentity](/docs/installation) to complete this tutorial.
> This tutorial was tested with [zentity-1.0.0-elasticsearch-6.2.4](/docs/releases).


## <a name="prepare"></a>1. Prepare for the tutorial


### <a name="install-phonetic-analysis-plugin"></a>1.1. Install the required plugins

This tutorial uses the [phonetic analysis plugin](https://www.elastic.co/guide/en/elasticsearch/plugins/current/analysis-phonetic.html)
and [ICU analysis plugin](https://www.elastic.co/guide/en/elasticsearch/plugins/current/analysis-icu.html) for Elasticsearch. You will
need to stop Elasticsearch, install these plugin, and start Elasticsearch. You can learn more about Elasticsearch plugin management
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


### <a name="open-kibana-console-ui"></a>1.2. Open the Kibana Console UI

The [Kibana Console UI](https://www.elastic.co/guide/en/kibana/current/console-kibana.html) makes it easy to submit requests to Elasticsearch and read responses.


### <a name="delete-old-tutorial-indices"></a>1.3. Delete any old tutorial indices

Let's start from scratch. Delete any tutorial indices you might have created from other tutorials.

```javascript
DELETE .zentity-tutorial-*
```


### <a name="create-tutorial-index"></a>1.4. Create the tutorial index

Now create the indices for this tutorial.

**Index A**

<span class="code-overflow"></span>
```javascript
PUT .zentity-tutorial-index-a
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
    "_doc": {
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
}
```

**Index B**

<span class="code-overflow"></span>
```javascript
PUT .zentity-tutorial-index-b
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
    "_doc": {
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
}
```


### <a name="load-tutorial-data"></a>1.5. Load the tutorial data

Add the tutorial data to the index.

```javascript
POST _bulk?refresh
{"index": {"_id": "1", "_index": ".zentity-tutorial-index-a", "_type": "_doc"}}
{"city_a": "Washington", "email_a": "allie@example.net", "first_name_a": "Allie", "id_a": "1", "last_name_a": "Jones", "phone_a": "202-555-1234", "state_a": "DC", "street_a": "123 Main St"}
{"index": {"_id": "2", "_index": ".zentity-tutorial-index-b", "_type": "_doc"}}
{"city_b": "Washington", "email_b": "", "first_name_b": "Alicia", "id_b": "2", "last_name_b": "Johnson", "phone_b": "202-123-4567", "state_b": "DC", "street_b": "300 Main St"}
{"index": {"_id": "3", "_index": ".zentity-tutorial-index-a", "_type": "_doc"}}
{"city_a": "Washington", "email_a": "", "first_name_a": "Allie", "id_a": "3", "last_name_a": "Jones", "phone_a": "", "state_a": "DC", "street_a": "123 Main St"}
{"index": {"_id": "4", "_index": ".zentity-tutorial-index-b", "_type": "_doc"}}
{"city_b": "", "email_b": "", "first_name_b": "Ally", "id_b": "4", "last_name_b": "Joans", "phone_b": "202-555-1234", "state_b": "", "street_b": ""}
{"index": {"_id": "5", "_index": ".zentity-tutorial-index-a", "_type": "_doc"}}
{"city_a": "Arlington", "email_a": "ej@example.net", "first_name_a": "Eli", "id_a": "5", "last_name_a": "Jonas", "phone_a": "", "state_a": "VA", "street_a": "500 23rd Street"}
{"index": {"_id": "6", "_index": ".zentity-tutorial-index-b", "_type": "_doc"}}
{"city_b": "Washington", "email_b": "allie@example.net", "first_name_b": "Allison", "id_b": "6", "last_name_b": "Jones", "phone_b": "202-555-1234", "state_b": "DC", "street_b": "123 Main St"}
{"index": {"_id": "7", "_index": ".zentity-tutorial-index-a", "_type": "_doc"}}
{"city_a": "Washington", "email_a": "", "first_name_a": "Allison", "id_a": "7", "last_name_a": "Smith", "phone_a": "+1 (202) 555 1234", "state_a": "DC", "street_a": "555 Broad St"}
{"index": {"_id": "8", "_index": ".zentity-tutorial-index-b", "_type": "_doc"}}
{"city_b": "Washington", "email_b": "alan.smith@example.net", "first_name_b": "Alan", "id_b": "8", "last_name_b": "Smith", "phone_b": "202-000-5555", "state_b": "DC", "street_b": "555 Broad St"}
{"index": {"_id": "9", "_index": ".zentity-tutorial-index-a", "_type": "_doc"}}
{"city_a": "Washington", "email_a": "alan.smith@example.net", "first_name_a": "Alan", "id_a": "9", "last_name_a": "Smith", "phone_a": "2020005555", "state_a": "DC", "street_a": "555 Broad St"}
{"index": {"_id": "10", "_index": ".zentity-tutorial-index-b", "_type": "_doc"}}
{"city_b": "Washington", "email_b": "", "first_name_b": "Alison", "id_b": "10", "last_name_b": "Smith", "phone_b": "202-555-9876", "state_b": "DC", "street_b": "555 Broad St"}
{"index": {"_id": "11", "_index": ".zentity-tutorial-index-a", "_type": "_doc"}}
{"city_a": "", "email_a": "allie@example.net", "first_name_a": "Alison", "id_a": "11", "last_name_a": "Jones-Smith", "phone_a": "2025559867", "state_a": "", "street_a": ""}
{"index": {"_id": "12", "_index": ".zentity-tutorial-index-b", "_type": "_doc"}}
{"city_b": "Washington", "email_b": "allison.j.smith@corp.example.net", "first_name_b": "Allison", "id_b": "12", "last_name_b": "Jones-Smith", "phone_b": "", "state_b": "DC", "street_b": "555 Broad St"}
{"index": {"_id": "13", "_index": ".zentity-tutorial-index-a", "_type": "_doc"}}
{"city_a": "Arlington", "email_a": "allison.j.smith@corp.example.net", "first_name_a": "Allison", "id_a": "13", "last_name_a": "Jones Smith", "phone_a": "703-555-5555", "state_a": "VA", "street_a": "1 Corporate Way"}
{"index": {"_id": "14", "_index": ".zentity-tutorial-index-b", "_type": "_doc"}}
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

Let's use the [Models API](/docs/rest-apis/models-api) to create the entity model below. We'll review each part of the model in depth.

```javascript
PUT _zentity/models/zentity-tutorial-person
{
  "attributes": {
    "name": {
      "type": "string"
    },
    "phone": {
      "type": "string"
    },
    "email": {
      "type": "string"
    },
    "dob": {
      "type": "string"
    },
    "zip": {
      "type": "string"
    }
  },
  "resolvers": {
    "name_phone": {
      "attributes": [ "name", "phone" ]
    },
    "name_email": {
      "attributes": [ "name", "email" ]
    },
    "name_dob_zip": {
      "attributes": [ "name", "dob", "zip" ]
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
            "fuzziness": "auto"
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
    },
  },
  "indices": {
    ".zentity-tutorial-index": {
      "fields": {
        "user": {
          "attribute": "name",
          "matcher": "fuzzy"
        },
        "user.clean": {
          "attribute": "name",
          "matcher": "simple"
        },
        "user.phonetic": {
          "attribute": "name",
          "matcher": "simple"
        },
        "phone.keyword": {
          "attribute": "phone",
          "matcher": "exact"
        },
        "email.keyword": {
          "attribute": "email",
          "matcher": "exact"
        },
        "dob.keyword": {
          "attribute": "dob",
          "matcher": "exact"
        },
        "zip": {
          "attribute": "zip",
          "matcher": "fuzzy"
        }
      }
    }
  }
}
```


### <a name="review-attributes"></a>2.1. Review the attributes

We defined five attributes as shown in this section:

```javascript
{
  "attributes": {
    "name": {
      "type": "string"
    },
    "phone": {
      "type": "string"
    },
    "email": {
      "type": "string"
    },
    "dob": {
      "type": "string"
    },
    "zip": {
      "type": "string"
    }
  }
}
```


### <a name="review-resolvers"></a>2.2. Review the resolvers

We defined three resolvers as shown in this section:

```javascript
{
  "resolvers": {
    "name_phone": {
      "attributes": [ "name", "phone" ]
    },
    "name_email": {
      "attributes": [ "name", "email" ]
    },
    "name_dob_zip": {
      "attributes": [ "name", "dob", "zip" ]
    }
  }
}
```


### <a name="review-matchers"></a>2.3. Review the matchers

We defined three matchers called `"simple"`, `"fuzzy"`, and `"exact"` as shown in this section:

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
            "fuzziness": "auto"
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


### <a name="review-indices"></a>2.4. Review the indices

We defined a single index as shown in this section:

```javascript
{
  "indices": {
    ".zentity-tutorial-index": {
      "fields": {
        "user": {
          "attribute": "name",
          "matcher": "fuzzy"
        },
        "user.clean": {
          "attribute": "name",
          "matcher": "simple"
        },
        "user.phonetic": {
          "attribute": "name",
          "matcher": "simple"
        },
        "phone.keyword": {
          "attribute": "phone",
          "matcher": "exact"
        },
        "email.keyword": {
          "attribute": "email",
          "matcher": "exact"
        },
        "dob.keyword": {
          "attribute": "dob",
          "matcher": "exact"
        },
        "zip.keyword": {
          "attribute": "zip",
          "matcher": "fuzzy"
        }
      }
    }
  }
}
```


## <a name="resolve-entity"></a>3. Resolve an entity

Let's use the [Resolution API](/docs/rest-apis/resolution-api) to resolve a person with the name "Alice":

```javascript
POST _zentity/resolution/zentity-tutorial-person
{
  "attributes": {
    "name": [ "Alice" ]
  }
}
```

The results will look like this:

```javascript
...
```

As expected, we retrieved ...


## <a name="conclusion"></a>Conclusion

Congratulations! You learned how to resolve an entity using multiple combinations of attributes mapped to multiple fields
across multiple indices.


&nbsp;

----

#### Continue Reading

|&#8249;|[Multiple Resolver Resolution](/docs/basic-usage/multiple-resolver-resolution)|[Advanced Usage](/docs/advanced-usage)|&#8250;|
|:---|:---|---:|---:|
|    |    |    |    |
