[Home](/#/) / [Documentation](/#/docs) / [Entity Models](/#/docs/entity-models) / Specification


# Entity Model Specification

```javascript
{
  "attributes": {
    ATTRIBUTE_NAME: {
      "type": ATTRIBUTE_TYPE,
      "params": {
        PARAM_NAME: PARAM_VALUE,
        ...
      }
    },
    ...
  },
  "resolvers": {
    RESOLVER_NAME: {
      "attributes": [
        ATTRIBUTE_NAME,
        ...
      ]
    }
    ...
  },
  "matchers": {
    MATCHER_NAME: {
      "clause": MATCHER_CLAUSE,
      "params": {
        PARAM_NAME: PARAM_VALUE,
        ...
      }
    },
    ...
  },
  "indices": {
    INDEX_NAME: {
      "fields": {
        INDEX_FIELD_NAME: {
          "attribute": ATTRIBUTE_NAME,
          "matcher": MATCHER_NAME
        },
        ...
      }
    },
    ...
  }
}
```

Entity models are [JSON](https://www.json.org/) documents. In the framework shown above, lowercase quoted values
(e.g. `"attributes"`) are constant fields, uppercase literal values (e.g. `ATTRIBUTE_NAME`) are variable fields or values,
and elipses (`...`) are optional repetitions of the preceding field or value.

An entity model has four required objects: **`"attributes"`**, **`"resolvers"`**, **`"matchers"`**, **`"indices"`**.


## `"attributes"`

**Model**

```javascript
{
  "attributes": {
    ATTRIBUTE_NAME: {
      "type": ATTRIBUTE_TYPE,
      "params": {
        PARAM_NAME: PARAM_VALUE,
        ...
      }
    },
    ...
  }
}
```

**Example**

```javascript
{
  "attributes": {
    "name": {
      "type": "string"
    },
    "street": {
      "type": "string"
    },
    "city": {
      "type": "string"
    },
    "state": {
      "type": "string",
      "params": {
        "fuzziness": 0
      }
    },
    "zip": {
      "type": "string"
    },
    "email": {
      "type": "string"
    },
    "phone": {
      "type": "string",
      "params": {
        "fuzziness": "auto"
      }
    }
  }
}
```

Attributes are elements that can assist the identification and resolution of entities. For example, some common
attributes of a person include name, date of birth, and phone number. Each attribute has its own particular data
qualities and purposes in the real world. Therefore, zentity matches the values of each attribute using logic that
is distinct to each attribute.

Some attributes can be matched using different methods. For example, a name could be matched by its exact value or its
phonetic value. Therefore the entity model allows each attribute to have one or more matchers. A matcher is simply a
clause of a [`"bool"` query](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-bool-query.html)
in Elasticsearch. This means that if *any* matcher of an attribute yields a match for a given value, then the attribute
will be considered a match regardless of the results of the other matchers.


### `"attributes".ATTRIBUTE_NAME`

A field with the name of a distinct attribute. Some examples might be `"name"`, `"dob"`, `"phone"`, etc. The value of the
field is an object that contains metadata about the attribute.

- Required: Yes
- Type: String


### `"attributes".ATTRIBUTE_NAME."type"`

The data type of the attribute. The default value is `"string"` if unspecified in the model. Data types of attribute
values are validated on input when submitting a request to the [Resolution API]("/#/docs/rest-apis/resolution-api") endpoint.
Attribute data types only affect the inputs to a resolution job and the queries submitted to Elasticsearch. The data types
of the values returned in the `"_attributes"` field of the documents in the resolution job response are kept as they were
in the `"_source"` fields of those documents.


- Required: No
- Type: String
- Default: `"string"`


### `"attributes".ATTRIBUTE_NAME."params"`

An optional object that passes arbitrary variables ("params") to the matcher clauses.

- Required: No
- Type: Object


### `"attributes".ATTRIBUTE_NAME."params".PARAM_NAME`

A field with the name of a distinct param for the attribute. Some examples might be `"fuzziness"` or `"format"`.

- Required: No
- Type: String


### `"attributes".ATTRIBUTE_NAME."params".PARAM_NAME.PARAM_VALUE`

A value for the param. This can be any JSON compliant value such as a string, number, boolean, array, or object. The value
will be serialized as a string when passed to the matcher clause. The value overrides the same field specified in
`"attributes".ATTRIBUTE_NAME."params"` in the model and `"matchers".MATCHER_NAME."params"`.

- Required: No
- Type: Any


#### Valid attribute types

Listed below are each of the currently valid attribute types.


##### `"string"`

Indicates that the values of an attribute must be supplied as JSON compliant string values. Elasticsearch can perform text
analysis, fuzzy matching, and other operations solely on string values.


##### `"number"`

Indicates that the values of an attribute must be supplied as JSON compliant number value. This includes any positive or
negative integer or fractional value. zentity handles the appropriate conversion of number values to floats, doubles,
integers, or longs.


##### `"boolean"`

Indicates that the values of an attribute must be supplied as JSON compliant boolean values (`true` or `false`).


##### `"date"`

Indicates that the values of an attribute must be supplied as JSON compliant string values. Additionally, date attributes
must include a param called `"format"` that contains an [Elasticsearch date format](https://www.elastic.co/guide/en/elasticsearch/reference/current/mapping-date-format.html).
Date values are queried and returned in the specified format. This is both useful and necessary when querying date fields
across indices that have disparate date formats.


## `"resolvers"`

**Model**

```javascript
{
  "resolvers": {
    RESOLVER_NAME: {
      "attributes": [
        ATTRIBUTE_NAME,
        ...
      ]
    }
    ...
  }
}
```

**Example**

```javascript
{
  "resolvers": {
    "name_street_city_state": {
      "attributes": [
        "name", "street", "city", "state"
      ]
    },
    "name_street_zip": {
      "attributes": [
        "name", "street", "zip"
      ]
    },
    "name_phone": {
      "attributes": [
        "name", "phone"
      ]
    },
    "name_email": {
      "attributes": [
        "name", "email"
      ]
    },
    "name_phone": {
      "attributes": [
        "name", "phone"
      ]
    },
    "email_phone": {
      "attributes": [
        "email", "phone"
      ]
    }
  }
}
```

Resolvers are combinations of attributes that imply a resolution. For example, you might decide to resolve entities
that share matching values for `"name"` and `"dob"` or `"name"` and `"phone"`. You can create a "resolver" for both
combinations of attributes. Then any documents whose values share either a matching `"name"` and `"dob"` or  `"name"`
and `"phone"` will resolve to the same entity.

Remember that attributes can be associated with more than one matcher in the `"indices"` object. This means that if
*any* matcher of an attribute yields a match for a given value, then the attribute will be considered a match
regardless of the results of the other matchers. So if you have an attribute called `name` with matchers called
`keyword` and `phonetic`, then any resolver that uses the `name` attribute is effectively saying that *either*
`name.keyword` *or* `name.phonetic` are required to match.


### `"resolvers".RESOLVER_NAME`

A field with the name of a distinct resolver. The value of the field is an object that contains metadata about the
resolver.

A resolver represents a combination of attributes that implies a resolution. For example, if a resolver lists the
attributes `"name"` and `"phone"`, then any documents whose values match those attributes -- either in the inputs
of the resolution job or any subsequent hops -- will be considered a match to the entity.

- Required: Yes
- Type: String


### `"resolvers".RESOLVER_NAME."attributes"`

A set of attribute names. The order of the values has no effect on resolution. Duplicate values are redundant and
have no effect on resolution.

- Required: Yes
- Type: Array


### `"resolvers".RESOLVER_NAME."attributes".ATTRIBUTE_NAME`

The name of an attribute from the `"attributes"` object of the entity model. If the attribute does not exist,
then the resolver will not be used in any resolution jobs.

- Required: Yes
- Type: String


## `"matchers"`

**Model**

```javascript
{
  "matchers": {
    MATCHER_NAME: {
      "clause": MATCHER_CLAUSE,
      "params": {
        PARAM_NAME: PARAM_VALUE,
        ...
      }
    },
    ...
  }
}
```

**Example**

```javascript
{
  "matchers": {
    "exact_matcher": {
      "clause": {
        "term": {
          "{{ field }}": "{{ value }}"
        }
      },
    },
    "fuzzy_matcher": {
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
    },
    "standard_matcher": {
      "clause": {
        "match": {
          "{{ field }}": "{{ value }}"
        }
      }
    },
    "timestamp_matcher": {
      "clause": {
        "range": {
          "{{ field }}": {
            "gte": "{{ value }}||-{{ params.window }}",
            "lte": "{{ value }}||+{{ params.window }}",
            "format": "{{ params.format }}"
          }
        }
      },
      "params": {
        "format": "yyyy-MM-dd'T'HH:mm:ss.SSS",
        "window": "15m"
      }
    }
  }
}
```


### `"matchers".MATCHER_NAME`

A field with the name of a distinct matcher. The value of the field is an object that contains metadata about the
matcher.

A matcher is a templated clause of a [`"bool"` query](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-bool-query.html)
that can be populated with the names of index fields and the values of attributes.

- Required: Yes
- Type: String


### `"matchers".MATCHER_NAME."clause"`

An object that represents the clause of a [`"bool"` query](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-bool-query.html)
in Elasticsearch. Each clause will be stitched together to form a single `"bool"` query, so it must follow the correct
syntax for a `"bool"` query clause, except you don't need to include the top-level field `"bool"` or its subfields such
as `"must"` or `"should"`.

Matcher clauses use Mustache syntax to pass two important variables: **`{{ field }}`** and **`{{ value }}`**.
The `field` variable will be populated with the index field that maps to the attribute. The `value` field will be
populated with the value that will be queried for that attribute. This syntax is the same as the one used by
Elasticsearch [search templates](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-template.html).

- Required: Yes
- Type: Object


### `"matchers".MATCHER_NAME."params"`

An optional object that specifies the default values for any variables ("params") in the matcher clause.

- Required: No
- Type: Object


### `"matchers".MATCHER_NAME."params".PARAM_NAME`

A field with the name of a distinct param for the matcher clause. Some examples might be `"fuzziness"` or `"format"`.

- Required: No
- Type: String


### `"matchers".MATCHER_NAME."params".PARAM_NAME.PARAM_VALUE`

A value for the param. This can be any JSON compliant value such as a string, number, boolean, array, or object. The value
will be serialized as a string when passed to the matcher clause. The value is overridden by the same field specified in
`"attributes".ATTRIBUTE_NAME."params"` in either the input or the model.

- Required: No
- Type: Any


## `"indices"`

**Model**

```javascript
{
  "indices": {
    INDEX_NAME: {
      "fields": {
        INDEX_FIELD_NAME: {
          "attribute": ATTRIBUTE_NAME,
          "matcher": MATCHER_NAME
        },
        ...
      }
    },
    ...
  }
}
```

**Example**

```javascript
{
  "indices": {
    "users": {
      "fields": {
        "name": {
          "attribute": "name",
          "matcher": "fuzzy_matcher"
        },
        "zip.keyword": {
          "attribute": "zip",
          "matcher": "exact_matcher"
        },
        "email.keyword": {
          "attribute": "email",
          "matcher": "exact_matcher"
        }
      }
    },
    "registrants": {
      "fields": {
        "full_name": {
          "attribute": "name",
          "matcher": "fuzzy_matcher"
        },
        "addr_street": {
          "attribute": "street",
          "matcher": "fuzzy_matcher"
        },
        "addr_city": {
          "attribute": "city",
          "matcher": "standard_matcher"
        },
        "addr_state_code.keyword": {
          "attribute": "state",
          "matcher": "exact_matcher"
        },
        "addr_state_postal_code.keyword": {
          "attribute": "zip",
          "matcher": "exact_matcher"
        },
        "email_address": {
          "attribute": "email",
          "matcher": "exact_matcher"
        },
        "phone_number.keyword": {
          "attribute": "phone",
          "matcher": "exact_matcher"
        }
      }
    }
  }
}
```

Different indices in Elasticsearch might have data that can be matched as attributes, but each index might use slightly
different field names or data types for the same data. Therefore, zentity uses a map to translate the different field
names to the attributes of our entity model.

The entity model maps attributes and matchers to index fields. Remember how each attribute can be matched in different ways,
such as a name that can be matched by its exact value or its phonetic value? Elasticsearch would index those different
values as distinct fields, such as `"name.keyword"` and `"name.phonetic"`. This is why the entity model maps attributes
and matchers -- not just attributes -- to index fields.


### `"indices".INDEX_NAME`

A field with the name of a distinct Elasticsearch [index](https://www.elastic.co/guide/en/elasticsearch/reference/current/_basic_concepts.html#_index)
or [index pattern](https://www.elastic.co/guide/en/elasticsearch/reference/current/multi-index.html). The value of the
field is an object that contains metadata about the index.

zentity does not verify the existence of indices or the validity of index patterns or the syntax of field names that
Elasticsearch requires. Elasticsearch may respond with an error for resolution jobs that submit queries to indices
that do not exist.

- Required: Yes
- Type: String


### `"indices".INDEX_NAME."fields"`

An object that maps an index field name to an attribute and a matcher.


### `"indices".INDEX_NAME."fields".INDEX_FIELD_NAME`

A field with the name of a distinct [property](https://www.elastic.co/guide/en/elasticsearch/reference/current/properties.html)
or [field](https://www.elastic.co/guide/en/elasticsearch/reference/current/multi-fields.html) in an Elasticsearch index.
The value of the field is an object that contians metadata about the index field, particularly the attribute and matcher
that is mapped to it.

zentity does not verify the existence of field names within indices or the syntax of field names that Elasticsearch
requires.


### `"indices".INDEX_NAME."fields".INDEX_FIELD_NAME."attribute"`

The name of an attribute from the `"attributes"` object of the entity model. If the attribute does not exist,
then the index field will not be queried in any resolution jobs and will not be returned in the `"_attributes"`
field of the documents matched in a resolution job.

- Required: Yes
- Type: String


### `"indices".INDEX_NAME."fields".INDEX_FIELD_NAME."matcher"`

The name of a matcher from the `"matchers"` object of the entity model. If the matcher does not exist,
then the index field will not be queried in any resolution jobs. However, the index field can still be returned
in the `"attributes"` field of the documents matched in a resolution job if those documents matched the attributes
of other resolvers.

Let's illustrate how index fields relate to matchers and attributes during a resolution job. Assume you are resolving
an entity with an email address of `"user@example.net"` and one of the indices has an field name of `"email.keyword"`.
And assume that the index field is mapped to the matcher clause below:

```javascript
{
  "term": {
    "{{ field }}": "{{ value }}"
  }
}
```

The final clause will look like this:

```javascript
{
  "term": {
    "email.keyword": "user@example.net"
  }
}
```

The `"matcher"` field is optional. The index field won't be queried if the `"matcher"` field is unspecified.
There are valid reasons to map an index field only an attribute and not a matcher. It allows the value of index field
to be returned as the `"attribute"` if the document is matched by other resolvers. For example, an attribute for
`"salary"` might not be useful in identifying and resolving entities, but it could be useful to return salary data
from disparate indices under a field with a common name. These are sometimes called "payload" attributes.

- Required: No
- Type: String


&nbsp;

----

#### Continue Reading

|&#8249;|[Entity Models](/#/docs/entity-models)|[Tips](/#/docs/entity-models/tips)|&#8250;|
|:---|:---|---:|---:|
|    |    |    |    |
