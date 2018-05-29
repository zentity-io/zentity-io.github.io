[Home](/) / [Documentation](/docs) / [Basic Usage](/docs/basic-usage) / Robust Name Matching


#### <a name="contents"></a>Basic Usage Tutorials

This tutorial is part of a series to help you learn and perform the basic functions of zentity. Each tutorial adds a little more
sophistication to the prior tutorials, so you can start simple and learn the more advanced features over time.

1. [Exact Name Matching](/docs/basic-usage/exact-name-matching)
2. **Robust Name Matching** *&#8592; You are here.*
3. [Multiple Attribute Resolution](/docs/basic-usage/multiple-attribute-resolution)
4. [Multiple Resolver Resolution](/docs/basic-usage/multiple-resolver-resolution)
5. [Cross Index Resolution](/docs/basic-usage/cross-index-resolution)
6. [Cross Cluster Resolution](/docs/basic-usage/cross-cluster-resolution)

---


# <a name="robust-name-matching"></a>Robust Name Matching

This tutorial adds a little more sophistication to the last tutorial on [exact name matching](/docs/basic-usage/exact-name-matching).
This time you will map a single attribute to *multiple fields* of a single index.

Using a one-to-many relationship between attributes and index fields, you can compare the value of an attribute to multiple representations
in the index. Elasticsearch allows you to create [subfields](https://www.elastic.co/guide/en/elasticsearch/reference/current/multi-fields.html)
where you can index the same value in different ways. For example, you might want to index a name by its exact value (the
[`keyword`](https://www.elastic.co/guide/en/elasticsearch/reference/current/keyword.html) data type), its full text value (the
[`text`](https://www.elastic.co/guide/en/elasticsearch/reference/current/text.html) data type), or its phonetic encoding using the
[phonetic analysis plugin](https://www.elastic.co/guide/en/elasticsearch/plugins/current/analysis-phonetic.html). Elasticsearch
allows you to query any of these representations of the name and return the original value of the name.

You can use this to your advantage with zentity. All you need to do is map the attribute and a matcher to each of those fields.
When you [submit an entity resolution job](/docs/rest-apis/resolution-api), attributes will be compared to every index field to which
they are mapped.

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
          "clean": {
            "tokenizer": "standard",
            "filter": [
              "icu_normalizer",
              "icu_folding"
            ]
          },
          "phonetic": {
            "tokenizer": "standard",
            "filter": [
              "icu_normalizer",
              "icu_folding",
              "phonetic"
            ]
          }
        },
        "filter": {
          "phonetic": {
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

Notice that this index defines multiple fields under the `user` field. There are three fields we can query for the `user`:

- `user` uses the standard analyzer.
- `user.clean` uses a custom `clean` analyzer.
- `user.phonetic` uses a custom `phonetic` analyzer.


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
    }
  },
  "resolvers": {
    "name_only": {
      "attributes": [ "name" ]
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
    }
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
        }
      }
    }
  }
}
```


### <a name="review-attributes"></a>2.1. Review the attributes

We defined a single attribute called `"name"` as shown in this section:

```javascript
{
  "attributes": {
    "name": {
      "type": "string"
    }
  }
}
```

This is identical to the `"attributes"` field of the entity model in the [exact name matching](/docs/basic-usage/exact-name-matching#create-entity-model) tutorial.


### <a name="review-resolvers"></a>2.2. Review the resolvers

We defined a single resolver called `"name_only"` as shown in this section:

```javascript
{
  "resolvers": {
    "name_only": {
      "attributes": [ "name" ]
    }
  }
}
```

This is identical to the `"resolvers"` field of the entity model in the [exact name matching](/docs/basic-usage/exact-name-matching#create-entity-model) tutorial.

> **Tip**
> 
> Most resolvers should use multiple attributes to resolve an entity to minimize false positives. Many people share the same name, but few people share the same name and address. Consider all the combinations of attributes that could resolve an entity with confidence, and then create a resolver for each combination. [Other tutorials](/docs/basic-usage) explore how to use resolvers with multiple attributes.


### <a name="review-matchers"></a>2.3. Review the matchers

We defined two matchers called `"simple"` and `"fuzzy"` as shown in this section:

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
    "simple": {
      "clause": {
        "match": {
          "{{ field }}": {
            "query": "{{ value }}",
            "fuzziness": "auto"
          }
        }
      }
    }
  }
}
```

The `"simple"` matcher uses a simple [`match` clause](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-match-query.html):

```javascript
{
  "match": {
    "{{ field }}": "{{ value }}"
  }
}
```

The `"fuzzy"` matcher uses a `match` clause with the [`fuzziness`](https://www.elastic.co/guide/en/elasticsearch/guide/current/fuzzy-match-query.html) parameter,
which matches values with minor dissimilarities such as typos. Elasticsearch uses the [Damerau-Levenshtein edit distance](https://www.elastic.co/guide/en/elasticsearch/guide/current/fuzziness.html)
to perform this match.

```javascript
{
  "match": {
    "{{ field }}": {
      "query": "{{ value }}"
      "fuzziness": "auto"
    }
  }
}
```

The `"{{ field }}"` and `"{{ value }}"` strings are special variables. Every matcher should have these variables defined somewhere in the `"clause"` field. zentity will replace the `"{{ field }}"` variable with the name of an index field and the `"{{ value }}"` variable with the value of an attribute.


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
        }
      }
    }
  }
}
```

We mapped the `"name"` attribute to the `"user"`, `"user.clean"`, and `"user.phonetic"` fields in `.zentity-tutorial-index`.
The `"user"` field will use the `"fuzzy"` matcher and the other two fields will use the `"simple"` matcher.


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

Congratulations! You learned how to map a single attribute to multiple fields in a single index. You also observed how to
perform more robust name matching by using fuzziness, phonetic analyzers, and ICU analyzers.

But we can do better than name matching, right? Lots of people share the same name. How can we improve accuracy?

The next tutorial will introduce [multiple attribute resolution](/docs/basic-usage/multiple-attribute-resolution). You will
resolve an entity using multiple attributes mapped to multiple fields of a single index.


&nbsp;

----

#### Continue Reading

|&#8249;|[Exact Name Matching](/docs/basic-usage/exact-name-matching)|[Multiple Attribute Resolution](/docs/basic-usage/multiple-attribute-resolution)|&#8250;|
|:---|:---|---:|---:|
|    |    |    |    |
