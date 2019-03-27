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

Welcome to the "Hello world!" of entity resolution.

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
  "mappings": {
    "_doc": {
      "properties": {
        "id": {
          "type": "keyword"
        },
        "first_name": {
          "type": "text"
        },
        "last_name": {
          "type": "text"
        },
        "street": {
          "type": "text"
        },
        "city": {
          "type": "text"
        },
        "state": {
          "type": "text"
        },
        "phone": {
          "type": "text"
        },
        "email": {
          "type": "text"
        }
      }
    }
  }
}
```


### <a name="load-tutorial-data"></a>1.4. Load the tutorial data

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

Let's use the [Models API](/docs/rest-apis/models-api) to create the entity model below. We'll review
each part of the model in depth.

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
    }
  },
  "indices": {
    ".zentity-tutorial-index": {
      "fields": {
        "first_name": {
          "attribute": "first_name",
          "matcher": "simple"
        },
        "last_name": {
          "attribute": "last_name",
          "matcher": "simple"
        }
      }
    }
  }
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

The default type of any attribute is `"string"`. You can exclude `"type"` to simplify the entity model
like this:

```javascript
{
  "attributes": {
    "first_name": {},
    "last_name": {}
  }
}
```


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

This resolver requires only the `"first_name"` and `"last_name"` attributes to resolve an entity. So if you try to resolve a
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
        "first_name": {
          "attribute": "first_name",
          "matcher": "simple"
        },
        "last_name": {
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
  "took" : 2,
  "hits" : {
    "total" : 2,
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
    } ]
  }
}
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
