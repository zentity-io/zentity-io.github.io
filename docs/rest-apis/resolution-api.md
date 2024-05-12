[Home](/) / [Documentation](/docs) / [REST APIs](/docs/rest-apis) / Resolution API


# <a name="resolution-api"></a>Resolution API

Runs an entity resolution job and returns the results.

The request accepts two endpoints:

```javascript
POST _zentity/resolution
POST _zentity/resolution/{entity_type}
```


### Example Request

This example request resolves a `person` identified by a `name`, a `dob`, and
two `phone` values, while limiting the search to one index called `users_index`
and two resolvers called `name_dob` and `name_phone`. The request passes a param
called `fuzziness` to the `phone` attribute, which can be referenced in any
matcher clause that uses the `fuzziness` param. Note that an attribute can
accept either an array of values or an object with the values specified in a
field called `"values"`. It's also valid to specify an attribute with no values
but to override the default params, such as to format the results of any date
attributes in the response.

Read the **[input specification](/docs/entity-resolution/input-specification)** for complete details about the structure of a request.


```javascript
POST _zentity/resolution/person?pretty
{
  "attributes": {
    "name": [ "Alice Jones" ],
    "dob": {
      "values": [ "1984-01-01" ]
    },
    "phone": {
      "values": [
        "555-123-4567",
        "555-987-6543"
      ],
      "params": {
        "fuzziness": 2
      }
    }
  },
  "scope": {
    "exclude": {
      "attributes": {
        "name": [
          "unknown",
          "n/a"
        ],
        "phone": "555-555-5555"
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


### Example Response

This example response took 64 milliseconds and returned 2 hits. The `_source`
field contains the fields and values as they exist in the document indexed in
Elasticsearch. The `_attributes` field contains any values from the `_source`
field that can be mapped to the [`"attributes"`](/docs/entity-models/specification#attributes)
field of the entity model. The `_hop` field shows the level of recursion at
which the document was fetched. Entities with many documents can span many hops
if they have highly varied attribute values.

Read the **[output specification](/docs/entity-resolution/output-specification)**
for complete details about the structure of a response.

```javascript
{
  "took": 64,
  "hits": {
    "total": 2,
    "hits": [
      {
        "_index": "users_index",
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


### HTTP Headers

|Header|Value|
|------|-----|
|`Content-Type`|`application/json`|


### URL Parameters

|Parameter|Type|Default|Required|Description|
|---------|----|-------|--------|-----------|
|`_attributes`|Boolean|`true`|No|Return the [`"_attributes"`](/docs/entity-resolution/output-specification/#hits.hits._attributes) field in each doc.|
|`_explanation`|Boolean|`false`|No|Return the [`"_explanation"`](/docs/entity-resolution/output-specification/#hits.hits._explanation) field in each doc.|
|`_seq_no_primary_term`|Boolean|`false`|No|Return the [`"_seq_no"`](https://www.elastic.co/guide/en/elasticsearch/reference/current/optimistic-concurrency-control.html) and [`"_primary_term"`](https://www.elastic.co/guide/en/elasticsearch/reference/current/optimistic-concurrency-control.html) fields in each doc.|
|`_source`|Boolean|`true`|No|Return the [`"_source"`](https://www.elastic.co/guide/en/elasticsearch/reference/current/mapping-source-field.html) field in each doc.|
|`_version`|Boolean|`false`|No|Return the [`"_version"`](https://www.elastic.co/blog/elasticsearch-versioning-support) field in each doc.|
|`entity_type`|String| |Depends|The entity type. Required if `model` is not specified.|
|`error_trace`|Boolean|`true`|No|Return the Java stack trace when an exception is thrown.|
|`hits`|Boolean|`true`|No|Return the [`"hits"`](/docs/entity-resolution/output-specification/#hits) field in the response.|
|`max_docs_per_query`|Integer|`1000`|No|Maximum number of docs per query result. See [`size`](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-request-body.html#request-body-search-from-size)|
|`max_hops`|Integer|`100`|No|Maximum level of recursion.|
|`max_time_per_query`|String|`10s`|No|Timeout per query. Uses [time units](https://www.elastic.co/guide/en/elasticsearch/reference/current/common-options.html#time-units). Timeouts are best effort and not guaranteed ([more info](https://github.com/elastic/elasticsearch/issues/3627)).|
|`pretty`|Boolean|`false`|No|Indents the JSON response data.|
|`profile`|Boolean|`false`|No|[Profile](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-profile.html) each query. Used for debugging.|
|`queries`|Boolean|`false`|No|Return the [`"queries"`](/docs/entity-resolution/output-specification/#queries) field in the response. Used for debugging.|


### URL Parameters (advanced)

These are advanced search optimizations. Most users will not require them. It's recommended to use the default settings of the cluster unless you know what you're doing.

|Parameter|Type|Default|Required|Description|
|---------|----|-------|--------|-----------|
|`search.allow_partial_search_results`|Boolean|Cluster default|No|[`allow_partial_search_results`](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-search.html#search-search-api-query-params)|
|`search.batched_reduce_size`|Integer|Cluster default|No|[`batched_reduce_size`](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-search.html#search-search-api-query-params)|
|`search.max_concurrent_shard_requests`|Integer|Cluster default|No|[`max_concurrent_shard_requests`](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-search.html#search-search-api-query-params)|
|`search.preference`|String|Cluster default|No|[`preference`](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-request-body.html#request-body-search-preference)|
|`search.pre_filter_shard_size`|Integer|Cluster default|No|[`pre_filter_shard_size`](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-search.html#search-search-api-query-params)|
|`search.request_cache`|Boolean|Cluster default|No|[`request_cache`](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-search.html#search-search-api-query-params)|


### Request Body Parameters

|Parameter|Type|Default|Required|Description|
|---------|----|-------|--------|-----------|
|`attributes`|Object| |Deopends|The initial attribute values to search. Required if `terms` and `ids` are not specified.|
|`terms`|Object| |Depends|The initial terms to search. Required if `attributes` and `ids` are not specified.|
|`ids`|Object| |Depends|The initial document _ids to search. Required if `attributes` and `terms` are not specified.|
|`scope.exclude`|Object| |No|The names of indices to limit the job to.|
|`scope.exclude.attributes`|Object| |No|The names and values of attributes to exclude in each query.|
|`scope.exclude.indices`|Object| |No|The names of indices to exclude in each query.|
|`scope.exclude.resolvers`|Object| |No|The names of resolvers to exclude in each query.|
|`scope.include.attributes`|Object| |No|The names and values of attributes to require in each query.|
|`scope.include.indices`|Object| |No|The names of indices to require in each query.|
|`scope.include.resolvers`|Object| |No|The names of resolvers to require in each query.|
|`model`|Object| |Depends|The entity model. Required if `entity_type` is not specified.|


### Notes

- If you define an `entity_type`, zentity will use its model from the `.zentity-models` index.
- If you don't define an `entity_type`, then you must include a `model` object in the request body.
- You can define an `entity_type` in the request body or the URL, but not both.


### Tips

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

|&#8249;|[Bulk Models API](/docs/rest-apis/bulk-models-api)|[Bulk Resolution API](/docs/rest-apis/bulk-resolution-api)|&#8250;|
|:---|:---|---:|---:|
|    |    |    |    |
