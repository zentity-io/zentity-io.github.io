[Home](/#/) / [Documentation](/#/docs) / [REST APIs](/#/docs/rest-apis) / Resolution API


# Resolution API

Runs an entity resolution job and returns the results.

The request accepts two endpoints:

```javascript
POST _zentity/resolution
POST _zentity/resolution/{entity_type}
```

**Example request:**

This example request resolves a `person` identified by a `name`, a `dob`, and two `phone` values, while limiting the
search to one index called `users_index` ane two resolvers called `name_dob` and `name_phone`.

```javascript
POST _zentity/resolution/person?pretty
{
  "attributes": {
    "name": "Alice Jones",
    "dob": "1984-01-01",
    "phone": [
      "555-123-4567",
      "555-987-6543"
    ]
  },
  "scope": {
    "exclude": {
      "attributes": {
        "name": [
          "unknown",
          "n/a"
        ]
      }
    },
    "include": {
      "indices": [
        "users_index"
      ],
      "resolvers": [
        "name_dob",
        "name_phone"
      ]
    }
  }
}
```

**Example response:**

This example response took 64 milliseconds and returned 2 hits. The `_source` field contains the fields and values
as they exist in the document indexed in Elasticsearch. The `_attributes` field contains any values from the
`_source` field that can be mapped to the [`"attributes"`](/#/docs/entity-models/specification) field of the entity model.
The `_hop` field shows the level of recursion at which the document was fetched. Entities with many documents can
span many hops if they have highly varied attribute values.

```javascript
{
  "took": 64,
  "hits": {
    "total": 2,
    "hits": [
      {
        "_index": "users_index",
        "_type": "doc",
        "_id": "iaCn-mABDJZDR09hUNon",
        "_hop": 0,
        "_attributes": {
          "city": "Beverly Halls",
          "first_name": "Alice",
          "last_name": "Jones",
          "phone": "555 123 4567",
          "state": "CA",
          "street": "123 Main St",
          "zip": "90210-0000"
        },
        "_source": {
          "@version": "1",
          "city": "Beverly Halls",
          "fname": "Alice",
          "lname": "Jones",
          "phone": "555 987 6543",
          "state": "CA",
          "street": "123 Main St",
          "zip": "90210-0000"
        }
      },
      {
        "_index": "users_index",
        "_type": "doc",
        "_id": "iqCn-mABDJZDR09hUNoo",
        "_hop": 0,
        "_attributes": {
          "city": "Beverly Hills",
          "first_name": "Alice",
          "last_name": "Jones",
          "phone": "(555)-987-6543",
          "state": "CA",
          "street": "123 W Main Street",
          "zip": "90210"
        }
        "_source": {
          "@version": "1",
          "city": "Beverly Hills",
          "fname": "Alice",
          "lname": "Jones",
          "phone": "(555)-987-6543",
          "state": "CA",
          "street": "123 W Main Street",
          "zip": "90210"
        }
      }
    ]
  }
}
```

**URL query string parameters:**

|Param|Type|Default|Required|Description|
|-----|----|-------|--------|-----------|
|`_attributes`|Boolean|`true`|No|Return the `_attributes` field in each doc.|
|`_source`|Boolean|`true`|No|Return the `_source` field in each doc.|
|`hits`|Boolean|`true`|No|Return the `hits` field in the response.|
|`max_docs_per_query`|Integer|`1000`|No|Maximum number of docs per query result.|
|`max_hops`|Integer|`100`|No|Maximum level of recursion.|
|`pretty`|Boolean|`false`|No|Indents the JSON response data.|
|`profile`|Boolean|`false`|No|[Profile](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-profile.html) each query. Used for debugging.|
|`queries`|Boolean|`false`|No|Return the `queries` field in the response. Used for debugging.|

**Request body parameters:**

|Param|Type|Default|Required|Description|
|-----|----|-------|--------|-----------|
|`attributes`|Object| |Yes|The initial attribute values to search.|
|`entity_type`|String| |Depends|The entity type. Required if `model` is not specified.|
|`scope.exclude`|Object| |No|The names of indices to limit the job to.|
|`scope.exclude.attributes`|Object| |No|The names and values of attributes to exclude in each query.|
|`scope.exclude.indices`|Object| |No|The names of indices to exclude in each query.|
|`scope.exclude.resolvers`|Object| |No|The names of resolvers to exclude in each query.|
|`scope.include.attributes`|Object| |No|The names and values of attributes to require in each query.|
|`scope.include.indices`|Object| |No|The names of indices to require in each query.|
|`scope.include.resolvers`|Object| |No|The names of resolvers to require in each query.|
|`model`|Object| |Depends|The entity model. Required if `entity_type` is not specified.|

**Notes:**

- If you define an `entity_type`, zentity will use its model from the `.zentity-models` index.
- If you don't define an `entity_type`, then you must include a `model` object in the request body.
- You can define an `entity_type` in the request body or the URL, but not both.

**Tips:**

- If you only need to search a few indices, use `scope.exclude.indices` and
`scope.include.indices` parameter to prevent the job from searching unnecessary
indices in the entity model at each hop.
- Beware if your data is ***transactional*** or has ***many duplicates***.
You might need to lower the values of `max_hops` and `max_docs_per_query` if
your jobs are timing out.
- Use `scope.exclude.attributes` to prevent entities from being over-resolved
(a.k.a. "snowballed") due to common meaningless values such as "unknown" or "n/a".
- Use `scope.include.attributes` to limit the job within a particular context,
such as by matching documents only within a given state or country.


&nbsp;

----

#### Continue Reading

|&#8249;|[REST APIs](/#/docs/rest-apis)|[Models API](/#/docs/rest-apis/models-api)|&#8250;|
|:---|:---|---:|---:|
|    |    |    |    |