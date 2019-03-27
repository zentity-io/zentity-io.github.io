[Home](/) / [Documentation](/docs) / [Basic Usage](/docs/basic-usage) / Robust Name Matching


#### <a name="contents"></a>Basic Usage Tutorials

This tutorial is part of a series to help you learn and perform the basic functions of zentity. Each tutorial adds a little more
sophistication to the prior tutorials, so you can start simple and learn the more advanced features over time.

1. [Exact Name Matching](/docs/basic-usage/exact-name-matching)
2. **Robust Name Matching** *&#8592; You are here.*
3. [Multiple Attribute Resolution](/docs/basic-usage/multiple-attribute-resolution)
4. [Multiple Resolver Resolution](/docs/basic-usage/multiple-resolver-resolution)
5. [Cross Index Resolution](/docs/basic-usage/cross-index-resolution)

---


# <a name="robust-name-matching"></a>Robust Name Matching

This tutorial adds a little more sophistication to the prior tutorial on [exact name matching](/docs/basic-usage/exact-name-matching).
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

Notice that this index defines multiple fields under the `first_name` and `last_name` fields. There are three fields we can query for `first_name` and `last_name`:

- `first_name` and `last_name` use the standard analyzer.
- `first_name.clean` and `last_name.clean` use a custom analyzer called `clean_analyzer`.
- `first_name.phonetic` and `last_name.phonetic` use a custom analyzer called `phonetic_analyzer`.

We defined `clean_analyzer` and `phonetic_analyzer` in the settings of the index. `clean_analyzer` uses the `icu_normalizer` and `icu_folding`
filters to convert any accented Unicode characters to their ASCII equivalent and normalize the casing of the characters. `phonetic_analyzer`
does the same thing, and then it transforms the tokens of the value into their phonetic representations using the `nysiis` phonetic encoding
algorithm.

> **Tip**
> 
> Analyzers are powerful tools to improve the accuracy of entity resolution. But they come with costs. The first cost is performance. Whenever
> a query is submitting to Elasticsearch, the analyzers will process the input values. zentity can submit many queries in a single entity resolution job,
> and the overall performance of a job can degrade significantly if you use regular expressions or other compute intensive filters in your analyzers.
> The second cost is flexibility. You can't change the analyzers of fields without reindexing the data to an index with different analyzers. So you
> should put careful thought into your analyzers and test them before using them in production.

Let's see how these analyzers produce different tokens for the same value.

#### Example of `clean_analyzer`

**Request**

```javascript
POST .zentity-tutorial-index/_analyze
{ "text": "Alice Jones-Smith", "analyzer": "clean" }
```

**Response**

```javascript
{
  "tokens": [
    {
      "token": "alice",
      "start_offset": 0,
      "end_offset": 5,
      "type": "<ALPHANUM>",
      "position": 0
    },
    {
      "token": "jones",
      "start_offset": 6,
      "end_offset": 11,
      "type": "<ALPHANUM>",
      "position": 1
    },
    {
      "token": "smith",
      "start_offset": 12,
      "end_offset": 17,
      "type": "<ALPHANUM>",
      "position": 2
    }
  ]
}
```

#### Example of `phonetic_analyzer`

**Request**

```javascript
POST .zentity-tutorial-index/_analyze
{ "text": "Alice Jones-Smith", "analyzer": "phonetic" }
```

**Response**

```javascript
{
  "tokens": [
    {
      "token": "ALAC",
      "start_offset": 0,
      "end_offset": 5,
      "type": "<ALPHANUM>",
      "position": 0
    },
    {
      "token": "JAN",
      "start_offset": 6,
      "end_offset": 11,
      "type": "<ALPHANUM>",
      "position": 1
    },
    {
      "token": "SNAT",
      "start_offset": 12,
      "end_offset": 17,
      "type": "<ALPHANUM>",
      "position": 2
    }
  ]
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
    }
  },
  "resolvers": {
    "name_only": {
      "attributes": [ "first_name", "last_name" ]
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

We defined two attributes called `"first_name"` and `"last_name"` as shown in this section:

```javascript
{
  "attributes": {
    "first_name": {
      "type": "string"
    },
    "last_name": {
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
      "attributes": [ "first_name", "last_name" ]
    }
  }
}
```

This is identical to the `"resolvers"` field of the entity model in the [exact name matching](/docs/basic-usage/exact-name-matching#create-entity-model) tutorial.

> **Tip**
> 
> Most resolvers should use multiple attributes to resolve an entity to minimize false positives. Many people share the same name,
but few people share the same name and address. Consider all the combinations of attributes that could resolve an entity with confidence,
and then create a resolver for each combination. [Other tutorials](/docs/basic-usage) explore how to use resolvers with multiple attributes.


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
    "fuzzy": {
      "clause": {
        "match": {
          "{{ field }}": {
            "query": "{{ value }}",
            "fuzziness": "1"
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
      "fuzziness": "1"
    }
  }
}
```

The `"{{ field }}"` and `"{{ value }}"` strings are special variables. Every matcher should have these variables defined somewhere
in the `"clause"` field. zentity will replace the `"{{ field }}"` variable with the name of an index field and the `"{{ value }}"`
variable with the value of an attribute.


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
    "first_name": [ "Allie" ],
    "last_name": [ "Jones" ]
  }
}
```

The results will look like this:

```javascript
{
  "took" : 12,
  "hits" : {
    "total" : 3,
    "hits" : [ {
      "_index" : ".zentity-tutorial-index",
      "_type" : "_doc",
      "_id" : "1",
      "_hop" : 0,
      "_attributes" : {
        "first_name" : "Allie",
        "last_name" : "Jones"
      },
      "_source" : {
        "city" : "Washington",
        "email" : "allie@example.net",
        "first_name" : "Allie",
        "id" : "1",
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
        "first_name" : "Allie",
        "last_name" : "Jones"
      },
      "_source" : {
        "city" : "Washington",
        "email" : "",
        "first_name" : "Allie",
        "id" : "3",
        "last_name" : "Jones",
        "phone" : "",
        "state" : "DC",
        "street" : "123 Main St"
      }
    }, {
      "_index" : ".zentity-tutorial-index",
      "_type" : "_doc",
      "_id" : "4",
      "_hop" : 0,
      "_attributes" : {
        "first_name" : "Ally",
        "last_name" : "Joans"
      },
      "_source" : {
        "city" : "",
        "email" : "",
        "first_name" : "Ally",
        "id" : "4",
        "last_name" : "Joans",
        "phone" : "202-555-1234",
        "state" : "",
        "street" : ""
      }
    } ]
  }
}
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
