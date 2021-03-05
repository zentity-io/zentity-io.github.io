[Home](/) / [Documentation](/docs) / [REST APIs](/docs/rest-apis) / Bulk Models API


# <a name="bulk-models-api"></a>Bulk Models API

Performs multiple [Models API](/docs/rest-apis/models-api) operations in series.
Supported operations include:
[`"create"`](/docs/rest-apis/models-api#create-entity-model),
[`"update"`](/docs/rest-apis/models-api#update-entity-model),
[`"delete"`](/docs/rest-apis/models-api#delete-entity-model)

```javascript
POST _zentity/models/_bulk
{ OPERATION: PARAMETERS }
ENTITY_MODEL
...
```

The `_bulk` endpoint requires [NDJSON](http://ndjson.org/) syntax. The payload
consists of pairs of lines. Each pair represents a single operation. The first
line of the pair describes the operation and its parameters. The second line
contains the [entity model](/docs/entity-models/specification), or an empty
object (`{}`) for `"delete"` operations. Each line must be an unindented JSON
object.

The supported values for `OPERATION` are:

- [`"create"`](/docs/rest-apis/models-api#create-entity-model)
- [`"update"`](/docs/rest-apis/models-api#update-entity-model)
- [`"delete"`](/docs/rest-apis/models-api#delete-entity-model)


### Example Request

This example performs three [Models API](/docs/rest-apis/models-api) operations
in series. The first request creates an empty entity model for a `"person"`
entity type. The second operation updates the entity model by adding an
attribute called `"first_name"`. The third operation deletes the entity model.

```javascript
POST _zentity/models/_bulk
{"create":{"entity_type":"person"}}
{"attributes":{},"resolvers":{},"matchers":{},"indices":{}}
{"update":{"entity_type":"person"}}
{"attributes":{"first_name":{}},"resolvers":{},"matchers":{},"indices":{}}
{"delete":{"entity_type":"person"}}
{}
```


### Example Response

```javascript
{
  "took": 208,
  "errors": false,
  "items": [
    {
      "create": {
        "_index": ".zentity-models",
        "_type": "doc",
        "_id": "person",
        "_version": 1,
        "result": "created",
        "_shards": {
          "total": 2,
          "successful": 1,
          "failed": 0
        },
        "_seq_no": 1,
        "_primary_term": 3
      }
    },
    {
      "update": {
        "_index": ".zentity-models",
        "_type": "doc",
        "_id": "person",
        "_version": 2,
        "result": "updated",
        "_shards": {
          "total": 2,
          "successful": 1,
          "failed": 0
        },
        "_seq_no": 1,
        "_primary_term": 3
      }
    },
    {
      "delete": {
        "_index": ".zentity-models",
        "_type": "doc",
        "_id": "person",
        "_version": 3,
        "result": "deleted",
        "_shards": {
          "total": 2,
          "successful": 1,
          "failed": 0
        },
        "_seq_no": 1,
        "_primary_term": 3
      }
    }
  ]
}
```


### HTTP Headers

|Header|Value|
|------|-----|
|`Content-Type`|`application/x-ndjson`|


### URL Parameters

|Parameter|Type|Default|Required|Description|
|---------|----|-------|--------|-----------|
|`pretty`|Boolean|`false`|No|Indents the JSON response data.|


### Notes

The `_bulk` endpoint optimizes performance in three ways:

- Ensures the existence of the `.zentity-models` index just once before running
the operations
- Refreshes the `.zentity-models` index once after running the operations.
- Minimizes the network latency that would have occurred from multiple single
requests between the client and Elasticsearch.


&nbsp;

----

#### Continue Reading

|&#8249;|[Models API](/docs/rest-apis/models-api)|[Resolution API](/docs/rest-apis/resolution-api)|&#8250;|
|:---|:---|---:|---:|
|    |    |    |    |
