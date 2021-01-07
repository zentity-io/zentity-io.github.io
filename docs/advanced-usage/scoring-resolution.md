[Home](/) / [Documentation](/docs) / [Advanced Usage](/docs/advanced-usage) / Scoring Resolution


#### <a name="contents"></a>Advanced Usage Tutorials 📖

This tutorial is part of a series to help you learn and perform the advanced
functions of zentity. You should complete the [basic usage](/docs/basic-usage)
tutorials before completing these advanced usage tutorials.

1. **Scoring Resolution** *&#8592; You are here.*
2. [Matcher Parameters](/docs/advanced-usage/matcher-parameters)
3. [Date Attributes](/docs/advanced-usage/date-attributes)
4. [Payload Attributes](/docs/advanced-usage/payload-attributes)

---


# <a name="scoring-resolution"></a>Scoring Resolution

zentity lets you score the matching documents of an entity resolution job. This
is a powerful tool for adjudicating the quality of matches, and it enables
client-side sorting or filtering of results based on the confidence of the
matches.

Let's dive in.

> **Before you start**
>
> You must install [Elasticsearch](https://www.elastic.co/downloads/elasticsearch),
> [Kibana](https://www.elastic.co/downloads/kibana), and [zentity](/docs/installation)
> to complete this tutorial. This tutorial was tested with
> [zentity-{$ tutorial.zentity $}-elasticsearch-{$ tutorial.elasticsearch $}](/releases#zentity-{$ tutorial.zentity $}).
>
> **Quick start**
>
> You can use the [zentity sandbox](/sandbox) which has the required software
> and data for these tutorials. This will let you skip many of the setup steps.


## <a name="prepare"></a>1. Prepare for the tutorial


### <a name="install-required-plugins"></a>1.1 Install the required plugins

> **Note:** Skip this step if you're using the [zentity sandbox](/sandbox).

This tutorial uses the [phonetic analysis plugin](https://www.elastic.co/guide/en/elasticsearch/plugins/current/analysis-phonetic.html)
and [ICU analysis plugin](https://www.elastic.co/guide/en/elasticsearch/plugins/current/analysis-icu.html)
for Elasticsearch. You will need to stop Elasticsearch, install these plugin,
and start Elasticsearch. You can learn more about Elasticsearch plugin management
[here](https://www.elastic.co/guide/en/elasticsearch/plugins/current/plugin-management.html).

For Linux (in the `$ES_HOME` directory of a .tar.gz installation):

```sh
sudo bin/elasticsearch-plugin install analysis-phonetic
sudo bin/elasticsearch-plugin install analysis-icu
```

For Windows (in the `$ES_HOME` directory of a .zip installation):

```sh
bin/elasticsearch-plugin.bat install analysis-phonetic
bin/elasticsearch-plugin.bat install analysis-icu
```


### <a name="open-kibana-console-ui"></a>1.2 Open the Kibana Console UI

The [Kibana Console UI](https://www.elastic.co/guide/en/kibana/current/console-kibana.html)
makes it easy to submit requests to Elasticsearch and read responses.


### <a name="delete-old-tutorial-indices"></a>1.3 Delete any old tutorial indices

> **Note:** Skip this step if you're using the [zentity sandbox](/sandbox).

Let's start from scratch. Delete any tutorial indices you might have created
from other tutorials.

```javascript
DELETE zentity_tutorial_4_*
```


### <a name="create-tutorial-index"></a>1.4 Create the tutorial index

> **Note:** Skip this step if you're using the [zentity sandbox](/sandbox).

Now create the template for this tutorial.

```javascript
PUT zentity_tutorial_4_multiple_resolver_resolution
{
  "settings": {
    "index": {
      "number_of_shards": 1,
      "number_of_replicas": 0,
      "analysis" : {
        "filter" : {
          "street_suffix_map" : {
            "pattern" : "(st)",
            "type" : "pattern_replace",
            "replacement" : "street"
          },
          "phonetic" : {
            "type" : "phonetic",
            "encoder" : "nysiis"
          },
          "punct_white" : {
            "pattern" : "\\p{Punct}",
            "type" : "pattern_replace",
            "replacement" : " "
          },
          "remove_non_digits" : {
            "pattern" : "[^\\d]",
            "type" : "pattern_replace",
            "replacement" : ""
          }
        },
        "analyzer" : {
          "name_clean" : {
            "filter" : [
              "icu_normalizer",
              "icu_folding",
              "punct_white"
            ],
            "tokenizer" : "standard"
          },
          "name_phonetic" : {
            "filter" : [
              "icu_normalizer",
              "icu_folding",
              "punct_white",
              "phonetic"
            ],
            "tokenizer" : "standard"
          },
          "street_clean" : {
            "filter" : [
              "icu_normalizer",
              "icu_folding",
              "punct_white",
              "trim"
            ],
            "tokenizer" : "keyword"
          },
          "phone_clean" : {
            "filter" : [
              "remove_non_digits"
            ],
            "tokenizer" : "keyword"
          }
        }
      }
    }
  },
  "mappings": {
    "properties": {
      "id": {
        "type": "keyword"
      },
      "first_name": {
        "type": "text",
        "fields": {
          "clean": {
            "type": "text",
            "analyzer": "name_clean"
          },
          "phonetic": {
            "type": "text",
            "analyzer": "name_phonetic"
          }
        }
      },
      "last_name": {
        "type": "text",
        "fields": {
          "clean": {
            "type": "text",
            "analyzer": "name_clean"
          },
          "phonetic": {
            "type": "text",
            "analyzer": "name_phonetic"
          }
        }
      },
      "street": {
        "type": "text",
        "fields": {
          "clean": {
            "type": "text",
            "analyzer": "street_clean"
          }
        }
      },
      "city": {
        "type": "text",
        "fields": {
          "clean": {
            "type": "text",
            "analyzer": "name_clean"
          }
        }
      },
      "state": {
        "type": "text",
        "fields": {
          "keyword": {
            "type": "keyword"
          }
        }
      },
      "phone": {
        "type": "text",
        "fields": {
          "clean": {
            "type": "text",
            "analyzer": "phone_clean"
          }
        }
      },
      "email": {
        "type": "text",
        "fields": {
          "keyword": {
            "type": "keyword"
          }
        }
      }
    }
  }
}
```


### <a name="load-tutorial-data"></a>1.5 Load the tutorial data

> **Note:** Skip this step if you're using the [zentity sandbox](/sandbox).

Add the tutorial data to the index.

```javascript
POST _bulk?refresh
{"index": {"_id": "1", "_index": "zentity_tutorial_4_multiple_resolver_resolution"}}
{"city": "Washington", "email": "allie@example.net", "first_name": "Allie", "id": "1", "last_name": "Jones", "phone": "202-555-1234", "state": "DC", "street": "123 Main St"}
{"index": {"_id": "2", "_index": "zentity_tutorial_4_multiple_resolver_resolution"}}
{"city": "Washington", "email": "", "first_name": "Alicia", "id": "2", "last_name": "Johnson", "phone": "202-123-4567", "state": "DC", "street": "300 Main St"}
{"index": {"_id": "3", "_index": "zentity_tutorial_4_multiple_resolver_resolution"}}
{"city": "Washington", "email": "", "first_name": "Allie", "id": "3", "last_name": "Jones", "phone": "", "state": "DC", "street": "123 Main St"}
{"index": {"_id": "4", "_index": "zentity_tutorial_4_multiple_resolver_resolution"}}
{"city": "", "email": "", "first_name": "Ally", "id": "4", "last_name": "Joans", "phone": "202-555-1234", "state": "", "street": ""}
{"index": {"_id": "5", "_index": "zentity_tutorial_4_multiple_resolver_resolution"}}
{"city": "Arlington", "email": "ej@example.net", "first_name": "Eli", "id": "5", "last_name": "Jonas", "phone": "", "state": "VA", "street": "500 23rd Street"}
{"index": {"_id": "6", "_index": "zentity_tutorial_4_multiple_resolver_resolution"}}
{"city": "Washington", "email": "allie@example.net", "first_name": "Allison", "id": "6", "last_name": "Jones", "phone": "202-555-1234", "state": "DC", "street": "123 Main St"}
{"index": {"_id": "7", "_index": "zentity_tutorial_4_multiple_resolver_resolution"}}
{"city": "Washington", "email": "", "first_name": "Allison", "id": "7", "last_name": "Smith", "phone": "+1 (202) 555 1234", "state": "DC", "street": "555 Broad St"}
{"index": {"_id": "8", "_index": "zentity_tutorial_4_multiple_resolver_resolution"}}
{"city": "Washington", "email": "alan.smith@example.net", "first_name": "Alan", "id": "8", "last_name": "Smith", "phone": "202-000-5555", "state": "DC", "street": "555 Broad St"}
{"index": {"_id": "9", "_index": "zentity_tutorial_4_multiple_resolver_resolution"}}
{"city": "Washington", "email": "alan.smith@example.net", "first_name": "Alan", "id": "9", "last_name": "Smith", "phone": "2020005555", "state": "DC", "street": "555 Broad St"}
{"index": {"_id": "10", "_index": "zentity_tutorial_4_multiple_resolver_resolution"}}
{"city": "Washington", "email": "", "first_name": "Alison", "id": "10", "last_name": "Smith", "phone": "202-555-9876", "state": "DC", "street": "555 Broad St"}
{"index": {"_id": "11", "_index": "zentity_tutorial_4_multiple_resolver_resolution"}}
{"city": "", "email": "allie@example.net", "first_name": "Alison", "id": "11", "last_name": "Jones-Smith", "phone": "2025559867", "state": "", "street": ""}
{"index": {"_id": "12", "_index": "zentity_tutorial_4_multiple_resolver_resolution"}}
{"city": "Washington", "email": "allison.j.smith@corp.example.net", "first_name": "Allison", "id": "12", "last_name": "Jones-Smith", "phone": "", "state": "DC", "street": "555 Broad St"}
{"index": {"_id": "13", "_index": "zentity_tutorial_4_multiple_resolver_resolution"}}
{"city": "Arlington", "email": "allison.j.smith@corp.example.net", "first_name": "Allison", "id": "13", "last_name": "Jones Smith", "phone": "703-555-5555", "state": "VA", "street": "1 Corporate Way"}
{"index": {"_id": "14", "_index": "zentity_tutorial_4_multiple_resolver_resolution"}}
{"city": "Arlington", "email": "elise.jonas@corp.example.net", "first_name": "Elise", "id": "14", "last_name": "Jonas", "phone": "703-555-5555", "state": "VA", "street": "1 Corporate Way"}
```

Here's what the tutorial data looks like.

|id|first_name|last_name|street|city|state|phone|email|
|:---|:---|:---|:---|:---|:---|:---|:---|
|1|Allie|Jones|123 Main St|Washington|DC|202-555-1234|allie@example.net|
|2|Alicia|Johnson|300 Main St|Washington|DC|202-123-4567||
|3|Allie|Jones|123 Main St|Washington|DC|||
|4|Ally|Joans||||202-555-1234||
|5|Eli|Jonas|500 23rd Street|Arlington|VA||ej@example.net|
|6|Allison|Jones|123 Main St|Washington|DC|202-555-1234|allie@example.net|
|7|Allison|Smith|555 Broad St|Washington|DC|+1 (202) 555 1234||
|8|Alan|Smith|555 Broad St|Washington|DC|202-000-5555|alan.smith@example.net|
|9|Alan|Smith|555 Broad St|Washington|DC|2020005555|alan.smith@example.net|
|10|Alison|Smith|555 Broad St|Washington|DC|202-555-9876||
|11|Alison|Jones-Smith||||2025559867|allie@example.net|
|12|Allison|Jones-Smith|555 Broad St|Washington|DC||allison.j.smith@corp.example.net|
|13|Allison|Jones Smith|1 Corporate Way|Arlington|VA|703-555-5555|allison.j.smith@corp.example.net|
|14|Elise|Jonas|1 Corporate Way|Arlington|VA|703-555-5555|elise.jonas@corp.example.net|


## <a name="create-entity-model"></a>2. Create the entity model

> **Note:** Skip this step if you're using the [zentity sandbox](/sandbox).

Let's use the [Models API](/docs/rest-apis/models-api) to create the entity
model below. We'll review each part of the model in depth.

**Request**

```javascript
PUT _zentity/models/zentity_tutorial_4_person
{
  "attributes": {
    "first_name": {
      "type": "string",
      "score": 0.6125
    },
    "last_name": {
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
      "score": 0.5125
    },
    "phone": {
      "type": "string",
      "score": 0.85
    },
    "email": {
      "type": "string",
      "score": 0.95
    }
  },
  "resolvers": {
    "name_street_city_state": {
      "attributes": [ "first_name", "last_name", "street", "city", "state" ]
    },
    "name_phone": {
      "attributes": [ "first_name", "last_name", "phone" ]
    },
    "name_email": {
      "attributes": [ "first_name", "last_name", "email" ]
    },
    "email_phone": {
      "attributes": [ "email", "phone" ]
    }
  },
  "matchers": {
    "simple": {
      "clause": {
        "match": {
          "{{ field }}": "{{ value }}"
        }
      },
      "quality": 0.975
    },
    "fuzzy": {
      "clause": {
        "match": {
          "{{ field }}": {
            "query": "{{ value }}",
            "fuzziness": "1"
          }
        }
      },
      "quality": 0.95
    },
    "exact": {
      "clause": {
        "term": {
          "{{ field }}": "{{ value }}"
        }
      },
      "quality": 1.0
    }
  },
  "indices": {
    "zentity_tutorial_4_multiple_resolver_resolution": {
      "fields": {
        "first_name.clean": {
          "attribute": "first_name",
          "matcher": "fuzzy",
          "quality": 0.975
        },
        "first_name.phonetic": {
          "attribute": "first_name",
          "matcher": "simple",
          "quality": 0.925
        },
        "last_name.clean": {
          "attribute": "last_name",
          "matcher": "fuzzy",
          "quality": 0.975
        },
        "last_name.phonetic": {
          "attribute": "last_name",
          "matcher": "simple",
          "quality": 0.925
        },
        "street.clean": {
          "attribute": "street",
          "matcher": "fuzzy",
          "quality": 0.975
        },
        "city.clean": {
          "attribute": "city",
          "matcher": "fuzzy",
          "quality": 0.975
        },
        "state.keyword": {
          "attribute": "state",
          "matcher": "exact"
        },
        "phone.clean": {
          "attribute": "phone",
          "matcher": "fuzzy",
          "quality": 0.975
        },
        "email.keyword": {
          "attribute": "email",
          "matcher": "exact"
        }
      }
    }
  }
}
```

**Response**

```javascript
{
  "_index" : ".zentity-models",
  "_type" : "doc",
  "_id" : "zentity_tutorial_4_person",
  "_version" : 1,
  "result" : "created",
  "_shards" : {
    "total" : 2,
    "successful" : 1,
    "failed" : 0
  },
  "_seq_no" : 1,
  "_primary_term" : 1
}
```


### <a name="review-attributes"></a>2.1 Review the attributes

We defined seven attributes as shown in this section:

```javascript
{
  "attributes": {
    "first_name": {
      "type": "string",
      "score": 0.6125
    },
    "last_name": {
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
      "score": 0.5125
    },
    "phone": {
      "type": "string",
      "score": 0.85
    },
    "email": {
      "type": "string",
      "score": 0.95
    }
  }
}
```

Each attribute now has a `"score"` field, which represents the **attribute
identity confidence base score**.

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

> **Tip**
>
> Care should be taken when using a base score of `1.0` or `0.0`, because it
> would allow a single attribute identity confidence score to determine the
> document [`"_score"`](/docs/entity-resolution/output-specification/#hits.hits._explanation.matches.score).
> Whenever there is an attribute identity confidence score of `1.0` or `0.0`, it
> takes precedence over any other attribute identity confidence score in the
> document. For example, you might have an `"id"` field that you absolutely
> trust to identify an entity. If you allow the score of the `"id"` field to be
> `1.0`, then anytime the `"id"` field matches in a document, no other attribute
> identity confidence score would matter because you've already stated that the
> `"id"` field always indicates a match with perfect confidence. A best practice
> would be to use a high number such as `0.99` to allow for some small level of
> variability and more nuanced rankings of documents.

The entity model in this tutorial chose the following `"score"` values:

**High cardinality fields**

- `"email"` - `0.95` - This field may have a high chance of uniquely identifying
the entity. People rarely share email addresses, and applications often tie the
identity of the user to an email address. Sometimes an email address is shared
by a family or a division of a company, so it would be wise to allow for some
uncertainty by keeping the score below `1.0`.
- `"phone"` - `0.85` - This field may have a high chance of uniquely identifying
the entity. Phone numbers can be changed and used by other people over time.
Sometimes family members share phone numbers. Nevertheless, while a phone number
might not be quite as reliable of an identifier as an email address, many phone
numbers will be associated with a single entity.

Example:

In our tutorial model, if the `"email"` and `"phone"` attributes match in a
document, then composite identity confidence score of the two attributes would
be approximately `0.9908` using the following formula:

`(.95 * .85) / ((.95 * .85) + ((1 - .95) * (1 - .85))) = 0.99079754601`

**Normal cardinality fields**

- `"street"` - `0.75` - Like phone numbers, street addresses can be changed and
used by other people over time. Sometimes family members share street addresses.
It's not uncommon for a street address to appear in multiple cities and states.
Therefore, while a street address could have a significant influence on the
composite identity confidence score, there should be other matching attributes
present to corroborate the confidence of the match.
- `"last_name"` - `0.65` - Many people share the same last name, so it wouldn't
be wise to rely on just a last name to identify an entity. Additional attributes
should be present to enhance the composite identity confidence score, such as
the first name and other attributes.
- `"first_name"` - `0.6125` - First names are shared even more frequently than
last names.

Example:

In our tutorial model, if the `"first_name"` and `"last_name"` attributes match
in a document, then composite identity confidence score of the two attributes
would be approximately `0.7459` using the following formula:

`(.65 * .6125) / ((.65 * .6125) + ((1 - .65) * (1 - .6125))) = 0.74590163934`

**Low cardinality fields**

- `"city"` - `0.55` - Thousands or millions of people may live in the same city.
The city field alone should not identify an entity, but it may influence the
composite identity confidence score when there are additional matching
attributes.
- `"state"` - `0.5125` - Just like the city field, millions of people may live
in the same state. It should not significantly affect the composite identity
confidence score unless there are additional matching attributes.

Example:

In our tutorial model, if the `"city"` and `"state"` attributes match in a
document, then composite identity confidence score of the two attributes would
be approximately `0.5623` using the following formula:

`(.55 * .5125) / ((.55 * .5125) + ((1 - .55) * (1 - .5125))) = 0.56234413965`

**More examples**

In our tutorial model, if the `"first_name"`, `"last_name"`, `"street"`,
`"city"` and `"state"` attributes match in a document, then composite identity
confidence score of the two attributes would be approximately `0.7904` using the
following formula:

`(.65 * .6125 * .55 * .5125) / ((.65 * .6125 * .55 * .5125) + ((1 - .65) * (1 - .6125) * (1 - .55) * (1 - .5125))) = 0.79043565348`

If the `"phone"`, `"last_name"`, and `"city"` attributes match in a document,
then composite identity confidence score of the two attributes would be
approximately `0.9279` using the following formula:

`(.85 * .65 * .55) / ((.85 * .65 * .55) + ((1 - .85) * (1 - .65) * (1 - .55))) = 0.92786259542`

Every example above can be modified using [matcher quality scores](/docs/entity-models/specification/#matchers.MATCHER_NAME.quality)
and [index field quality scores](/docs/entity-models/specification/#indices.INDEX_NAME.fields.INDEX_FIELD_NAME.quality)
to represent increased uncertainty due to known imperfections in the matchers or
data fields that led to a match.


### <a name="review-matchers"></a>2.2 Review the matchers

We defined three matchers called `"simple"`, `"fuzzy"`, and `"exact"` as shown
in this section:

```javascript
{
  "matchers": {
    "simple": {
      "clause": {
        "match": {
          "{{ field }}": "{{ value }}"
        }
      },
      "quality": 0.975
    },
    "fuzzy": {
      "clause": {
        "match": {
          "{{ field }}": {
            "query": "{{ value }}",
            "fuzziness": "1"
          }
        }
      },
      "quality": 0.95
    },
    "exact": {
      "clause": {
        "term": {
          "{{ field }}": "{{ value }}"
        }
      },
      "quality": 1.0
    }
  }
}
```

Each attribute now has a `"quality"` field. A matcher quality score represents
the quality or trustworthiness of a matcher. It modifies the [attribute identity
confidence base score](#attributes.ATTRIBUTE_NAME.score) and contributes to the
final attribute identity confidence score.

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

**Examples**

In our tutorial model, we assigned quality scores to the matchers:

- `"simple"` - `0.975` - The simple matcher uses a [`"match"`](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-match-query.html)
query, which may allow for some variation between the input value and the
indexed value. The degree of variation depends primary on the [analyzer](https://www.elastic.co/guide/en/elasticsearch/reference/current/analyzer.html)
of the text field, which should be reflected in the index field quality score.
However, we can start with a slight general penalty to any `"match"` query by
reducing the quality score of this matcher. The lower matcher quality score will
lead to a lower attribute identity confidence score.
- `"fuzzy"` - `0.95` - The fuzzy matcher also uses a [`"match"`](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-match-query.html)
query, but it also uses the [`"fuzziness"`](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-match-query.html#match-field-params)
parameter to allow for more variation in the match. The matcher's tolerance for
fuzziness introduces a slightly greater chance of false matches. The lower
matcher quality score will lead to a lower attribute identity confidence score.
- `"exact"` - `1.0` The exact matcher uses a [`"term"`](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-term-query.html)
query, which looks for an exact match between an input value and an indexed
value. We can leave this at `1.0` (or `null` or omitted altogether) because the
matcher introduces no quality issues to the resolution process.


### <a name="review-indices"></a>2.3 Review the indices

We defined a single index as shown in this section:

```javascript
{
  "indices": {
    "zentity_tutorial_4_multiple_resolver_resolution": {
      "fields": {
        "first_name.clean": {
          "attribute": "first_name",
          "matcher": "fuzzy"
        },
        "first_name.phonetic": {
          "attribute": "first_name",
          "matcher": "simple"
        },
        "last_name.clean": {
          "attribute": "last_name",
          "matcher": "fuzzy"
        },
        "last_name.phonetic": {
          "attribute": "last_name",
          "matcher": "simple"
        },
        "street.clean": {
          "attribute": "street",
          "matcher": "fuzzy"
        },
        "city.clean": {
          "attribute": "city",
          "matcher": "fuzzy"
        },
        "state.keyword": {
          "attribute": "state",
          "matcher": "exact"
        },
        "phone.clean": {
          "attribute": "phone",
          "matcher": "fuzzy"
        },
        "email.keyword": {
          "attribute": "email",
          "matcher": "exact"
        }
      }
    }
  }
}
```


## <a name="resolve-entity"></a>3. Resolve an entity


### <a name="resolve-entity-basic"></a>3.1 Run a resolution job with `"_score"`

Let's use the [Resolution API](/docs/rest-apis/resolution-api) to resolve a
person with a known first name, last name, and phone number. We'll set
`_score=true` to implement scoring and `_source=false` to focus only on the
normalized data.

**Request**

```javascript
POST _zentity/resolution/zentity_tutorial_4_person?pretty&_source=false&_score=true
{
  "attributes": {
    "first_name": [ "Allie" ],
    "last_name": [ "Jones" ],
    "phone": [ "202-555-1234" ]
  }
}
```

**Response**

```javascript
{
  "took" : 46,
  "hits" : {
    "total" : 9,
    "hits" : [ {
      "_index" : "zentity_tutorial_4_multiple_resolver_resolution",
      "_type" : "_doc",
      "_id" : "1",
      "_hop" : 0,
      "_query" : 0,
      "_score" : 0.9268137343974269,
      "_attributes" : {
        "city" : [ "Washington" ],
        "email" : [ "allie@example.net" ],
        "first_name" : [ "Allie" ],
        "last_name" : [ "Jones" ],
        "phone" : [ "202-555-1234" ],
        "state" : [ "DC" ],
        "street" : [ "123 Main St" ]
      }
    }, {
      "_index" : "zentity_tutorial_4_multiple_resolver_resolution",
      "_type" : "_doc",
      "_id" : "4",
      "_hop" : 0,
      "_query" : 0,
      "_score" : 0.9249425179947204,
      "_attributes" : {
        "city" : [ "" ],
        "email" : [ "" ],
        "first_name" : [ "Ally" ],
        "last_name" : [ "Joans" ],
        "phone" : [ "202-555-1234" ],
        "state" : [ "" ],
        "street" : [ "" ]
      }
    }, {
      "_index" : "zentity_tutorial_4_multiple_resolver_resolution",
      "_type" : "_doc",
      "_id" : "3",
      "_hop" : 1,
      "_query" : 0,
      "_score" : 0.9030972510297278,
      "_attributes" : {
        "city" : [ "Washington" ],
        "email" : [ "" ],
        "first_name" : [ "Allie" ],
        "last_name" : [ "Jones" ],
        "phone" : [ "" ],
        "state" : [ "DC" ],
        "street" : [ "123 Main St" ]
      }
    }, {
      "_index" : "zentity_tutorial_4_multiple_resolver_resolution",
      "_type" : "_doc",
      "_id" : "6",
      "_hop" : 1,
      "_query" : 0,
      "_score" : 0.9981643732697082,
      "_attributes" : {
        "city" : [ "Washington" ],
        "email" : [ "allie@example.net" ],
        "first_name" : [ "Allison" ],
        "last_name" : [ "Jones" ],
        "phone" : [ "202-555-1234" ],
        "state" : [ "DC" ],
        "street" : [ "123 Main St" ]
      }
    }, {
      "_index" : "zentity_tutorial_4_multiple_resolver_resolution",
      "_type" : "_doc",
      "_id" : "11",
      "_hop" : 2,
      "_query" : 0,
      "_score" : 0.9808891618065275,
      "_attributes" : {
        "city" : [ "" ],
        "email" : [ "allie@example.net" ],
        "first_name" : [ "Alison" ],
        "last_name" : [ "Jones-Smith" ],
        "phone" : [ "2025559867" ],
        "state" : [ "" ],
        "street" : [ "" ]
      }
    }, {
      "_index" : "zentity_tutorial_4_multiple_resolver_resolution",
      "_type" : "_doc",
      "_id" : "7",
      "_hop" : 3,
      "_query" : 0,
      "_score" : 0.9412842840763994,
      "_attributes" : {
        "city" : [ "Washington" ],
        "email" : [ "" ],
        "first_name" : [ "Allison" ],
        "last_name" : [ "Smith" ],
        "phone" : [ "+1 (202) 555 1234" ],
        "state" : [ "DC" ],
        "street" : [ "555 Broad St" ]
      }
    }, {
      "_index" : "zentity_tutorial_4_multiple_resolver_resolution",
      "_type" : "_doc",
      "_id" : "10",
      "_hop" : 3,
      "_query" : 0,
      "_score" : 0.9412842840763994,
      "_attributes" : {
        "city" : [ "Washington" ],
        "email" : [ "" ],
        "first_name" : [ "Alison" ],
        "last_name" : [ "Smith" ],
        "phone" : [ "202-555-9876" ],
        "state" : [ "DC" ],
        "street" : [ "555 Broad St" ]
      }
    }, {
      "_index" : "zentity_tutorial_4_multiple_resolver_resolution",
      "_type" : "_doc",
      "_id" : "12",
      "_hop" : 4,
      "_query" : 0,
      "_score" : 0.9030972510297278,
      "_attributes" : {
        "city" : [ "Washington" ],
        "email" : [ "allison.j.smith@corp.example.net" ],
        "first_name" : [ "Allison" ],
        "last_name" : [ "Jones-Smith" ],
        "phone" : [ "" ],
        "state" : [ "DC" ],
        "street" : [ "555 Broad St" ]
      }
    }, {
      "_index" : "zentity_tutorial_4_multiple_resolver_resolution",
      "_type" : "_doc",
      "_id" : "13",
      "_hop" : 5,
      "_query" : 0,
      "_score" : 0.9808891618065275,
      "_attributes" : {
        "city" : [ "Arlington" ],
        "email" : [ "allison.j.smith@corp.example.net" ],
        "first_name" : [ "Allison" ],
        "last_name" : [ "Jones Smith" ],
        "phone" : [ "703-555-5555" ],
        "state" : [ "VA" ],
        "street" : [ "1 Corporate Way" ]
      }
    } ]
  }
}
```

Each document now has a `"_score"` field that represents the confidence by which
the document matched known attributes of the entity. A higher `"_score"`
indicates greater confidence in the match.


### <a name="resolve-entity-source"></a>3.2 Show the `"_explanation"`

We can learn more about why a document matched and received its `"_score"` by
using the `"_explanation"` field. Let's run the job again and include the [`"_explanation"`](/docs/entity-resolution/output-specification/#hits.hits._explanation)
field of each document. The `"_explanation"` field tells us which resolvers
caused a document to match, and more specifically, which input value matched
which indexed value using which matcher and any parameters.

**Request**

```javascript
POST _zentity/resolution/zentity_tutorial_4_person?pretty&_source=false&_score=true&_explanation=true
{
  "attributes": {
    "first_name": [ "Allie" ],
    "last_name": [ "Jones" ],
    "phone": [ "202-555-1234" ]
  }
}
```

**Response**

```javascript
{
  "took" : 47,
  "hits" : {
    "total" : 9,
    "hits" : [ {
      "_index" : "zentity_tutorial_4_multiple_resolver_resolution",
      "_type" : "_doc",
      "_id" : "1",
      "_hop" : 0,
      "_query" : 0,
      "_score" : 0.9268137343974269,
      "_attributes" : {
        "city" : [ "Washington" ],
        "email" : [ "allie@example.net" ],
        "first_name" : [ "Allie" ],
        "last_name" : [ "Jones" ],
        "phone" : [ "202-555-1234" ],
        "state" : [ "DC" ],
        "street" : [ "123 Main St" ]
      },
      "_explanation" : {
        "resolvers" : {
          "name_phone" : {
            "attributes" : [ "first_name", "last_name", "phone" ]
          }
        },
        "matches" : [ {
          "attribute" : "first_name",
          "target_field" : "first_name.clean",
          "target_value" : "Allie",
          "input_value" : "Allie",
          "input_matcher" : "fuzzy",
          "input_matcher_params" : { },
          "score" : 0.6042031250000001
        }, {
          "attribute" : "first_name",
          "target_field" : "first_name.phonetic",
          "target_value" : "Allie",
          "input_value" : "Allie",
          "input_matcher" : "simple",
          "input_matcher_params" : { },
          "score" : 0.6014609375000001
        }, {
          "attribute" : "last_name",
          "target_field" : "last_name.clean",
          "target_value" : "Jones",
          "input_value" : "Jones",
          "input_matcher" : "fuzzy",
          "input_matcher_params" : { },
          "score" : 0.6389374999999999
        }, {
          "attribute" : "last_name",
          "target_field" : "last_name.phonetic",
          "target_value" : "Jones",
          "input_value" : "Jones",
          "input_matcher" : "simple",
          "input_matcher_params" : { },
          "score" : 0.63528125
        }, {
          "attribute" : "phone",
          "target_field" : "phone.clean",
          "target_value" : "202-555-1234",
          "input_value" : "202-555-1234",
          "input_matcher" : "fuzzy",
          "input_matcher_params" : { },
          "score" : 0.8241875
        } ]
      }
    }, {
      "_index" : "zentity_tutorial_4_multiple_resolver_resolution",
      "_type" : "_doc",
      "_id" : "4",
      "_hop" : 0,
      "_query" : 0,
      "_score" : 0.9249425179947204,
      "_attributes" : {
        "city" : [ "" ],
        "email" : [ "" ],
        "first_name" : [ "Ally" ],
        "last_name" : [ "Joans" ],
        "phone" : [ "202-555-1234" ],
        "state" : [ "" ],
        "street" : [ "" ]
      },
      "_explanation" : {
        "resolvers" : {
          "name_phone" : {
            "attributes" : [ "first_name", "last_name", "phone" ]
          }
        },
        "matches" : [ {
          "attribute" : "first_name",
          "target_field" : "first_name.phonetic",
          "target_value" : "Ally",
          "input_value" : "Allie",
          "input_matcher" : "simple",
          "input_matcher_params" : { },
          "score" : 0.6014609375000001
        }, {
          "attribute" : "last_name",
          "target_field" : "last_name.phonetic",
          "target_value" : "Joans",
          "input_value" : "Jones",
          "input_matcher" : "simple",
          "input_matcher_params" : { },
          "score" : 0.63528125
        }, {
          "attribute" : "phone",
          "target_field" : "phone.clean",
          "target_value" : "202-555-1234",
          "input_value" : "202-555-1234",
          "input_matcher" : "fuzzy",
          "input_matcher_params" : { },
          "score" : 0.8241875
        } ]
      }
    }, {
      "_index" : "zentity_tutorial_4_multiple_resolver_resolution",
      "_type" : "_doc",
      "_id" : "3",
      "_hop" : 1,
      "_query" : 0,
      "_score" : 0.9030972510297278,
      "_attributes" : {
        "city" : [ "Washington" ],
        "email" : [ "" ],
        "first_name" : [ "Allie" ],
        "last_name" : [ "Jones" ],
        "phone" : [ "" ],
        "state" : [ "DC" ],
        "street" : [ "123 Main St" ]
      },
      "_explanation" : {
        "resolvers" : {
          "name_street_city_state" : {
            "attributes" : [ "city", "first_name", "last_name", "state", "street" ]
          }
        },
        "matches" : [ {
          "attribute" : "city",
          "target_field" : "city.clean",
          "target_value" : "Washington",
          "input_value" : "Washington",
          "input_matcher" : "fuzzy",
          "input_matcher_params" : { },
          "score" : 0.5463125
        }, {
          "attribute" : "first_name",
          "target_field" : "first_name.clean",
          "target_value" : "Allie",
          "input_value" : "Allie",
          "input_matcher" : "fuzzy",
          "input_matcher_params" : { },
          "score" : 0.6042031250000001
        }, {
          "attribute" : "first_name",
          "target_field" : "first_name.phonetic",
          "target_value" : "Allie",
          "input_value" : "Allie",
          "input_matcher" : "simple",
          "input_matcher_params" : { },
          "score" : 0.6014609375000001
        }, {
          "attribute" : "first_name",
          "target_field" : "first_name.phonetic",
          "target_value" : "Allie",
          "input_value" : "Ally",
          "input_matcher" : "simple",
          "input_matcher_params" : { },
          "score" : 0.6014609375000001
        }, {
          "attribute" : "last_name",
          "target_field" : "last_name.clean",
          "target_value" : "Jones",
          "input_value" : "Jones",
          "input_matcher" : "fuzzy",
          "input_matcher_params" : { },
          "score" : 0.6389374999999999
        }, {
          "attribute" : "last_name",
          "target_field" : "last_name.phonetic",
          "target_value" : "Jones",
          "input_value" : "Joans",
          "input_matcher" : "simple",
          "input_matcher_params" : { },
          "score" : 0.63528125
        }, {
          "attribute" : "last_name",
          "target_field" : "last_name.phonetic",
          "target_value" : "Jones",
          "input_value" : "Jones",
          "input_matcher" : "simple",
          "input_matcher_params" : { },
          "score" : 0.63528125
        }, {
          "attribute" : "state",
          "target_field" : "state.keyword",
          "target_value" : "DC",
          "input_value" : "DC",
          "input_matcher" : "exact",
          "input_matcher_params" : { },
          "score" : 0.5125
        }, {
          "attribute" : "street",
          "target_field" : "street.clean",
          "target_value" : "123 Main St",
          "input_value" : "123 Main St",
          "input_matcher" : "fuzzy",
          "input_matcher_params" : { },
          "score" : 0.7315624999999999
        } ]
      }
    }, {
      "_index" : "zentity_tutorial_4_multiple_resolver_resolution",
      "_type" : "_doc",
      "_id" : "6",
      "_hop" : 1,
      "_query" : 0,
      "_score" : 0.9981643732697082,
      "_attributes" : {
        "city" : [ "Washington" ],
        "email" : [ "allie@example.net" ],
        "first_name" : [ "Allison" ],
        "last_name" : [ "Jones" ],
        "phone" : [ "202-555-1234" ],
        "state" : [ "DC" ],
        "street" : [ "123 Main St" ]
      },
      "_explanation" : {
        "resolvers" : {
          "email_phone" : {
            "attributes" : [ "email", "phone" ]
          }
        },
        "matches" : [ {
          "attribute" : "city",
          "target_field" : "city.clean",
          "target_value" : "Washington",
          "input_value" : "Washington",
          "input_matcher" : "fuzzy",
          "input_matcher_params" : { },
          "score" : 0.5463125
        }, {
          "attribute" : "email",
          "target_field" : "email.keyword",
          "target_value" : "allie@example.net",
          "input_value" : "allie@example.net",
          "input_matcher" : "exact",
          "input_matcher_params" : { },
          "score" : 0.95
        }, {
          "attribute" : "last_name",
          "target_field" : "last_name.clean",
          "target_value" : "Jones",
          "input_value" : "Jones",
          "input_matcher" : "fuzzy",
          "input_matcher_params" : { },
          "score" : 0.6389374999999999
        }, {
          "attribute" : "last_name",
          "target_field" : "last_name.phonetic",
          "target_value" : "Jones",
          "input_value" : "Joans",
          "input_matcher" : "simple",
          "input_matcher_params" : { },
          "score" : 0.63528125
        }, {
          "attribute" : "last_name",
          "target_field" : "last_name.phonetic",
          "target_value" : "Jones",
          "input_value" : "Jones",
          "input_matcher" : "simple",
          "input_matcher_params" : { },
          "score" : 0.63528125
        }, {
          "attribute" : "phone",
          "target_field" : "phone.clean",
          "target_value" : "202-555-1234",
          "input_value" : "202-555-1234",
          "input_matcher" : "fuzzy",
          "input_matcher_params" : { },
          "score" : 0.8241875
        }, {
          "attribute" : "state",
          "target_field" : "state.keyword",
          "target_value" : "DC",
          "input_value" : "DC",
          "input_matcher" : "exact",
          "input_matcher_params" : { },
          "score" : 0.5125
        }, {
          "attribute" : "street",
          "target_field" : "street.clean",
          "target_value" : "123 Main St",
          "input_value" : "123 Main St",
          "input_matcher" : "fuzzy",
          "input_matcher_params" : { },
          "score" : 0.7315624999999999
        } ]
      }
    }, {
      "_index" : "zentity_tutorial_4_multiple_resolver_resolution",
      "_type" : "_doc",
      "_id" : "11",
      "_hop" : 2,
      "_query" : 0,
      "_score" : 0.9808891618065275,
      "_attributes" : {
        "city" : [ "" ],
        "email" : [ "allie@example.net" ],
        "first_name" : [ "Alison" ],
        "last_name" : [ "Jones-Smith" ],
        "phone" : [ "2025559867" ],
        "state" : [ "" ],
        "street" : [ "" ]
      },
      "_explanation" : {
        "resolvers" : {
          "name_email" : {
            "attributes" : [ "email", "first_name", "last_name" ]
          }
        },
        "matches" : [ {
          "attribute" : "email",
          "target_field" : "email.keyword",
          "target_value" : "allie@example.net",
          "input_value" : "allie@example.net",
          "input_matcher" : "exact",
          "input_matcher_params" : { },
          "score" : 0.95
        }, {
          "attribute" : "first_name",
          "target_field" : "first_name.clean",
          "target_value" : "Alison",
          "input_value" : "Allison",
          "input_matcher" : "fuzzy",
          "input_matcher_params" : { },
          "score" : 0.6042031250000001
        }, {
          "attribute" : "first_name",
          "target_field" : "first_name.phonetic",
          "target_value" : "Alison",
          "input_value" : "Allison",
          "input_matcher" : "simple",
          "input_matcher_params" : { },
          "score" : 0.6014609375000001
        }, {
          "attribute" : "last_name",
          "target_field" : "last_name.clean",
          "target_value" : "Jones-Smith",
          "input_value" : "Jones",
          "input_matcher" : "fuzzy",
          "input_matcher_params" : { },
          "score" : 0.6389374999999999
        }, {
          "attribute" : "last_name",
          "target_field" : "last_name.phonetic",
          "target_value" : "Jones-Smith",
          "input_value" : "Joans",
          "input_matcher" : "simple",
          "input_matcher_params" : { },
          "score" : 0.63528125
        }, {
          "attribute" : "last_name",
          "target_field" : "last_name.phonetic",
          "target_value" : "Jones-Smith",
          "input_value" : "Jones",
          "input_matcher" : "simple",
          "input_matcher_params" : { },
          "score" : 0.63528125
        } ]
      }
    }, {
      "_index" : "zentity_tutorial_4_multiple_resolver_resolution",
      "_type" : "_doc",
      "_id" : "7",
      "_hop" : 3,
      "_query" : 0,
      "_score" : 0.9412842840763994,
      "_attributes" : {
        "city" : [ "Washington" ],
        "email" : [ "" ],
        "first_name" : [ "Allison" ],
        "last_name" : [ "Smith" ],
        "phone" : [ "+1 (202) 555 1234" ],
        "state" : [ "DC" ],
        "street" : [ "555 Broad St" ]
      },
      "_explanation" : {
        "resolvers" : {
          "name_phone" : {
            "attributes" : [ "first_name", "last_name", "phone" ]
          }
        },
        "matches" : [ {
          "attribute" : "city",
          "target_field" : "city.clean",
          "target_value" : "Washington",
          "input_value" : "Washington",
          "input_matcher" : "fuzzy",
          "input_matcher_params" : { },
          "score" : 0.5463125
        }, {
          "attribute" : "first_name",
          "target_field" : "first_name.clean",
          "target_value" : "Allison",
          "input_value" : "Alison",
          "input_matcher" : "fuzzy",
          "input_matcher_params" : { },
          "score" : 0.6042031250000001
        }, {
          "attribute" : "first_name",
          "target_field" : "first_name.clean",
          "target_value" : "Allison",
          "input_value" : "Allison",
          "input_matcher" : "fuzzy",
          "input_matcher_params" : { },
          "score" : 0.6042031250000001
        }, {
          "attribute" : "first_name",
          "target_field" : "first_name.phonetic",
          "target_value" : "Allison",
          "input_value" : "Alison",
          "input_matcher" : "simple",
          "input_matcher_params" : { },
          "score" : 0.6014609375000001
        }, {
          "attribute" : "first_name",
          "target_field" : "first_name.phonetic",
          "target_value" : "Allison",
          "input_value" : "Allison",
          "input_matcher" : "simple",
          "input_matcher_params" : { },
          "score" : 0.6014609375000001
        }, {
          "attribute" : "last_name",
          "target_field" : "last_name.clean",
          "target_value" : "Smith",
          "input_value" : "Jones-Smith",
          "input_matcher" : "fuzzy",
          "input_matcher_params" : { },
          "score" : 0.6389374999999999
        }, {
          "attribute" : "last_name",
          "target_field" : "last_name.phonetic",
          "target_value" : "Smith",
          "input_value" : "Jones-Smith",
          "input_matcher" : "simple",
          "input_matcher_params" : { },
          "score" : 0.63528125
        }, {
          "attribute" : "phone",
          "target_field" : "phone.clean",
          "target_value" : "+1 (202) 555 1234",
          "input_value" : "202-555-1234",
          "input_matcher" : "fuzzy",
          "input_matcher_params" : { },
          "score" : 0.8241875
        }, {
          "attribute" : "state",
          "target_field" : "state.keyword",
          "target_value" : "DC",
          "input_value" : "DC",
          "input_matcher" : "exact",
          "input_matcher_params" : { },
          "score" : 0.5125
        } ]
      }
    }, {
      "_index" : "zentity_tutorial_4_multiple_resolver_resolution",
      "_type" : "_doc",
      "_id" : "10",
      "_hop" : 3,
      "_query" : 0,
      "_score" : 0.9412842840763994,
      "_attributes" : {
        "city" : [ "Washington" ],
        "email" : [ "" ],
        "first_name" : [ "Alison" ],
        "last_name" : [ "Smith" ],
        "phone" : [ "202-555-9876" ],
        "state" : [ "DC" ],
        "street" : [ "555 Broad St" ]
      },
      "_explanation" : {
        "resolvers" : {
          "name_phone" : {
            "attributes" : [ "first_name", "last_name", "phone" ]
          }
        },
        "matches" : [ {
          "attribute" : "city",
          "target_field" : "city.clean",
          "target_value" : "Washington",
          "input_value" : "Washington",
          "input_matcher" : "fuzzy",
          "input_matcher_params" : { },
          "score" : 0.5463125
        }, {
          "attribute" : "first_name",
          "target_field" : "first_name.clean",
          "target_value" : "Alison",
          "input_value" : "Alison",
          "input_matcher" : "fuzzy",
          "input_matcher_params" : { },
          "score" : 0.6042031250000001
        }, {
          "attribute" : "first_name",
          "target_field" : "first_name.clean",
          "target_value" : "Alison",
          "input_value" : "Allison",
          "input_matcher" : "fuzzy",
          "input_matcher_params" : { },
          "score" : 0.6042031250000001
        }, {
          "attribute" : "first_name",
          "target_field" : "first_name.phonetic",
          "target_value" : "Alison",
          "input_value" : "Alison",
          "input_matcher" : "simple",
          "input_matcher_params" : { },
          "score" : 0.6014609375000001
        }, {
          "attribute" : "first_name",
          "target_field" : "first_name.phonetic",
          "target_value" : "Alison",
          "input_value" : "Allison",
          "input_matcher" : "simple",
          "input_matcher_params" : { },
          "score" : 0.6014609375000001
        }, {
          "attribute" : "last_name",
          "target_field" : "last_name.clean",
          "target_value" : "Smith",
          "input_value" : "Jones-Smith",
          "input_matcher" : "fuzzy",
          "input_matcher_params" : { },
          "score" : 0.6389374999999999
        }, {
          "attribute" : "last_name",
          "target_field" : "last_name.phonetic",
          "target_value" : "Smith",
          "input_value" : "Jones-Smith",
          "input_matcher" : "simple",
          "input_matcher_params" : { },
          "score" : 0.63528125
        }, {
          "attribute" : "phone",
          "target_field" : "phone.clean",
          "target_value" : "202-555-9876",
          "input_value" : "2025559867",
          "input_matcher" : "fuzzy",
          "input_matcher_params" : { },
          "score" : 0.8241875
        }, {
          "attribute" : "state",
          "target_field" : "state.keyword",
          "target_value" : "DC",
          "input_value" : "DC",
          "input_matcher" : "exact",
          "input_matcher_params" : { },
          "score" : 0.5125
        } ]
      }
    }, {
      "_index" : "zentity_tutorial_4_multiple_resolver_resolution",
      "_type" : "_doc",
      "_id" : "12",
      "_hop" : 4,
      "_query" : 0,
      "_score" : 0.9030972510297278,
      "_attributes" : {
        "city" : [ "Washington" ],
        "email" : [ "allison.j.smith@corp.example.net" ],
        "first_name" : [ "Allison" ],
        "last_name" : [ "Jones-Smith" ],
        "phone" : [ "" ],
        "state" : [ "DC" ],
        "street" : [ "555 Broad St" ]
      },
      "_explanation" : {
        "resolvers" : {
          "name_street_city_state" : {
            "attributes" : [ "city", "first_name", "last_name", "state", "street" ]
          }
        },
        "matches" : [ {
          "attribute" : "city",
          "target_field" : "city.clean",
          "target_value" : "Washington",
          "input_value" : "Washington",
          "input_matcher" : "fuzzy",
          "input_matcher_params" : { },
          "score" : 0.5463125
        }, {
          "attribute" : "first_name",
          "target_field" : "first_name.clean",
          "target_value" : "Allison",
          "input_value" : "Alison",
          "input_matcher" : "fuzzy",
          "input_matcher_params" : { },
          "score" : 0.6042031250000001
        }, {
          "attribute" : "first_name",
          "target_field" : "first_name.clean",
          "target_value" : "Allison",
          "input_value" : "Allison",
          "input_matcher" : "fuzzy",
          "input_matcher_params" : { },
          "score" : 0.6042031250000001
        }, {
          "attribute" : "first_name",
          "target_field" : "first_name.phonetic",
          "target_value" : "Allison",
          "input_value" : "Alison",
          "input_matcher" : "simple",
          "input_matcher_params" : { },
          "score" : 0.6014609375000001
        }, {
          "attribute" : "first_name",
          "target_field" : "first_name.phonetic",
          "target_value" : "Allison",
          "input_value" : "Allison",
          "input_matcher" : "simple",
          "input_matcher_params" : { },
          "score" : 0.6014609375000001
        }, {
          "attribute" : "last_name",
          "target_field" : "last_name.clean",
          "target_value" : "Jones-Smith",
          "input_value" : "Jones",
          "input_matcher" : "fuzzy",
          "input_matcher_params" : { },
          "score" : 0.6389374999999999
        }, {
          "attribute" : "last_name",
          "target_field" : "last_name.clean",
          "target_value" : "Jones-Smith",
          "input_value" : "Jones-Smith",
          "input_matcher" : "fuzzy",
          "input_matcher_params" : { },
          "score" : 0.6389374999999999
        }, {
          "attribute" : "last_name",
          "target_field" : "last_name.clean",
          "target_value" : "Jones-Smith",
          "input_value" : "Smith",
          "input_matcher" : "fuzzy",
          "input_matcher_params" : { },
          "score" : 0.6389374999999999
        }, {
          "attribute" : "last_name",
          "target_field" : "last_name.phonetic",
          "target_value" : "Jones-Smith",
          "input_value" : "Joans",
          "input_matcher" : "simple",
          "input_matcher_params" : { },
          "score" : 0.63528125
        }, {
          "attribute" : "last_name",
          "target_field" : "last_name.phonetic",
          "target_value" : "Jones-Smith",
          "input_value" : "Jones",
          "input_matcher" : "simple",
          "input_matcher_params" : { },
          "score" : 0.63528125
        }, {
          "attribute" : "last_name",
          "target_field" : "last_name.phonetic",
          "target_value" : "Jones-Smith",
          "input_value" : "Jones-Smith",
          "input_matcher" : "simple",
          "input_matcher_params" : { },
          "score" : 0.63528125
        }, {
          "attribute" : "last_name",
          "target_field" : "last_name.phonetic",
          "target_value" : "Jones-Smith",
          "input_value" : "Smith",
          "input_matcher" : "simple",
          "input_matcher_params" : { },
          "score" : 0.63528125
        }, {
          "attribute" : "state",
          "target_field" : "state.keyword",
          "target_value" : "DC",
          "input_value" : "DC",
          "input_matcher" : "exact",
          "input_matcher_params" : { },
          "score" : 0.5125
        }, {
          "attribute" : "street",
          "target_field" : "street.clean",
          "target_value" : "555 Broad St",
          "input_value" : "555 Broad St",
          "input_matcher" : "fuzzy",
          "input_matcher_params" : { },
          "score" : 0.7315624999999999
        } ]
      }
    }, {
      "_index" : "zentity_tutorial_4_multiple_resolver_resolution",
      "_type" : "_doc",
      "_id" : "13",
      "_hop" : 5,
      "_query" : 0,
      "_score" : 0.9808891618065275,
      "_attributes" : {
        "city" : [ "Arlington" ],
        "email" : [ "allison.j.smith@corp.example.net" ],
        "first_name" : [ "Allison" ],
        "last_name" : [ "Jones Smith" ],
        "phone" : [ "703-555-5555" ],
        "state" : [ "VA" ],
        "street" : [ "1 Corporate Way" ]
      },
      "_explanation" : {
        "resolvers" : {
          "name_email" : {
            "attributes" : [ "email", "first_name", "last_name" ]
          }
        },
        "matches" : [ {
          "attribute" : "email",
          "target_field" : "email.keyword",
          "target_value" : "allison.j.smith@corp.example.net",
          "input_value" : "allison.j.smith@corp.example.net",
          "input_matcher" : "exact",
          "input_matcher_params" : { },
          "score" : 0.95
        }, {
          "attribute" : "first_name",
          "target_field" : "first_name.clean",
          "target_value" : "Allison",
          "input_value" : "Alison",
          "input_matcher" : "fuzzy",
          "input_matcher_params" : { },
          "score" : 0.6042031250000001
        }, {
          "attribute" : "first_name",
          "target_field" : "first_name.clean",
          "target_value" : "Allison",
          "input_value" : "Allison",
          "input_matcher" : "fuzzy",
          "input_matcher_params" : { },
          "score" : 0.6042031250000001
        }, {
          "attribute" : "first_name",
          "target_field" : "first_name.phonetic",
          "target_value" : "Allison",
          "input_value" : "Alison",
          "input_matcher" : "simple",
          "input_matcher_params" : { },
          "score" : 0.6014609375000001
        }, {
          "attribute" : "first_name",
          "target_field" : "first_name.phonetic",
          "target_value" : "Allison",
          "input_value" : "Allison",
          "input_matcher" : "simple",
          "input_matcher_params" : { },
          "score" : 0.6014609375000001
        }, {
          "attribute" : "last_name",
          "target_field" : "last_name.clean",
          "target_value" : "Jones Smith",
          "input_value" : "Jones",
          "input_matcher" : "fuzzy",
          "input_matcher_params" : { },
          "score" : 0.6389374999999999
        }, {
          "attribute" : "last_name",
          "target_field" : "last_name.clean",
          "target_value" : "Jones Smith",
          "input_value" : "Jones-Smith",
          "input_matcher" : "fuzzy",
          "input_matcher_params" : { },
          "score" : 0.6389374999999999
        }, {
          "attribute" : "last_name",
          "target_field" : "last_name.clean",
          "target_value" : "Jones Smith",
          "input_value" : "Smith",
          "input_matcher" : "fuzzy",
          "input_matcher_params" : { },
          "score" : 0.6389374999999999
        }, {
          "attribute" : "last_name",
          "target_field" : "last_name.phonetic",
          "target_value" : "Jones Smith",
          "input_value" : "Joans",
          "input_matcher" : "simple",
          "input_matcher_params" : { },
          "score" : 0.63528125
        }, {
          "attribute" : "last_name",
          "target_field" : "last_name.phonetic",
          "target_value" : "Jones Smith",
          "input_value" : "Jones",
          "input_matcher" : "simple",
          "input_matcher_params" : { },
          "score" : 0.63528125
        }, {
          "attribute" : "last_name",
          "target_field" : "last_name.phonetic",
          "target_value" : "Jones Smith",
          "input_value" : "Jones-Smith",
          "input_matcher" : "simple",
          "input_matcher_params" : { },
          "score" : 0.63528125
        }, {
          "attribute" : "last_name",
          "target_field" : "last_name.phonetic",
          "target_value" : "Jones Smith",
          "input_value" : "Smith",
          "input_matcher" : "simple",
          "input_matcher_params" : { },
          "score" : 0.63528125
        } ]
      }
    } ]
  }
}
```

Let's look at the `"_explanation"` of the document with the highest `"_score"`
to see what led to its high confidence:

```javascript
{
  "_index" : "zentity_tutorial_4_multiple_resolver_resolution",
  "_type" : "_doc",
  "_id" : "6",
  "_hop" : 1,
  "_query" : 0,
  "_score" : 0.9981643732697082,
  "_attributes" : {
    "city" : [ "Washington" ],
    "email" : [ "allie@example.net" ],
    "first_name" : [ "Allison" ],
    "last_name" : [ "Jones" ],
    "phone" : [ "202-555-1234" ],
    "state" : [ "DC" ],
    "street" : [ "123 Main St" ]
  },
  "_explanation" : {
    "resolvers" : {
      "email_phone" : {
        "attributes" : [ "email", "phone" ]
      }
    },
    "matches" : [ {
      "attribute" : "city",
      "target_field" : "city.clean",
      "target_value" : "Washington",
      "input_value" : "Washington",
      "input_matcher" : "fuzzy",
      "input_matcher_params" : { },
      "score" : 0.5463125
    }, {
      "attribute" : "email",
      "target_field" : "email.keyword",
      "target_value" : "allie@example.net",
      "input_value" : "allie@example.net",
      "input_matcher" : "exact",
      "input_matcher_params" : { },
      "score" : 0.95
    }, {
      "attribute" : "last_name",
      "target_field" : "last_name.clean",
      "target_value" : "Jones",
      "input_value" : "Jones",
      "input_matcher" : "fuzzy",
      "input_matcher_params" : { },
      "score" : 0.6389374999999999
    }, {
      "attribute" : "last_name",
      "target_field" : "last_name.phonetic",
      "target_value" : "Jones",
      "input_value" : "Joans",
      "input_matcher" : "simple",
      "input_matcher_params" : { },
      "score" : 0.63528125
    }, {
      "attribute" : "last_name",
      "target_field" : "last_name.phonetic",
      "target_value" : "Jones",
      "input_value" : "Jones",
      "input_matcher" : "simple",
      "input_matcher_params" : { },
      "score" : 0.63528125
    }, {
      "attribute" : "phone",
      "target_field" : "phone.clean",
      "target_value" : "202-555-1234",
      "input_value" : "202-555-1234",
      "input_matcher" : "fuzzy",
      "input_matcher_params" : { },
      "score" : 0.8241875
    }, {
      "attribute" : "state",
      "target_field" : "state.keyword",
      "target_value" : "DC",
      "input_value" : "DC",
      "input_matcher" : "exact",
      "input_matcher_params" : { },
      "score" : 0.5125
    }, {
      "attribute" : "street",
      "target_field" : "street.clean",
      "target_value" : "123 Main St",
      "input_value" : "123 Main St",
      "input_matcher" : "fuzzy",
      "input_matcher_params" : { },
      "score" : 0.7315624999999999
    } ]
  }
}
```

The `"_explanation"` field shows the details of each matching attribute in the
document, including the attribute's `"score"`. Some attributes in this document
matched multiple times, such as the `"last_name"` attribute. The scores for
those attributes were affected by the `"quality"` score modifiers of the
matchers and index fields in the entity model.

The algorithm for the overall document `"_score"` takes the maximum score of
each attribute and calculates the conflation probability of those scores. Let's
run that calculation now using the attribute scores in this document.

First we must find the maximum scores of each matching attribute in the document:

|Attribute|Maximum Score|
|----|----|
|`"city"`|`0.5463125`|
|`"email"`|`0.95`|
|`"last_name"`|`0.6389374999999999`|
|`"phone"`|`0.8241875`|
|`"state"`|`0.5125`|
|`"street"`|`0.7315624999999999`|

Then we will calculate the conflation probability of those scores:

`(0.5463125 * 0.95 * 0.6389374999999999 * 0.8241875 * 0.5125 * 0.7315624999999999) / ((0.5463125 * 0.95 * 0.6389374999999999 * 0.8241875 * 0.5125 * 0.7315624999999999) + ((1 - 0.5463125) * (1 - 0.95) * (1 - 0.6389374999999999) * (1 - 0.8241875) * (1 - 0.5125) * (1 - 0.7315624999999999)))`

This yields the overall document `"_score"`:

`0.9981643732697082`


## <a name="conclusion"></a>Conclusion

You learned how to score documents in the results of a resolution job, and how
to analyze the explanation of those scores. This is a powerful tool for
adjudicating the quality of the results of entity resolution.


&nbsp;

----

#### Continue Reading

|&#8249;|[Advanced Usage](/docs/advanced-usage)|[Matcher Parameters](/docs/advanced-usage/matcher-parameters)|&#8250;|
|:---|:---|---:|---:|
|    |    |    |    |
