[Home](/) / Releases


# <a name="releases">Releases</a>

[View on Github](https://github.com/zentity-io/zentity/releases)



<a name="latest"></a>
## <a name="zentity-1.0.3">zentity-1.0.3 (latest)</a>

### Download

Select the plugin version that matches your version of Elasticsearch:

- [Elasticsearch 6.7.0](https://zentity.io/releases/zentity-1.0.3-elasticsearch-6.7.0.zip)
- [Elasticsearch 6.6.2](https://zentity.io/releases/zentity-1.0.3-elasticsearch-6.6.2.zip)
- [Elasticsearch 6.6.1](https://zentity.io/releases/zentity-1.0.3-elasticsearch-6.6.1.zip)
- [Elasticsearch 6.6.0](https://zentity.io/releases/zentity-1.0.3-elasticsearch-6.6.0.zip)
- [Elasticsearch 6.5.4](https://zentity.io/releases/zentity-1.0.3-elasticsearch-6.5.4.zip)
- [Elasticsearch 6.5.3](https://zentity.io/releases/zentity-1.0.3-elasticsearch-6.5.3.zip)
- [Elasticsearch 6.5.2](https://zentity.io/releases/zentity-1.0.3-elasticsearch-6.5.2.zip)
- [Elasticsearch 6.5.1](https://zentity.io/releases/zentity-1.0.3-elasticsearch-6.5.1.zip)
- [Elasticsearch 6.5.0](https://zentity.io/releases/zentity-1.0.3-elasticsearch-6.5.0.zip)

### Release notes

- **Bug fix** - Fixed bug where model attribute params did not override matcher params.
([3e0728b](https://github.com/zentity-io/zentity/commit/3e0728ba4b9dca6b87b7dd72a257eb473d0c6eec))
- **Security** - Updated Jackson dependency to resolve security vulnerabilities CVE-2018-12022, CVE-2018-19360, CVE-2018-19361, CVE-2018-19362, CVE-2018-14721, CVE-2018-14718, CVE-2018-14719, CVE-2018-14720.
([1ad9127](https://github.com/zentity-io/zentity/commit/1ad9127996769423d72e44aba74d30091b1b6308))


## <a name="zentity-1.0.2">zentity-1.0.2</a>

### Download

Select the plugin version that matches your version of Elasticsearch:

- [Elasticsearch 6.7.0](https://zentity.io/releases/zentity-1.0.2-elasticsearch-6.7.0.zip)
- [Elasticsearch 6.6.2](https://zentity.io/releases/zentity-1.0.2-elasticsearch-6.6.2.zip)
- [Elasticsearch 6.6.1](https://zentity.io/releases/zentity-1.0.2-elasticsearch-6.6.1.zip)
- [Elasticsearch 6.6.0](https://zentity.io/releases/zentity-1.0.2-elasticsearch-6.6.0.zip)
- [Elasticsearch 6.5.4](https://zentity.io/releases/zentity-1.0.2-elasticsearch-6.5.4.zip)
- [Elasticsearch 6.5.3](https://zentity.io/releases/zentity-1.0.2-elasticsearch-6.5.3.zip)
- [Elasticsearch 6.5.2](https://zentity.io/releases/zentity-1.0.2-elasticsearch-6.5.2.zip)
- [Elasticsearch 6.5.1](https://zentity.io/releases/zentity-1.0.2-elasticsearch-6.5.1.zip)
- [Elasticsearch 6.5.0](https://zentity.io/releases/zentity-1.0.2-elasticsearch-6.5.0.zip)

### Release notes

- **Security** - Updated Jackson dependency to resolve security vulnerability CVE-2018-7489.
([214eee1](https://github.com/zentity-io/zentity/commit/214eee19a734047504a5bee3d6afa48632e06da4))


## <a name="zentity-1.0.1">zentity-1.0.1</a>

### Download

Select the plugin version that matches your version of Elasticsearch:

- [Elasticsearch 6.5.2](https://zentity.io/releases/zentity-1.0.1-elasticsearch-6.5.2.zip)
- [Elasticsearch 6.5.1](https://zentity.io/releases/zentity-1.0.1-elasticsearch-6.5.1.zip)
- [Elasticsearch 6.5.0](https://zentity.io/releases/zentity-1.0.1-elasticsearch-6.5.0.zip)

### Release notes

- Plugin now supports Elasticsearch 6.5.x, and compatibility with older versions of Elasticsearch
will no longer be maintained. Updated painless script for formatting dates.
([56b94b7](https://github.com/zentity-io/zentity/commit/56b94b7dfa53e3465b9a875fb45d0c2ec4580327))


## <a name="zentity-1.0.0">zentity-1.0.0</a>

### Download

Select the plugin version that matches your version of Elasticsearch:

- [Elasticsearch 6.2.4](https://zentity.io/releases/zentity-1.0.0-elasticsearch-6.2.4.zip)
- [Elasticsearch 6.2.3](https://zentity.io/releases/zentity-1.0.0-elasticsearch-6.2.3.zip)
- [Elasticsearch 6.2.2](https://zentity.io/releases/zentity-1.0.0-elasticsearch-6.2.2.zip)
- [Elasticsearch 6.2.1](https://zentity.io/releases/zentity-1.0.0-elasticsearch-6.2.1.zip)
- [Elasticsearch 6.2.0](https://zentity.io/releases/zentity-1.0.0-elasticsearch-6.2.0.zip)
- [Elasticsearch 6.1.3](https://zentity.io/releases/zentity-1.0.0-elasticsearch-6.1.3.zip)
- [Elasticsearch 6.1.2](https://zentity.io/releases/zentity-1.0.0-elasticsearch-6.1.2.zip)
- [Elasticsearch 6.1.1](https://zentity.io/releases/zentity-1.0.0-elasticsearch-6.1.1.zip)
- [Elasticsearch 6.0.1](https://zentity.io/releases/zentity-1.0.0-elasticsearch-6.0.1.zip)
- [Elasticsearch 6.0.0](https://zentity.io/releases/zentity-1.0.0-elasticsearch-6.0.0.zip)

### Release notes

- **Feature** - Added the `"ids"` field in the request payload of the [Resolution API](/docs/rest-apis/resolution-api).
This allows a job to be started by selecting document(s) by _id(s) known to be associated with an entity. Either or both
of the `"ids"` and `"attributes"` fields must be present and valid to start a job.
([b2f48bc](https://github.com/zentity-io/zentity/commit/b2f48bcd4db838bf5f7726b6756c9301b61c39d5))
- **Feature** - Added the `POST _zentity/_setup` endpoint to create the `.zentity-models` index. This allows an
administrator to set up the index in advance without having to give users permission to create or manage the index when
using X-Pack Security. And it allows the number of shards and replicas to be defined as URI parameters.
([79a00e3](https://github.com/zentity-io/zentity/commit/79a00e36ffe486e8d34af769edf8d2c70de4a3da))
- **Bug fix** - Fixed a NullPointerException whenever an `entity_type` does not exist when submitting a resolution job.
([b5b6d88](https://github.com/zentity-io/zentity/commit/b5b6d88007537323e12d6ec6a50654bdee85f0d9))


## <a name="zentity-0.5.0-beta.2">zentity-0.5.0-beta.2</a>

### Download

Select the plugin version that matches your version of Elasticsearch:

- [Elasticsearch 6.2.4](https://zentity.io/releases/zentity-0.5.0-beta.2-elasticsearch-6.2.4.zip)
- [Elasticsearch 6.2.3](https://zentity.io/releases/zentity-0.5.0-beta.2-elasticsearch-6.2.3.zip)
- [Elasticsearch 6.2.2](https://zentity.io/releases/zentity-0.5.0-beta.2-elasticsearch-6.2.2.zip)
- [Elasticsearch 6.2.1](https://zentity.io/releases/zentity-0.5.0-beta.2-elasticsearch-6.2.1.zip)
- [Elasticsearch 6.2.0](https://zentity.io/releases/zentity-0.5.0-beta.2-elasticsearch-6.2.0.zip)
- [Elasticsearch 6.1.3](https://zentity.io/releases/zentity-0.5.0-beta.2-elasticsearch-6.1.3.zip)
- [Elasticsearch 6.1.2](https://zentity.io/releases/zentity-0.5.0-beta.2-elasticsearch-6.1.2.zip)
- [Elasticsearch 6.1.1](https://zentity.io/releases/zentity-0.5.0-beta.2-elasticsearch-6.1.1.zip)
- [Elasticsearch 6.0.1](https://zentity.io/releases/zentity-0.5.0-beta.2-elasticsearch-6.0.1.zip)
- [Elasticsearch 6.0.0](https://zentity.io/releases/zentity-0.5.0-beta.2-elasticsearch-6.0.0.zip)

### Release notes

- **Bug fix** - Removed a log statement that was printing the contents of each query and slowing
down resolution jobs.
([b421fc5](https://github.com/zentity-io/zentity/commit/b421fc5033cebae2979bee56fca6972ce72a3751))


## <a name="zentity-0.5.0-beta.1">zentity-0.5.0-beta.1</a>

### Download

Select the plugin version that matches your version of Elasticsearch:

- [Elasticsearch 6.2.4](https://zentity.io/releases/zentity-0.5.0-beta.1-elasticsearch-6.2.4.zip)
- [Elasticsearch 6.2.3](https://zentity.io/releases/zentity-0.5.0-beta.1-elasticsearch-6.2.3.zip)
- [Elasticsearch 6.2.2](https://zentity.io/releases/zentity-0.5.0-beta.1-elasticsearch-6.2.2.zip)
- [Elasticsearch 6.2.1](https://zentity.io/releases/zentity-0.5.0-beta.1-elasticsearch-6.2.1.zip)
- [Elasticsearch 6.2.0](https://zentity.io/releases/zentity-0.5.0-beta.1-elasticsearch-6.2.0.zip)
- [Elasticsearch 6.1.3](https://zentity.io/releases/zentity-0.5.0-beta.1-elasticsearch-6.1.3.zip)
- [Elasticsearch 6.1.2](https://zentity.io/releases/zentity-0.5.0-beta.1-elasticsearch-6.1.2.zip)
- [Elasticsearch 6.1.1](https://zentity.io/releases/zentity-0.5.0-beta.1-elasticsearch-6.1.1.zip)
- [Elasticsearch 6.0.1](https://zentity.io/releases/zentity-0.5.0-beta.1-elasticsearch-6.0.1.zip)
- [Elasticsearch 6.0.0](https://zentity.io/releases/zentity-0.5.0-beta.1-elasticsearch-6.0.0.zip)

### Release notes

- **Feature** - Arbitrary params can be passed to the matchers clauses as variables,
using the syntax `{{ params.<param_value> }}` (example: `{{ params.fuzziness }}`).
Default params can be specified in `"matchers".MATCHER_NAME."params"` and overridden
in `"attributes".ATTRIBUTE_NAME."params"` in either the model or the input.
([b2bdb09](https://github.com/zentity-io/zentity/commit/b2bdb091428df5fa736883758ce2c289d68730b8))

- **Feature** - Added the `"date"` attribute type which requires a `"format"` param
to be specified. Date values are queried and returned in the specified format.
([325b98c](https://github.com/zentity-io/zentity/commit/325b98c5634ad63044af9160f679fb3acb9921f2))

- **Breaking change** - Input attribute values must always be specified in arrays.
For example, `{ "attributes": { "id": "123" }}` would need to be changed to
`{ "attributes": { "id": [ "123" ] }}`.
([b2bdb09](https://github.com/zentity-io/zentity/commit/b2bdb091428df5fa736883758ce2c289d68730b8))

- **Breaking change** - Deprecated the `"matchers".MATCHER_NAME."type"` field.
Matcher types will not be necessary given the ability to pass arbitrary params
into the matcher clauses. Any existing models with this field will need to be
updated to have this field removed.
([b2bdb09](https://github.com/zentity-io/zentity/commit/b2bdb091428df5fa736883758ce2c289d68730b8))

- **Breaking change** - Deprecated the `"entity_id"` field of the request payload for the
[Resolution API](/docs/rest-apis/resolution-api). If an `entity_id` is to be specified,
it must always be done in the path of the Resolution API endpoint (`_zentity/resolution/<entity_type>`).
Any clients that are specifying the `entity_id` in the request payload will need to be changed
to use this endpoint instead.
([b2bdb09](https://github.com/zentity-io/zentity/commit/b2bdb091428df5fa736883758ce2c289d68730b8))


## <a name="zentity-0.4.0-beta.1">zentity-0.4.0-beta.1</a>

### Download

Select the plugin version that matches your version of Elasticsearch:

- [Elasticsearch 6.2.4](https://zentity.io/releases/zentity-0.4.0-beta.1-elasticsearch-6.2.4.zip)
- [Elasticsearch 6.2.3](https://zentity.io/releases/zentity-0.4.0-beta.1-elasticsearch-6.2.3.zip)
- [Elasticsearch 6.2.2](https://zentity.io/releases/zentity-0.4.0-beta.1-elasticsearch-6.2.2.zip)
- [Elasticsearch 6.2.1](https://zentity.io/releases/zentity-0.4.0-beta.1-elasticsearch-6.2.1.zip)
- [Elasticsearch 6.2.0](https://zentity.io/releases/zentity-0.4.0-beta.1-elasticsearch-6.2.0.zip)
- [Elasticsearch 6.1.3](https://zentity.io/releases/zentity-0.4.0-beta.1-elasticsearch-6.1.3.zip)
- [Elasticsearch 6.1.2](https://zentity.io/releases/zentity-0.4.0-beta.1-elasticsearch-6.1.2.zip)
- [Elasticsearch 6.1.1](https://zentity.io/releases/zentity-0.4.0-beta.1-elasticsearch-6.1.1.zip)
- [Elasticsearch 6.0.1](https://zentity.io/releases/zentity-0.4.0-beta.1-elasticsearch-6.0.1.zip)
- [Elasticsearch 6.0.0](https://zentity.io/releases/zentity-0.4.0-beta.1-elasticsearch-6.0.0.zip)

### Release notes

- **Feature** - Resolution jobs now support exclusive and inclusive scoping
(i.e. blacklisting and whitelisting) based on attributes, resolvers, and indices.
Exclusive scoping takes precedence over inclusive scoping.
([28fcea5](https://github.com/zentity-io/zentity/commit/28fcea56c2b85d9706b975f02d59c39be3d9164b))
New parameters include:
    - `scope.exclude.attributes`
    - `scope.exclude.indices`
    - `scope.exclude.resolvers`
    - `scope.include.attributes`
    - `scope.include.indices`
    - `scope.include.resolvers`

- **Breaking change** - The `scope.indices` and `scope.resolvers` parameters
of the [Resolution API](/docs/rest-apis/resolution-api) have been replaced
with `scope.exclude` and `scope.include`.
([28fcea5](https://github.com/zentity-io/zentity/commit/28fcea56c2b85d9706b975f02d59c39be3d9164b))


## <a name="zentity-0.3.0-beta.1">zentity-0.3.0-beta.1</a>

### Download

Select the plugin version that matches your version of Elasticsearch:

- [Elasticsearch 6.2.3](https://zentity.io/releases/zentity-0.3.0-beta.1-elasticsearch-6.2.3.zip)
- [Elasticsearch 6.2.2](https://zentity.io/releases/zentity-0.3.0-beta.1-elasticsearch-6.2.2.zip)
- [Elasticsearch 6.2.1](https://zentity.io/releases/zentity-0.3.0-beta.1-elasticsearch-6.2.1.zip)
- [Elasticsearch 6.2.0](https://zentity.io/releases/zentity-0.3.0-beta.1-elasticsearch-6.2.0.zip)
- [Elasticsearch 6.1.3](https://zentity.io/releases/zentity-0.3.0-beta.1-elasticsearch-6.1.3.zip)
- [Elasticsearch 6.1.2](https://zentity.io/releases/zentity-0.3.0-beta.1-elasticsearch-6.1.2.zip)
- [Elasticsearch 6.1.1](https://zentity.io/releases/zentity-0.3.0-beta.1-elasticsearch-6.1.1.zip)
- [Elasticsearch 6.0.1](https://zentity.io/releases/zentity-0.3.0-beta.1-elasticsearch-6.0.1.zip)
- [Elasticsearch 6.0.0](https://zentity.io/releases/zentity-0.3.0-beta.1-elasticsearch-6.0.0.zip)

### Release notes

- **Feature** - Queries with multiple resolvers now nest the clauses for each
attribute as a tree instead of a flat list of lists, eliminating redundant
clauses. For example, a query with two resolvers `[ "name", "email" ]` and
`[ "name", "phone" ]` will nest the `"email"` and `"phone"` clauses under the
`"name"` clause instead of duplicating the `"name"` clause.
([f425f4f](https://github.com/zentity-io/zentity/commit/f425f4f4c77a4b734923cbbeb418cca42e928957))

- **Feature** - The `queries` parameter of the [Resolution API](/docs/rest-apis/resolution-api)
now include `"_hop"`, `"_index"`, and `"resolvers"` for each query. The
`"resolvers"` field lists the names of the resolvers used in the query
(`"resolvers.list"`) and the nested structure of the attribute clauses
(`"resolvers.tree"`).
([f425f4f](https://github.com/zentity-io/zentity/commit/f425f4f4c77a4b734923cbbeb418cca42e928957))

- **Breaking change** - The `queries` parameter of the [Resolution API](/docs/rest-apis/resolution-api)
has moved the `"request"` and `"response"` fields of each query under a field
called `"search"`.
([f425f4f](https://github.com/zentity-io/zentity/commit/f425f4f4c77a4b734923cbbeb418cca42e928957))


## <a name="zentity-0.2.1-beta.1">zentity-0.2.1-beta.1</a>

### Download

Select the plugin version that matches your version of Elasticsearch:

- [Elasticsearch 6.2.3](https://zentity.io/releases/zentity-0.2.1-beta.1-elasticsearch-6.2.3.zip)
- [Elasticsearch 6.2.2](https://zentity.io/releases/zentity-0.2.1-beta.1-elasticsearch-6.2.2.zip)
- [Elasticsearch 6.2.1](https://zentity.io/releases/zentity-0.2.1-beta.1-elasticsearch-6.2.1.zip)
- [Elasticsearch 6.2.0](https://zentity.io/releases/zentity-0.2.1-beta.1-elasticsearch-6.2.0.zip)
- [Elasticsearch 6.1.3](https://zentity.io/releases/zentity-0.2.1-beta.1-elasticsearch-6.1.3.zip)
- [Elasticsearch 6.1.2](https://zentity.io/releases/zentity-0.2.1-beta.1-elasticsearch-6.1.2.zip)
- [Elasticsearch 6.1.1](https://zentity.io/releases/zentity-0.2.1-beta.1-elasticsearch-6.1.1.zip)
- [Elasticsearch 6.0.1](https://zentity.io/releases/zentity-0.2.1-beta.1-elasticsearch-6.0.1.zip)
- [Elasticsearch 6.0.0](https://zentity.io/releases/zentity-0.2.1-beta.1-elasticsearch-6.0.0.zip)

### Release notes

- **Feature** - Index fields with nested properties of arbitrary depth
(e.g. `"person.name.first.keyword"`) are now supported.
([75d4fb8](https://github.com/zentity-io/zentity/commit/75d4fb878101c327c8f8424ae87d6180ba956fdc))

- **Bug fix** - Fixed two NullPointerExceptions by skipping cases where the
attribute or matcher of an index field do not exist in the entity model.
([75d4fb8](https://github.com/zentity-io/zentity/commit/75d4fb878101c327c8f8424ae87d6180ba956fdc))


## <a name="zentity-0.2.0-beta.1">zentity-0.2.0-beta.1</a>

### Download

Select the plugin version that matches your version of Elasticsearch:

- [Elasticsearch 6.2.3](https://zentity.io/releases/zentity-0.2.0-beta.1-elasticsearch-6.2.3.zip)
- [Elasticsearch 6.2.2](https://zentity.io/releases/zentity-0.2.0-beta.1-elasticsearch-6.2.2.zip)
- [Elasticsearch 6.2.1](https://zentity.io/releases/zentity-0.2.0-beta.1-elasticsearch-6.2.1.zip)
- [Elasticsearch 6.2.0](https://zentity.io/releases/zentity-0.2.0-beta.1-elasticsearch-6.2.0.zip)
- [Elasticsearch 6.1.3](https://zentity.io/releases/zentity-0.2.0-beta.1-elasticsearch-6.1.3.zip)
- [Elasticsearch 6.1.2](https://zentity.io/releases/zentity-0.2.0-beta.1-elasticsearch-6.1.2.zip)
- [Elasticsearch 6.1.1](https://zentity.io/releases/zentity-0.2.0-beta.1-elasticsearch-6.1.1.zip)
- [Elasticsearch 6.0.1](https://zentity.io/releases/zentity-0.2.0-beta.1-elasticsearch-6.0.1.zip)
- [Elasticsearch 6.0.0](https://zentity.io/releases/zentity-0.2.0-beta.1-elasticsearch-6.0.0.zip)

### Release notes

- **Feature** - Overhauled the [entity model specification](/docs/entity-models/specification)
to allow new features to be added to it without causing breaking changes.
Decoupled `"attributes"` and `"matchers"`. The `"indices"` object now maps index
`"fields"` to an `"attribute"` and a `"matcher"`.
([5b28a26](https://github.com/zentity-io/zentity/commit/5b28a26807785d12ab52e2b825d3efd05aa3437a))

- **Feature** - Introduced the concept of attribute types. Added the `"string"`,
`"number"`, and `"boolean"` attribute types.
([19f7047](https://github.com/zentity-io/zentity/commit/19f70472ab574bd006e75e9588d02e05026f7c22))

- **Feature** - Introduced the concept of matcher types. Added the `"value"`
matcher type.
([19f7047](https://github.com/zentity-io/zentity/commit/19f70472ab574bd006e75e9588d02e05026f7c22)) 

- **Bug fix** - Returning the values of attributes in the `"_attributes"` field
as they existed in the `"_source"` field instead of trying to manually convert
their data types.
([19f7047](https://github.com/zentity-io/zentity/commit/19f70472ab574bd006e75e9588d02e05026f7c22))

- **Breaking change** - Entity models must be recreated to conform to the new
[entity model specification](/docs/entity-models/specification).
([5b28a26](https://github.com/zentity-io/zentity/commit/5b28a26807785d12ab52e2b825d3efd05aa3437a))


## <a name="zentity-0.1.1-beta.2">zentity-0.1.1-beta.2</a>

### Download

Select the plugin version that matches your version of Elasticsearch:

- [Elasticsearch 6.2.3](https://zentity.io/releases/zentity-0.1.1-beta.2-elasticsearch-6.2.3.zip)
- [Elasticsearch 6.2.2](https://zentity.io/releases/zentity-0.1.1-beta.2-elasticsearch-6.2.2.zip)
- [Elasticsearch 6.2.1](https://zentity.io/releases/zentity-0.1.1-beta.2-elasticsearch-6.2.1.zip)
- [Elasticsearch 6.2.0](https://zentity.io/releases/zentity-0.1.1-beta.2-elasticsearch-6.2.0.zip)
- [Elasticsearch 6.1.3](https://zentity.io/releases/zentity-0.1.1-beta.2-elasticsearch-6.1.3.zip)
- [Elasticsearch 6.1.2](https://zentity.io/releases/zentity-0.1.1-beta.2-elasticsearch-6.1.2.zip)
- [Elasticsearch 6.1.1](https://zentity.io/releases/zentity-0.1.1-beta.2-elasticsearch-6.1.1.zip)
- [Elasticsearch 6.0.1](https://zentity.io/releases/zentity-0.1.1-beta.2-elasticsearch-6.0.1.zip)
- [Elasticsearch 6.0.0](https://zentity.io/releases/zentity-0.1.1-beta.2-elasticsearch-6.0.0.zip)

### Release notes

- **Bug fix** - Renamed `max_docs_per_hop` to `max_docs_per_query` in the
[Resolution API](/docs/rest-apis/resolution-api).
([6cde2ef](https://github.com/zentity-io/zentity/commit/6cde2ef4574e612a0be32b3d9287775f1c7f2458))

- **Breaking change** - Any requests using the `max_docs_per_hop` parameter
must replace it with `max_docs_per_query`.
([6cde2ef](https://github.com/zentity-io/zentity/commit/6cde2ef4574e612a0be32b3d9287775f1c7f2458))


## <a name="zentity-0.1.1-beta.1">zentity-0.1.1-beta.1</a>

### Download

Select the plugin version that matches your version of Elasticsearch:

- [Elasticsearch 6.2.3](https://zentity.io/releases/zentity-0.1.1-beta.1-elasticsearch-6.2.3.zip)
- [Elasticsearch 6.2.2](https://zentity.io/releases/zentity-0.1.1-beta.1-elasticsearch-6.2.2.zip)
- [Elasticsearch 6.2.1](https://zentity.io/releases/zentity-0.1.1-beta.1-elasticsearch-6.2.1.zip)
- [Elasticsearch 6.2.0](https://zentity.io/releases/zentity-0.1.1-beta.1-elasticsearch-6.2.0.zip)
- [Elasticsearch 6.1.3](https://zentity.io/releases/zentity-0.1.1-beta.1-elasticsearch-6.1.3.zip)
- [Elasticsearch 6.1.2](https://zentity.io/releases/zentity-0.1.1-beta.1-elasticsearch-6.1.2.zip)
- [Elasticsearch 6.1.1](https://zentity.io/releases/zentity-0.1.1-beta.1-elasticsearch-6.1.1.zip)
- [Elasticsearch 6.0.1](https://zentity.io/releases/zentity-0.1.1-beta.1-elasticsearch-6.0.1.zip)
- [Elasticsearch 6.0.0](https://zentity.io/releases/zentity-0.1.1-beta.1-elasticsearch-6.0.0.zip)

### Release notes

Initial release.