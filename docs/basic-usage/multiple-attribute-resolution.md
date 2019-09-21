[Home](/) / [Documentation](/docs) / [Basic Usage](/docs/basic-usage) / Multiple Attribute Resolution


#### <a name="contents"></a>Basic Usage Tutorials 📖

This tutorial is part of a series to help you learn and perform the basic
functions of zentity. Each tutorial adds a little more sophistication to the
prior tutorials, so you can start simple and learn the more advanced features
over time.

1. [Exact Name Matching](/docs/basic-usage/exact-name-matching)
2. [Robust Name Matching](/docs/basic-usage/robust-name-matching)
3. **Multiple Attribute Resolution** *&#8592; You are here.*
4. [Multiple Resolver Resolution](/docs/basic-usage/multiple-resolver-resolution)
5. [Cross Index Resolution](/docs/basic-usage/cross-index-resolution)
6. [Scoping Resolution](/docs/basic-usage/scoping-resolution)

---


# <a name="multiple-attribute-resolution"></a>Multiple Attribute Resolution

Never trust a single attribute in isolation, as a general rule.

Using a single attribute for entity resolution is a bad practice &ndash; an
anti-pattern. It's an easy way to "snowball" many different entities together
and drive up your false positive rate. The problem with using a single attribute
is that any attribute is prone to error. Many people can share the same name or
date of birth. A home address can be shared by family members or past residents.
A Social Security Number can be forged, reissued, shared, or mistyped. A bogus
value such as "N/A" or "unknown" can link many entities together.

Instead, trust multiple attributes to corroborate a match.

Consider this an exercise in probability theory. Suppose you have an index of
millions of people. What's the probability that two people share the same name?
It's probably high. What's the probability that people share the same name *and*
the same phone number? It's probably much lower.

This tutorial adds more sophistication to the prior tutorials on
[exact name matching](/docs/basic-usage/exact-name-matching) and
[robust name matching](/docs/basic-usage/robust-name-matching). This time you
will map **multiple attributes** to **multiple fields** of a **single index**.

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

The [Kibana Console UI](https://www.elastic.co/guide/en/kibana/current/console-kibana.html) makes it easy to submit requests to Elasticsearch and read responses.


### <a name="delete-old-tutorial-indices"></a>1.3 Delete any old tutorial indices

> **Note:** Skip this step if you're using the [zentity sandbox](/sandbox).

Let's start from scratch. Delete any tutorial indices you might have created from other tutorials.

```javascript
DELETE zentity_tutorial_3_*
```


### <a name="create-tutorial-index"></a>1.4 Create the tutorial index

> **Note:** Skip this step if you're using the [zentity sandbox](/sandbox).

Now create the index for this tutorial.

```javascript
PUT zentity_tutorial_3_multiple_attribute_resolution
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


### <a name="load-tutorial-data"></a>1.5 Load the tutorial data

> **Note:** Skip this step if you're using the [zentity sandbox](/sandbox).

Add the tutorial data to the index.

```javascript
POST _bulk?refresh
{"index": {"_id": "1", "_index": "zentity_tutorial_3_multiple_attribute_resolution"}}
{"city": "Washington", "email": "allie@example.net", "first_name": "Allie", "id": "1", "last_name": "Jones", "phone": "202-555-1234", "state": "DC", "street": "123 Main St"}
{"index": {"_id": "2", "_index": "zentity_tutorial_3_multiple_attribute_resolution"}}
{"city": "Washington", "email": "", "first_name": "Alicia", "id": "2", "last_name": "Johnson", "phone": "202-123-4567", "state": "DC", "street": "300 Main St"}
{"index": {"_id": "3", "_index": "zentity_tutorial_3_multiple_attribute_resolution"}}
{"city": "Washington", "email": "", "first_name": "Allie", "id": "3", "last_name": "Jones", "phone": "", "state": "DC", "street": "123 Main St"}
{"index": {"_id": "4", "_index": "zentity_tutorial_3_multiple_attribute_resolution"}}
{"city": "", "email": "", "first_name": "Ally", "id": "4", "last_name": "Joans", "phone": "202-555-1234", "state": "", "street": ""}
{"index": {"_id": "5", "_index": "zentity_tutorial_3_multiple_attribute_resolution"}}
{"city": "Arlington", "email": "ej@example.net", "first_name": "Eli", "id": "5", "last_name": "Jonas", "phone": "", "state": "VA", "street": "500 23rd Street"}
{"index": {"_id": "6", "_index": "zentity_tutorial_3_multiple_attribute_resolution"}}
{"city": "Washington", "email": "allie@example.net", "first_name": "Allison", "id": "6", "last_name": "Jones", "phone": "202-555-1234", "state": "DC", "street": "123 Main St"}
{"index": {"_id": "7", "_index": "zentity_tutorial_3_multiple_attribute_resolution"}}
{"city": "Washington", "email": "", "first_name": "Allison", "id": "7", "last_name": "Smith", "phone": "+1 (202) 555 1234", "state": "DC", "street": "555 Broad St"}
{"index": {"_id": "8", "_index": "zentity_tutorial_3_multiple_attribute_resolution"}}
{"city": "Washington", "email": "alan.smith@example.net", "first_name": "Alan", "id": "8", "last_name": "Smith", "phone": "202-000-5555", "state": "DC", "street": "555 Broad St"}
{"index": {"_id": "9", "_index": "zentity_tutorial_3_multiple_attribute_resolution"}}
{"city": "Washington", "email": "alan.smith@example.net", "first_name": "Alan", "id": "9", "last_name": "Smith", "phone": "2020005555", "state": "DC", "street": "555 Broad St"}
{"index": {"_id": "10", "_index": "zentity_tutorial_3_multiple_attribute_resolution"}}
{"city": "Washington", "email": "", "first_name": "Alison", "id": "10", "last_name": "Smith", "phone": "202-555-9876", "state": "DC", "street": "555 Broad St"}
{"index": {"_id": "11", "_index": "zentity_tutorial_3_multiple_attribute_resolution"}}
{"city": "", "email": "allie@example.net", "first_name": "Alison", "id": "11", "last_name": "Jones-Smith", "phone": "2025559867", "state": "", "street": ""}
{"index": {"_id": "12", "_index": "zentity_tutorial_3_multiple_attribute_resolution"}}
{"city": "Washington", "email": "allison.j.smith@corp.example.net", "first_name": "Allison", "id": "12", "last_name": "Jones-Smith", "phone": "", "state": "DC", "street": "555 Broad St"}
{"index": {"_id": "13", "_index": "zentity_tutorial_3_multiple_attribute_resolution"}}
{"city": "Arlington", "email": "allison.j.smith@corp.example.net", "first_name": "Allison", "id": "13", "last_name": "Jones Smith", "phone": "703-555-5555", "state": "VA", "street": "1 Corporate Way"}
{"index": {"_id": "14", "_index": "zentity_tutorial_3_multiple_attribute_resolution"}}
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
PUT _zentity/models/zentity_tutorial_3_person
{
  "attributes": {
    "first_name": {
      "type": "string"
    },
    "last_name": {
      "type": "string"
    },
    "phone": {
      "type": "string"
    }
  },
  "resolvers": {
    "name_phone": {
      "attributes": [ "first_name", "last_name", "phone" ]
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
    "zentity_tutorial_3_multiple_attribute_resolution": {
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
        "phone.clean": {
          "attribute": "phone",
          "matcher": "fuzzy"
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
  "_type" : "doc",
  "_id" : "zentity_tutorial_3_person",
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

We defined three attribute called `"first_name"`, `"last_name"`, and `"phone"`
as shown in this section:

```javascript
{
  "attributes": {
    "first_name": {
      "type": "string"
    },
    "last_name": {
      "type": "string"
    },
    "phone": {
      "type": "string"
    }
  }
}
```


### <a name="review-resolvers"></a>2.2 Review the resolvers

We defined a single resolver called `"name_phone"` as shown in this section:

```javascript
{
  "resolvers": {
    "name_phone": {
      "attributes": [ "first_name", "last_name", "phone" ]
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

The `"exact"` matcher uses a simple [`term` clause](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-term-query.html).
`term` queries apply exact matching for [`keyword`](https://www.elastic.co/guide/en/elasticsearch/reference/current/keyword.html)
fields, while `match` queries apply fuzzy matching for [`text`](https://www.elastic.co/guide/en/elasticsearch/reference/current/text.html)
fields. We can use our `"exact"` matcher on index fields that have a `keyword`
data type.

```javascript
{
  "term": {
    "{{ field }}": "{{ value }}"
  }
}
```


### <a name="review-indices"></a>2.4 Review the indices

We defined a single index as shown in this section:

```javascript
{
  "indices": {
    "zentity_tutorial_3_multiple_attribute_resolution": {
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
        "phone.clean": {
          "attribute": "phone",
          "matcher": "fuzzy"
        }
      }
    }
  }
}
```

> **Tip**
> 
> Notice that the `"phone.keyword"` field is mapped to our `"exact"` matcher
> which uses a `term` query. Elasticsearch expects [`term`](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-term-query.html)
> queries to be executed on the exact value of [`keyword`](https://www.elastic.co/guide/en/elasticsearch/reference/current/keyword.html)
> fields, whereas [`match`](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-match-query.html)
> queries apply [full text](https://www.elastic.co/guide/en/elasticsearch/reference/current/keyword.html)
> analysis to values before performing the search. You might not get the results
> you'd expect if you run either a `term` query on a `text` field or a `match`
> query on a `keyword` field.


## <a name="resolve-entity"></a>3. Resolve an entity


### <a name="resolve-entity-basic"></a>3.1 Run a basic resolution job

Let's use the [Resolution API](/docs/rest-apis/resolution-api) to resolve a
person with a known first name, last name, and phone number.

**Request**

```javascript
POST _zentity/resolution/zentity_tutorial_3_person?pretty&_source=false
{
  "attributes": {
    "first_name": [ "Allison" ],
    "last_name": [ "Jones" ],
    "phone": [ "202-555-9876" ]
  }
}
```

**Response**

```javascript
{
  "took" : 15,
  "hits" : {
    "total" : 2,
    "hits" : [ {
      "_index" : "zentity_tutorial_3_multiple_attribute_resolution",
      "_type" : "_doc",
      "_id" : "11",
      "_hop" : 0,
      "_query" : 0,
      "_attributes" : {
        "first_name" : [ "Alison" ],
        "last_name" : [ "Jones-Smith" ],
        "phone" : [ "2025559867" ]
      }
    }, {
      "_index" : "zentity_tutorial_3_multiple_attribute_resolution",
      "_type" : "_doc",
      "_id" : "10",
      "_hop" : 1,
      "_query" : 0,
      "_attributes" : {
        "first_name" : [ "Alison" ],
        "last_name" : [ "Smith" ],
        "phone" : [ "202-555-9876" ]
      }
    } ]
  }
}
```

As expected, we retrieved two documents each with a matching first name, last
name, and phone number. The documents were retrieved from different queries to
the same index, as shown in the `"_index"`, `"_hop"`, and `"_query"` fields. All
other documents were excluded from the results because they did not meet those
criteria.


### <a name="resolve-entity-source"></a>3.2 Show the `"_source"`

We can include the original values of each document as they exist in
Elasticsearch.

Let's run the job again, and now let's include the [`"_source"`](/docs/entity-resolution/output-specification/#hits.hits._source)
field of each document. The [`"_source"`](https://www.elastic.co/guide/en/elasticsearch/reference/current/mapping-source-field.html)
field is the original JSON document that's stored in an Elasticsearch index.

**Request**

```javascript
POST _zentity/resolution/zentity_tutorial_3_person?pretty&_source=true
{
  "attributes": {
    "first_name": [ "Allison" ],
    "last_name": [ "Jones" ],
    "phone": [ "202-555-9876" ]
  }
}
```

**Response**

```javascript
{
  "took" : 16,
  "hits" : {
    "total" : 2,
    "hits" : [ {
      "_index" : "zentity_tutorial_3_multiple_attribute_resolution",
      "_type" : "_doc",
      "_id" : "11",
      "_hop" : 0,
      "_query" : 0,
      "_attributes" : {
        "first_name" : [ "Alison" ],
        "last_name" : [ "Jones-Smith" ],
        "phone" : [ "2025559867" ]
      },
      "_source" : {
        "city" : "",
        "email" : "allie@example.net",
        "first_name" : "Alison",
        "id" : "11",
        "last_name" : "Jones-Smith",
        "phone" : "2025559867",
        "state" : "",
        "street" : ""
      }
    }, {
      "_index" : "zentity_tutorial_3_multiple_attribute_resolution",
      "_type" : "_doc",
      "_id" : "10",
      "_hop" : 1,
      "_query" : 0,
      "_attributes" : {
        "first_name" : [ "Alison" ],
        "last_name" : [ "Smith" ],
        "phone" : [ "202-555-9876" ]
      },
      "_source" : {
        "city" : "Washington",
        "email" : "",
        "first_name" : "Alison",
        "id" : "10",
        "last_name" : "Smith",
        "phone" : "202-555-9876",
        "state" : "DC",
        "street" : "555 Broad St"
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
POST _zentity/resolution/zentity_tutorial_3_person?pretty&_source=true&_explanation=true
{
  "attributes": {
    "first_name": [ "Allison" ],
    "last_name": [ "Jones" ],
    "phone": [ "202-555-9876" ]
  }
}
```

**Response**

```javascript
{
  "took" : 20,
  "hits" : {
    "total" : 2,
    "hits" : [ {
      "_index" : "zentity_tutorial_3_multiple_attribute_resolution",
      "_type" : "_doc",
      "_id" : "11",
      "_hop" : 0,
      "_query" : 0,
      "_attributes" : {
        "first_name" : [ "Alison" ],
        "last_name" : [ "Jones-Smith" ],
        "phone" : [ "2025559867" ]
      },
      "_explanation" : {
        "resolvers" : {
          "name_phone" : {
            "attributes" : [ "first_name", "last_name", "phone" ]
          }
        },
        "matches" : [ {
          "attribute" : "first_name",
          "target_field" : "first_name.clean",
          "target_value" : "Alison",
          "input_value" : "Allison",
          "input_matcher" : "fuzzy",
          "input_matcher_params" : { }
        }, {
          "attribute" : "first_name",
          "target_field" : "first_name.phonetic",
          "target_value" : "Alison",
          "input_value" : "Allison",
          "input_matcher" : "simple",
          "input_matcher_params" : { }
        }, {
          "attribute" : "last_name",
          "target_field" : "last_name.clean",
          "target_value" : "Jones-Smith",
          "input_value" : "Jones",
          "input_matcher" : "fuzzy",
          "input_matcher_params" : { }
        }, {
          "attribute" : "last_name",
          "target_field" : "last_name.phonetic",
          "target_value" : "Jones-Smith",
          "input_value" : "Jones",
          "input_matcher" : "simple",
          "input_matcher_params" : { }
        }, {
          "attribute" : "phone",
          "target_field" : "phone.clean",
          "target_value" : "2025559867",
          "input_value" : "202-555-9876",
          "input_matcher" : "fuzzy",
          "input_matcher_params" : { }
        } ]
      },
      "_source" : {
        "city" : "",
        "email" : "allie@example.net",
        "first_name" : "Alison",
        "id" : "11",
        "last_name" : "Jones-Smith",
        "phone" : "2025559867",
        "state" : "",
        "street" : ""
      }
    }, {
      "_index" : "zentity_tutorial_3_multiple_attribute_resolution",
      "_type" : "_doc",
      "_id" : "10",
      "_hop" : 1,
      "_query" : 0,
      "_attributes" : {
        "first_name" : [ "Alison" ],
        "last_name" : [ "Smith" ],
        "phone" : [ "202-555-9876" ]
      },
      "_explanation" : {
        "resolvers" : {
          "name_phone" : {
            "attributes" : [ "first_name", "last_name", "phone" ]
          }
        },
        "matches" : [ {
          "attribute" : "first_name",
          "target_field" : "first_name.clean",
          "target_value" : "Alison",
          "input_value" : "Alison",
          "input_matcher" : "fuzzy",
          "input_matcher_params" : { }
        }, {
          "attribute" : "first_name",
          "target_field" : "first_name.clean",
          "target_value" : "Alison",
          "input_value" : "Allison",
          "input_matcher" : "fuzzy",
          "input_matcher_params" : { }
        }, {
          "attribute" : "first_name",
          "target_field" : "first_name.phonetic",
          "target_value" : "Alison",
          "input_value" : "Alison",
          "input_matcher" : "simple",
          "input_matcher_params" : { }
        }, {
          "attribute" : "first_name",
          "target_field" : "first_name.phonetic",
          "target_value" : "Alison",
          "input_value" : "Allison",
          "input_matcher" : "simple",
          "input_matcher_params" : { }
        }, {
          "attribute" : "last_name",
          "target_field" : "last_name.clean",
          "target_value" : "Smith",
          "input_value" : "Jones-Smith",
          "input_matcher" : "fuzzy",
          "input_matcher_params" : { }
        }, {
          "attribute" : "last_name",
          "target_field" : "last_name.phonetic",
          "target_value" : "Smith",
          "input_value" : "Jones-Smith",
          "input_matcher" : "simple",
          "input_matcher_params" : { }
        }, {
          "attribute" : "phone",
          "target_field" : "phone.clean",
          "target_value" : "202-555-9876",
          "input_value" : "202-555-9876",
          "input_matcher" : "fuzzy",
          "input_matcher_params" : { }
        }, {
          "attribute" : "phone",
          "target_field" : "phone.clean",
          "target_value" : "202-555-9876",
          "input_value" : "2025559867",
          "input_matcher" : "fuzzy",
          "input_matcher_params" : { }
        } ]
      },
      "_source" : {
        "city" : "Washington",
        "email" : "",
        "first_name" : "Alison",
        "id" : "10",
        "last_name" : "Smith",
        "phone" : "202-555-9876",
        "state" : "DC",
        "street" : "555 Broad St"
      }
    } ]
  }
}
```

Each document matched because of the `"name_phone"` resolver as shown under
`"_explanation"."resolvers"`. But the resolvers matched for different reasons
in each document. Notice that the first document matched on hop 0 and the other
document matched on hop 1. The `"last_name"` of the input (`"Jones"`) matched
the `"last_name"` of the second matching document (`"Smith"`) because both
matched the `"last_name"` of the first matching document (`"Jones-Smith"`) and
each document also had matching `"first_name"` and `"phone"` attributes.

You can see that our `"fuzzy"` matcher is handling messy values successfully,
too, as shown in the example below. Notice how the last two numbers are
transposed (`76` and `67`), which is a common form of typo.

```javascript
"_explanation": {
  ...
  "matches": [
    {
      "attribute" : "phone",
      "target_field" : "phone.clean",
      "target_value" : "202-555-9876",
      "input_value" : "2025559867",
      "input_matcher" : "fuzzy",
      "input_matcher_params" : { }
    },
    ...
  ]
}
```


## <a name="conclusion"></a>Conclusion

Congratulations! You learned how to map multiple attributes to multiple fields
in a single index.

Hopefully a couple things are becoming clear in this tutorial:

1. Entity resolution is complex. This tutorial shows a simple example, and
already there are many nuances to consider in the results, as we can see in the
`"_explanation"` field.
2. The `"_explanation"` field is a powerful tool for understanding,
troubleshooting, and optimizing your match logic &ndash; especially as your data
and models become more complex.

The next tutorial will introduce [multiple resolver resolution](/docs/basic-usage/multiple-resolver-resolution).
You will resolve an entity using **multiple combinations of attributes**
(i.e. "resolvers") mapped to **multiple fields** of a **single index**.


&nbsp;

----

#### Continue Reading

|&#8249;|[Robust Name Matching](/docs/basic-usage/robust-name-matching)|[Multiple Resolver Resolution](/docs/basic-usage/multiple-resolver-resolution)|&#8250;|
|:---|:---|---:|---:|
|    |    |    |    |
