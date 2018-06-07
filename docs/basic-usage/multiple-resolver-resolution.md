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

Now create the index for this tutorial.

<span class="code-overflow"></span>
```javascript
PUT .zentity-tutorial-index
{
  "settings": {
    "index": {
      "number_of_shards": 1,
      "number_of_replicas": 0,
      "analysis": {
        "analyzer": {
          "clean_analyzer": {
            "tokenizer": "standard",
            "filter": [
              "icu_normalizer",
              "icu_folding"
            ]
          },
          "phonetic_analyzer": {
            "tokenizer": "standard",
            "filter": [
              "icu_normalizer",
              "icu_folding",
              "phonetic_filter"
            ]
          }
        },
        "filter": {
          "phonetic_filter": {
            "type": "phonetic",
            "encoder": "nysiis"
          }
        }
      }
    }
  },
  "mapping": {
    "doc": {
      "properties": {
        "id": {
          "type": "keyword"
        },
        "user": {
          "type": "text",
          "fields": {
            "phonetic": {
              "type": "text",
              "analyzer": "clean"
            },
            "phonetic": {
              "type": "text",
              "analyzer": "phonetic"
            }
          }
        },
        "phone": {
          "type": "text",
          "fields": {
            "keyword": {
              "type": "keyword"
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
        },
        "dob": {
          "type": "date",
          "format": "yyyy-MM-dd"
        },
        "zip": {
          "type": "integer"
        }
      }
    }
  }
}
```


### <a name="load-tutorial-data"></a>1.5. Load the tutorial data

Add the tutorial data to the index.

```javascript
POST .zentity-tutorial-index/_bulk
{
  ...
}
```

Here's what the tutorial data looks like.

|id|user|phone|email|dob|zip|
|:---|:---|:---|:---|:---|:---|
|1|Alice|555-123-4567|alice@example.net|1984-01-01|90210|
|2|Alice|555-123-4567|alice@example.net|1984-01-01|90210|
|3|Elise|555-987-6543|elise@example.com|1984-01-01|90210|
|4|Bob|555-555-5555|bob@example.net|1989-05-15|90210|


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

Congratulations! You learned how to resolve an entity using multiple combinations of attributes mapped to multiple fields in a single index.

The next tutorial will introduce [cross index resolution](/docs/basic-usage/cross-index-resolution). You will
resolve an entity using multiple combinations of multiple attributes mapped to multiple fields across multiple indices.


&nbsp;

----

#### Continue Reading

|&#8249;|[Multiple Attribute Resolution](/docs/basic-usage/multiple-attribute-resolution)|[Cross Index Resolution](/docs/basic-usage/cross-index-resolution)|&#8250;|
|:---|:---|---:|---:|
|    |    |    |    |
