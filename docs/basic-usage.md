[Home](/#/) / [Documentation](/#/docs) / Basic Usage


# Basic Usage


## Step 1. Index some data.

zentity operates on data that is indexed in **[Elasticsearch](https://www.elastic.co/products/elasticsearch)**,
an open source search engine for real-time search and analytics at scale. The most common tools for indexing
documents in Elasticsearch are [Logstash](https://www.elastic.co/guide/en/logstash/6.1/introduction.html) and
[Beats](https://www.elastic.co/guide/en/beats/libbeat/current/beats-reference.html). You can also index single
documents using the [Index API](https://www.elastic.co/guide/en/elasticsearch/guide/current/index-doc.html) or
[Bulk API](https://www.elastic.co/guide/en/elasticsearch/reference/current/docs-bulk.html).


## Step 2. Define an entity model.

***[Entity models](/#/docs/entity-models)*** are the most important constructs you need to learn about. zentity uses entity
models to construct queries, match attributes across disparate indices, and resolve entities.

An *entity model* defines the logic for resolving an *entity type* such as a person or organization. It defines the
attributes of the entity ([`"attributes"`](/#/docs/entity-models/specification)), the logic to match each attribute
([`"matchers"`](Entity-Models#attributes.matcher)), the logic to resolve documents to an entity based on the
matching attributes ([`"resolvers"`](/#/docs/entity-models/specification)), and the associations between attribute matchers and
index fields ([`"indices"`](/#/docs/entity-models/specification)). This is the step that demands the most thinking. You need to
think about what attributes constitute an entity type, what logic goes into matching each attribute, what "attribute
matchers" map to what indexed fields, and what combinations of matched attributes lead to resolution.

Luckily, all this thinking will pay off quickly, because entity models have two great features:

**Reusability**

Once you have an entity model you can use it everywhere. As you index new data sets with fields that map to familiar
attributes, you can include them in your entity resolution jobs. If you index data with new attributes that aren't
already in your model, you can simply update your model to support them.

**Flexibility**

You don't need to change your data to use an entity model. An entity model only controls the execution of queries.
So there's no risk in updating or experimenting with an entity model.


## Step 3. Submit a resolution request.

So you have some data and an entity model. Now you can resolve entities!

Once you have an [entity model](/#/docs/entity-models), you can use the ***[Resolution API](/#/docs/rest-apis/resolution-api)*** to run an
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

Run an entity resolution job using an embeded entity model. This example uses three attributes (each with two
matchers), two indices, and two resolvers.

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
          "text": {
            "match": {
              "{{ field }}": {
                "query": "{{ value }}",
                "fuzziness": 2
              }
            }
          },
          "phonetic": {
            "match": {
              "{{ field }}": {
                "query": "{{ value }}",
                "fuzziness": 0
              }
            }
          }
        },
        "dob": {
          "text": {
            "match": {
              "{{ field }}": "{{ value }}"
            }
          },
          "keyword": {
            "term": {
              "{{ field }}": "{{ value }}"
            }
          }
        },
        "phone": {
          "text": {
            "match": {
              "{{ field }}": "{{ value }}"
            }
          },
          "keyword": {
            "term": {
              "{{ field }}": "{{ value }}"
            }
          }
        }
    },
    "indices": {
      "foo_index": {
        "name.text": "full_name",
        "name.phonetic": "full_name.phonetic",
        "dob.keyword": "date_of_birth.keyword",
        "phone.keyword": "telephone.keyword"
      },
      "bar_index": {
        "name.text": "nm",
        "dob.text": "db",
        "phone.text": "ph"
      }
    },
    "resolvers": {
      "name_dob": [ "name", "dob" ],
      "name_phone": [ "name", "phone" ]
    }
  }
}
```