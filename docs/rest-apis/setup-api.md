[Home](/) / [Documentation](/docs) / [REST APIs](/docs/rest-apis) / Setup API


# <a name="setup-api"></a>Setup API

Creates the `.zentity-models` index.

The request accepts one endpoint:

```javascript
POST _zentity/_setup
```

**URL query string parameters**

|Param|Type|Default|Required|Description|
|-----|----|-------|--------|-----------|
|`number_of_shards`|Integer|1|No|Define the number of primary shards for the index.|
|`number_of_replicas`|Integer|1|No|Define the number of replica shards for the index.|


&nbsp;

----

#### Continue Reading

|&#8249;|[REST APIs](/docs/rest-apis)|[Models API](/docs/rest-apis/models-api)|&#8250;|
|:---|:---|---:|---:|
|    |    |    |    |