[Home](/) / [Documentation](/docs) / [Entity Resolution](/docs/entity-resolution) / Input


# <a name="input">Entity Resolution Input Specification</a>

```javascript
{
  "attributes": {
    ATTRIBUTE_NAME: {
      "values": [
        ATTRIBUTE_VALUE,
        ...
      ],
      "params": {
        PARAM_NAME: PARAM_VALUE,
        ...
      }
    },
    ...
  },
  "scope": {
    "exclude": {
      "attributes": {
        ATTRIBUTE_NAME: [
          ATTRIBUTE_VALUE,
          ...
        ],
        ...
      },
      "indices": [
        INDEX_NAME,
        ...
      ],
      "resolvers": [
        RESOLVER_NAME,
        ...
      ]
    },
    "include": {
      "attributes": {
        ATTRIBUTE_NAME: [
          ATTRIBUTE_VALUE,
          ...
        ],
        ...
      },
      "indices": [
        INDEX_NAME,
        ...
      ],
      "resolvers": [
        RESOLVER_NAME,
        ...
      ]
    }
  },
  "model": ENTITY_MODEL
}
```

Entity resolution inputs are [JSON](https://www.json.org/) documents. In the framework shown above, lowercase quoted values
(e.g. `"attributes"`) are constant fields, uppercase literal values (e.g. `ATTRIBUTE_NAME`) are variable fields or values,
and elipses (`...`) are optional repetitions of the preceding field or value.

An entity resolution input has one required object (**[`"attributes"`](#attributes)**), one optional object
(**[`"scope"`](#scope)**) and one object that is required only if `entity_type` is not specified in the endpoint of the request
(**[`"model"`](#model)**).  Not all elements within these objects are required. Optional elements are noted in the descriptions
of each element listed on this page. Some elements have alternate forms that are acceptable, and those are also noted in the
descriptions of each element.


## <a name="attributes"></a>`"attributes"`

**Model**

```javascript
{
  "attributes": {
    ATTRIBUTE_NAME: {
      "values": [
        ATTRIBUTE_VALUE,
        ...
      ],
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
      "values": [
        "Allie Jones",
        "Allison Jones-Smith",
      ]
    },
    "phone": {
      "values": [
        "555-123-4567"
      ],
      "params": {
        "fuzziness": "auto"
      }
    },
    "dob": {
      "params": {
        "format": "yyyy-MM-dd"
      }
    }
  }
}
```

**Shorthand Model**

```javascript
{
  "attributes": {
    ATTRIBUTE_NAME: [
      ATTRIBUTE_VALUE,
      ...
    ],
    ...
  }
}
```

**Shorthand Example**

```javascript
{
  "attributes": {
    "name": [
      "Allie Jones",
      "Allison Jones-Smith",
    ],
    "phone": [
      "555-123-4567"
    ]
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


### <a name="attributes.ATTRIBUTE_NAME"></a>`"attributes".ATTRIBUTE_NAME`

A field with the name of a distinct attribute. Some examples might be `"name"`, `"dob"`, `"phone"`, etc.

The value of the field can be one of two things:

- An object that contains the **[`"values"`](#attributes.ATTRIBUTE_NAME.values)** and/or **[`"params`"](#attributes.ATTRIBUTE_NAME.params)** of the attribute.
- An array that contains the **[`"values`"](#attributes.ATTRIBUTE_NAME.values)** of the attribute.

At least one attribute must be specified, otherwise there would be no input to supply to the entity resolution job.

- Required: Yes
- Type: String


### <a name="attributes.ATTRIBUTE_NAME.type"></a>`"attributes".ATTRIBUTE_NAME."values"`

An array of attribute values. These values will serve as the initial inputs to the entity resolution job.

Each value must conform to the respective [attribute type](/docs/entity-models/specification#attributes.ATTRIBUTE_NAME.type)
specified in the [entity model](/docs/entity-models). For example, [string](/docs/entity-models/specification#attribute-type-string) values
must be JSON compliant string values, [number](/docs/entity-models/specification#attribute-type-number) values must be JSON compliant number values,
and [date](/docs/entity-models/specification#attribute-type-date) values must include a `"format"` field in the **[`"params"`](#attributes.ATTRIBUTE_NAME.params)**
object if it was not already specified in either the attribute or matcher of the entity model.

This field is not necessarily required. It would be valid to specify and attribute with no values and to override the
[`"params"`](#attributes.ATTRIBUTE_NAME.params) of the attribute or matcher of the entity model. One reason might be to override the
`"format"` param of a [`"date"`](/docs/entity-models/specification#attribute-type-date) attribute, which would affect the format of
any date values for that attribute returned by the entity resolution job.

At least one attribute must have the `"values"` field specified, otherwise there would be no input to supply to the entity resolution job.

- Required: At least for one attribute
- Type: Array


### <a name="attributes.ATTRIBUTE_NAME.params"></a>`"attributes".ATTRIBUTE_NAME."params"`

An optional object that passes arbitrary variables (`"params"`) to the matcher clauses.

- Required: No
- Type: Object


### <a name="attributes.ATTRIBUTE_NAME.params.PARAM_NAME"></a>`"attributes".ATTRIBUTE_NAME."params".PARAM_NAME`

A field with the name of a distinct param for the attribute. Some examples might be `"fuzziness"` or `"format"`.

- Required: No
- Type: String


### <a name="attributes.ATTRIBUTE_NAME.params.PARAM_NAME.PARAM_VALUE"></a>`"attributes".ATTRIBUTE_NAME."params".PARAM_NAME.PARAM_VALUE`

A value for the param. This can be any JSON compliant value such as a string, number, boolean, array, or object. The value
will be serialized as a string when passed to the matcher clause. The value overrides the same field specified in
**[`"attributes".ATTRIBUTE_NAME."params"`](#attributes.ATTRIBUTE_NAME.params)** in the model and
**[`"matchers".MATCHER_NAME."params"`](#matchers.MATCHER_NAME.params)**.

- Required: No
- Type: Any


## <a name="scope"></a>`"scope"`

**Model**

```javascript
{
  "scope": {
    "exclude": {
      "attributes": {
        ATTRIBUTE_NAME: [
          ATTRIBUTE_VALUE,
          ...
        ],
        ...
      },
      "indices": [
        INDEX_NAME,
        ...
      ],
      "resolvers": [
        RESOLVER_NAME,
        ...
      ]
    },
    "include": {
      "attributes": {
        ATTRIBUTE_NAME: [
          ATTRIBUTE_VALUE,
          ...
        ],
        ...
      },
      "indices": [
        INDEX_NAME,
        ...
      ],
      "resolvers": [
        RESOLVER_NAME,
        ...
      ]
    }
  }
}
```

**Example**

```javascript
{
  "scope": {
    "exclude": {
      "attributes": {
        "name": [
          "unknown",
          "n/a"
        ],
        "phone": [
          "555-555-5555"
        ],
        "dob": [
          "0000-00-00",
          "1900-01-01"
        ]
      },
      "resolvers": [
        "name_ssn"
      ]
    },
    "include": {
      "attributes": {
        "country": [
          "US"
        ]
      },
      "indices": [
        "users"
      ]
    }
  }
}
```

An optional field that contains an object to limit the scope of the [resolution request](/docs/rest-apis/resolution-api).
Scope can be controlled by **[excluding](#scope.exclude)** ("blacklisting") or **[including](#scope.include)** ("whitelisting") attribute values,
indices, and resolvers.

- Required: No
- Type: Object


### <a name="scope.exclude"></a>`"scope"."exclude"`

An optional field that excludes **[`"attributes"`](#scope.exclude.attributes)**, **[`"indices"`](#scope.exclude.indices)**, or **[`"resolvers"`](#scope.exclude.resolvers)**
from the [resolution job](/docs/rest-apis/resolution-api). By setting any of these exclusions, no query will be allowed to include the given
attribute values, indices, or resolvers.

The values in `"scope"."exclude"` take precedence over any duplicate values specified [`"scope"."include"`](#scope.include).

- Required: No
- Type: Object


### <a name="scope.exclude.attributes"></a>`"scope"."exclude"."attributes"`

An optional field that excludes specific attribute values from the [resolution job](/docs/rest-apis/resolution-api).
By setting any of these attributes, no query will be allowed to include the values specified within them.

- Required: No
- Type: Object


### <a name="scope.exclude.attributes.ATTRIBUTE_NAME"></a>`"scope"."exclude"."attributes".ATTRIBUTE_NAME`

A field with the name of a distinct attribute. Some examples might be `"name"`, `"dob"`, `"phone"`, etc.
By setting an attribute, no query will be allowed to include the values specified within it.

- Required: No
- Type: Array


### <a name="scope.exclude.indices"></a>`"scope"."exclude"."indices"`

An optional field that excludes specific indices from the [resolution job](/docs/rest-apis/resolution-api).
By setting any of these indices, no query will be allowed to include those indices.

- Required: No
- Type: Object


### <a name="scope.exclude.indices.INDEX_NAME"></a>`"scope"."exclude"."indices".INDEX_NAME`

The name of a distinct index. By setting an index, no query will be allowed to include it.

- Required: No
- Type: String


### <a name="scope.exclude.resolvers"></a>`"scope"."exclude"."resolvers"`

An optional field that excludes specific resolvers from the [resolution job](/docs/rest-apis/resolution-api).
By setting any of these resolvers, no query will be allowed to include those resolvers.

- Required: No
- Type: Object


### <a name="scope.exclude.resolvers.RESOLVER_NAME"></a>`"scope"."exclude"."resolvers".RESOLVER_NAME`

The name of a distinct resolver. By setting an resolver, no query will be allowed to include it.

- Required: No
- Type: String


### <a name="scope.include"></a>`"scope"."include"`

An optional field that includes **[`"attributes"`](#scope.include.attributes)**, **[`"indices"`](#scope.include.indices)**, or **[`"resolvers"`](#scope.include.resolvers)**
from the [resolution job](/docs/rest-apis/resolution-api). By setting any of these inclusions, no query will be allowed to exclude the given
attribute values, indices, or resolvers.

The values in [`"scope"."exclude"`](#scope.exclude) take precedence over any duplicate values specified `"scope"."include"`.

- Required: No
- Type: Object


### <a name="scope.include.attributes"></a>`"scope"."include"."attributes"`

An optional field that includes specific attribute values from the [resolution job](/docs/rest-apis/resolution-api).
By setting any of these attributes, no query will be allowed to exclude the values specified within them.

- Required: No
- Type: Object


### <a name="scope.include.attributes.ATTRIBUTE_NAME"></a>`"scope"."include"."attributes".ATTRIBUTE_NAME`

A field with the name of a distinct attribute. Some examples might be `"name"`, `"dob"`, `"phone"`, etc.
By setting an attribute, no query will be allowed to exclude the values specified within it.

- Required: No
- Type: Array


### <a name="scope.include.indices"></a>`"scope"."include"."indices"`

An optional field that includes specific indices from the [resolution job](/docs/rest-apis/resolution-api).
By setting any of these indices, no query will be allowed to exclude those indices.

- Required: No
- Type: Object


### <a name="scope.include.indices.INDEX_NAME"></a>`"scope"."include"."indices".INDEX_NAME`

The name of a distinct index. By setting an index, no query will be allowed to exclude it.

- Required: No
- Type: String


### <a name="scope.include.resolvers"></a>`"scope"."include"."resolvers"`

An optional field that includes specific resolvers from the [resolution job](/docs/rest-apis/resolution-api).
By setting any of these resolvers, no query will be allowed to exclude those resolvers.

- Required: No
- Type: Object


### <a name="scope.include.resolvers.RESOLVER_NAME"></a>`"scope"."include"."resolvers".RESOLVER_NAME`

The name of a distinct resolver. By setting an resolver, no query will be allowed to exclude it.

- Required: No
- Type: String


## <a name="model"></a>`"model"`

The [entity model](/docs/entity-models) to use for the entity resolution job. This is only required if `entity_type` is not specified
in the endpoint of the [resolution request](/docs/rest-apis/resolution-api). Otherwise this field **must not** be present.

- Required: Only if `entity_type` is not specified in the endpoint of the [resolution request](/docs/rest-apis/resolution-api)
- Type: Object


&nbsp;

----

#### Continue Reading

|&#8249;|[Entity Resolution](/docs/entity-resolution)|[Output](/docs/entity-resolution/output)|&#8250;|
|:---|:---|---:|---:|
|    |    |    |    |