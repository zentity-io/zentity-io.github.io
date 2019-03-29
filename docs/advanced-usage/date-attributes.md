[Home](/) / [Documentation](/docs) / [Advanced Usage](/docs/advanced-usage) / Date Attributes


#### <a name="contents"></a>Advanced Usage Tutorials 📖

This tutorial is part of a series to help you learn and perform the advanced
functions of zentity. You should complete the [basic usage](/docs/basic-usage)
tutorials before completing these advanced usage tutorials.

1. [Matcher Parameters](/docs/advanced-usage/matcher-parameters)
2. **Date Attributes** *&#8592; You are here.*
3. [Payload Attributes](/docs/advanced-usage/payload-attributes)

---


# <a name="date-attributes"></a>Date Attributes

Date attributes are useful in many applications of entity resolution. You can resolve a person with the aid of a date of birth, a credit card with a date of expiration,
a driver's license with a date of issuance, or an event with a specific timestamp. You can use a date range to disambiguate two people who occupied the same home address at different times,
preventing a false match. You can reliably sessionize events in an application log by the client IP address if you match the events within a small time window, knowing that IP addresses
can change owners over longer periods of time.

Date matching comes its own challenges. Indices can represent dates and times in different formats
and at different levels of precision. Sometimes it makes sense to match within a date or time range rather than a specific point in time. zentity uses date attributes to help surmount these challenges.

The [`"date"`](/docs/entity-models/specification#attribute-type-date) attribute type can be used to match [date](https://www.elastic.co/guide/en/elasticsearch/reference/current/date.html) fields in Elasticsearch.
Date attributes use [matcher parameters](/docs/advanced-usage/matcher-parameters) to define the ["format"](https://www.elastic.co/guide/en/elasticsearch/reference/current/mapping-date-format.html) of the date field.
A `"format"` parameter is required to ensure that matchers use the date format that the indexed date field expects.
You must understand how matcher parameters work before writing date matchers.

This tutorial will show you how to write a matcher that gives you control over the window of a date range query.

Let's dive in.

> **Important**
> 
> You must install [Elasticsearch](https://www.elastic.co/downloads/elasticsearch), [Kibana](https://www.elastic.co/downloads/kibana), and [zentity](/docs/installation) to complete this tutorial.
> This tutorial was tested with [zentity-1.0.2-elasticsearch-6.7.0](/docs/releases).


## <a name="prepare"></a>1. Prepare for the tutorial


### <a name="open-kibana-console-ui"></a>1.1 Open the Kibana Console UI

The [Kibana Console UI](https://www.elastic.co/guide/en/kibana/current/console-kibana.html) makes it easy to submit requests to Elasticsearch and read responses.


### <a name="delete-old-tutorial-indices"></a>1.2 Delete any old tutorial indices

Let's start from scratch. Delete any tutorial indices you might have created from other tutorials.

```javascript
DELETE .zentity-tutorial-*
```


### <a name="create-tutorial-index"></a>1.3 Create the tutorial index

Now create the index for this tutorial.

```javascript
PUT .zentity-tutorial-index
{
  "settings": {
    "index": {
      "number_of_shards": 1,
      "number_of_replicas": 0
    }
  },
  "mappings": {
    "_doc": {
      "properties": {
        "@timestamp": {
          "type": "date"
        },
        "id": {
          "type": "keyword"
        },
        "ip": {
          "type": "keyword"
        },
        "path": {
          "type": "keyword"
        }
      }
    }
  }
}
```


### <a name="load-tutorial-data"></a>1.4 Load the tutorial data

Add the tutorial data to the index.

```javascript
POST _bulk?refresh
{"index": {"_id": "1", "_index": ".zentity-tutorial-index", "_type": "_doc"}}
{"@timestamp": "2019-02-28T23:01:45.248", "id": "1", "ip": "192.168.0.1", "path": "/"}
{"index": {"_id": "2", "_index": ".zentity-tutorial-index", "_type": "_doc"}}
{"@timestamp": "2019-02-28T23:02:05.658", "id": "2", "ip": "192.168.0.1", "path": "/docs"}
{"index": {"_id": "3", "_index": ".zentity-tutorial-index", "_type": "_doc"}}
{"@timestamp": "2019-02-28T23:02:08.782", "id": "3", "ip": "192.168.2.1", "path": "/"}
{"index": {"_id": "4", "_index": ".zentity-tutorial-index", "_type": "_doc"}}
{"@timestamp": "2019-02-28T23:02:12.024", "id": "4", "ip": "192.168.0.1", "path": "/docs/installation"}
{"index": {"_id": "5", "_index": ".zentity-tutorial-index", "_type": "_doc"}}
{"@timestamp": "2019-02-28T23:02:27.745", "id": "5", "ip": "192.168.2.1", "path": "/"}
{"index": {"_id": "6", "_index": ".zentity-tutorial-index", "_type": "_doc"}}
{"@timestamp": "2019-02-28T23:02:15.628", "id": "6", "ip": "192.168.0.1", "path": "/releases"}
{"index": {"_id": "7", "_index": ".zentity-tutorial-index", "_type": "_doc"}}
{"@timestamp": "2019-02-28T23:14:01.956", "id": "7", "ip": "192.168.0.1", "path": "/docs"}
{"index": {"_id": "8", "_index": ".zentity-tutorial-index", "_type": "_doc"}}
{"@timestamp": "2019-02-28T23:14:08.345", "id": "8", "ip": "192.168.3.1", "path": "/"}
{"index": {"_id": "9", "_index": ".zentity-tutorial-index", "_type": "_doc"}}
{"@timestamp": "2019-02-28T23:14:08.921", "id": "9", "ip": "192.168.0.1", "path": "/docs/installation"}
{"index": {"_id": "10", "_index": ".zentity-tutorial-index", "_type": "_doc"}}
{"@timestamp": "2019-02-28T23:21:00.003", "id": "10", "ip": "192.168.2.1", "path": "/"}
{"index": {"_id": "11", "_index": ".zentity-tutorial-index", "_type": "_doc"}}
{"@timestamp": "2019-02-28T23:22:07.565", "id": "11", "ip": "192.168.2.1", "path": "/"}
{"index": {"_id": "12", "_index": ".zentity-tutorial-index", "_type": "_doc"}}
{"@timestamp": "2019-02-28T23:28:11.114", "id": "12", "ip": "192.168.0.1", "path": "/docs/basic-usage"}
{"index": {"_id": "13", "_index": ".zentity-tutorial-index", "_type": "_doc"}}
{"@timestamp": "2019-02-28T23:30:45.346", "id": "13", "ip": "192.168.3.1", "path": "/docs/releases"}
{"index": {"_id": "14", "_index": ".zentity-tutorial-index", "_type": "_doc"}}
{"@timestamp": "2019-03-01T10:30:45.982", "id": "14", "ip": "192.168.4.1", "path": "/"}
{"index": {"_id": "15", "_index": ".zentity-tutorial-index", "_type": "_doc"}}
{"@timestamp": "2019-03-02T12:30:45.452", "id": "15", "ip": "192.168.0.1", "path": "/"}
{"index": {"_id": "16", "_index": ".zentity-tutorial-index", "_type": "_doc"}}
{"@timestamp": "2019-03-03T14:32:01.837", "id": "16", "ip": "192.168.0.1", "path": "/"}
{"index": {"_id": "17", "_index": ".zentity-tutorial-index", "_type": "_doc"}}
{"@timestamp": "2019-03-03T14:32:03.897", "id": "17", "ip": "192.168.0.1", "path": "/releases"}
{"index": {"_id": "18", "_index": ".zentity-tutorial-index", "_type": "_doc"}}
{"@timestamp": "2019-03-03T12:33:56.553", "id": "18", "ip": "192.168.0.1", "path": "/docs"}
```

Here's what the tutorial data looks like.

|id|timestamp|ip|path|
|:---|:---|:---|:---|
|1|2019-02-28T23:01:45.248|192.168.0.1|/|
|2|2019-02-28T23:02:05.658|192.168.0.1|/docs|
|3|2019-02-28T23:02:08.782|192.168.2.1|/|
|4|2019-02-28T23:02:12.024|192.168.0.1|/docs/installation|
|5|2019-02-28T23:02:27.745|192.168.2.1|/|
|6|2019-02-28T23:02:15.628|192.168.0.1|/releases|
|7|2019-02-28T23:14:01.956|192.168.0.1|/docs|
|8|2019-02-28T23:14:08.345|192.168.3.1|/|
|9|2019-02-28T23:14:08.921|192.168.0.1|/docs/installation|
|10|2019-02-28T23:21:00.003|192.168.2.1|/|
|11|2019-02-28T23:22:07.565|192.168.2.1|/|
|12|2019-02-28T23:28:11.114|192.168.0.1|/docs/basic-usage|
|13|2019-02-28T23:30:45.346|192.168.3.1|/releases|
|14|2019-03-01T10:30:45.982|192.168.4.1|/|
|15|2019-03-02T12:30:45.452|192.168.0.1|/|
|16|2019-03-03T14:32:01.837|192.168.0.1|/|
|17|2019-03-03T14:32:03.897|192.168.0.1|/releases|
|18|2019-03-03T12:33:56.553|192.168.0.1|/docs|


## <a name="create-entity-model"></a>2. Create the entity model

Let's use the [Models API](/docs/rest-apis/models-api) to create the entity model below. We'll review the matchers in depth.

```javascript
PUT _zentity/models/zentity-tutorial-http-session
{
  "attributes": {
    "timestamp": {
      "type": "date"
    },
    "ip": {
      "type": "string"
    }
  },
  "resolvers": {
    "timestamp_ip": {
      "attributes": [ "timestamp", "ip" ]
    }
  },
  "matchers": {
    "exact": {
      "clause": {
        "term": {
          "{{ field }}": "{{ value }}"
        }
      }
    },
    "time_range": {
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
  },
  "indices": {
    ".zentity-tutorial-index": {
      "fields": {
        "@timestamp": {
          "attribute": "timestamp",
          "matcher": "time_range"
        },
        "ip": {
          "attribute": "ip",
          "matcher": "exact"
        }
      }
    }
  }
}
```

### <a name="review-matchers"></a>2.1 Review the matchers

We defined two matchers called `"exact"` and `"time_range"`. The `"exact"`
matcher is used to match the IP address.

Let's focus on the `"time_range"` matcher. Our matcher uses a [range query](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-range-query.html#ranges-on-dates)
with [date math](https://www.elastic.co/guide/en/elasticsearch/reference/current/common-options.html#date-math)
to match documents within a given time window.

Here is an example of a range query with date math as shown in the documentation:

**Example Range Query with Date Math**

```javascript
GET _search
{
  "query": {
    "range" : {
      "date" : {
        "gte": "now-1d/d",
        "lt":  "now/d"
      }
    }
  }
}
```

Here is how we adapted that range query and added the parameters in our
`"time_range"` matcher. Notice that it includes the `"format"` parameter that
date attributes require, and a `"window"` parameter to control the time window
of the range query.

```javascript
{
  "matchers": {
    "time_range": {
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


## <a name="resolve-entity"></a>3. Resolve an entity

Let's use the [Resolution API](/docs/rest-apis/resolution-api) to resolve a
web traffic session with a known IP address at a given timestamp:

Submit a resolution job with the `"window"` parameter set to its default value,
which we defined as `"15m"` in the matcher.

```javascript
POST _zentity/resolution/zentity-tutorial-http-session?pretty
{
  "attributes": {
    "ip": [ "192.168.0.1" ],
    "timestamp": [ "2019-02-28T23:02:15.628" ]
  }
}
```

The results will look like this.

```javascript
{
  "took" : 25,
  "hits" : {
    "total" : 7,
    "hits" : [ {
      "_index" : ".zentity-tutorial-index",
      "_type" : "_doc",
      "_id" : "1",
      "_hop" : 0,
      "_attributes" : {
        "ip" : "192.168.0.1",
        "timestamp" : "2019-02-28T23:01:45.248"
      },
      "_source" : {
        "@timestamp" : "2019-02-28T23:01:45.248",
        "id" : "1",
        "ip" : "192.168.0.1",
        "path" : "/"
      }
    }, {
      "_index" : ".zentity-tutorial-index",
      "_type" : "_doc",
      "_id" : "2",
      "_hop" : 0,
      "_attributes" : {
        "ip" : "192.168.0.1",
        "timestamp" : "2019-02-28T23:02:05.658"
      },
      "_source" : {
        "@timestamp" : "2019-02-28T23:02:05.658",
        "id" : "2",
        "ip" : "192.168.0.1",
        "path" : "/docs"
      }
    }, {
      "_index" : ".zentity-tutorial-index",
      "_type" : "_doc",
      "_id" : "4",
      "_hop" : 0,
      "_attributes" : {
        "ip" : "192.168.0.1",
        "timestamp" : "2019-02-28T23:02:12.024"
      },
      "_source" : {
        "@timestamp" : "2019-02-28T23:02:12.024",
        "id" : "4",
        "ip" : "192.168.0.1",
        "path" : "/docs/installation"
      }
    }, {
      "_index" : ".zentity-tutorial-index",
      "_type" : "_doc",
      "_id" : "6",
      "_hop" : 0,
      "_attributes" : {
        "ip" : "192.168.0.1",
        "timestamp" : "2019-02-28T23:02:15.628"
      },
      "_source" : {
        "@timestamp" : "2019-02-28T23:02:15.628",
        "id" : "6",
        "ip" : "192.168.0.1",
        "path" : "/releases"
      }
    }, {
      "_index" : ".zentity-tutorial-index",
      "_type" : "_doc",
      "_id" : "7",
      "_hop" : 0,
      "_attributes" : {
        "ip" : "192.168.0.1",
        "timestamp" : "2019-02-28T23:14:01.956"
      },
      "_source" : {
        "@timestamp" : "2019-02-28T23:14:01.956",
        "id" : "7",
        "ip" : "192.168.0.1",
        "path" : "/docs"
      }
    }, {
      "_index" : ".zentity-tutorial-index",
      "_type" : "_doc",
      "_id" : "9",
      "_hop" : 0,
      "_attributes" : {
        "ip" : "192.168.0.1",
        "timestamp" : "2019-02-28T23:14:08.921"
      },
      "_source" : {
        "@timestamp" : "2019-02-28T23:14:08.921",
        "id" : "9",
        "ip" : "192.168.0.1",
        "path" : "/docs/installation"
      }
    }, {
      "_index" : ".zentity-tutorial-index",
      "_type" : "_doc",
      "_id" : "12",
      "_hop" : 1,
      "_attributes" : {
        "ip" : "192.168.0.1",
        "timestamp" : "2019-02-28T23:28:11.114"
      },
      "_source" : {
        "@timestamp" : "2019-02-28T23:28:11.114",
        "id" : "12",
        "ip" : "192.168.0.1",
        "path" : "/docs/basic-usage"
      }
    } ]
  }
}
```

Notice how the document with an `"_id"` of "`12`" has a timestamp that is
greater than 15 minutes from the timestamp of our input, even though our default
`"window"` parameter is `"15m"`. That is because the timestamp of that document
was within 15 minutes of another document that was within 15 minutes of the
initial results, which was the document with an `"_id"` of `"9"`. The `"window"`
parameter limits the time range of each hop, not the time range of the entire
resolution job. It is entirely possible to chain together many documents over
a long time range where each pair of documents must match within a much
smaller time range.

Now let's expand the `"window"` parameter from `"15m"` to `"2d"`.

```javascript
POST _zentity/resolution/zentity-tutorial-http-session?pretty
{
  "attributes": {
    "ip": [ "192.168.0.1" ],
    "timestamp": {
      "values": [ "2019-02-28T23:02:15.628" ],
      "params": {
        "window": "2d"
      }
    }
  }
}
```

The results will look like this:

```javascript
{
  "took" : 12,
  "hits" : {
    "total" : 11,
    "hits" : [ {
      "_index" : ".zentity-tutorial-index",
      "_type" : "_doc",
      "_id" : "1",
      "_hop" : 0,
      "_attributes" : {
        "ip" : "192.168.0.1",
        "timestamp" : "2019-02-28T23:01:45.248"
      },
      "_source" : {
        "@timestamp" : "2019-02-28T23:01:45.248",
        "id" : "1",
        "ip" : "192.168.0.1",
        "path" : "/"
      }
    }, {
      "_index" : ".zentity-tutorial-index",
      "_type" : "_doc",
      "_id" : "2",
      "_hop" : 0,
      "_attributes" : {
        "ip" : "192.168.0.1",
        "timestamp" : "2019-02-28T23:02:05.658"
      },
      "_source" : {
        "@timestamp" : "2019-02-28T23:02:05.658",
        "id" : "2",
        "ip" : "192.168.0.1",
        "path" : "/docs"
      }
    }, {
      "_index" : ".zentity-tutorial-index",
      "_type" : "_doc",
      "_id" : "4",
      "_hop" : 0,
      "_attributes" : {
        "ip" : "192.168.0.1",
        "timestamp" : "2019-02-28T23:02:12.024"
      },
      "_source" : {
        "@timestamp" : "2019-02-28T23:02:12.024",
        "id" : "4",
        "ip" : "192.168.0.1",
        "path" : "/docs/installation"
      }
    }, {
      "_index" : ".zentity-tutorial-index",
      "_type" : "_doc",
      "_id" : "6",
      "_hop" : 0,
      "_attributes" : {
        "ip" : "192.168.0.1",
        "timestamp" : "2019-02-28T23:02:15.628"
      },
      "_source" : {
        "@timestamp" : "2019-02-28T23:02:15.628",
        "id" : "6",
        "ip" : "192.168.0.1",
        "path" : "/releases"
      }
    }, {
      "_index" : ".zentity-tutorial-index",
      "_type" : "_doc",
      "_id" : "7",
      "_hop" : 0,
      "_attributes" : {
        "ip" : "192.168.0.1",
        "timestamp" : "2019-02-28T23:14:01.956"
      },
      "_source" : {
        "@timestamp" : "2019-02-28T23:14:01.956",
        "id" : "7",
        "ip" : "192.168.0.1",
        "path" : "/docs"
      }
    }, {
      "_index" : ".zentity-tutorial-index",
      "_type" : "_doc",
      "_id" : "9",
      "_hop" : 0,
      "_attributes" : {
        "ip" : "192.168.0.1",
        "timestamp" : "2019-02-28T23:14:08.921"
      },
      "_source" : {
        "@timestamp" : "2019-02-28T23:14:08.921",
        "id" : "9",
        "ip" : "192.168.0.1",
        "path" : "/docs/installation"
      }
    }, {
      "_index" : ".zentity-tutorial-index",
      "_type" : "_doc",
      "_id" : "12",
      "_hop" : 0,
      "_attributes" : {
        "ip" : "192.168.0.1",
        "timestamp" : "2019-02-28T23:28:11.114"
      },
      "_source" : {
        "@timestamp" : "2019-02-28T23:28:11.114",
        "id" : "12",
        "ip" : "192.168.0.1",
        "path" : "/docs/basic-usage"
      }
    }, {
      "_index" : ".zentity-tutorial-index",
      "_type" : "_doc",
      "_id" : "15",
      "_hop" : 0,
      "_attributes" : {
        "ip" : "192.168.0.1",
        "timestamp" : "2019-03-02T12:30:45.452"
      },
      "_source" : {
        "@timestamp" : "2019-03-02T12:30:45.452",
        "id" : "15",
        "ip" : "192.168.0.1",
        "path" : "/"
      }
    }, {
      "_index" : ".zentity-tutorial-index",
      "_type" : "_doc",
      "_id" : "16",
      "_hop" : 1,
      "_attributes" : {
        "ip" : "192.168.0.1",
        "timestamp" : "2019-03-03T14:32:01.837"
      },
      "_source" : {
        "@timestamp" : "2019-03-03T14:32:01.837",
        "id" : "16",
        "ip" : "192.168.0.1",
        "path" : "/"
      }
    }, {
      "_index" : ".zentity-tutorial-index",
      "_type" : "_doc",
      "_id" : "17",
      "_hop" : 1,
      "_attributes" : {
        "ip" : "192.168.0.1",
        "timestamp" : "2019-03-03T14:32:03.897"
      },
      "_source" : {
        "@timestamp" : "2019-03-03T14:32:03.897",
        "id" : "17",
        "ip" : "192.168.0.1",
        "path" : "/releases"
      }
    }, {
      "_index" : ".zentity-tutorial-index",
      "_type" : "_doc",
      "_id" : "18",
      "_hop" : 1,
      "_attributes" : {
        "ip" : "192.168.0.1",
        "timestamp" : "2019-03-03T12:33:56.553"
      },
      "_source" : {
        "@timestamp" : "2019-03-03T12:33:56.553",
        "id" : "18",
        "ip" : "192.168.0.1",
        "path" : "/docs"
      }
    } ]
  }
}
```

Expanding the time range allowed us to return four more documents that appeared
several days after the other documents.

What if we contracted the `"window"` parameter to a small value such as `"2m"`?
Let's find out.

```javascript
POST _zentity/resolution/zentity-tutorial-http-session?pretty
{
  "attributes": {
    "ip": [ "192.168.0.1" ],
    "timestamp": {
      "values": [ "2019-02-28T23:02:15.628" ],
      "params": {
        "window": "2d"
      }
    }
  }
}
```

The results will look like this:

```javascript
{
  "took" : 8,
  "hits" : {
    "total" : 4,
    "hits" : [ {
      "_index" : ".zentity-tutorial-index",
      "_type" : "_doc",
      "_id" : "1",
      "_hop" : 0,
      "_attributes" : {
        "ip" : "192.168.0.1",
        "timestamp" : "2019-02-28T23:01:45.248"
      },
      "_source" : {
        "@timestamp" : "2019-02-28T23:01:45.248",
        "id" : "1",
        "ip" : "192.168.0.1",
        "path" : "/"
      }
    }, {
      "_index" : ".zentity-tutorial-index",
      "_type" : "_doc",
      "_id" : "2",
      "_hop" : 1,
      "_attributes" : {
        "ip" : "192.168.0.1",
        "timestamp" : "2019-02-28T23:02:05.658"
      },
      "_source" : {
        "@timestamp" : "2019-02-28T23:02:05.658",
        "id" : "2",
        "ip" : "192.168.0.1",
        "path" : "/docs"
      }
    }, {
      "_index" : ".zentity-tutorial-index",
      "_type" : "_doc",
      "_id" : "4",
      "_hop" : 1,
      "_attributes" : {
        "ip" : "192.168.0.1",
        "timestamp" : "2019-02-28T23:02:12.024"
      },
      "_source" : {
        "@timestamp" : "2019-02-28T23:02:12.024",
        "id" : "4",
        "ip" : "192.168.0.1",
        "path" : "/docs/installation"
      }
    }, {
      "_index" : ".zentity-tutorial-index",
      "_type" : "_doc",
      "_id" : "6",
      "_hop" : 1,
      "_attributes" : {
        "ip" : "192.168.0.1",
        "timestamp" : "2019-02-28T23:02:15.628"
      },
      "_source" : {
        "@timestamp" : "2019-02-28T23:02:15.628",
        "id" : "6",
        "ip" : "192.168.0.1",
        "path" : "/releases"
      }
    } ]
  }
}
```

This returned four results over two hops. The first result matched one document
whose timestamp was within two minutes of our input, and the remaining documents
had timestamps that were within two minutes of the first result.


## <a name="conclusion"></a>Conclusion

You learned about date attributes and how to write a matcher that matches dates
within an arbitrary window of time.


&nbsp;

----

#### Continue Reading

|&#8249;|[Matcher Parameters](/docs/advanced-usage/matcher-parameters)|[Payload Attributes](/docs/advanced-usage/payload-attributes)|&#8250;|
|:---|:---|---:|---:|
|    |    |    |    |
