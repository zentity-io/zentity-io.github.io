[Home](/#/) / [Documentation](/#/docs) / [Entity Models](/#/docs/entity-models) / Specification


# Specification


Let's look at what's inside an entity model.

```javascript
{
  "attributes": {
    ATTRIBUTE: {
      MATCHER: QUERY_TEMPLATE,
      ...
    },
    ...
  },
  "indices": {
    INDEX: {
      ATTRIBUTE.MATCHER: FIELD,
      ...
    },
    ...
  },
  "resolvers": {
    RESOLVER: [
      ATTRIBUTE,
      ...
    ],
    ...
  }
}
```

An entity model has three required objects: **`"attributes"`**, **`"indices"`**, **`"resolvers"`**.


## "attributes"

Attributes are elements that can assist the resolution of entities. For example, some common attributes of a person
include name, date of birth, and phone number. Each attribute has its own particular data qualities and purposes in the
real world. Therefore, zentity matches the values of each attribute using logic that is distinct to each attribute.

Some attributes can be matched using different methods. For example, a name could be matched by its exact value or its
phonetic value. Therefore the entity model allows each attribute to have one or more "matchers." A matcher is simply a
clause of a [`"bool"` query](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-bool-query.html)
in Elasticsearch. This means that if *any* matcher of an attribute yields a match for a given value, then the attribute
will be considered a match regardless of the results of the other matchers.

- **`ATTRIBUTE`** - The distinct name of an attribute. Some examples could include `"name"`, `"dob"`, `"phone"`, etc.
The name cannot include periods. The values of the attribute are one or more `MATCHER` objects.

- **`MATCHER`** - The distinct name of a matcher. Each matcher represents one valid method for matching an attribute.
The name cannot include periods. The value of the matcher is a `QUERY_TEMPLATE` object.

- **`QUERY_TEMPLATE`** - An object that represents the clause of a [`"bool"` query](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-bool-query.html)
in Elasticsearch. Each query template will be stitched together in a single `"bool"` query, so it must follow the
correct syntax for a `"bool"` query clause, except you don't need to include the top-level field `"bool"` or its
subfields such as `"must"` or `"should"`. The query template uses Mustache syntax to pass two important variables:
**`{{ field }}`** and **`{{ value }}`**. The `field` variable will be populated with the index field that maps to the
attribute. The `value` field will be populated with the value that will be queried for that attribute.


## "indices"

Different indices in Elasticsearch might have data that can be matched as attributes, but each index might use slightly
different field names or data types for the same data. Therefore, zentity uses a map to translate the different field
names to the attributes of our entity model.

The entity model maps attribute matchers to index fields. Remember how each attribute can be matched in different ways,
such as a name that can be matched by its exact value or its phonetic value? Elasticsearch would index those different
values as distinct fields, such as `"name.keyword"` and `"name.phonetic"`. This is why the entity model maps attribute
matchers -- not just attributes -- to index fields.

- **`INDEX`** - The distinct name of an index in Elasticsearch.

- **`ATTRIBUTE.MATCHER`** - The name of an `ATTRIBUTE` and `MATCHER` concatenated by a period.

- **`FIELD`** - The distinct name of a field in the index.


## "resolvers"

Resolvers are combinations of attributes that lead to a resolution. For example, you might decide to resolve entities
that share matching values for `"name"` and `"dob"` or `"name"` and `"phone"`. You can create a "resolver" for both
combinations of attributes. Then any documents whose values share either a matching `"name"` and `"dob"` or  `"name"`
and `"phone"` will resolve to the same entity.

Remember that attributes can have more than one matcher. This means that if *any* matcher of an attribute yields a
match for a given value, then the attribute will be considered a match regardless of the results of the other matchers.
So if you have an attribute called `name` with matchers called `keyword` and `phonetic`, then any resolver that uses
the `name` attribute is effectively saying that *either* `name.keyword` *or* `name.phonetic` are required to match.

- **`RESOLVER`** - The distinct name of the resolver. Each resolver represents one combination of attributes that lead
to resolution. The name cannot include periods The value of the resolver is an array of strings, each of which
represents the name of an `ATTRIBUTE`.

- **`ATTRIBUTE`** - The distinct name of an attribute. Some examples could include `"name"`, `"dob"`, `"phone"`, etc.
The name cannot include periods.


&nbsp;

----

#### Continue Reading

|&#8249;|[Usage](/#/docs/entity-models/usage)|[Tips](/#/docs/entity-models/tips)|&#8250;|
|:---|:---|---:|---:|
|    |    |    |    |