[Home](/) / [Documentation](/docs) / [Basic Usage](/docs/basic-usage) / Multiple Resolver Resolution


#### <a name="contents"></a>Basic Usage Tutorials

This tutorial is part of a series to help you learn and perform the basic functions of zentity. Each tutorial adds a little more
sophistication to the prior tutorials, so you can start simple and learn the more advanced features over time.

1. [Exact Name Matching](/docs/basic-usage/exact-name-matching)
2. [Robust Name Matching](/docs/basic-usage/robust-name-matching)
3. [Multiple Attribute Resolution](/docs/basic-usage/multiple-attribute-resolution)
4. **Multiple Resolver Resolution** *&#8592; You are here.*
5. [Cross Index Resolution](/docs/basic-usage/cross-index-resolution)

---


# <a name="multiple-resolver-resolution"></a>Multiple Resolver Resolution

This tutorial adds more sophistication to the prior tutorial on [multiple attribute resolution](/docs/basic-usage/multiple-attribute-resolution).
This time you will map *multiple combinations* of multiple attributes to multiple fields of a single index.

One of the critical challenges of entity resolution is to minimize false positives and false negatives. The reduction of one tends to lead
to the increase of the other. So far we have shown how you can reduce false negatives by using [robust matchers](/docs/basic-usage/robust-name-matching)
and reduce false positives by using [multiple attributes](/docs/basic-usage/multiple-attribute-resolution) in your resolver.

A good way to reduce both types of errors is to define multiple resolvers each with conservative matching logic.

For example, suppose you have a dataset of people with five attributes: name, phone, email, date of birth, postal code. There are several ways you
might try to match the people in this data set. Name and phone, name and email, name and date of birth and postal code, and perhaps even email and
date of birth or phone and date of birth. Each of these combinations of attributes is likely "just enough" to match an entity. You can define each
of these combinations as a resolver, and zentity can attempt to resolve the entities in each of these ways.

Let's dive in.

> **Important**
> 
> You must install [Elasticsearch](https://www.elastic.co/downloads/elasticsearch), [Kibana](https://www.elastic.co/downloads/kibana), and [zentity](/docs/installation) to complete this tutorial.
> This tutorial was tested with [zentity-1.0.2-elasticsearch-6.5.2](/docs/releases).


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

Now create the index for this tutorial.

<span class="code-overflow"></span>
```javascript
PUT .zentity-tutorial-index
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
        "id": {
          "type": "keyword"
        },
        "first_name": {
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
        "last_name": {
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
        "street": {
          "type": "text",
          "fields": {
            "clean": {
              "type": "text",
              "analyzer": "street_clean"
            }
          }
        },
        "city": {
          "type": "text",
          "fields": {
            "clean": {
              "type": "text",
              "analyzer": "name_clean"
            }
          }
        },
        "state": {
          "type": "text",
          "fields": {
            "keyword": {
              "type": "keyword"
            }
          }
        },
        "phone": {
          "type": "text",
          "fields": {
            "clean": {
              "type": "text",
              "analyzer": "phone_clean"
            }
          }
        },
        "email": {
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
{"index": {"_id": "1", "_index": ".zentity-tutorial-index", "_type": "_doc"}}
{"city": "Washington", "email": "allie@example.net", "first_name": "Allie", "id": "1", "last_name": "Jones", "phone": "202-555-1234", "state": "DC", "street": "123 Main St"}
{"index": {"_id": "2", "_index": ".zentity-tutorial-index", "_type": "_doc"}}
{"city": "Washington", "email": "", "first_name": "Alicia", "id": "2", "last_name": "Johnson", "phone": "202-123-4567", "state": "DC", "street": "300 Main St"}
{"index": {"_id": "3", "_index": ".zentity-tutorial-index", "_type": "_doc"}}
{"city": "Washington", "email": "", "first_name": "Allie", "id": "3", "last_name": "Jones", "phone": "", "state": "DC", "street": "123 Main St"}
{"index": {"_id": "4", "_index": ".zentity-tutorial-index", "_type": "_doc"}}
{"city": "", "email": "", "first_name": "Ally", "id": "4", "last_name": "Joans", "phone": "202-555-1234", "state": "", "street": ""}
{"index": {"_id": "5", "_index": ".zentity-tutorial-index", "_type": "_doc"}}
{"city": "Arlington", "email": "ej@example.net", "first_name": "Eli", "id": "5", "last_name": "Jonas", "phone": "", "state": "VA", "street": "500 23rd Street"}
{"index": {"_id": "6", "_index": ".zentity-tutorial-index", "_type": "_doc"}}
{"city": "Washington", "email": "allie@example.net", "first_name": "Allison", "id": "6", "last_name": "Jones", "phone": "202-555-1234", "state": "DC", "street": "123 Main St"}
{"index": {"_id": "7", "_index": ".zentity-tutorial-index", "_type": "_doc"}}
{"city": "Washington", "email": "", "first_name": "Allison", "id": "7", "last_name": "Smith", "phone": "+1 (202) 555 1234", "state": "DC", "street": "555 Broad St"}
{"index": {"_id": "8", "_index": ".zentity-tutorial-index", "_type": "_doc"}}
{"city": "Washington", "email": "alan.smith@example.net", "first_name": "Alan", "id": "8", "last_name": "Smith", "phone": "202-000-5555", "state": "DC", "street": "555 Broad St"}
{"index": {"_id": "9", "_index": ".zentity-tutorial-index", "_type": "_doc"}}
{"city": "Washington", "email": "alan.smith@example.net", "first_name": "Alan", "id": "9", "last_name": "Smith", "phone": "2020005555", "state": "DC", "street": "555 Broad St"}
{"index": {"_id": "10", "_index": ".zentity-tutorial-index", "_type": "_doc"}}
{"city": "Washington", "email": "", "first_name": "Alison", "id": "10", "last_name": "Smith", "phone": "202-555-9876", "state": "DC", "street": "555 Broad St"}
{"index": {"_id": "11", "_index": ".zentity-tutorial-index", "_type": "_doc"}}
{"city": "", "email": "allie@example.net", "first_name": "Alison", "id": "11", "last_name": "Jones-Smith", "phone": "2025559867", "state": "", "street": ""}
{"index": {"_id": "12", "_index": ".zentity-tutorial-index", "_type": "_doc"}}
{"city": "Washington", "email": "allison.j.smith@corp.example.net", "first_name": "Allison", "id": "12", "last_name": "Jones-Smith", "phone": "", "state": "DC", "street": "555 Broad St"}
{"index": {"_id": "13", "_index": ".zentity-tutorial-index", "_type": "_doc"}}
{"city": "Arlington", "email": "allison.j.smith@corp.example.net", "first_name": "Allison", "id": "13", "last_name": "Jones Smith", "phone": "703-555-5555", "state": "VA", "street": "1 Corporate Way"}
{"index": {"_id": "14", "_index": ".zentity-tutorial-index", "_type": "_doc"}}
{"city": "Arlington", "email": "elise.jonas@corp.example.net", "first_name": "Elise", "id": "14", "last_name": "Jonas", "phone": "703-555-5555", "state": "VA", "street": "1 Corporate Way"}
```

Here's what the tutorial data looks like.

|id|first_name|last_name|street|city|state|phone|email|
|:---|:---|:---|:---|:---|:---|:---|:---|
|1|Allie|Jones|123 Main St|Washington|DC|202-555-1234|allie@example.net|
|2|Alicia|Johnson|300 Main St|Washington|DC|202-123-4567||
|3|Allie|Jones|123 Main St|Washington|DC|||
|4|Ally|Joans||||202-555-1234||
|5|Eli|Jonas|500 23rd Street|Arlington|VA||ej@example.net|
|6|Allison|Jones|123 Main St|Washington|DC|202-555-1234|allie@example.net|
|7|Allison|Smith|555 Broad St|Washington|DC|+1 (202) 555 1234||
|8|Alan|Smith|555 Broad St|Washington|DC|202-000-5555|alan.smith@example.net|
|9|Alan|Smith|555 Broad St|Washington|DC|2020005555|alan.smith@example.net|
|10|Alison|Smith|555 Broad St|Washington|DC|202-555-9876||
|11|Alison|Jones-Smith||||2025559867|allie@example.net|
|12|Allison|Jones-Smith|555 Broad St|Washington|DC||allison.j.smith@corp.example.net|
|13|Allison|Jones Smith|1 Corporate Way|Arlington|VA|703-555-5555|allison.j.smith@corp.example.net|
|14|Elise|Jonas|1 Corporate Way|Arlington|VA|703-555-5555|elise.jonas@corp.example.net|


## <a name="create-entity-model"></a>2. Create the entity model

Let's use the [Models API](/docs/rest-apis/models-api) to create the entity model below. We'll review each part of the model in depth.

```javascript
PUT _zentity/models/zentity-tutorial-person
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
    ".zentity-tutorial-index": {
      "fields": {
        "first_name.clean": {
          "attribute": "first_name",
          "matcher": "fuzzy"
        },
        "first_name.phonetic": {
          "attribute": "first_name",
          "matcher": "simple"
        },
        "last_name.clean": {
          "attribute": "last_name",
          "matcher": "fuzzy"
        },
        "last_name.phonetic": {
          "attribute": "last_name",
          "matcher": "simple"
        },
        "street.clean": {
          "attribute": "street",
          "matcher": "fuzzy"
        },
        "city.clean": {
          "attribute": "city",
          "matcher": "fuzzy"
        },
        "state.keyword": {
          "attribute": "state",
          "matcher": "exact"
        },
        "phone.clean": {
          "attribute": "phone",
          "matcher": "fuzzy"
        },
        "email.keyword": {
          "attribute": "email",
          "matcher": "exact"
        }
      }
    }
  }
}
```

The response will look like this:

```javascript
{
  "_index" : ".zentity-models",
  "_type" : "doc",
  "_id" : "zentity-tutorial-person",
  "_version" : 1,
  "result" : "created",
  "_shards" : {
    "total" : 2,
    "successful" : 1,
    "failed" : 0
  },
  "_seq_no" : 1,
  "_primary_term" : 3
}
```


### <a name="review-attributes"></a>2.1. Review the attributes

We defined seven attributes as shown in this section:

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


### <a name="review-resolvers"></a>2.2. Review the resolvers

We defined three resolvers as shown in this section:

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


### <a name="review-indices"></a>2.4. Review the indices

We defined a single index as shown in this section:

```javascript
{
  "indices": {
    ".zentity-tutorial-index": {
      "fields": {
        "first_name.clean": {
          "attribute": "first_name",
          "matcher": "fuzzy"
        },
        "first_name.phonetic": {
          "attribute": "first_name",
          "matcher": "simple"
        },
        "last_name.clean": {
          "attribute": "last_name",
          "matcher": "fuzzy"
        },
        "last_name.phonetic": {
          "attribute": "last_name",
          "matcher": "simple"
        },
        "street.clean": {
          "attribute": "street",
          "matcher": "fuzzy"
        },
        "city.clean": {
          "attribute": "city",
          "matcher": "fuzzy"
        },
        "state.keyword": {
          "attribute": "state",
          "matcher": "exact"
        },
        "phone.clean": {
          "attribute": "phone",
          "matcher": "fuzzy"
        },
        "email.keyword": {
          "attribute": "email",
          "matcher": "exact"
        }
      }
    }
  }
}
```


## <a name="resolve-entity"></a>3. Resolve an entity

Let's use the [Resolution API](/docs/rest-apis/resolution-api) to resolve a person with a known name and phone number:

```javascript
POST _zentity/resolution/zentity-tutorial-person?_source=false
{
  "attributes": {
    "first_name": [ "Allie" ],
    "last_name": [ "Jones" ],
    "phone": [ "202-555-1234" ]
  }
}
```

The results will look like this:

```javascript
{
  "took" : 30,
  "hits" : {
    "total" : 9,
    "hits" : [ {
      "_index" : ".zentity-tutorial-index",
      "_type" : "_doc",
      "_id" : "1",
      "_hop" : 0,
      "_attributes" : {
        "city" : "Washington",
        "email" : "allie@example.net",
        "first_name" : "Allie",
        "last_name" : "Jones",
        "phone" : "202-555-1234",
        "state" : "DC",
        "street" : "123 Main St"
      }
    }, {
      "_index" : ".zentity-tutorial-index",
      "_type" : "_doc",
      "_id" : "3",
      "_hop" : 0,
      "_attributes" : {
        "city" : "Washington",
        "email" : "",
        "first_name" : "Allie",
        "last_name" : "Jones",
        "phone" : "",
        "state" : "DC",
        "street" : "123 Main St"
      }
    }, {
      "_index" : ".zentity-tutorial-index",
      "_type" : "_doc",
      "_id" : "4",
      "_hop" : 1,
      "_attributes" : {
        "city" : "",
        "email" : "",
        "first_name" : "Ally",
        "last_name" : "Joans",
        "phone" : "202-555-1234",
        "state" : "",
        "street" : ""
      }
    }, {
      "_index" : ".zentity-tutorial-index",
      "_type" : "_doc",
      "_id" : "6",
      "_hop" : 1,
      "_attributes" : {
        "city" : "Washington",
        "email" : "allie@example.net",
        "first_name" : "Allison",
        "last_name" : "Jones",
        "phone" : "202-555-1234",
        "state" : "DC",
        "street" : "123 Main St"
      }
    }, {
      "_index" : ".zentity-tutorial-index",
      "_type" : "_doc",
      "_id" : "11",
      "_hop" : 2,
      "_attributes" : {
        "city" : "",
        "email" : "allie@example.net",
        "first_name" : "Alison",
        "last_name" : "Jones-Smith",
        "phone" : "2025559867",
        "state" : "",
        "street" : ""
      }
    }, {
      "_index" : ".zentity-tutorial-index",
      "_type" : "_doc",
      "_id" : "7",
      "_hop" : 3,
      "_attributes" : {
        "city" : "Washington",
        "email" : "",
        "first_name" : "Allison",
        "last_name" : "Smith",
        "phone" : "+1 (202) 555 1234",
        "state" : "DC",
        "street" : "555 Broad St"
      }
    }, {
      "_index" : ".zentity-tutorial-index",
      "_type" : "_doc",
      "_id" : "10",
      "_hop" : 3,
      "_attributes" : {
        "city" : "Washington",
        "email" : "",
        "first_name" : "Alison",
        "last_name" : "Smith",
        "phone" : "202-555-9876",
        "state" : "DC",
        "street" : "555 Broad St"
      }
    }, {
      "_index" : ".zentity-tutorial-index",
      "_type" : "_doc",
      "_id" : "12",
      "_hop" : 4,
      "_attributes" : {
        "city" : "Washington",
        "email" : "allison.j.smith@corp.example.net",
        "first_name" : "Allison",
        "last_name" : "Jones-Smith",
        "phone" : "",
        "state" : "DC",
        "street" : "555 Broad St"
      }
    }, {
      "_index" : ".zentity-tutorial-index",
      "_type" : "_doc",
      "_id" : "13",
      "_hop" : 5,
      "_attributes" : {
        "city" : "Arlington",
        "email" : "allison.j.smith@corp.example.net",
        "first_name" : "Allison",
        "last_name" : "Jones Smith",
        "phone" : "703-555-5555",
        "state" : "VA",
        "street" : "1 Corporate Way"
      }
    } ]
  }
}
```

As expected, we retrieved ...


## <a name="conclusion"></a>Conclusion

Congratulations! You learned how to resolve an entity using multiple combinations of attributes mapped to multiple fields in a single index.

The next tutorial will introduce [cross index resolution](/docs/basic-usage/cross-index-resolution). You will
resolve an entity using multiple combinations of multiple attributes mapped to multiple fields across multiple indices.


&nbsp;

----

#### Continue Reading

|&#8249;|[Multiple Attribute Resolution](/docs/basic-usage/multiple-attribute-resolution)|[Cross Index Resolution](/docs/basic-usage/cross-index-resolution)|&#8250;|
|:---|:---|---:|---:|
|    |    |    |    |
