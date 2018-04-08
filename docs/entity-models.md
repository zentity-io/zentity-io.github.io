[Home](/#/) / [Documentation](/#/docs) / Entity Models


# Entity Models


zentity relies on objects called ***[entity models](/#/entity-models/specification)*** to control the execution of entity resolution jobs.

Entity models serve multiple purposes:

1. They define which attributes map to which fields of which Elasticsearch indices.
2. They define how to match an attribute for any index field it maps to.
3. They define which combinations of matching attributes imply a resolution.

Read the [entity model specification](/#/entity-models/specification) for specific details on the contents of entity models.


## Usage

You must provide an entity model when making a resolution request. You can provide it in two ways:

1. You can embed the entity model in the request under a field called `"model"`.
2. You can index the entity model using the [Models API](/#/docs/rest-apis/models-api) and reference it by its `entity_type`.

Option (2) gives you the ability to share, reuse, and build upon existing entity models. You can manage entity models
using the [Models API](REST-APIs#models-api). zentity stores entity models in an Elasticsearch index called `.zentity-models`.
Each document in this index represents the entity model for a distinct entity type. The entity type is listed in the
[`_id`](https://www.elastic.co/guide/en/elasticsearch/reference/current/mapping-id-field.html) field of the document.
There can be only one entity model for a given entity type. Once you have indexed an entity model, you can use it by
setting the `entity_type` parameter in your requests.

## More info

- [Specification](/#/docs/entity-models/specification)
- [Tips](/#/docs/entity-models/tips)


&nbsp;

----

#### Continue Reading

|&#8249;|[Basic Usage](/#/docs/basic-usage)|[Specification](/#/docs/entity-models/specification)|&#8250;|
|:---|:---|---:|---:|
|    |    |    |    |