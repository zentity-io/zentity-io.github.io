[Home](/) / [Documentation](/docs) / [Basic Usage](/docs/basic-usage) / Exact Name Matching


#### <a name="contents"></a>Basic Usage Tutorials

This tutorial is part of a series to help you learn and perform the basic functions of zentity. Each tutorial adds a little more
sophistication to the prior tutorials, so you can start simple and learn the more advanced features over time.

1. **Exact Name Matching** *&#8592; You are here.*
2. [Robust Name Matching](/docs/basic-usage/robust-name-matching)
3. [Multiple Attribute Resolution](/docs/basic-usage/multiple-attribute-resolution)
4. [Multiple Resolver Resolution](/docs/basic-usage/multiple-resolver-resolution)
5. [Cross Index Resolution](/docs/basic-usage/cross-index-resolution)

---


# <a name="exact-name-matching"></a>Exact Name Matching

This tutorial will guide you through one the simplest forms of entity resolution &ndash; exact name matching. You will learn
how to create an entity model and how to resolve an entity using a single attribute mapped to a single field of a single index.
This is meant to introduce you to the most basic functions of entity resolution with zentity.

Let's dive in.

> **Important**
> 
> You must install [Elasticsearch](https://www.elastic.co/downloads/elasticsearch), [Kibana](https://www.elastic.co/downloads/kibana), and [zentity](/docs/installation) to complete this tutorial.
> This tutorial was tested with [zentity-1.0.0-elasticsearch-6.2.4](/docs/releases).


## <a name="prepare"></a>1. Prepare for the tutorial


### <a name="open-kibana-console-ui"></a>1.1. Open the Kibana Console UI

The [Kibana Console UI](https://www.elastic.co/guide/en/kibana/current/console-kibana.html) makes it easy to
submit requests to Elasticsearch and read responses.


### <a name="delete-old-tutorial-indices"></a>1.2. Delete any old tutorial indices

Let's start from scratch. Delete any tutorial indices you might have created from other tutorials.

```javascript
DELETE .zentity-tutorial-*
```


### <a name="create-tutorial-index"></a>1.3. Create the tutorial index

Now create the index for this tutorial.

<span class="code-overflow"></span>
```javascript
PUT .zentity-tutorial-index
{
  "settings": {
    "index": {
      "number_of_shards": 1,
      "number_of_replicas": 0
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
            "keyword": {
              "type": "keyword"
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


### <a name="load-tutorial-data"></a>1.4. Load the tutorial data

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

Let's use the [Models API](/docs/rest-apis/models-api) to create the entity model below. We'll review
each part of the model in depth.

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
    }
  },
  "indices": {
    ".zentity-tutorial-index": {
      "fields": {
        "user": {
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

The default type of any attribute is `"string"`. You can exclude `"type"` to simplify the entity model
like this:

```javascript
{
  "attributes": {
    "name": {}
  }
}
```


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

This resolver requires only the `"name"` attribute to resolve an entity. So if you try to resolve a
person named "Alice," then every document with the name "Alice" will be grouped with her. Obviously
this would raise many false positives in the real world. We're doing this as a gentle introduction to
the concept of entity resolution.

> **Tip**
> 
> Most resolvers should use multiple attributes to resolve an entity to minimize false positives.
Many people share the same name, but few people share the same name and address. Consider all the
combinations of attributes that could resolve an entity with confidence, and then create a resolver
for each combination. [Other tutorials](/docs/basic-usage) explore how to use resolvers with
multiple attributes.


### <a name="review-matchers"></a>2.3. Review the matchers

We defined a single matcher called `"simple"` as shown in this section:

```javascript
{
  "matchers": {
    "simple": {
      "clause": {
        "match": {
          "{{ field }}": "{{ value }}"
        }
      }
    }
  }
}
```

This matcher uses a simple [`match` clause](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-match-query.html):

```javascript
{
  "match": {
    "{{ field }}": "{{ value }}"
  }
}
```

The `"{{ field }}"` and `"{{ value }}"` strings are special variables. Every matcher should have these
variables defined somewhere in the `"clause"` field. zentity will replace the `"{{ field }}"` variable
with the name of an index field and the `"{{ value }}"` variable with the value of an attribute.


### <a name="review-indices"></a>2.4. Review the indices

We defined a single index as shown in this section:

```javascript
{
  "indices": {
    ".zentity-tutorial-index": {
      "fields": {
        "user": {
          "attribute": "name",
          "matcher": "simple"
        }
      }
    }
  }
}
```

We mapped the `"name"` attribute and the `"simple"` matcher to the `"user"` field of `.zentity-tutorial-index`.


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

Congratulations! You just did one of the simplest forms of entity resolution &ndash; exact name matching.

Not too exciting yet, right? Let's make things a little more interesting.

The next tutorial will show [robust name matching](/docs/basic-usage/robust-name-matching) using multiple forms
of a name to challenges such as typos or phonetic variance. You will resolve an entity using a single attribute
matched to multiple fields of a single index, rather than a single field of a single index.


&nbsp;

----

#### Continue Reading

|&#8249;|[Basic Usage](/docs/basic-usage)|[Robust Name Matching](/docs/basic-usage/robust-name-matching)|&#8250;|
|:---|:---|---:|---:|
|    |    |    |    |
