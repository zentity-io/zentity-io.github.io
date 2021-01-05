[Home](/) / [Documentation](/docs) / [Advanced Usage](/docs/advanced-usage) / Payload Attributes


#### <a name="contents"></a>Advanced Usage Tutorials 📖

This tutorial is part of a series to help you learn and perform the advanced
functions of zentity. You should complete the [basic usage](/docs/basic-usage)
tutorials before completing these advanced usage tutorials.

1. [Scoring Resolution](/docs/advanced-usage/scoring-resolution)
2. [Matcher Parameters](/docs/advanced-usage/matcher-parameters)
3. [Date Attributes](/docs/advanced-usage/date-attributes)
4. **Payload Attributes** *&#8592; You are here.*

---


# <a name="payload-attributes"></a>Payload Attributes

Payload attributes are data elements that don't represent the entity that you
resolve, but are worth retrieving when you resolve the entity. They are not used
in matching, but they relate to the entity nonetheless. Think of payload
attributes as data that you join to the entity, so that you can analyze
information that relates to the entity.

For example, let's say you have two indices with purchase order receipts, where
each document has details about the customer, the product, and the amount paid.
You might want to resolve a customer or a product from the two indices. You
might also want to retrieve information about the amount paid so that you can
calculate its sum. "Amount paid" is not an attribute of the customer or the
product. But you can return the amount paid simply by defining it as an
attribute.

There is no distinct concept of a payload attribute in zentity. Attributes will
automatically function as payloads if you don't define a [`"matcher"`](/docs/entity-models/specification#indices.INDEX_NAME.fields.INDEX_FIELD_NAME.matcher)
for the field associated with that attribute in the [`"indices"`](/docs/entity-models/specification#indices)
object of the entity model. Without a matcher, the attribute will not be used
for matching. But if two records are matched with other attributes in the index,
then the attributes without matchers will be returned with the result as payload
attributes.


&nbsp;

----

#### Continue Reading

|&#8249;|[Date Attributes](/docs/advanced-usage/date-attributes)|[Entity Models](/docs/entity-models)|&#8250;|
|:---|:---|---:|---:|
|    |    |    |    |
