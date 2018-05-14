[Home](/) / [Documentation](/docs) / [REST APIs](/docs/rest-apis) / Models API


# <a name="models-api">Models API</a>


## <a name="get-entity-models">Get all entity models</a>

```javascript
GET _zentity/models
```

Returns all entity models from the `.zentity-models` index.

**URL Params:**

|Param|Type|Default|Required|Description|
|-----|----|-------|--------|-----------|
|`pretty`|Boolean|`false`|No|Indents the JSON response data.|


## <a name="get-entity-model">Get an entity model</a>

```javascript
GET _zentity/models/{entity_type}
```

Returns the entity model for a given `entity_type` from the `.zentity-models` index.

**URL Params:**

|Param|Type|Default|Required|Description|
|-----|----|-------|--------|-----------|
|`entity_type`|String| |Yes|Entity type.|
|`pretty`|Boolean|`false`|No|Indents the JSON response data.|


## <a name="create-entity-model">Create an entity model</a>

Creates an entity model for a given `entity_type` and puts it in the `.zentity-models` index.
Returns an error if an entity model already exists for that `entity_type`.

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

**URL Params:**

|Param|Type|Default|Required|Description|
|-----|----|-------|--------|-----------|
|`entity_type`|String| |Yes|Entity type.|
|`pretty`|Boolean|`false`|No|Indents the JSON response data.|


## <a name="update-entity-model">Update an entity model</a>

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

**URL Params:**

|Param|Type|Default|Required|Description|
|-----|----|-------|--------|-----------|
|`entity_type`|String| |Yes|Entity type.|
|`pretty`|Boolean|`false`|No|Indents the JSON response data.|


## <a name="delete-entity-model">Delete an entity model</a>

Deletes the entity model for a given `entity_type` from the `.zentity-models` index.

```javascript
DELETE _zentity/models/{entity_type}
```

**URL Params:**

|Param|Type|Default|Required|Description|
|-----|----|-------|--------|-----------|
|`entity_type`|String| |Yes|Entity type.|
|`pretty`|Boolean|`false`|No|Indents the JSON response data.|


&nbsp;

----

#### Continue Reading

|&#8249;|[Resolution API](/docs/rest-apis/resolution-api)|[Security](/docs/security)|&#8250;|
|:---|:---|---:|---:|
|    |    |    |    |
