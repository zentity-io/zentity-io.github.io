[Home](/) / [Documentation](/docs) / [Entity Models](/docs/entity-models) / Tips


# Tips


**1. Become familiar with your data.**

The real world has countless entity types and ways of resolving them. Start with what's relevant to your data. Look at
your data and understand the qualities of the fields and values within them. Are the values consistent? Are the values
created by end users with poor quality control measures? Are there duplicate values? Are there empty values? Do some
values appear more frequently than others? Which fields have high cardinality? Which fields are useful or useless for
identification purposes?

Knowing your data will help you determine what entity types you can resolve, which attributes constitute which entity
type, and what logic is needed to match the attributes and resolve the entities.

**2. Outline the attributes of your entity types.**

The first step to understanding an entity is to think about the attributes that describe it. Useful attributes will
include anything that can help identify an entity. For example, some common attributes to identify a person include
`name`, `address`, `dob`, `email`, `phone`, `ssn`, etc. Some attributes can also be represented in different ways. For
example, you might have an attribute for `address` and more specific attributes for `street`, `city`, `state`, `zip`,
`country`.

Start with the attributes that you know exist in your data. Don't worry about how to match an email address if you
don't have any email addresses in your data. Afterward, you can consider any additional attributes that you might see
in future data sets. You can always update your entity models later without having to reindex any data, so there's no
pressure to get it right the first time.

**3. Determine the matching logic for each attribute.**

You need to write at least one [matcher](/docs/entity-models/specification) for the resolution job to build queries.
A matcher is simply a clause of a [`"bool"` query](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-bool-query.html)
in Elasticsearch. Some attributes might have exact matches. Some attributes such as a `name` will tolerate
[fuzziness](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-fuzzy-query.html) or target
[phonetic tokens](https://www.elastic.co/guide/en/elasticsearch/guide/current/phonetic-matching.html), while other
attributes such as an `email address` might not.

Below is an example of two matchers called `text` and `phonetic`. You might use the `text` matcher, which uses the
`"fuzziness"` field to allow for typos, on indexed name fields that used the [standard analyzer](https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis-standard-analyzer.html).
You might use the `phonetic` matcher on indexed name fields that used a [phonetic token filter](https://www.elastic.co/guide/en/elasticsearch/plugins/current/analysis-phonetic-token-filter.html),
which is already a loose match that wouldn't benefit from the `"fuzziness"` field and might even generate more false
positives if you did use it.

**Example**

```javascript
{
  "matchers": {
    "text": {
      "clause": {
        "match": {
          "{{ field }}": {
            "query": "{{ value }}",
            "fuzziness": 2
          }
        }
      }
    },
    "phonetic": {
      "clause": {
        "match": {
          "{{ field }}": {
            "query": "{{ value }}",
            "fuzziness": 0
          }
        }
      }
    }
  }
}
```

**4. Determine which combinations attributes lead to resolution.**
 
Usually you don't want to rely on a single attribute to resolve an entity. Imagine how many false positives you would
get if you tried to resolve a person by a name, like John Smith! Even attributes like Social Security Numbers (SSNs)
can be fraught with errors such as typos or bogus numbers, and there are valid reasons why a person might change an
SSN.

Instead, try to write resolvers that use combinations of attributes to avoid those "snowballs" of false positives.
Each combination represents a minimum amount of matching attributes that you would need to resolve an entity with
confidence. Below is an example that shows how you might combine the attributes `name`, `dob`, `street`, `city`,
`state`, `zip`, `email`, `phone` to resolve a `person` entity type.

**Example**

```javascript
{
  "resolvers": {
    "name_dob_city_state": {
        "attributes": [
          "name", "dob", "city", "state"
        ]
    },
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

What combinations of attributes are right for you? That depends entirely on your data and your tolerance to errors.
You will need to experiment do determine what combinations of attributes yield satisfactory error rates on your
particular data sets.

**5. Use custom analyzers to index data in clever ways to improve accuracy.**
 
One of the goals of zentity is to prevent you from ever needing to reindex your data. But there are still cases
where you might want to do this. For example, you might have an indexed field called `name` that was indexed using
the [standard analyzer](https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis-standard-analyzer.html).
You can write a matcher that performs a basic match on this field, perhaps allowing for some fuzziness. But you
might want to have a [phonetic](https://www.elastic.co/guide/en/elasticsearch/plugins/current/analysis-phonetic-token-filter.html)
matcher, too. There are many ways to spell transliterated names, such as Muhammad: *Muhammed, Muhamad, Muhamed, Muhamet, Mahamed,
Mohamad, Mohamed, Mohammad, Mohammed*, etc. All of these spelling variations can be reduced to the same phonetic value. But that
value has to exist in the index if we want to use it for matching. If it doesn't exist, you would need to update your index mapping
to create a field that uses a [custom analyzer](https://www.elastic.co/guide/en/elasticsearch/guide/current/custom-analyzers.html)
using a phonetic tokenizer, and then [reindex](https://www.elastic.co/guide/en/elasticsearch/reference/current/docs-reindex.html)
the data.


&nbsp;

----

#### Continue Reading

|&#8249;|[Specification](/docs/entity-models/specification)|[REST APIs](/docs/rest-apis)|&#8250;|
|:---|:---|---:|---:|
|    |    |    |    |