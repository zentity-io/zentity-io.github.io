[Home](/) / [Documentation](/docs) / Basic Usage


# <a name="basic-usage"></a>Basic Usage


## <a name="index-data"></a>Step 1. Index some data.

zentity operates on data that is indexed in **[Elasticsearch](https://www.elastic.co/products/elasticsearch)**,
an open source search engine for real-time search and analytics at scale. The most common tools for indexing
documents in Elasticsearch are [Logstash](https://www.elastic.co/guide/en/logstash/6.1/introduction.html) and
[Beats](https://www.elastic.co/guide/en/beats/libbeat/current/beats-reference.html). You can also index single
documents using the [Index API](https://www.elastic.co/guide/en/elasticsearch/guide/current/index-doc.html) or
[Bulk API](https://www.elastic.co/guide/en/elasticsearch/reference/current/docs-bulk.html).


## <a name="define-entity-model"></a>Step 2. Define an entity model.

**[Entity models](/docs/entity-models)** are the most important constructs you need to learn about. zentity uses entity
models to construct queries, match attributes across disparate indices, and resolve entities.

An *entity model* defines the logic for resolving an *entity type* such as a person or organization. It defines the
attributes of the entity ([`"attributes"`](/docs/entity-models/specification#attributes)), the logic to match each attribute
([`"matchers"`](/docs/entity-models/specification#matchers)), the logic to resolve documents to an entity based on the
matching attributes ([`"resolvers"`](/docs/entity-models/specification#resolvers)), and the associations between attributes and matchers with
index fields ([`"indices"`](/docs/entity-models/specification#indices)). This is the step that demands the most thinking. You need to
think about what attributes constitute an entity type, what logic goes into matching each attribute, which attributes and
matchers map to which fields of which indices, and what combinations of matched attributes lead to resolution.

Luckily, all this thinking will pay off quickly, because entity models have two great features:

**Reusability**

Once you have an entity model you can use it everywhere. As you index new data sets with fields that map to familiar
attributes, you can include them in your entity resolution jobs. If you index data with new attributes that aren't
already in your model, you can simply update your model to support them.

**Flexibility**

You don't need to change your data to use an entity model. An entity model only controls the execution of queries.
So there's no risk in updating or experimenting with an entity model.


## <a name="submit-resolution-request"></a>Step 3. Submit a resolution request.

So you have some data and an entity model. Now you can resolve entities!

Once you have an [entity model](/docs/entity-models), you can use the **[Resolution API](/docs/rest-apis/resolution-api)** to run an
entity resolution job using some input.

**Example**

Run an entity resolution job using an indexed entity model called `person`.

```javascript
POST _zentity/resolution/person?pretty
{
  "attributes": {
    "name": "Alice Jones",
    "dob": "1984-01-01",
    "phone": [ "555-123-4567", "555-987-6543" ]
  }
}
```

Run an entity resolution job using an embeded entity model. This example uses three attributes, two resolvers, and two indices.

```javascript
POST _zentity/resolution?pretty
{
  "attributes": {
    "name": "Alice Jones",
    "dob": "1984-01-01",
    "phone": [ "555-123-4567", "555-987-6543" ]
  },
  "model": {
    "attributes": {
      "name": {
        "type": "string"
      },
      "dob": {
        "type": "string"
      },
      "phone": {
        "type": "string"
      }
    },
    "resolvers": {
      "name_dob": {
        "attributes": [
          "name", "dob"
        ]
      },
      "name_phone": {
        "attributes": [
          "name", "phone"
        ]
      }
    },
    "matchers": {
      "exact": {
        "clause": {
          "term": {
            "{{ field }}": "{{ value }}"
          }
        }
      },
      "fuzzy": {
        "clause": {
          "match": {
            "{{ field }}": {
              "query": "{{ value }}",
              "fuzziness": 2
            }
          }
        }
      },
      "standard": {
        "match": {
          "{{ field }}": "{{ value }}"
        }
      }
    },
    "indices": {
      "foo_index": {
        "fields": {
          "full_name": {
            "attribute": "name",
            "matcher": "fuzzy"
          },
          "full_name.phonetic": {
            "attribute": "name",
            "matcher": "standard"
          },
          "date_of_birth.keyword": {
            "attribute": "dob",
            "matcher": "exact"
          },
          "telephone.keyword": {
            "attribute": "phone",
            "matcher": "exact"
          }
        }
      },
      "bar_index": {
        "fields": {
          "nm": {
            "attribute": "name",
            "matcher": "fuzzy"
          },
          "db": {
            "attribute": "dob",
            "matcher": "standard"
          },
          "ph": {
            "attribute": "phone",
            "matcher": "standard"
          }
        }
      }
    }
  }
}
```


&nbsp;

----

#### Continue Reading

|&#8249;|[Installation](/docs/installation)|[Exact Name Matching](/docs/basic-usage/exact-name-matching)|&#8250;|
|:---|:---|---:|---:|
|    |    |    |    |
