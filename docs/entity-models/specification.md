[Home](/) / [Documentation](/docs) / [Entity Models](/docs/entity-models) / Specification


# <a name="specification"></a>Entity Model Specification

```javascript
{
  "attributes": {
    ATTRIBUTE_NAME: {
      "type": ATTRIBUTE_TYPE,
      "params": {
        PARAM_NAME: PARAM_VALUE,
        ...
      },
      "score": ATTRIBUTE_IDENTITY_CONFIDENCE_BASE_SCORE
    },
    ...
  },
  "resolvers": {
    RESOLVER_NAME: {
      "attributes": [
        ATTRIBUTE_NAME,
        ...
      ],
      "weight": WEIGHT_LEVEL
    }
    ...
  },
  "matchers": {
    MATCHER_NAME: {
      "clause": MATCHER_CLAUSE,
      "params": {
        PARAM_NAME: PARAM_VALUE,
        ...
      },
      "quality": MATCHER_QUALITY_SCORE
    },
    ...
  },
  "indices": {
    INDEX_NAME: {
      "fields": {
        INDEX_FIELD_NAME: {
          "attribute": ATTRIBUTE_NAME,
          "matcher": MATCHER_NAME,
          "quality": INDEX_FIELD_QUALITY_SCORE
        },
        ...
      }
    },
    ...
  }
}
```

Entity models are [JSON](https://www.json.org/) documents. In the framework
shown above, lowercase quoted values (e.g. `"attributes"`) are constant fields,
uppercase literal values (e.g. `ATTRIBUTE_NAME`) are variable fields or values,
and elipses (`...`) are optional repetitions of the preceding field or value.

An entity model has four required objects: **[`"attributes"`](#attributes)**,
**[`"resolvers"`](#resolvers)**, **[`"matchers"`](#matchers)**, **[`"indices"`](#indices)**.
Not all elements within these objects are required. Optional elements are noted
in the descriptions of each element listed on this page.


## <a name="attributes"></a>`"attributes"`

**Model**

```javascript
{
  "attributes": {
    ATTRIBUTE_NAME: {
      "type": ATTRIBUTE_TYPE,
      "params": {
        PARAM_NAME: PARAM_VALUE,
        ...
      },
      "score": ATTRIBUTE_IDENTITY_CONFIDENCE_BASE_SCORE
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
      "type": "string",
      "score": 0.65
    },
    "street": {
      "type": "string",
      "score": 0.75
    },
    "city": {
      "type": "string",
      "score": 0.55
    },
    "state": {
      "type": "string",
      "params": {
        "fuzziness": 0
      },
      "score": 0.52
    },
    "zip": {
      "type": "string",
      "score": 0.6
    },
    "email": {
      "type": "string",
      "score": 0.95
    },
    "phone": {
      "type": "string",
      "params": {
        "fuzziness": "auto"
      },
      "score": 0.9
    }
  }
}
```

Attributes are elements that can assist the identification and resolution of
entities. For example, some common attributes of a person include name, date of
birth, and phone number. Each attribute has its own particular data qualities
and purposes in the real world. Therefore, zentity matches the values of each
attribute using logic that is distinct to each attribute.

Some attributes can be matched using different methods. For example, a name
could be matched by its exact value or its phonetic value. Therefore the entity
model allows each attribute to have one or more matchers. A matcher is simply a
clause of a [`"bool"` query](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-bool-query.html)
in Elasticsearch. This means that if *any* matcher of an attribute yields a
match for a given value, then the attribute will be considered a match
regardless of the results of the other matchers.


### <a name="attributes.ATTRIBUTE_NAME"></a>`"attributes".ATTRIBUTE_NAME`

A field with the name of a distinct attribute. Some examples might be `"name"`,
`"dob"`, `"phone"`, etc. The value of the field is an object that contains
metadata about the attribute.

- Required: Yes
- Type: String


### <a name="attributes.ATTRIBUTE_NAME.type"></a>`"attributes".ATTRIBUTE_NAME."type"`

The data type of the attribute. The default value is `"string"` if unspecified
in the model. Data types of attribute values are validated on input when
submitting a request to the [Resolution API](/docs/rest-apis/resolution-api)
endpoint. Attribute data types only affect the inputs to a resolution job and
the queries submitted to Elasticsearch. The data types of the values returned in
the `"_attributes"` field of the documents in the resolution job response are
kept as they were in the `"_source"` fields of those documents.


- Required: No
- Type: String
- Default: `"string"`


### <a name="attributes.ATTRIBUTE_NAME.params"></a>`"attributes".ATTRIBUTE_NAME."params"`

An optional object that passes arbitrary variables (`"params"`) to the matcher
clauses.

- Required: No
- Type: Object


### <a name="attributes.ATTRIBUTE_NAME.params.PARAM_NAME"></a>`"attributes".ATTRIBUTE_NAME."params".PARAM_NAME`

A field with the name of a distinct param for the attribute. Some examples might
be `"fuzziness"` or `"format"`.

- Required: No
- Type: String


### <a name="attributes.ATTRIBUTE_NAME.params.PARAM_NAME.PARAM_VALUE"></a>`"attributes".ATTRIBUTE_NAME."params".PARAM_NAME.PARAM_VALUE`

A value for the param. This can be any JSON compliant value such as a string,
number, boolean, array, or object. The value will be serialized as a string when
passed to the matcher clause. The value overrides the same field specified in
[`"attributes".ATTRIBUTE_NAME."params"`](#attributes.ATTRIBUTE_NAME.params) in
the model and [`"matchers".MATCHER_NAME."params"`](#matchers.MATCHER_NAME.params).

- Required: No
- Type: Any


#### <a name="valid-attribute-types"></a>Valid attribute types

Listed below are each of the currently valid attribute types.


##### <a name="attribute-type-string"></a>`"string"`

Indicates that the values of an attribute must be supplied as JSON compliant
string values. Elasticsearch can perform text analysis, fuzzy matching, and
other operations solely on string values.


##### <a name="attribute-type-number"></a>`"number"`

Indicates that the values of an attribute must be supplied as JSON compliant
number value. This includes any positive or negative integer or fractional value.
zentity handles the appropriate conversion of number values to floats, doubles,
integers, or longs.


##### <a name="attribute-type-boolean"></a>`"boolean"`

Indicates that the values of an attribute must be supplied as JSON compliant
boolean values (`true` or `false`).


##### <a name="attribute-type-date"></a>`"date"`

Indicates that the values of an attribute must be supplied as JSON compliant
string values. Additionally, date attributes must include a param called
`"format"` that contains an [Elasticsearch date format](https://www.elastic.co/guide/en/elasticsearch/reference/current/mapping-date-format.html).
Date values are queried and returned in the specified format. This is both
useful and necessary when querying date fields across indices that have
disparate date formats.


### <a name="attributes.ATTRIBUTE_NAME.score"></a>`"attributes".ATTRIBUTE_NAME."score"`

An attribute identity confidence base score represents the confidence that an
attribute would uniquely identify the entity if it were to match, assuming the
quality of its matcher and index field are perfect. The score is a floating
point number in the range of `0.0` - `1.0`.

- A score of `1.0` represents 100% confidence that the attribute identifies the entity.
- A score of `0.0` represents 100% confidence that the attribute does not identify the entity.
- A score of `0.5` represents 100% uncertainty that the attribute identifies the entity.
- A score of `null` indicates that the attribute lacks a base score.

Effectively, if a document matches with one or more attributes:

- The document [`"_score"`](/docs/entity-resolution/output-specification/#hits.hits._explanation.matches.score)
always will be `1.0` if any attribute has a score of `1.0`.
- The document [`"_score"`](/docs/entity-resolution/output-specification/#hits.hits._explanation.matches.score)
always will be `0.0` if any attribute has a score of `0.0`.
- The document [`"_score"`](/docs/entity-resolution/output-specification/#hits.hits._explanation.matches.score)
will be unaffected by any attribute with a score of `0.5`.
- The document [`"_score"`](/docs/entity-resolution/output-specification/#hits.hits._explanation.matches.score)
will be unaffected by any attribute with a score of `null`.

Generally it makes sense for every attribute to have a base score between
`0.5` - `1.0`. A base score that's less than `0.5` would indicate that the
matching attribute represents some level of a false match, which is contrary to
the general usage of zentity where a matching attribute represents some level
of a true match.

[Cardinality](https://stackoverflow.com/a/25548661/11150348) would be a good
statistic by which to define a base score. For example:

- "High" cardinality attributes such as `"ssn"` or `"phone"` or `"ip"` should
have a base score closer to `1.0` because they're more likely to uniquely
identify the entity.
- "Low" cardinality attributes such as `"sex"` should have a base score closer
to `0.5` because they don't contribute significantly to the identification of
the entity.
- "Normal" cardinality attributes such as `"first_name"` or `"street"` or
`"dob"` should have a base score somewhere in between the two extremes of `0.5`
and `1.0`.

Care should be taken when using a base score of `1.0` or `0.0`, because it would
allow a single attribute identity confidence score to determine the document
[`"_score"`](/docs/entity-resolution/output-specification/#hits.hits._explanation.matches.score).
Whenever there is an attribute identity confidence score of `1.0` or `0.0`, it
takes precedence over any other attribute identity confidence score in the
document. For example, you might have an `"id"` field that you absolutely trust
to identify an entity. If you allow the score of the `"id"` field to be `1.0`,
then anytime the `"id"` field matches in a document, no other attribute identity
confidence score would matter because you've already stated that the `"id"`
field always indicates a match with perfect confidence. A best practice would be
to use a high number such as `0.99` to allow for some small level of variability
and more nuanced rankings of documents.

- Required: No
- Type: Float
- Default: `null`


## <a name="resolvers"></a>`"resolvers"`

**Model**

```javascript
{
  "resolvers": {
    RESOLVER_NAME: {
      "attributes": [
        ATTRIBUTE_NAME,
        ...
      ],
      "weight": WEIGHT_LEVEL
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
    },
    "ssn": {
      "attributes": [
        "ssn"
      ],
      "weight": 1
    }
  }
}
```

Resolvers are combinations of attributes that imply a resolution. For example,
you might decide to resolve entities that share matching values for `"name"` and
`"dob"` or `"name"` and `"phone"`. You can create a resolver for both
combinations of attributes. Then any documents whose values share either a
matching `"name"` and `"dob"` or  `"name"` and `"phone"` will resolve to the
same entity.

Remember that attributes can be associated with more than one matcher in the
[`"indices"`](#indices) object. This means that if *any* matcher of an attribute
yields a match for a given value, then the attribute will be considered a match
regardless of the results of the other matchers. So if you have an attribute
called `name` with matchers called `keyword` and `phonetic`, then any resolver
that uses the `name` attribute is effectively saying that *either* `name.keyword`
*or* `name.phonetic` are required to match.


### <a name="resolvers.RESOLVER_NAME"></a>`"resolvers".RESOLVER_NAME`

A field with the name of a distinct resolver. The value of the field is an
object that contains metadata about the
resolver.

A resolver represents a combination of attributes that implies a resolution.
For example, if a resolver lists the attributes `"name"` and `"phone"`, then any
documents whose values match those attributes -- either in the inputs of the
resolution job or any subsequent hops -- will be considered a match to the
entity.

- Required: Yes
- Type: String


### <a name="resolvers.RESOLVER_NAME.attributes"></a>`"resolvers".RESOLVER_NAME."attributes"`

A set of attribute names. The order of the values has no effect on resolution.
Duplicate values are redundant and have no effect on resolution.

- Required: Yes
- Type: Array


### <a name="resolvers.RESOLVER_NAME.attributes.ATTRIBUTE_NAME"></a>`"resolvers".RESOLVER_NAME."attributes".ATTRIBUTE_NAME`

The name of an attribute from the [`"attributes"`](#attributes) object of the
entity model. If the attribute does not exist, then the resolver will not be
used in any resolution jobs.

- Required: Yes
- Type: String


### <a name="resolvers.RESOLVER_NAME.weight.WEIGHT_LEVEL"></a>`"resolvers".RESOLVER_NAME."weight".WEIGHT_LEVEL`

The weight level of the resolver. Resolvers with higher weight levels take
precedence over resolvers with lower weight levels. If a resolution job uses
resolvers with different weight levels, then the higher weight resolvers either
must match or must not exist. This behavior can help prevent false matches.

For example, let's say you have three resolvers: `"name_phone"` has a weight of
`0`, `"ssn"` has a weight of `1`, and `"id"` has a weight of `2`. Because the
`"id"` resolver has the highest weight, it will always match documents with the
same `"id"` attribute. The `"ssn"` resolver has a lower weight than the `"id"`
resolver, and so the `"ssn"` resolver will only match documents if the `"id"`
resolver either matches or does not exist in the documents. And the
`"name_phone"` resolver has the lowest weight, so the `"name_phone"` resolver
will only match documents if both the `"ssn"` and `"id"` resolvers either match
or do not exist in the documents.

- Required: No
- Type: Integer
- Default: `0`


## <a name="matchers"></a>`"matchers"`

**Model**

```javascript
{
  "matchers": {
    MATCHER_NAME: {
      "clause": MATCHER_CLAUSE,
      "params": {
        PARAM_NAME: PARAM_VALUE,
        ...
      },
      "quality": MATCHER_QUALITY_SCORE
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
      }
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
      },
      "quality": 0.95
    },
    "standard_matcher": {
      "clause": {
        "match": {
          "{{ field }}": "{{ value }}"
        }
      },
      "quality": 0.98
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
      },
      "quality": 0.92
    }
  }
}
```


### <a name="matchers.MATCHER_NAME"></a>`"matchers".MATCHER_NAME`

A field with the name of a distinct matcher. The value of the field is an object
that contains metadata about the matcher.

A matcher is a templated clause of a [`"bool"` query](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-bool-query.html)
that can be populated with the names of index fields and the values of
attributes.

- Required: Yes
- Type: String


### <a name="matchers.MATCHER_NAME.clause"></a>`"matchers".MATCHER_NAME."clause"`

An object that represents the clause of a [`"bool"` query](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-bool-query.html)
in Elasticsearch. Each clause will be stitched together to form a single `"bool"`
query, so it must follow the correct syntax for a `"bool"` query clause, except
you don't need to include the top-level field `"bool"` or its subfields such as
`"must"` or `"should"`.

Matcher clauses use Mustache syntax to pass two important variables:
**`{{ field }}`** and **`{{ value }}`**. The `field` variable will be populated
with the index field that maps to the attribute. The `value` field will be
populated with the value that will be queried for that attribute. This syntax is
the same as the one used by Elasticsearch [search templates](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-template.html).

- Required: Yes
- Type: Object


### <a name="matchers.MATCHER_NAME.params"></a>`"matchers".MATCHER_NAME."params"`

An optional object that specifies the default values for any variables
("params") in the matcher clause.

- Required: No
- Type: Object


### <a name="matchers.MATCHER_NAME.params.PARAM_NAME"></a>`"matchers".MATCHER_NAME."params".PARAM_NAME`

A field with the name of a distinct param for the matcher clause. Some examples
might be `"fuzziness"` or `"format"`.

- Required: No
- Type: String


### <a name="matchers.MATCHER_NAME.params.PARAM_NAME.PARAM_VALUE"></a>`"matchers".MATCHER_NAME."params".PARAM_NAME.PARAM_VALUE`

A value for the param. This can be any JSON compliant value such as a string,
number, boolean, array, or object. The value will be serialized as a string when
passed to the matcher clause. The value is overridden by the same field
specified in [`"attributes".ATTRIBUTE_NAME."params"`](#attributes.ATTRIBUTE_NAME.params)
in either the input or the model.

- Required: No
- Type: Any


### <a name="matchers.MATCHER_NAME.quality"></a>`"matchers".MATCHER_NAME."quality"`

A matcher quality score represents the quality or trustworthiness of a matcher.
It modifies the [attribute identity confidence base score](#attributes.ATTRIBUTE_NAME.score)
and contributes to the final attribute identity confidence score.

- A quality score of `1.0` represents 100% confidence that the matcher can be trusted.
- A quality score of `0.0` represents 100% confidence that the matcher cannot be trusted.
- A quality score of `null` indicates that the matcher lacks a quality score.

Effectively this means:

- A quality score of `1.0` will not affect the attribute identity confidence base score.
- A quality score of less than `1.0` will penalize the attribute identity confidence base score.
- A quality score of `0.0` will set the attribute identity confidence base score to `0.5`.
- A quality score of `null` will not affect the attribute identity confidence base score.

The purpose of the matcher quality score is to reflect any dubious matcher
quality in the final document [`"_score"`](/docs/entity-resolution/output-specification/#hits.hits._explanation.matches.score).
For example, an exact matcher may have a quality score of `1.0`, while a fuzzy
matcher may have a quality score of `0.95` to express slightly less confidence
in the quality of the match.

- Required: No
- Type: Float
- Default: `null`


## <a name="indices"></a>`"indices"`

**Model**

```javascript
{
  "indices": {
    INDEX_NAME: {
      "fields": {
        INDEX_FIELD_NAME: {
          "attribute": ATTRIBUTE_NAME,
          "matcher": MATCHER_NAME,
          "quality": INDEX_FIELD_QUALITY_SCORE
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
          "matcher": "fuzzy_matcher",
          "quality": 0.95
        },
        "zip.keyword": {
          "attribute": "zip",
          "matcher": "exact_matcher",
          "quality": 0.98
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
          "matcher": "fuzzy_matcher",
          "quality": 0.98
        },
        "addr_street": {
          "attribute": "street",
          "matcher": "fuzzy_matcher",
          "quality": 0.95
        },
        "addr_city": {
          "attribute": "city",
          "matcher": "standard_matcher",
          "quality": 0.98
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

Different indices in Elasticsearch might have data that can be matched as
attributes, but each index might use slightly different field names or data
types for the same data. Therefore, zentity uses a map to translate the
different field names to the attributes of our entity model.

The entity model maps attributes and matchers to index fields. Remember how each
attribute can be matched in different ways, such as a name that can be matched
by its exact value or its phonetic value? Elasticsearch would index those
different values as distinct fields, such as `"name.keyword"` and
`"name.phonetic"`. This is why the entity model maps attributes and matchers --
not just attributes -- to index fields.


### <a name="indices.INDEX_NAME"></a>`"indices".INDEX_NAME`

A field with the name of a distinct Elasticsearch [index](https://www.elastic.co/guide/en/elasticsearch/reference/current/_basic_concepts.html#_index)
or [index pattern](https://www.elastic.co/guide/en/elasticsearch/reference/current/multi-index.html).
The value of the field is an object that contains metadata about the index.

zentity does not verify the existence of indices or the validity of index
patterns or the syntax of field names that Elasticsearch requires. Elasticsearch
may respond with an error for resolution jobs that submit queries to indices
that do not exist.

- Required: Yes
- Type: String


### <a name="indices.INDEX_NAME.fields"></a>`"indices".INDEX_NAME."fields"`

An object that maps an index field name to an attribute and a matcher.


### <a name="indices.INDEX_NAME.fields.INDEX_FIELD_NAME"></a>`"indices".INDEX_NAME."fields".INDEX_FIELD_NAME`

A field with the name of a distinct [property](https://www.elastic.co/guide/en/elasticsearch/reference/current/properties.html)
or [field](https://www.elastic.co/guide/en/elasticsearch/reference/current/multi-fields.html)
in an Elasticsearch index. The value of the field is an object that contians
metadata about the index field, particularly the attribute and matcher that is
mapped to it.

zentity does not verify the existence of field names within indices or the
syntax of field names that Elasticsearch
requires.


### <a name="indices.INDEX_NAME.fields.INDEX_FIELD_NAME.attribute"></a>`"indices".INDEX_NAME."fields".INDEX_FIELD_NAME."attribute"`

The name of an attribute from the [`"attributes"`](#attributes) object of the
entity model. If the attribute does not exist, then the index field will not be
queried in any resolution jobs and will not be returned in the `"_attributes"`
field of the documents matched in a resolution job.

- Required: Yes
- Type: String


### <a name="indices.INDEX_NAME.fields.INDEX_FIELD_NAME.matcher"></a>`"indices".INDEX_NAME."fields".INDEX_FIELD_NAME."matcher"`

The name of a matcher from the [`"matchers"`](#matchers) object of the entity
model. If the matcher does not exist, then the index field will not be queried
in any resolution jobs. However, the index field can still be returned in the
[`"attributes"`](#attributes) field of the documents matched in a resolution job
if those documents matched the attributes of other resolvers.

Let's illustrate how index fields relate to matchers and attributes during a
resolution job. Assume you are resolving an entity with an email address of
`"user@example.net"` and one of the indices has an field name of
`"email.keyword"`. And assume that the index field is mapped to the matcher
clause below:

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

The `"matcher"` field is optional. The index field won't be queried if the
`"matcher"` field is unspecified. There are valid reasons to map an index field
only an attribute and not a matcher. It allows the value of index field to be
returned as the `"attribute"` if the document is matched by other resolvers. For
example, an attribute for `"salary"` might not be useful in identifying and
resolving entities, but it could be useful to return salary data from disparate
indices under a field with a common name. These are sometimes called "payload"
attributes.

- Required: No
- Type: String


### <a name="indices.INDEX_NAME.fields.INDEX_FIELD_NAME.quality"></a>`"indices".INDEX_NAME."fields".INDEX_FIELD_NAME."quality"`

An index field quality score represents the quality or trustworthiness of the
data in an index field. It modifies the [attribute identity confidence base score](#attributes.ATTRIBUTE_NAME.score)
and contributes to the final attribute identity confidence score.

- A quality score of `1.0` represents 100% confidence that the index field data can be trusted.
- A quality score of `0.0` represents 100% confidence that the index field data cannot be trusted.
- A quality score of `null` indicates that the index field lacks a quality score.

Effectively this means:

- A quality score of `1.0` will not affect the attribute identity confidence base score.
- A quality score of less than `1.0` will penalize the attribute identity confidence base score.
- A quality score of `0.0` will set the attribute identity confidence base score to `0.5`.
- A quality score of `null` will not affect the attribute identity confidence base score.

The purpose of the index field quality score is to reflect any dubious data
quality in the final document [`"_score"`](/docs/entity-resolution/output-specification/#hits.hits._explanation.matches.score).
For example, an index field with perfectly clean and governed data may have a
quality score of `1.0`, while an index field with known data quality issues may
have a quality score of `0.95` to express slightly less confidence in the
quality of the match.


&nbsp;

----

#### Continue Reading

|&#8249;|[Entity Models](/docs/entity-models)|[Entity Modeling Tips](/docs/entity-models/tips)|&#8250;|
|:---|:---|---:|---:|
|    |    |    |    |
