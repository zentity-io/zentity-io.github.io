[Home](/) / [Documentation](/docs) / [Entity Resolution](/docs/entity-resolution) / Output


# <a name="output">Entity Resolution Output Specification</a>

```javascript
{
  "took": TOOK_IN_MILLIS,
  "hits": {
    "total": HITS_TOTAL,
    "hits": [
      {
        "_index": INDEX_NAME,
        "_type": DOC_TYPE,
        "_id": DOC_ID,
        "_hop": HOP_NUMBER,
        "_attributes": {
          ATTRIBUTE_NAME: ATTRIBUTE_VALUE,
          ...
        },
        "_source": {
          FIELD_NAME: FIELD_VALUE,
          ...
        }
      },
      ...
    ]
  },
  "queries": [
    {
      "_hop": HOP_NUMBER,
      "_index": INDEX_NAME,
      "resolvers": {
        "list": [
          RESOLVER_NAME,
          ...
        ],
        "tree": {
          RESOLVER_NAME: {
            ...
          },
          ...
        }
      },
      "search": {
        "request": SEARCH_REQUEST,
        "response": SEARCH_RESPONSE
      }
    },
    ...
  ]
}
```

Entity resolution outputs are [JSON](https://www.json.org/) documents. In the framework shown above, lowercase quoted values
(e.g. `"attributes"`) are constant fields, uppercase literal values (e.g. `ATTRIBUTE_NAME`) are variable fields or values,
and elipses (`...`) are optional repetitions of the preceding field or value.

An entity resolution output is the response to a **[resolution request](/docs/rest-apis/resolution-api)**. Its structure is
similar to the response of an Elasticsearch [Search API](https://www.elastic.co/guide/en/elasticsearch/reference/current/search.html) query.
It contains the documents ([`"hits"`](#hits.hits)) associated with the entity as well as information about the job itself.
Documents can contain the original source values, the normalized attribute values, and information about the index and hop number
from which the document was retrieved.

The **[`"queries"`](#queries)**, **[`"_source"`](#hits.hits.DOCUMENT._source)**, and **[`"_hits"`](#hits)** fields each can be excluded
from the output. By default, **[`"queries"`](#queries)** is excluded to reduce the amount of data transferred from the cluster to the client.


&nbsp;

----

#### Continue Reading

|&#8249;|[Input](/docs/entity-resolution/input)|[REST APIs](/docs/rest-apis)|&#8250;|
|:---|:---|---:|---:|
|    |    |    |    |