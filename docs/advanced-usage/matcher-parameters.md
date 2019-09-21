[Home](/) / [Documentation](/docs) / [Advanced Usage](/docs/advanced-usage) / Matcher Parameters


#### <a name="contents"></a>Advanced Usage Tutorials 📖

This tutorial is part of a series to help you learn and perform the advanced
functions of zentity. You should complete the [basic usage](/docs/basic-usage)
tutorials before completing these advanced usage tutorials.

1. **Matcher Parameters** *&#8592; You are here.*
2. [Date Attributes](/docs/advanced-usage/date-attributes)
3. [Payload Attributes](/docs/advanced-usage/payload-attributes)

---


# <a name="matcher-parameters"></a>Matcher Parameters

You can parameterize any **[`"clause"`](/docs/entity-models/specification#matchers.MATCHER_NAME.clause)**
in the the **[`"matchers"`](/docs/entity-models/specification#matchers)** object
of an entity model. Matcher parameters (**[`"params"`](/docs/entity-models/specification#matchers.MATCHER_NAME.params)**)
are variables that allow you to pass arbitrary values from the attribute to the
matcher. This gives you more flexibility and control over the matching process
when you run a resolution job.

This tutorial will show how to define and override matcher parameters to modify
the behavior of matchers at runtime.

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


### <a name="open-kibana-console-ui"></a>1.1 Open the Kibana Console UI

The [Kibana Console UI](https://www.elastic.co/guide/en/kibana/current/console-kibana.html)
makes it easy to submit requests to Elasticsearch and read responses.


### <a name="delete-old-tutorial-indices"></a>1.2 Delete any old tutorial indices

> **Note:** Skip this step if you're using the [zentity sandbox](/sandbox).

Let's start from scratch. Delete any tutorial indices you might have created from
other tutorials.

```javascript
DELETE zentity_tutorial_7_*
```


### <a name="create-tutorial-index"></a>1.3 Create the tutorial index

> **Note:** Skip this step if you're using the [zentity sandbox](/sandbox).

Now create the index for this tutorial.

```javascript
PUT zentity_tutorial_7_matcher_parameters
{
  "settings": {
    "index": {
      "number_of_shards": 1,
      "number_of_replicas": 0,
      "analysis" : {
        "filter" : {
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
              "lowercase",
              "punct_white"
            ],
            "tokenizer" : "standard"
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
          }
        }
      },
      "last_name": {
        "type": "text",
        "fields": {
          "clean": {
            "type": "text",
            "analyzer": "name_clean"
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
      }
    }
  }
}
```


### <a name="load-tutorial-data"></a>1.4 Load the tutorial data

> **Note:** Skip this step if you're using the [zentity sandbox](/sandbox).

Add the tutorial data to the index.

```javascript
POST _bulk?refresh
{"index": {"_id": "1", "_index": "zentity_tutorial_7_matcher_parameters"}}
{"first_name": "Allie", "id": "1", "last_name": "Jones", "phone": "202-555-1234"}
{"index": {"_id": "2", "_index": "zentity_tutorial_7_matcher_parameters"}}
{"first_name": "Alicia", "id": "2", "last_name": "Johnson", "phone": "202-123-4567"}
{"index": {"_id": "3", "_index": "zentity_tutorial_7_matcher_parameters"}}
{"first_name": "Allie", "id": "3", "last_name": "Joans", "phone": "202-555-1432"}
{"index": {"_id": "4", "_index": "zentity_tutorial_7_matcher_parameters"}}
{"first_name": "Ellie", "id": "4", "last_name": "Jones", "phone": "202-555-1234"}
{"index": {"_id": "5", "_index": "zentity_tutorial_7_matcher_parameters"}}
{"first_name": "Ali", "id": "5", "last_name": "Jones", "phone": "202-555-1234"}
```

Here's what the tutorial data looks like.

|id|first_name|last_name|phone|
|:---|:---|:---|:---|
|1|Allie|Jones|202-555-1234|
|2|Alicia|Johnson|202-123-4567|
|3|Allie|Joans|202-555-1423|
|4|Ellie|Jones|202-555-1234|
|5|Ali|Jones|202-555-1234|


## <a name="create-entity-model"></a>2. Create the entity model

> **Note:** Skip this step if you're using the [zentity sandbox](/sandbox).

Let's use the [Models API](/docs/rest-apis/models-api) to create the entity
model below. We'll review the matchers in depth.

**Request**

```javascript
PUT _zentity/models/zentity_tutorial_7_person
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
    "fuzzy": {
      "clause":{
        "match": {
          "{{ field }}": {
            "query": "{{ value }}",
            "fuzziness": "auto"
          }
        }
      }
    },
    "fuzzy_params": {
      "clause":{
        "match": {
          "{{ field }}": {
            "query": "{{ value }}",
            "fuzziness": "{{ params.fuzziness }}"
          }
        }
      },
      "params": {
        "fuzziness": "auto"
      }
    }
  },
  "indices": {
    "zentity_tutorial_7_matcher_parameters": {
      "fields": {
        "first_name.clean": {
          "attribute": "first_name",
          "matcher": "fuzzy_params"
        },
        "last_name.clean": {
          "attribute": "last_name",
          "matcher": "fuzzy_params"
        },
        "phone.clean": {
          "attribute": "phone",
          "matcher": "fuzzy_params"
        }
      }
    }
  }
}
```


### <a name="review-matchers"></a>2.1 Review the matchers

We defined two matchers called `"fuzzy"` and `"fuzzy_params"` as shown in this
section:

```javascript
{
  "matchers": {
    "fuzzy": {
      "clause":{
        "match": {
          "{{ field }}": {
            "query": "{{ value }}",
            "fuzziness": "auto"
          }
        }
      }
    },
    "fuzzy_params": {
      "clause":{
        "match": {
          "{{ field }}": {
            "query": "{{ value }}",
            "fuzziness": "{{ params.fuzziness }}"
          }
        }
      },
      "params": {
        "fuzziness": "auto"
      }
    }
  }
}
```

These matchers are nearly identical. Both will perform the same fuzzy matching
logic by default. But the `"fuzzy_params"` matcher uses `"params"` to turn the
`"fuzziness"` field into a variable.

According to the [entity model specification](/docs/entity-models/specification),
the [`"clause"`](/docs/entity-models/specification#matchers.MATCHER_NAME.clause)
of any matcher requires two variables:

> Matcher clauses use Mustache syntax to pass two important variables:
**`{{ field }}`** and **`{{ value }}`**. The `field` variable will be populated
with the index field that maps to the attribute. The `value` field will be
populated with the value that will be queried for that attribute. This syntax is
the same as the one used by Elasticsearch [search templates](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-template.html).

Let's look at our `"fuzzy"` matcher. This matcher uses no params.

```javascript
{
  "matchers": {
    "fuzzy": {
      "clause":{
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

Additional variables or "params" can be passed to the matcher using the syntax
**`{{ params.PARAM_NAME }}`** where `PARAM_NAME` is the name of your parameter.
You must define the default values for each parameter in the [`"params"`](/docs/entity-models/specification#matchers.MATCHER_NAME.params)
object adjacent to the [`"clause"`](/docs/entity-models/specification#matchers.MATCHER_NAME.clause)
object of a matcher.

Now let's look at our `"fuzzy_params"` matcher. This matcher uses `"params"` to
allow the `"fuzziness"` field of the `match` clause to be changed at runtime.

```javascript
{
  "matchers": {
    "fuzzy_params": {
      "clause":{
        "match": {
          "{{ field }}": {
            "query": "{{ value }}",
            "fuzziness": "{{ params.fuzziness }}"
          }
        }
      },
      "params": {
        "fuzziness": "auto"
      }
    }
  }
}
```

Now that we have defined a matcher with parameters, let's see how we can
override the default values of those parameters.


## <a name="resolve-entity"></a>3. Resolve an entity

Let's use the [Resolution API](/docs/rest-apis/resolution-api) to resolve a
person with a known first name, last name, and phone number.

**Request**

```javascript
POST _zentity/resolution/zentity_tutorial_7_person?pretty&_source=false&_explanation=true
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
  "took" : 7,
  "hits" : {
    "total" : 2,
    "hits" : [ {
      "_index" : "zentity_tutorial_7_matcher_parameters",
      "_type" : "_doc",
      "_id" : "1",
      "_hop" : 0,
      "_query" : 0,
      "_attributes" : {
        "first_name" : [ "Allie" ],
        "last_name" : [ "Jones" ],
        "phone" : [ "202-555-1234" ]
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
          "target_value" : "Allie",
          "input_value" : "Allie",
          "input_matcher" : "fuzzy_params",
          "input_matcher_params" : { }
        }, {
          "attribute" : "last_name",
          "target_field" : "last_name.clean",
          "target_value" : "Jones",
          "input_value" : "Jones",
          "input_matcher" : "fuzzy_params",
          "input_matcher_params" : { }
        }, {
          "attribute" : "phone",
          "target_field" : "phone.clean",
          "target_value" : "202-555-1234",
          "input_value" : "202-555-1234",
          "input_matcher" : "fuzzy_params",
          "input_matcher_params" : { }
        } ]
      }
    }, {
      "_index" : "zentity_tutorial_7_matcher_parameters",
      "_type" : "_doc",
      "_id" : "4",
      "_hop" : 0,
      "_query" : 0,
      "_attributes" : {
        "first_name" : [ "Ellie" ],
        "last_name" : [ "Jones" ],
        "phone" : [ "202-555-1234" ]
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
          "target_value" : "Ellie",
          "input_value" : "Allie",
          "input_matcher" : "fuzzy_params",
          "input_matcher_params" : { }
        }, {
          "attribute" : "last_name",
          "target_field" : "last_name.clean",
          "target_value" : "Jones",
          "input_value" : "Jones",
          "input_matcher" : "fuzzy_params",
          "input_matcher_params" : { }
        }, {
          "attribute" : "phone",
          "target_field" : "phone.clean",
          "target_value" : "202-555-1234",
          "input_value" : "202-555-1234",
          "input_matcher" : "fuzzy_params",
          "input_matcher_params" : { }
        } ]
      }
    } ]
  }
}
```

Only two results were returned. Out of the five documents that exist in the
index, four of them appear to be the entity that we are searching for. We need
to allow more fuzziness to capture those other two documents.

Our `"fuzzy_params"` matcher uses a `"fuzziness"` value of `"auto"`. According
to its [documentation](https://www.elastic.co/guide/en/elasticsearch/reference/current/common-options.html#fuzziness),
a value of `"auto"` will match strings that differ by one character if the
strings are 3-5 characters long, and it will match strings that differ by two
characters if the strings are 6+ characters long. The first name and last name
of our entity falls within the range of 3-5 characters, which will allow only
one character difference to match.

Let's set the value of `"fuzziness"` to `2` for our `"first_name"` attribute.

**Request**

```javascript
POST _zentity/resolution/zentity_tutorial_7_person?pretty&_source=false&_explanation=true
{
  "attributes": {
    "first_name": {
      "values": [ "Allie" ],
      "params": {
        "fuzziness": "2"
      }
    },
    "last_name": [ "Jones" ],
    "phone": [ "202-555-1234" ]
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
      "_index" : "zentity_tutorial_7_matcher_parameters",
      "_type" : "_doc",
      "_id" : "1",
      "_hop" : 0,
      "_query" : 0,
      "_attributes" : {
        "first_name" : [ "Allie" ],
        "last_name" : [ "Jones" ],
        "phone" : [ "202-555-1234" ]
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
          "target_value" : "Allie",
          "input_value" : "Allie",
          "input_matcher" : "fuzzy_params",
          "input_matcher_params" : {
            "fuzziness" : "2"
          }
        }, {
          "attribute" : "last_name",
          "target_field" : "last_name.clean",
          "target_value" : "Jones",
          "input_value" : "Jones",
          "input_matcher" : "fuzzy_params",
          "input_matcher_params" : { }
        }, {
          "attribute" : "phone",
          "target_field" : "phone.clean",
          "target_value" : "202-555-1234",
          "input_value" : "202-555-1234",
          "input_matcher" : "fuzzy_params",
          "input_matcher_params" : { }
        } ]
      }
    }, {
      "_index" : "zentity_tutorial_7_matcher_parameters",
      "_type" : "_doc",
      "_id" : "4",
      "_hop" : 0,
      "_query" : 0,
      "_attributes" : {
        "first_name" : [ "Ellie" ],
        "last_name" : [ "Jones" ],
        "phone" : [ "202-555-1234" ]
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
          "target_value" : "Ellie",
          "input_value" : "Allie",
          "input_matcher" : "fuzzy_params",
          "input_matcher_params" : {
            "fuzziness" : "2"
          }
        }, {
          "attribute" : "last_name",
          "target_field" : "last_name.clean",
          "target_value" : "Jones",
          "input_value" : "Jones",
          "input_matcher" : "fuzzy_params",
          "input_matcher_params" : { }
        }, {
          "attribute" : "phone",
          "target_field" : "phone.clean",
          "target_value" : "202-555-1234",
          "input_value" : "202-555-1234",
          "input_matcher" : "fuzzy_params",
          "input_matcher_params" : { }
        } ]
      }
    }, {
      "_index" : "zentity_tutorial_7_matcher_parameters",
      "_type" : "_doc",
      "_id" : "5",
      "_hop" : 0,
      "_query" : 0,
      "_attributes" : {
        "first_name" : [ "Ali" ],
        "last_name" : [ "Jones" ],
        "phone" : [ "202-555-1234" ]
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
          "target_value" : "Ali",
          "input_value" : "Allie",
          "input_matcher" : "fuzzy_params",
          "input_matcher_params" : {
            "fuzziness" : "2"
          }
        }, {
          "attribute" : "last_name",
          "target_field" : "last_name.clean",
          "target_value" : "Jones",
          "input_value" : "Jones",
          "input_matcher" : "fuzzy_params",
          "input_matcher_params" : { }
        }, {
          "attribute" : "phone",
          "target_field" : "phone.clean",
          "target_value" : "202-555-1234",
          "input_value" : "202-555-1234",
          "input_matcher" : "fuzzy_params",
          "input_matcher_params" : { }
        } ]
      }
    } ]
  }
}
```

This returned three of the four matching documents. The first names "Allie" and
"Ali" now match because they differ by two characters.

Let's also set the value of `"fuzziness"` to `2` for our `"last_name"` attribute.

**Request**

```javascript
POST _zentity/resolution/zentity_tutorial_7_person?pretty&_source=false&_explanation=true
{
  "attributes": {
    "first_name": {
      "values": [ "Allie" ],
      "params": {
        "fuzziness": "2"
      }
    },
    "last_name": {
      "values": [ "Jones" ],
      "params": {
        "fuzziness": "2"
      }
    },
    "phone": [ "202-555-1234" ]
  }
}
```

**Response**

```javascript
{
  "took" : 15,
  "hits" : {
    "total" : 4,
    "hits" : [ {
      "_index" : "zentity_tutorial_7_matcher_parameters",
      "_type" : "_doc",
      "_id" : "1",
      "_hop" : 0,
      "_query" : 0,
      "_attributes" : {
        "first_name" : [ "Allie" ],
        "last_name" : [ "Jones" ],
        "phone" : [ "202-555-1234" ]
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
          "target_value" : "Allie",
          "input_value" : "Allie",
          "input_matcher" : "fuzzy_params",
          "input_matcher_params" : {
            "fuzziness" : "2"
          }
        }, {
          "attribute" : "last_name",
          "target_field" : "last_name.clean",
          "target_value" : "Jones",
          "input_value" : "Jones",
          "input_matcher" : "fuzzy_params",
          "input_matcher_params" : {
            "fuzziness" : "2"
          }
        }, {
          "attribute" : "phone",
          "target_field" : "phone.clean",
          "target_value" : "202-555-1234",
          "input_value" : "202-555-1234",
          "input_matcher" : "fuzzy_params",
          "input_matcher_params" : { }
        } ]
      }
    }, {
      "_index" : "zentity_tutorial_7_matcher_parameters",
      "_type" : "_doc",
      "_id" : "3",
      "_hop" : 0,
      "_query" : 0,
      "_attributes" : {
        "first_name" : [ "Allie" ],
        "last_name" : [ "Joans" ],
        "phone" : [ "202-555-1432" ]
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
          "target_value" : "Allie",
          "input_value" : "Allie",
          "input_matcher" : "fuzzy_params",
          "input_matcher_params" : {
            "fuzziness" : "2"
          }
        }, {
          "attribute" : "last_name",
          "target_field" : "last_name.clean",
          "target_value" : "Joans",
          "input_value" : "Jones",
          "input_matcher" : "fuzzy_params",
          "input_matcher_params" : {
            "fuzziness" : "2"
          }
        }, {
          "attribute" : "phone",
          "target_field" : "phone.clean",
          "target_value" : "202-555-1432",
          "input_value" : "202-555-1234",
          "input_matcher" : "fuzzy_params",
          "input_matcher_params" : { }
        } ]
      }
    }, {
      "_index" : "zentity_tutorial_7_matcher_parameters",
      "_type" : "_doc",
      "_id" : "4",
      "_hop" : 0,
      "_query" : 0,
      "_attributes" : {
        "first_name" : [ "Ellie" ],
        "last_name" : [ "Jones" ],
        "phone" : [ "202-555-1234" ]
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
          "target_value" : "Ellie",
          "input_value" : "Allie",
          "input_matcher" : "fuzzy_params",
          "input_matcher_params" : {
            "fuzziness" : "2"
          }
        }, {
          "attribute" : "last_name",
          "target_field" : "last_name.clean",
          "target_value" : "Jones",
          "input_value" : "Jones",
          "input_matcher" : "fuzzy_params",
          "input_matcher_params" : {
            "fuzziness" : "2"
          }
        }, {
          "attribute" : "phone",
          "target_field" : "phone.clean",
          "target_value" : "202-555-1234",
          "input_value" : "202-555-1234",
          "input_matcher" : "fuzzy_params",
          "input_matcher_params" : { }
        } ]
      }
    }, {
      "_index" : "zentity_tutorial_7_matcher_parameters",
      "_type" : "_doc",
      "_id" : "5",
      "_hop" : 0,
      "_query" : 0,
      "_attributes" : {
        "first_name" : [ "Ali" ],
        "last_name" : [ "Jones" ],
        "phone" : [ "202-555-1234" ]
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
          "target_value" : "Ali",
          "input_value" : "Allie",
          "input_matcher" : "fuzzy_params",
          "input_matcher_params" : {
            "fuzziness" : "2"
          }
        }, {
          "attribute" : "last_name",
          "target_field" : "last_name.clean",
          "target_value" : "Jones",
          "input_value" : "Jones",
          "input_matcher" : "fuzzy_params",
          "input_matcher_params" : {
            "fuzziness" : "2"
          }
        }, {
          "attribute" : "phone",
          "target_field" : "phone.clean",
          "target_value" : "202-555-1234",
          "input_value" : "202-555-1234",
          "input_matcher" : "fuzzy_params",
          "input_matcher_params" : { }
        } ]
      }
    } ]
  }
}
```

Now we have all four matching results. The last names "Jones" and "Joans" now 
match because they differ by two characters. The phone number for document `"3"`
also differs by two characters from the other phone numbers. They matched
because a fuzziness value of `"auto"` allows two characters to differ when the
length of the strings are greater than or equal to six characters.

What if we disabled `"fuzziness"` on every attribute? Let's try it.

**Request**

```javascript
POST _zentity/resolution/zentity_tutorial_7_person?pretty&_source=false&_explanation=true
{
  "attributes": {
    "first_name": {
      "values": [ "Allie" ],
      "params": {
        "fuzziness": "0"
      }
    },
    "last_name": {
      "values": [ "Jones" ],
      "params": {
        "fuzziness": "0"
      }
    },
    "phone": {
      "values": [ "202-555-1234" ],
      "params": {
        "fuzziness": "0"
      }
    }
  }
}
```

**Response**

```javascript
{
  "took" : 2,
  "hits" : {
    "total" : 1,
    "hits" : [ {
      "_index" : "zentity_tutorial_7_matcher_parameters",
      "_type" : "_doc",
      "_id" : "1",
      "_hop" : 0,
      "_query" : 0,
      "_attributes" : {
        "first_name" : [ "Allie" ],
        "last_name" : [ "Jones" ],
        "phone" : [ "202-555-1234" ]
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
          "target_value" : "Allie",
          "input_value" : "Allie",
          "input_matcher" : "fuzzy_params",
          "input_matcher_params" : {
            "fuzziness" : "0"
          }
        }, {
          "attribute" : "last_name",
          "target_field" : "last_name.clean",
          "target_value" : "Jones",
          "input_value" : "Jones",
          "input_matcher" : "fuzzy_params",
          "input_matcher_params" : {
            "fuzziness" : "0"
          }
        }, {
          "attribute" : "phone",
          "target_field" : "phone.clean",
          "target_value" : "202-555-1234",
          "input_value" : "202-555-1234",
          "input_matcher" : "fuzzy_params",
          "input_matcher_params" : {
            "fuzziness" : "0"
          }
        } ]
      }
    } ]
  }
}
```

Only one document matched because every attribute matched our inputs exactly.


## <a name="conclusion"></a>Conclusion

You learned how to parameterize the clauses of matchers in entity models. This
gives you the ability to modify the behavior of matchers at runtime.

The next tutorial will introduce [date attributes](/docs/advanced-usage/date-attributes),
which require matcher parameters and can be used to match both points in time
and ranges of time.


&nbsp;

----

#### Continue Reading

|&#8249;|[Advanced Usage](/docs/advanced-usage)|[Date Attributes](/docs/advanced-usage/date-attributes)|&#8250;|
|:---|:---|---:|---:|
|    |    |    |    |
