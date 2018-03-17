[Home](/#/) / [Documentation](/#/docs) / [Entity Models](/#/docs/entity-models) / Usage


# Usage


You must provide an entity model when making a resolution request. You can provide it in two ways:

- Option 1. You can embed the entity model in the request under a field called `"model"`.
- Option 2. You can index the entity model using the [Models API](/#/docs/rest-apis/models-api) and reference it by its `entity_type`.

Option (2) gives you the ability to share, reuse, and build upon existing entity models. You can manage entity models
using the [Models API](REST-APIs#models-api). zentity stores entity models in an Elasticsearch index called `.zentity-models`.
Each document in this index represents the entity model for a distinct entity type. The entity type is listed in the
[`_id`](https://www.elastic.co/guide/en/elasticsearch/reference/current/mapping-id-field.html) field of the document.
There can be only one entity model for a given entity type. Once you have indexed an entity model, you can use it by
setting the `entity_type` parameter in your requests.


&nbsp;

----

#### Continue Reading

|&#8249;|[Entity Models](/#/docs/entity-models)|[Specification](/#/docs/entity-models/specification)|&#8250;|
|:---|:---|---:|---:|
|    |    |    |    |