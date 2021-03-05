[Home](/) / [Documentation](/docs) / [REST APIs](/docs/rest-apis) / Models API


# <a name="models-api"></a>Models API


The Models API is a set of endpoints to create, retrieve, update, and delete
entity models.

- [Get all entity models](#get-entity-models)
- [Get an entity model](#get-entity-model)
- [Create an entity model](#create-entity-model)
- [Update an entity model](#update-entity-model)
- [Delete an entity model](#delete-entity-model)


## <a name="get-entity-models"></a>Get all entity models

Returns all entity models from the `.zentity-models` index.

```javascript
GET _zentity/models
```


### HTTP Headers

|Header|Value|
|------|-----|
|`Content-Type`|`application/json`|

### URL Parameters

|Parameter|Type|Default|Required|Description|
|---------|----|-------|--------|-----------|
|`pretty`|Boolean|`false`|No|Indents the JSON response data.|


## <a name="get-entity-model"></a>Get an entity model

Returns the entity model for a given `entity_type` from the `.zentity-models`
index.

```javascript
GET _zentity/models/{entity_type}
```


### HTTP Headers

|Header|Value|
|------|-----|
|`Content-Type`|`application/json`|


### URL Parameters

|Parameter|Type|Default|Required|Description|
|---------|----|-------|--------|-----------|
|`entity_type`|String| |Yes|Entity type.|
|`pretty`|Boolean|`false`|No|Indents the JSON response data.|


## <a name="create-entity-model"></a>Create an entity model

Creates an entity model for a given `entity_type` and puts it in the
`.zentity-models` index. Returns an error if an entity model already exists for
that `entity_type`.

For more details about the contents of the payload, read the
[entity model specification](/docs/entity-models/specification).

```javascript
POST _zentity/models/{entity_type}
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


### HTTP Headers

|Header|Value|
|------|-----|
|`Content-Type`|`application/json`|


### URL Parameters

|Parameter|Type|Default|Required|Description|
|---------|----|-------|--------|-----------|
|`entity_type`|String| |Yes|Entity type.|
|`pretty`|Boolean|`false`|No|Indents the JSON response data.|


## <a name="update-entity-model"></a>Update an entity model

Updates an entity model for a given `entity_type`.
Creates the entity model if it does not already exist.

For more details about the contents of the payload, read the
[entity model specification](/docs/entity-models/specification).

```javascript
PUT _zentity/models/{entity_type}
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


### HTTP Headers

|Header|Value|
|------|-----|
|`Content-Type`|`application/json`|


### URL Parameters

|Parameter|Type|Default|Required|Description|
|---------|----|-------|--------|-----------|
|`entity_type`|String| |Yes|Entity type.|
|`pretty`|Boolean|`false`|No|Indents the JSON response data.|


## <a name="delete-entity-model"></a>Delete an entity model

Deletes the entity model for a given `entity_type` from the `.zentity-models`
index.

```javascript
DELETE _zentity/models/{entity_type}
```

### URL Parameters

|Parameter|Type|Default|Required|Description|
|---------|----|-------|--------|-----------|
|`entity_type`|String| |Yes|Entity type.|
|`pretty`|Boolean|`false`|No|Indents the JSON response data.|


&nbsp;

----

#### Continue Reading

|&#8249;|[Setup API](/docs/rest-apis/setup-api)|[Bulk Models API](/docs/rest-apis/bulk-models-api)|&#8250;|
|:---|:---|---:|---:|
|    |    |    |    |
