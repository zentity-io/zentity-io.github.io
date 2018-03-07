[Home](/#/) / [Documentation](/#/docs) / [REST APIs](/#/docs/rest-apis) / Models API


# Models API


## Get all entity models

```javascript
GET _zentity/models
```

Returns all entity models from the `.zentity-models` index.

**URL Params:**

|Param|Type|Default|Required|Description|
|-----|----|-------|--------|-----------|
|`pretty`|Boolean|`false`|No|Indents the JSON response data.|


## Get an entity model

```javascript
GET _zentity/models/{entity_type}
```

Returns the entity model for a given `entity_type` from the `.zentity-models` index.

**URL Params:**

|Param|Type|Default|Required|Description|
|-----|----|-------|--------|-----------|
|`entity_type`|String| |Yes|Entity type.|
|`pretty`|Boolean|`false`|No|Indents the JSON response data.|


## Create an entity model

Creates an entity model for a given `entity_type` and puts it in the `.zentity-models` index.
Returns an error if an entity model already exists for that `entity_type`.

```javascript
POST _zentity/models/{entity_type}
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

**URL Params:**

|Param|Type|Default|Required|Description|
|-----|----|-------|--------|-----------|
|`entity_type`|String| |Yes|Entity type.|
|`pretty`|Boolean|`false`|No|Indents the JSON response data.|


## Update an entity model

Updates an entity model for a given `entity_type`.
Creates the entity model if it does not already exist.

```javascript
PUT _zentity/models/{entity_type}
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

**URL Params:**

|Param|Type|Default|Required|Description|
|-----|----|-------|--------|-----------|
|`entity_type`|String| |Yes|Entity type.|
|`pretty`|Boolean|`false`|No|Indents the JSON response data.|


## Delete an entity model

Deletes the entity model for a given `entity_type` from the `.zentity-models` index.

```javascript
DELETE _zentity/models/{entity_type}
```

**URL Params:**

|Param|Type|Default|Required|Description|
|-----|----|-------|--------|-----------|
|`entity_type`|String| |Yes|Entity type.|
|`pretty`|Boolean|`false`|No|Indents the JSON response data.|
