[Home](/) / [Documentation](/docs) / [Basic Usage](/docs/basic-usage) / Multiple Attribute Resolution


#### <a name="contents"></a>Basic Usage Tutorials

This tutorial is part of a series to help you learn and perform the basic functions of zentity. Each tutorial adds a little more
sophistication to the prior tutorials, so you can start simple and learn the more advanced features over time.

1. [Exact Name Matching](/docs/basic-usage/exact-name-matching)
2. [Robust Name Matching](/docs/basic-usage/robust-name-matching)
3. **Multiple Attribute Resolution** *&#8592; You are here.*
4. [Multiple Resolver Resolution](/docs/basic-usage/multiple-resolver-resolution)
5. [Cross Index Resolution](/docs/basic-usage/cross-index-resolution)

---


# <a name="multiple-attribute-resolution"></a>Multiple Attribute Resolution

This tutorial adds more sophistication to the prior tutorials on [exact name matching](/docs/basic-usage/exact-name-matching) and
[robust name matching](/docs/basic-usage/robust-name-matching). This time you will map *multiple attributes* to multiple fields
of a single index.

Never trust a single attribute in isolation, as a general rule.

Using a single attribute for entity resolution is a bad practice &ndash; an anti-pattern. It's an easy way to "snowball" many different entities
together and drive up your false positive rate. The problem with using a single attribute is that any attribute is prone to error. Many people can
share the same name or or date of birth. One address can be shared by family members or past residents. A Social Security Number can be forged,
reissued, shared, or mistyped. A bogus value such as "N/A" can link many entities together.

Instead, trust multiple attributes to corroborate a match.

Consider this an exercise in probability theory. Suppose you have an index of millions of people. What's the probability that two people share
the same name? It's probably high. What's the probability that people share the same name *and* the same phone number? It's probably much lower.

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
    }
  },
  "resolvers": {
    "name_phone": {
      "attributes": [ "name", "phone" ]
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
        }
      }
    }
  }
}
```


### <a name="review-attributes"></a>2.1. Review the attributes

We defined two attribute called `"name"` and `"phone"` as shown in this section:

```javascript
{
  "attributes": {
    "name": {
      "type": "string"
    },
    "phone": {
      "type": "string"
    }
  }
}
```


### <a name="review-resolvers"></a>2.2. Review the resolvers

We defined a single resolver called `"name_phone"` as shown in this section:

```javascript
{
  "resolvers": {
    "name_phone": {
      "attributes": [ "name", "phone" ]
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

The `"exact"` matcher uses a simple [`term` clause](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-term-query.html).
`term` queries apply exact matching for [`keyword`](https://www.elastic.co/guide/en/elasticsearch/reference/current/keyword.html) fields,
while `match` queries apply fuzzy matching for [`text`](https://www.elastic.co/guide/en/elasticsearch/reference/current/text.html) fields.
We can use our `"exact"` matcher on index fields that have a `keyword` data type.

```javascript
{
  "term": {
    "{{ field }}": "{{ value }}"
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
        }
      }
    }
  }
}
```

We mapped the `"name"` attribute to the `"user"`, `"user.clean"`, and `"user.phonetic"` fields and the `"phone"` attribute
to the `"phone.keyword"` field in `.zentity-tutorial-index`.

> **Tip**
> 
> Notice that the `"phone.keyword"` field is mapped to our `"exact"` matcher which uses a `term` query.
> Elasticsearch expects [`term`](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-term-query.html) queries
> to be executed on the exact value of [`keyword`](https://www.elastic.co/guide/en/elasticsearch/reference/current/keyword.html) fields,
> whereas [`match`](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-match-query.html) queries apply
> [full text](https://www.elastic.co/guide/en/elasticsearch/reference/current/keyword.html) analysis to values before performing the search.
> You might not get the results you'd expect if you run either a `term` query on a `text` field or a `match` query on a `keyword` field.


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

Congratulations! You learned how to map multiple attributes to multiple fields in a single index.

The next tutorial will introduce [multiple attribute resolution](/docs/basic-usage/multiple-resolver-resolution). You will
resolve an entity using multiple combinations of attributes mapped to multiple fields of a single index.


&nbsp;

----

#### Continue Reading

|&#8249;|[Robust Name Matching](/docs/basic-usage/robust-name-matching)|[Multiple Resolver Resolution](/docs/basic-usage/multiple-resolver-resolution)|&#8250;|
|:---|:---|---:|---:|
|    |    |    |    |
