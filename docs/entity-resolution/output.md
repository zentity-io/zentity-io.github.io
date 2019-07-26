[Home](/) / [Documentation](/docs) / [Entity Resolution](/docs/entity-resolution) / Output Specification


# <a name="output"></a>Entity Resolution Output Specification

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
        "_query": QUERY_NUMBER,
        "_attributes": {
          ATTRIBUTE_NAME: ATTRIBUTE_VALUE,
          ...
        },
        "_explanation": {
          "resolvers": {
            RESOLVER_NAME: {
              "attributes": [
                ATTRIBUTE_NAME,
                ...
              ]
            },
            ...
          },
          "matches": [
            {
              "attribute": ATTRIBUTE_NAME,
              "target_field": FIELD_NAME,
              "target_value": FIELD_VALUE
              "input_value": ATTRIBUTE_VALUE,
              "input_matcher": MATCHER_NAME,
              "input_matcher_params": MATCHER_PARAMS,
            },
            ...
          ]
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
      "_query": QUERY_NUMBER,
      "_index": INDEX_NAME,
      "filters": {
        "attributes": {
          "tree": {
            WEIGHT_LEVEL: {
              ATTRIBUTE_NAME: {
                ...
              },
              ...
            },
            ...
          },
          "resolvers": {
            RESOLVER_NAME: {
              "attributes": [
                ATTRIBUTE_NAME,
                ...
              ]
            },
            ...
          }
        },
        "terms": {
          "tree": {
            WEIGHT_LEVEL: {
              ATTRIBUTE_NAME: {
                ...
              },
              ...
            },
            ...
          },
          "resolvers": {
            RESOLVER_NAME: {
              "attributes": [
                ATTRIBUTE_NAME,
                ...
              ]
            },
            ...
          }
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

An entity resolution output is the response to a [resolution request](/docs/rest-apis/resolution-api). Its structure is
similar to the response of an Elasticsearch [Search API](https://www.elastic.co/guide/en/elasticsearch/reference/current/search.html) query.
It contains the documents ([`"hits"`](#hits.hits)) associated with the entity as well as information about the job itself.
Documents can contain the original source values, the normalized attribute values, and information about the index and hop number
from which the document was retrieved.

The [`"queries"`](#queries), [`"_source"`](#hits.hits._source), [`"_attributes"`](#hits.hits._attributes), and [`"_hits"`](#hits) fields each can be excluded
from the output. By default, [`"queries"`](#queries) is excluded to reduce the amount of data transferred from the cluster to the client.


### <a name="took"></a>`"took"`

The number of milliseconds elapsed between the start time and stop time of the entity resolution job. This **excludes** the time it takes to
validate the request, request and parse the entity model, and serialize the response.


## <a name="hits"></a>`"hits"`

An object containing the documents that matched the input across all hops.

This field can be excluded from the output by setting `hits=false` in the URI parameters of the [resolution request](/docs/rest-apis/resolution-api).
This can help to get a slightly more accurate measurement of [`"took"`](#took) by excluding some processing of the responses from Elasticsearch.
This can also help to get slightly more accurate timing measurements when stress testing zentity by minimizing the amount of data transferred from
the cluster to the client.


### <a name="hits.total"></a>`"hits"."total"`

The total number of documents that matched the input across all hops.


### <a name="hits.hits"></a>`"hits"."hits"`

An array of objects, each of which is a document that matched the input.


### <a name="hits.hits._index"></a>`"hits"."hits"."_index"`

The name of the index from which the document was retrieved.


### <a name="hits.hits._type"></a>`"hits"."hits"."_type"`

The doc type of the document.


### <a name="hits.hits._id"></a>`"hits"."hits"."_id"`

The _id of the document.


### <a name="hits.hits._hop"></a>`"hits"."hits"."_hop"`

The hop number at which the document was received. A "hop" is an iteration in which zentity submits a query to each index that can be queried.


### <a name="hits.hits._query"></a>`"hits"."hits"."_query"`

The query number of a given [`"_hop"`](#hits.hits._hop) at which the document was received.


### <a name="hits.hits._attributes"></a>`"hits"."hits"."_attributes"`

An object containing the normalized values for each attribute of the document. This object is constructed by taking each [`"_source"`](#hits.hits._source)
field that is associated with an attribute in the entity model and mapping it to the name of the attribute. Some values, such as [dates](/docs/entity-models/specification#attribute-type-date),
are normalized into a format that will be common across documents from disparate indices.

This field can be excluded from the output by setting `_attributes=false` in the URI parameters of the [resolution request](/docs/rest-apis/resolution-api).


### <a name="hits.hits._explanation"></a>`"hits"."hits"."_explanation"`

An object that explains which [`"resolvers"`](#hits.hits._explanation.resolvers) caused the document to match and the reasons for the [`"matches"`](#hits.hits._explanation.matches).

This field can be included in the output by setting `_explanation=true` in the URI parameters of the [resolution request](/docs/rest-apis/resolution-api).


### <a name="hits.hits._explanation.resolvers"></a>`"hits"."hits"."_explanation"."resolvers"`

An object that explains which resolvers caused the document to match. A resolver is listed if each of its [`"attributes"`](#hits.hits._explanation.resolvers.RESOLVER_NAME.attributes) has at least one match. The reason for each match is listed in the [`"matches"`](#hits.hits._explanation.matches) array.


### <a name="hits.hits._explanation.resolvers.RESOLVER_NAME.attributes"></a>`"hits"."hits"."_explanation"."resolvers".RESOLVER_NAME."attributes"`

The attributes of a resolver that caused the document to match.


### <a name="hits.hits._explanation.matches"></a>`"hits"."hits"."_explanation"."matches"`

An array of objects that explains how the inputs of the search matched the fields of the document. Each object represents a match between an [input value](#hits.hits._explanation.matches.input_value) and an [indexed value](#hits.hits._explanation.matches.target_value) for a given [attribute](#hits.hits._explanation.matches.attribute) using a given [matcher](#hits.hits._explanation.matches.input_matcher) and its [params](#hits.hits._explanation.matches.input_matcher_params).


### <a name="hits.hits._explanation.matches.attribute"></a>`"hits"."hits"."_explanation"."matches"."attribute"`

The name of the attribute for a match.


### <a name="hits.hits._explanation.matches.target_field"></a>`"hits"."hits"."_explanation"."matches"."target_field"`

The name of the index field for a match.


### <a name="hits.hits._explanation.matches.target_value"></a>`"hits"."hits"."_explanation"."matches"."target_value"`

The value of the index field for a match.


### <a name="hits.hits._explanation.matches.input_value"></a>`"hits"."hits"."_explanation"."matches"."input_value"`

The value of the input for a match.


### <a name="hits.hits._explanation.matches.input_matcher"></a>`"hits"."hits"."_explanation"."matches"."input_matcher"`

The name of the matcher for a match.


### <a name="hits.hits._explanation.matches.input_matcher_params"></a>`"hits"."hits"."_explanation"."matches"."input_matcher_params"`

The params of the matcher for a match.


### <a name="hits.hits._source"></a>`"hits"."hits"."_source"`

The original fields from the document.

This field can be excluded from the output by setting `_source=false` in the URI parameters of the [resolution request](/docs/rest-apis/resolution-api).


## <a name="queries"></a>`"queries"`

An object containing information about the queries that were submitted to to Elasticsearch during the resolution job.

This field is excluded from the output by default. It can be included by setting `queries=true` in the URI parameters of the [resolution request](/docs/rest-apis/resolution-api).


### <a name="queries._hop"></a>`"queries"."_hop"`

The hop number at which the query was submitted.


### <a name="queries._query"></a>`"queries"."_query"`

The query number at which the query was submitted for a given [`"_hop"`](#queries._hop).


### <a name="queries._index"></a>`"queries"."_index"`

The index that was queried.


### <a name="queries.filters"></a>`"queries"."filters"`

An object containing information about the filters created to construct the query.


### <a name="queries.filters.attributes"></a>`"queries"."filters"."attributes"`

An object containing information about the filters created for known attribute
values of the entity.


### <a name="queries.filters.attributes.tree"></a>`"queries"."filters"."attributes"."tree"`

A recursive object containing the attributes of the resolvers as they were constructed in the query.

Different resolvers can share many of the same attributes. Consider the following:

```javascript
[
  [ "name", "street", "city", "state" ],
  [ "name", "street", "zip" ],
  [ "name", "dob", "state" ],
  [ "name", "phone" ],
  [ "name", "email" ],
  [ "id" ],
]
```

Many of these attributes (`"name"`, `"street"`, `"state"`) are shared by multiple resolvers.
It would be highly inefficient to populate the values of each attribute multiple times in a single query.
zentity optimizes queries by determining how the attributes can be nested to minimize redundant clauses.

Here's the effect of the optimization:

```javascript
{
  "0": {
    "name": {
      "street": {
        "city": {
          "state": {
            "zip": {}
          }
        },
        "zip": {}
      },
      "dob": {
        "state": {}
      },
      "phone": {},
      "email": {}
    },
    "id": {}
  }
}
```

In this example, zentity eliminates four redundant copies of `"name"` values and one redundant copy of `"street"` values.
The clauses of attributes at the same level of the hierarchy are combined with their siblings using `OR`, while the clauses
of child attributes are combined with their parents using `AND`.


### <a name="queries.filters.attributes.resolvers"></a>`"queries"."filters"."attributes"."resolvers"`

An object containing the resolvers that were used to construct the filter for the known attributes of the entity.


### <a name="queries.filters.terms"></a>`"queries"."filters"."terms"`

An object containing information about the filters created for arbitrary terms given in the resolution input.


### <a name="queries.filters.terms.tree"></a>`"queries"."filters"."terms"."tree"`

A recursive object containing the attributes of the resolvers as they were constructed in the query.
Follows the same structure as [`"queries"."filters"."attributes"."tree"`](#queries.filters.attributes.tree).


### <a name="queries.filters.terms.resolvers"></a>`"queries"."filters"."terms"."resolvers"`

An object containing the resolvers that were used to construct the filter for arbitrary terms given in the resolution input.


### <a name="queries.search"></a>`"queries"."search"`

An object containing information about the search request and response to and from Elasticsearch.


### <a name="queries.search.request"></a>`"queries"."search"."request"`

An object containing the search request payload to Elasticsearch.


### <a name="queries.search.response"></a>`"queries"."search"."response"`

An object containing the search response payload from Elasticsearch.

If `profile=true` was set in the URI parameters of the [resolution request](/docs/rest-apis/resolution-api), then the
query profile data will be included in this response field.


&nbsp;

----

#### Continue Reading

|&#8249;|[Entity Resolution Input Specification](/docs/entity-resolution/input-specification)|[REST APIs](/docs/rest-apis)|&#8250;|
|:---|:---|---:|---:|
|    |    |    |    |