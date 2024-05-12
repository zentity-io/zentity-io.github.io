[Home](/) / [Documentation](/docs) / [REST APIs](/docs/rest-apis) / Bulk Resolution API


# <a name="resolution-api"></a>Bulk Resolution API

Performs multiple [Resolution API](/docs/rest-apis/resolution-api) operations
in parallel.

The request accepts two endpoints:

```javascript
POST _zentity/resolution/_bulk
POST _zentity/resolution/{entity_type}/_bulk
```

The `_bulk` endpoint requires [NDJSON](http://ndjson.org/) syntax. The payload
consists of pairs of lines. Each pair represents a single resolution job. The
first line of the pair contains the parameters of the job, which may include
`"entity_type"` and any other parameters that would have been set in the URL of a
single resolution request. The second line contains the [entity resolution input](/docs/entity-resolution/input-specification/). Each line must be an unindented JSON object.

Parameters may be defined in both the URL and the payload. Payload parameters,
including `"entity_type"`, take precedence over URL parameters.


### Examples

The three examples below are functionally equivalent and yield the same response.

**Example 1** - This request performs two resolution operations, each with a
unique set of parameters and inputs.

```javascript
POST _zentity/resolution/_bulk
{"entity_type":"zentity_tutorial_4_person","_score":true,"_explanation":true}
{"attributes":{"first_name":["Allie"],"last_name":["Jones"],"phone":["202-555-1234"]}}
{"entity_type":"zentity_tutorial_4_person","_score":true}
{"terms":["ej@example.net"]}
```

**Example 2** - This request simplifies the prior request by moving the
`"entity_type"` parameter from the payload to the URL path. Both operations
resolve a `person` entity type, so that requirement can be specified once in the
URL.

```javascript
POST _zentity/resolution/zentity_tutorial_4_person/_bulk
{"_score":true,"_explanation":true}
{"attributes":{"first_name":["Allie"],"last_name":["Jones"],"phone":["202-555-1234"]}}
{"_score":true}
{"terms":["ej@example.net"]}
```

**Example 3** - This request simplifies the prior request by moving the
`"_score"` parameter from the payload to the URL parameters. Both operations
invoke the `"_score"` feature, so that requirement can be specified once in the
URL, too.

```javascript
POST _zentity/resolution/zentity_tutorial_4_person/_bulk?_score=true
{"_explanation":true}
{"attributes":{"first_name":["Allie"],"last_name":["Jones"],"phone":["202-555-1234"]}}
{}
{"terms":["ej@example.net"]}
```


### Example Response

```javascript
{
  "took" : 28,
  "errors" : false,
  "items" : [ {
    "took" : 46,
    "hits" : {
      "total" : 9,
      "hits" : [ {
        "_index" : "zentity_tutorial_4_multiple_resolver_resolution",
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
        },
        "_source" : {
          "city" : "Washington",
          "email" : "allie@example.net",
          "first_name" : "Allie",
          "id" : "1",
          "last_name" : "Jones",
          "phone" : "202-555-1234",
          "state" : "DC",
          "street" : "123 Main St"
        }
      }, {
        "_index" : "zentity_tutorial_4_multiple_resolver_resolution",
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
        },
        "_source" : {
          "city" : "",
          "email" : "",
          "first_name" : "Ally",
          "id" : "4",
          "last_name" : "Joans",
          "phone" : "202-555-1234",
          "state" : "",
          "street" : ""
        }
      }, {
        "_index" : "zentity_tutorial_4_multiple_resolver_resolution",
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
        },
        "_source" : {
          "city" : "Washington",
          "email" : "",
          "first_name" : "Allie",
          "id" : "3",
          "last_name" : "Jones",
          "phone" : "",
          "state" : "DC",
          "street" : "123 Main St"
        }
      }, {
        "_index" : "zentity_tutorial_4_multiple_resolver_resolution",
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
        },
        "_source" : {
          "city" : "Washington",
          "email" : "allie@example.net",
          "first_name" : "Allison",
          "id" : "6",
          "last_name" : "Jones",
          "phone" : "202-555-1234",
          "state" : "DC",
          "street" : "123 Main St"
        }
      }, {
        "_index" : "zentity_tutorial_4_multiple_resolver_resolution",
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
        },
        "_source" : {
          "city" : "",
          "email" : "allie@example.net",
          "first_name" : "Alison",
          "id" : "11",
          "last_name" : "Jones-Smith",
          "phone" : "2025559867",
          "state" : "",
          "street" : ""
        }
      }, {
        "_index" : "zentity_tutorial_4_multiple_resolver_resolution",
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
        },
        "_source" : {
          "city" : "Washington",
          "email" : "",
          "first_name" : "Allison",
          "id" : "7",
          "last_name" : "Smith",
          "phone" : "+1 (202) 555 1234",
          "state" : "DC",
          "street" : "555 Broad St"
        }
      }, {
        "_index" : "zentity_tutorial_4_multiple_resolver_resolution",
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
        },
        "_source" : {
          "city" : "Washington",
          "email" : "",
          "first_name" : "Alison",
          "id" : "10",
          "last_name" : "Smith",
          "phone" : "202-555-9876",
          "state" : "DC",
          "street" : "555 Broad St"
        }
      }, {
        "_index" : "zentity_tutorial_4_multiple_resolver_resolution",
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
        },
        "_source" : {
          "city" : "Washington",
          "email" : "allison.j.smith@corp.example.net",
          "first_name" : "Allison",
          "id" : "12",
          "last_name" : "Jones-Smith",
          "phone" : "",
          "state" : "DC",
          "street" : "555 Broad St"
        }
      }, {
        "_index" : "zentity_tutorial_4_multiple_resolver_resolution",
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
        },
        "_source" : {
          "city" : "Arlington",
          "email" : "allison.j.smith@corp.example.net",
          "first_name" : "Allison",
          "id" : "13",
          "last_name" : "Jones Smith",
          "phone" : "703-555-5555",
          "state" : "VA",
          "street" : "1 Corporate Way"
        }
      } ]
    }
  }, {
    "took" : 4,
    "hits" : {
      "total" : 1,
      "hits" : [ {
        "_index" : "zentity_tutorial_4_multiple_resolver_resolution",
        "_id" : "5",
        "_hop" : 0,
        "_query" : 0,
        "_score" : 0.9888974842717649,
        "_attributes" : {
          "city" : [ "Arlington" ],
          "email" : [ "ej@example.net" ],
          "first_name" : [ "Eli" ],
          "last_name" : [ "Jonas" ],
          "phone" : [ "" ],
          "state" : [ "VA" ],
          "street" : [ "500 23rd Street" ]
        },
        "_source" : {
          "city" : "Arlington",
          "email" : "ej@example.net",
          "first_name" : "Eli",
          "id" : "5",
          "last_name" : "Jonas",
          "phone" : "",
          "state" : "VA",
          "street" : "500 23rd Street"
        }
      } ]
    }
  } ]
}
```


### HTTP Headers

|Header|Value|
|------|-----|
|`Content-Type`|`application/x-ndjson`|


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


## URL Parameters (advanced)

These are advanced search optimizations. Most users will not require them. It's recommended to use the default settings of the cluster unless you know what you're doing.

|Parameter|Type|Default|Required|Description|
|---------|----|-------|--------|-----------|
|`search.allow_partial_search_results`|Boolean|Cluster default|No|[`allow_partial_search_results`](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-search.html#search-search-api-query-params)|
|`search.batched_reduce_size`|Integer|Cluster default|No|[`batched_reduce_size`](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-search.html#search-search-api-query-params)|
|`search.max_concurrent_shard_requests`|Integer|Cluster default|No|[`max_concurrent_shard_requests`](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-search.html#search-search-api-query-params)|
|`search.preference`|String|Cluster default|No|[`preference`](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-request-body.html#request-body-search-preference)|
|`search.pre_filter_shard_size`|Integer|Cluster default|No|[`pre_filter_shard_size`](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-search.html#search-search-api-query-params)|
|`search.request_cache`|Boolean|Cluster default|No|[`request_cache`](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-search.html#search-search-api-query-params)|


### Notes

The `_bulk` endpoint optimizes performance in three ways:

- Runs jobs in parallel to minimize end-to-end processing time of multiple jobs.
- Retrieves the entity model just once before running the jobs when the
`entity_type` is given in the URL.
- Minimizes the network latency that would have occurred from multiple single
requests between the client and Elasticsearch.


&nbsp;

----

#### Continue Reading

|&#8249;|[Resolution API](/docs/rest-apis/resolution-api)|[Security](/docs/security)|&#8250;|
|:---|:---|---:|---:|
|    |    |    |    |
