[Home](/) / [Documentation](/docs) / [Basic Usage](/docs/basic-usage) / Robust Name Matching


#### <a name="contents"></a>Basic Usage Tutorials 📖

This tutorial is part of a series to help you learn and perform the basic
functions of zentity. Each tutorial adds a little more sophistication to the
prior tutorials, so you can start simple and learn the more advanced features
over time.

1. [Exact Name Matching](/docs/basic-usage/exact-name-matching)
2. **Robust Name Matching** *&#8592; You are here.*
3. [Multiple Attribute Resolution](/docs/basic-usage/multiple-attribute-resolution)
4. [Multiple Resolver Resolution](/docs/basic-usage/multiple-resolver-resolution)
5. [Cross Index Resolution](/docs/basic-usage/cross-index-resolution)
6. [Scoping Resolution](/docs/basic-usage/scoping-resolution)

---


# <a name="robust-name-matching"></a>Robust Name Matching

This tutorial adds a little more sophistication to the prior tutorial on
[exact name matching](/docs/basic-usage/exact-name-matching). This time you will
map a **single attribute** to **multiple fields** of a **single index**.

Using a one-to-many relationship between attributes and index fields, you can
compare the value of an attribute to multiple representations in the index.
Elasticsearch allows you to create [subfields](https://www.elastic.co/guide/en/elasticsearch/reference/current/multi-fields.html)
where you can index the same value in different ways. For example, you might
want to index a name by its exact value using the [`keyword`](https://www.elastic.co/guide/en/elasticsearch/reference/current/keyword.html)
data type, its full text value using the [`text`](https://www.elastic.co/guide/en/elasticsearch/reference/current/text.html)
data type, or its phonetic encoding using the [phonetic analysis plugin](https://www.elastic.co/guide/en/elasticsearch/plugins/current/analysis-phonetic.html).
Elasticsearch allows you to query any of these representations of the name and
return the original value of the name.

You can use this to your advantage with zentity. All you need to do is map the
attribute and a matcher to each of those fields. When you [submit an entity resolution job](/docs/rest-apis/resolution-api),
attributes will be compared to every index field to which they are mapped.

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
DELETE zentity_tutorial_2_*
```


### <a name="create-tutorial-index"></a>1.4 Create the tutorial index

> **Note:** Skip this step if you're using the [zentity sandbox](/sandbox).

Now create the index for this tutorial.

```javascript
PUT zentity_tutorial_2_robust_name_matching
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
```

Notice that this index defines multiple fields under the `first_name` and
`last_name` fields. There are three fields we can query for `first_name` and
`last_name`:

- `first_name` and `last_name` use the standard analyzer.
- `first_name.clean` and `last_name.clean` use a custom analyzer called `name_clean`.
- `first_name.phonetic` and `last_name.phonetic` use a custom analyzer called `name_phonetic`.

We defined `name_clean` and `name_phonetic` in the settings of the index.
`name_clean` uses the `icu_normalizer` and `icu_folding` filters to convert any
accented Unicode characters to their ASCII equivalent and normalize the casing
of the characters. `name_phonetic` does the same thing, and then it transforms
the tokens of the value into their phonetic representations using the `nysiis`
phonetic encoding algorithm.

> **Tip**
> 
> Analyzers are powerful tools to improve the accuracy of entity resolution.
> But they come with costs. The first cost is performance. Whenever a query is
> submitting to Elasticsearch, the analyzers will process the input values.
> zentity can submit many queries in a single entity resolution job, and the
> overall performance of a job can degrade significantly if you use regular
> expressions or other compute intensive filters in your analyzers. The second
> cost is flexibility. You can't change the analyzers of fields without
> reindexing the data to an index with different analyzers. So you should put
> careful thought into your analyzers and test them before using them in
> production.

Let's see how these analyzers produce different tokens for the same value.

#### Example of `name_clean`

Our `name_clean` analyzer uses the standard tokenizer, converts accented
characters to their ASCII equivalent, and normalizes the case of the characters.

**Request**

```javascript
POST zentity_tutorial_2_robust_name_matching/_analyze
{
  "text": "Alice Jones-Smith",
  "analyzer": "name_clean"
}
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

#### Example of `name_phonetic`

Our `name_phonetic` analyzer performs the same steps as our `name_clean`
analyzer, and then it encodes each token using the [NYSIIS algorithm](https://en.wikipedia.org/wiki/New_York_State_Identification_and_Intelligence_System).
Notice how the token "Alice" becomes encoded as "ALAC," which is the same
encoding of phonetically similar names such as "Alicia" or typos such as
"Allice."

**Request**

```javascript
POST zentity_tutorial_2_robust_name_matching/_analyze
{
  "text": "Alice Jones-Smith",
  "analyzer": "name_phonetic"
}
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


### <a name="load-tutorial-data"></a>1.5 Load the tutorial data

> **Note:** Skip this step if you're using the [zentity sandbox](/sandbox).

Add the tutorial data to the index.

```javascript
POST _bulk?refresh
{"index": {"_id": "1", "_index": "zentity_tutorial_2_robust_name_matching"}}
{"city": "Washington", "email": "allie@example.net", "first_name": "Allie", "id": "1", "last_name": "Jones", "phone": "202-555-1234", "state": "DC", "street": "123 Main St"}
{"index": {"_id": "2", "_index": "zentity_tutorial_2_robust_name_matching"}}
{"city": "Washington", "email": "", "first_name": "Alicia", "id": "2", "last_name": "Johnson", "phone": "202-123-4567", "state": "DC", "street": "300 Main St"}
{"index": {"_id": "3", "_index": "zentity_tutorial_2_robust_name_matching"}}
{"city": "Washington", "email": "", "first_name": "Allie", "id": "3", "last_name": "Jones", "phone": "", "state": "DC", "street": "123 Main St"}
{"index": {"_id": "4", "_index": "zentity_tutorial_2_robust_name_matching"}}
{"city": "", "email": "", "first_name": "Ally", "id": "4", "last_name": "Joans", "phone": "202-555-1234", "state": "", "street": ""}
{"index": {"_id": "5", "_index": "zentity_tutorial_2_robust_name_matching"}}
{"city": "Arlington", "email": "ej@example.net", "first_name": "Eli", "id": "5", "last_name": "Jonas", "phone": "", "state": "VA", "street": "500 23rd Street"}
{"index": {"_id": "6", "_index": "zentity_tutorial_2_robust_name_matching"}}
{"city": "Washington", "email": "allie@example.net", "first_name": "Allison", "id": "6", "last_name": "Jones", "phone": "202-555-1234", "state": "DC", "street": "123 Main St"}
{"index": {"_id": "7", "_index": "zentity_tutorial_2_robust_name_matching"}}
{"city": "Washington", "email": "", "first_name": "Allison", "id": "7", "last_name": "Smith", "phone": "+1 (202) 555 1234", "state": "DC", "street": "555 Broad St"}
{"index": {"_id": "8", "_index": "zentity_tutorial_2_robust_name_matching"}}
{"city": "Washington", "email": "alan.smith@example.net", "first_name": "Alan", "id": "8", "last_name": "Smith", "phone": "202-000-5555", "state": "DC", "street": "555 Broad St"}
{"index": {"_id": "9", "_index": "zentity_tutorial_2_robust_name_matching"}}
{"city": "Washington", "email": "alan.smith@example.net", "first_name": "Alan", "id": "9", "last_name": "Smith", "phone": "2020005555", "state": "DC", "street": "555 Broad St"}
{"index": {"_id": "10", "_index": "zentity_tutorial_2_robust_name_matching"}}
{"city": "Washington", "email": "", "first_name": "Alison", "id": "10", "last_name": "Smith", "phone": "202-555-9876", "state": "DC", "street": "555 Broad St"}
{"index": {"_id": "11", "_index": "zentity_tutorial_2_robust_name_matching"}}
{"city": "", "email": "allie@example.net", "first_name": "Alison", "id": "11", "last_name": "Jones-Smith", "phone": "2025559867", "state": "", "street": ""}
{"index": {"_id": "12", "_index": "zentity_tutorial_2_robust_name_matching"}}
{"city": "Washington", "email": "allison.j.smith@corp.example.net", "first_name": "Allison", "id": "12", "last_name": "Jones-Smith", "phone": "", "state": "DC", "street": "555 Broad St"}
{"index": {"_id": "13", "_index": "zentity_tutorial_2_robust_name_matching"}}
{"city": "Arlington", "email": "allison.j.smith@corp.example.net", "first_name": "Allison", "id": "13", "last_name": "Jones Smith", "phone": "703-555-5555", "state": "VA", "street": "1 Corporate Way"}
{"index": {"_id": "14", "_index": "zentity_tutorial_2_robust_name_matching"}}
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

> **Note:** Skip this step if you're using the [zentity sandbox](/sandbox).

Let's use the [Models API](/docs/rest-apis/models-api) to create the entity
model below. We'll review each part of the model in depth.

**Request**

```javascript
PUT _zentity/models/zentity_tutorial_2_person
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
    "zentity_tutorial_2_robust_name_matching": {
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

**Response**

```javascript
{
  "_index" : ".zentity-models",
  "_id" : "zentity_tutorial_2_person",
  "_version" : 1,
  "result" : "created",
  "_shards" : {
    "total" : 2,
    "successful" : 1,
    "failed" : 0
  },
  "_seq_no" : 1,
  "_primary_term" : 1
}
```


### <a name="review-attributes"></a>2.1 Review the attributes

We defined two attributes called `"first_name"` and `"last_name"` as shown in
this section:

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

This is identical to the `"attributes"` field of the entity model in the
[exact name matching](/docs/basic-usage/exact-name-matching#create-entity-model)
tutorial.


### <a name="review-resolvers"></a>2.2 Review the resolvers

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

This is identical to the `"resolvers"` field of the entity model in the
[exact name matching](/docs/basic-usage/exact-name-matching#create-entity-model)
tutorial.

> **Tip**
> 
> Most resolvers should use multiple attributes to resolve an entity to minimize
> false positives. Many people share the same name, but few people share the
> same name and address. Consider all the combinations of attributes that could
> resolve an entity with confidence, and then create a resolver for each
> combination. [Other tutorials](/docs/basic-usage) explore how to use resolvers
> with multiple attributes.


### <a name="review-matchers"></a>2.3 Review the matchers

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

The `"fuzzy"` matcher uses a `match` clause with the [`fuzziness`](https://www.elastic.co/guide/en/elasticsearch/guide/current/fuzzy-match-query.html)
parameter, which matches values with minor dissimilarities such as typos.
Elasticsearch uses the [Damerau-Levenshtein edit distance](https://www.elastic.co/guide/en/elasticsearch/guide/current/fuzziness.html)
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

The `"{{ field }}"` and `"{{ value }}"` strings are special variables. Every
matcher should have these variables defined somewhere in the `"clause"` field.
zentity will replace the `"{{ field }}"` variable with the name of an index
field and the `"{{ value }}"` variable with the value of an attribute.


### <a name="review-indices"></a>2.4 Review the indices

We defined a single index as shown in this section:

```javascript
{
  "indices": {
    "zentity_tutorial_2_robust_name_matching": {
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

### <a name="resolve-entity-basic"></a>3.1 Run a basic resolution job

Let's use the [Resolution API](/docs/rest-apis/resolution-api) to resolve a
person with a known first name and last name.

**Request**

```javascript
POST _zentity/resolution/zentity_tutorial_2_person?pretty&_source=false
{
  "attributes": {
    "first_name": [ "Allie" ],
    "last_name": [ "Jones" ]
  }
}
```

**Response**

```javascript
{
  "took" : 10,
  "hits" : {
    "total" : 3,
    "hits" : [ {
      "_index" : "zentity_tutorial_2_robust_name_matching",
      "_id" : "1",
      "_hop" : 0,
      "_query" : 0,
      "_attributes" : {
        "first_name" : [ "Allie" ],
        "last_name" : [ "Jones" ]
      }
    }, {
      "_index" : "zentity_tutorial_2_robust_name_matching",
      "_id" : "3",
      "_hop" : 0,
      "_query" : 0,
      "_attributes" : {
        "first_name" : [ "Allie" ],
        "last_name" : [ "Jones" ]
      }
    }, {
      "_index" : "zentity_tutorial_2_robust_name_matching",
      "_id" : "4",
      "_hop" : 0,
      "_query" : 0,
      "_attributes" : {
        "first_name" : [ "Ally" ],
        "last_name" : [ "Joans" ]
      }
    } ]
  }
}
```

As expected, we retrieved three documents that match the first name "Allie" and
the last name "Jones," whether those matches were exact matches, phonetic
matches, or transposed matches. The results include a document with the first
name "Ally" and the last name "Joans," which meet this criteria. All documents
came from the same index at the same query of the same hop, as shown in the
`"_index"`, `"_hop"`, and `"_query"` fields.


### <a name="resolve-entity-source"></a>3.2 Show the `"_source"`

We can include the original values of each document as they exist in
Elasticsearch.

Let's run the job again, and now let's include the [`"_source"`](/docs/entity-resolution/output-specification/#hits.hits._source)
field of each document. The [`"_source"`](https://www.elastic.co/guide/en/elasticsearch/reference/current/mapping-source-field.html)
field is the original JSON document that's stored in an Elasticsearch index.

**Request**

```javascript
POST _zentity/resolution/zentity_tutorial_2_person?pretty&_source=true
{
  "attributes": {
    "first_name": [ "Allie" ],
    "last_name": [ "Jones" ]
  }
}
```

**Response**

```javascript
{
  "took" : 9,
  "hits" : {
    "total" : 3,
    "hits" : [ {
      "_index" : "zentity_tutorial_2_robust_name_matching",
      "_id" : "1",
      "_hop" : 0,
      "_query" : 0,
      "_attributes" : {
        "first_name" : [ "Allie" ],
        "last_name" : [ "Jones" ]
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
      "_index" : "zentity_tutorial_2_robust_name_matching",
      "_id" : "3",
      "_hop" : 0,
      "_query" : 0,
      "_attributes" : {
        "first_name" : [ "Allie" ],
        "last_name" : [ "Jones" ]
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
      "_index" : "zentity_tutorial_2_robust_name_matching",
      "_id" : "4",
      "_hop" : 0,
      "_query" : 0,
      "_attributes" : {
        "first_name" : [ "Ally" ],
        "last_name" : [ "Joans" ]
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

Now, in addition to the values mapped to our normalized `"_attributes"`, we can
see the values of those attributes and the values of every other field as they
exist in the `"_source"` of the documents.


### <a name="resolve-entity-explanation"></a>3.3 Show the `"_explanation"`

We can learn how the documents matched, too.

Let's run the job again, and now let's include the [`"_explanation"`](/docs/entity-resolution/output-specification/#hits.hits._explanation)
field to see exactly why each document matched. The `"_explanation"` field tells
us which resolvers caused a document to match, and more specifically, which
input value matched which indexed value using which matcher and any parameters.

**Request**

```javascript
POST _zentity/resolution/zentity_tutorial_2_person?pretty&_source=true&_explanation=true
{
  "attributes": {
    "first_name": [ "Allie" ],
    "last_name": [ "Jones" ]
  }
}
```

**Response**

```javascript
{
  "took" : 12,
  "hits" : {
    "total" : 3,
    "hits" : [ {
      "_index" : "zentity_tutorial_2_robust_name_matching",
      "_id" : "1",
      "_hop" : 0,
      "_query" : 0,
      "_attributes" : {
        "first_name" : [ "Allie" ],
        "last_name" : [ "Jones" ]
      },
      "_explanation" : {
        "resolvers" : {
          "name_only" : {
            "attributes" : [ "first_name", "last_name" ]
          }
        },
        "matches" : [ {
          "attribute" : "first_name",
          "target_field" : "first_name.clean",
          "target_value" : "Allie",
          "input_value" : "Allie",
          "input_matcher" : "fuzzy",
          "input_matcher_params" : { }
        }, {
          "attribute" : "first_name",
          "target_field" : "first_name.phonetic",
          "target_value" : "Allie",
          "input_value" : "Allie",
          "input_matcher" : "simple",
          "input_matcher_params" : { }
        }, {
          "attribute" : "last_name",
          "target_field" : "last_name.clean",
          "target_value" : "Jones",
          "input_value" : "Jones",
          "input_matcher" : "fuzzy",
          "input_matcher_params" : { }
        }, {
          "attribute" : "last_name",
          "target_field" : "last_name.phonetic",
          "target_value" : "Jones",
          "input_value" : "Jones",
          "input_matcher" : "simple",
          "input_matcher_params" : { }
        } ]
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
      "_index" : "zentity_tutorial_2_robust_name_matching",
      "_id" : "3",
      "_hop" : 0,
      "_query" : 0,
      "_attributes" : {
        "first_name" : [ "Allie" ],
        "last_name" : [ "Jones" ]
      },
      "_explanation" : {
        "resolvers" : {
          "name_only" : {
            "attributes" : [ "first_name", "last_name" ]
          }
        },
        "matches" : [ {
          "attribute" : "first_name",
          "target_field" : "first_name.clean",
          "target_value" : "Allie",
          "input_value" : "Allie",
          "input_matcher" : "fuzzy",
          "input_matcher_params" : { }
        }, {
          "attribute" : "first_name",
          "target_field" : "first_name.phonetic",
          "target_value" : "Allie",
          "input_value" : "Allie",
          "input_matcher" : "simple",
          "input_matcher_params" : { }
        }, {
          "attribute" : "last_name",
          "target_field" : "last_name.clean",
          "target_value" : "Jones",
          "input_value" : "Jones",
          "input_matcher" : "fuzzy",
          "input_matcher_params" : { }
        }, {
          "attribute" : "last_name",
          "target_field" : "last_name.phonetic",
          "target_value" : "Jones",
          "input_value" : "Jones",
          "input_matcher" : "simple",
          "input_matcher_params" : { }
        } ]
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
      "_index" : "zentity_tutorial_2_robust_name_matching",
      "_id" : "4",
      "_hop" : 0,
      "_query" : 0,
      "_attributes" : {
        "first_name" : [ "Ally" ],
        "last_name" : [ "Joans" ]
      },
      "_explanation" : {
        "resolvers" : {
          "name_only" : {
            "attributes" : [ "first_name", "last_name" ]
          }
        },
        "matches" : [ {
          "attribute" : "first_name",
          "target_field" : "first_name.phonetic",
          "target_value" : "Ally",
          "input_value" : "Allie",
          "input_matcher" : "simple",
          "input_matcher_params" : { }
        }, {
          "attribute" : "last_name",
          "target_field" : "last_name.phonetic",
          "target_value" : "Joans",
          "input_value" : "Jones",
          "input_matcher" : "simple",
          "input_matcher_params" : { }
        } ]
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

Each document matched because of the `"name_only"` resolver as shown under
`"_explanation"."resolvers"`. Two of the documents had attributes that each
matched in two different ways as shown in `"_explanation"."matches"`.

Let's look at a few of those matches:

```javascript
"_explanation": {
  ...
  "matches" : [
    {
      "attribute" : "first_name",
      "target_field" : "first_name.clean",
      "target_value" : "Allie",
      "input_value" : "Allie",
      "input_matcher" : "fuzzy",
      "input_matcher_params" : { }
    },{
      "attribute" : "first_name",
      "target_field" : "first_name.phonetic",
      "target_value" : "Allie",
      "input_value" : "Allie",
      "input_matcher" : "simple",
      "input_matcher_params" : { }
    },
    ...
  ]
}
```

These two matches tell us that the `"first_name"` attribute was discovered at
two index fields called `"first_name.clean"` and `"first_name.phonetic"`.
We can see that both fields had a value of `"Allie"` that matched a prior known
attribute value of `"Allie"` using the "`fuzzy`" and `"simple"` matchers that we
defined in our entity model. In other words, there were multiple reasons for the
match.

```javascript
"_explanation": {
  ...
  "matches" : [
    {
      "attribute" : "last_name",
      "target_field" : "last_name.phonetic",
      "target_value" : "Joans",
      "input_value" : "Jones",
      "input_matcher" : "simple",
      "input_matcher_params" : { }
    }
    ...
  ]
}
```

This match shows something more interesting than the prior tutorial on exact
name matching. This time the value of `"target_value"` (`"Joans"`) was different
from `"input_value"` (`"Jones"`). But they were considered a match because the
text value of `"last_name.phonetic"` is stored in a phonetic representation that
matched the text of the input value.

> **Tip**
> 
> Keep in mind that the `"target_value"` under the `"_explanation"."matches"`
> shows the value *prior* to any text analysis. In this example, the field
> `"last_name.phonetic"` was a text field that uses phonetic analysis. So the
> actual match was between the values of `"target_value"` and `"input_value"`
> *after* the values were analyzed.
> 
> 
> 
> ```javascript
> POST zentity_tutorial_2_robust_name_matching/_analyze
> {
>   "text": "Jones",
>   "analyzer": "name_phonetic"
> }
> ```
> 
> ```javascript
> POST zentity_tutorial_2_robust_name_matching/_analyze
> {
>   "text": "Joans",
>   "analyzer": "name_phonetic"
> }
> ```
> 
> Our `"name_phonetic"` analyzer, which we defined in our [index settings](/docs/basic-usage/robust-name-matching/#create-tutorial-index),
> converts both `"Jones"` and `"Joans"` to the token `"JAN"`, hence the match.


## <a name="conclusion"></a>Conclusion

Congratulations! You learned how to map a single attribute to multiple fields in
a single index. You also observed how to perform more robust name matching by
using fuzziness, phonetic analyzers, and ICU analyzers.

But we can do better than name matching, right? Lots of people share the same
name. How can we improve accuracy?

The next tutorial will introduce [multiple attribute resolution](/docs/basic-usage/multiple-attribute-resolution).
You will resolve an entity using **multiple attributes** mapped to
**multiple fields** of a **single index**.


&nbsp;

----

#### Continue Reading

|&#8249;|[Exact Name Matching](/docs/basic-usage/exact-name-matching)|[Multiple Attribute Resolution](/docs/basic-usage/multiple-attribute-resolution)|&#8250;|
|:---|:---|---:|---:|
|    |    |    |    |
