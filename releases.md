[Home](/) / Releases


# <a name="releases">Releases</a>

[View on Github](https://github.com/zentity-io/zentity/releases)


<a name="latest"></a>
## <a name="zentity-1.6.2">zentity-1.6.2 (latest)</a>

### Download

Select the plugin version that matches your version of Elasticsearch:

- [Elasticsearch 7.10.2](https://zentity.io/releases/zentity-1.6.2-elasticsearch-7.10.2.zip)
- [Elasticsearch 7.10.1](https://zentity.io/releases/zentity-1.6.2-elasticsearch-7.10.1.zip)
- [Elasticsearch 7.10.0](https://zentity.io/releases/zentity-1.6.2-elasticsearch-7.10.0.zip)
- [Elasticsearch 7.9.3](https://zentity.io/releases/zentity-1.6.2-elasticsearch-7.9.3.zip)
- [Elasticsearch 7.9.2](https://zentity.io/releases/zentity-1.6.2-elasticsearch-7.9.2.zip)
- [Elasticsearch 7.9.1](https://zentity.io/releases/zentity-1.6.2-elasticsearch-7.9.1.zip)
- [Elasticsearch 7.9.0](https://zentity.io/releases/zentity-1.6.2-elasticsearch-7.9.0.zip)
- [Elasticsearch 7.8.1](https://zentity.io/releases/zentity-1.6.2-elasticsearch-7.8.1.zip)
- [Elasticsearch 7.8.0](https://zentity.io/releases/zentity-1.6.2-elasticsearch-7.8.0.zip)
- [Elasticsearch 7.7.1](https://zentity.io/releases/zentity-1.6.2-elasticsearch-7.7.1.zip)
- [Elasticsearch 7.7.0](https://zentity.io/releases/zentity-1.6.2-elasticsearch-7.7.0.zip)

### Release notes

- **Bug fix** - Fixed an issue that affected the stability of clusters with
multiple nodes using Elasticsearch versions >= 7.9.0.
([Issue #56](https://github.com/zentity-io/zentity/issues/56))


## <a name="zentity-1.6.1">zentity-1.6.1</a>

### Download

Select the plugin version that matches your version of Elasticsearch:

> Note: There is an issue in zentity 1.6.1 that affects the stability of
> clusters with multiple nodes using Elasticsearch versions >= 7.9.0. It is
> strongly recommended to upgrade zentity.

- [Elasticsearch 7.10.2](https://zentity.io/releases/zentity-1.6.1-elasticsearch-7.10.2.zip)
- [Elasticsearch 7.10.1](https://zentity.io/releases/zentity-1.6.1-elasticsearch-7.10.1.zip)
- [Elasticsearch 7.10.0](https://zentity.io/releases/zentity-1.6.1-elasticsearch-7.10.0.zip)
- [Elasticsearch 7.9.3](https://zentity.io/releases/zentity-1.6.1-elasticsearch-7.9.3.zip)
- [Elasticsearch 7.9.2](https://zentity.io/releases/zentity-1.6.1-elasticsearch-7.9.2.zip)
- [Elasticsearch 7.9.1](https://zentity.io/releases/zentity-1.6.1-elasticsearch-7.9.1.zip)
- [Elasticsearch 7.9.0](https://zentity.io/releases/zentity-1.6.1-elasticsearch-7.9.0.zip)
- [Elasticsearch 7.8.1](https://zentity.io/releases/zentity-1.6.1-elasticsearch-7.8.1.zip)
- [Elasticsearch 7.8.0](https://zentity.io/releases/zentity-1.6.1-elasticsearch-7.8.0.zip)
- [Elasticsearch 7.7.1](https://zentity.io/releases/zentity-1.6.1-elasticsearch-7.7.1.zip)
- [Elasticsearch 7.7.0](https://zentity.io/releases/zentity-1.6.1-elasticsearch-7.7.0.zip)

### Release notes

- **Security** - Updated Jackson dependency to resolve security vulnerability
CVE-2020-14062.
([44b908c](https://github.com/zentity-io/zentity/commit/44b908c89ea32386eb086b3cf86aaa8b05aa0b07))

- **Other** - Compatibility with Elasticsearch versions prior to 7.7.0 will no
longer be maintained due to changes in the Elasticsearch Java API.
([44b908c](https://github.com/zentity-io/zentity/commit/44b908c89ea32386eb086b3cf86aaa8b05aa0b07))


## <a name="zentity-1.6.0">zentity-1.6.0</a>

### Download

Select the plugin version that matches your version of Elasticsearch:

- [Elasticsearch 7.6.1](https://zentity.io/releases/zentity-1.6.0-elasticsearch-7.6.1.zip)
- [Elasticsearch 7.6.0](https://zentity.io/releases/zentity-1.6.0-elasticsearch-7.6.0.zip)
- [Elasticsearch 7.5.2](https://zentity.io/releases/zentity-1.6.0-elasticsearch-7.5.2.zip)
- [Elasticsearch 7.5.1](https://zentity.io/releases/zentity-1.6.0-elasticsearch-7.5.1.zip)
- [Elasticsearch 7.5.0](https://zentity.io/releases/zentity-1.6.0-elasticsearch-7.5.0.zip)
- [Elasticsearch 7.4.2](https://zentity.io/releases/zentity-1.6.0-elasticsearch-7.4.2.zip)
- [Elasticsearch 7.4.1](https://zentity.io/releases/zentity-1.6.0-elasticsearch-7.4.1.zip)
- [Elasticsearch 7.4.0](https://zentity.io/releases/zentity-1.6.0-elasticsearch-7.4.0.zip)

### Release notes

- **Feature** - This release introduces identity confidence scoring to the [Resolution API](/docs/rest-apis/resolution-api).
Added the [attribute identity confidence base score](/docs/entity-models/specification/#attributes.ATTRIBUTE_NAME.score),
[matcher quality score](/docs/entity-models/specification/#matchers.MATCHER_NAME.quality),
and [index field quality score](/docs/entity-models/specification/#indices.INDEX_NAME.fields.INDEX_FIELD_NAME.quality)
to the [Entity Model Specification](/docs/entity-models/specification). Added
the [`"_score"`](/docs/entity-resolution/output-specification/#hits.hits._score)
field to the [Entity Resolution Output Specification](/docs/entity-resolution/output-specification).
Added an optional `_score` parameter to the [Resolution API](/docs/rest-apis/resolution-api).
([PR 39](https://github.com/zentity-io/zentity/pull/39))


## <a name="zentity-1.5.2">zentity-1.5.2</a>

### Download

Select the plugin version that matches your version of Elasticsearch:

- [Elasticsearch 7.6.1](https://zentity.io/releases/zentity-1.5.2-elasticsearch-7.6.1.zip)
- [Elasticsearch 7.6.0](https://zentity.io/releases/zentity-1.5.2-elasticsearch-7.6.0.zip)
- [Elasticsearch 7.5.2](https://zentity.io/releases/zentity-1.5.2-elasticsearch-7.5.2.zip)
- [Elasticsearch 7.5.1](https://zentity.io/releases/zentity-1.5.2-elasticsearch-7.5.1.zip)
- [Elasticsearch 7.5.0](https://zentity.io/releases/zentity-1.5.2-elasticsearch-7.5.0.zip)
- [Elasticsearch 7.4.2](https://zentity.io/releases/zentity-1.5.2-elasticsearch-7.4.2.zip)
- [Elasticsearch 7.4.1](https://zentity.io/releases/zentity-1.5.2-elasticsearch-7.4.1.zip)
- [Elasticsearch 7.4.0](https://zentity.io/releases/zentity-1.5.2-elasticsearch-7.4.0.zip)

### Release notes

- **Feature** - Added new URL parameters to the [Resolution API](/docs/rest-apis/resolution-api):
`max_time_per_query`, `_seq_no_primary_term`, `_version`, and several parameters
for advanced search optimizations.
([14bbe8a](https://github.com/zentity-io/zentity/commit/14bbe8a0dc1ef71ab3f8afedd94314e8738dc2d6))

- **Security** - Updated Jackson dependency to resolve security vulnerabilities
CVE-2019-14540, CVE-2019-16335, CVE-2019-16942, CVE-2019-16943, CVE-2019-17531,
CVE-2019-20330, CVE-2020-8840.
([3d325e2](https://github.com/zentity-io/zentity/commit/3d325e25283a197ecd0428669e74beb0d41a771e))

- **Other** - Compatibility with Elasticsearch versions prior to 7.4.0 will no
longer be maintained due to changes in the Elasticsearch Java API.
([84d101b](https://github.com/zentity-io/zentity/commit/84d101b48cce70dfad34e31e234a52982c0d6ec2))


## <a name="zentity-1.5.1">zentity-1.5.1</a>

### Download

Select the plugin version that matches your version of Elasticsearch:

- [Elasticsearch 7.3.2](https://zentity.io/releases/zentity-1.5.1-elasticsearch-7.3.2.zip)
- [Elasticsearch 7.3.1](https://zentity.io/releases/zentity-1.5.1-elasticsearch-7.3.1.zip)
- [Elasticsearch 7.3.0](https://zentity.io/releases/zentity-1.5.1-elasticsearch-7.3.0.zip)
- [Elasticsearch 7.2.1](https://zentity.io/releases/zentity-1.5.1-elasticsearch-7.2.1.zip)
- [Elasticsearch 7.2.0](https://zentity.io/releases/zentity-1.5.1-elasticsearch-7.2.0.zip)
- [Elasticsearch 7.1.1](https://zentity.io/releases/zentity-1.5.1-elasticsearch-7.1.1.zip)
- [Elasticsearch 7.1.0](https://zentity.io/releases/zentity-1.5.1-elasticsearch-7.1.0.zip)
- [Elasticsearch 7.0.1](https://zentity.io/releases/zentity-1.5.1-elasticsearch-7.0.1.zip)
- [Elasticsearch 7.0.0](https://zentity.io/releases/zentity-1.5.1-elasticsearch-7.0.0.zip)
- [Elasticsearch 6.8.2](https://zentity.io/releases/zentity-1.5.1-elasticsearch-6.8.2.zip)
- [Elasticsearch 6.8.1](https://zentity.io/releases/zentity-1.5.1-elasticsearch-6.8.1.zip)
- [Elasticsearch 6.8.0](https://zentity.io/releases/zentity-1.5.1-elasticsearch-6.8.0.zip)
- [Elasticsearch 6.7.2](https://zentity.io/releases/zentity-1.5.1-elasticsearch-6.7.2.zip)
- [Elasticsearch 6.7.1](https://zentity.io/releases/zentity-1.5.1-elasticsearch-6.7.1.zip)
- [Elasticsearch 6.7.0](https://zentity.io/releases/zentity-1.5.1-elasticsearch-6.7.0.zip)
- [Elasticsearch 6.6.2](https://zentity.io/releases/zentity-1.5.1-elasticsearch-6.6.2.zip)
- [Elasticsearch 6.6.1](https://zentity.io/releases/zentity-1.5.1-elasticsearch-6.6.1.zip)
- [Elasticsearch 6.6.0](https://zentity.io/releases/zentity-1.5.1-elasticsearch-6.6.0.zip)
- [Elasticsearch 6.5.4](https://zentity.io/releases/zentity-1.5.1-elasticsearch-6.5.4.zip)
- [Elasticsearch 6.5.3](https://zentity.io/releases/zentity-1.5.1-elasticsearch-6.5.3.zip)
- [Elasticsearch 6.5.2](https://zentity.io/releases/zentity-1.5.1-elasticsearch-6.5.2.zip)
- [Elasticsearch 6.5.1](https://zentity.io/releases/zentity-1.5.1-elasticsearch-6.5.1.zip)
- [Elasticsearch 6.5.0](https://zentity.io/releases/zentity-1.5.1-elasticsearch-6.5.0.zip)

### Release notes

- **Bug fix** - Ensure that null values and missing fields are not passed to the
`"_attributes"` object. This bug only affected the output of `"_attributes"` and
not the accuracy of the resolution job.
([c03ce76](https://github.com/zentity-io/zentity/commit/c03ce7657399cbab3ab0b72510e063be2109fb6d))


## <a name="zentity-1.5.0">zentity-1.5.0</a>

### Download

Select the plugin version that matches your version of Elasticsearch:

- [Elasticsearch 7.3.2](https://zentity.io/releases/zentity-1.5.0-elasticsearch-7.3.2.zip)
- [Elasticsearch 7.3.1](https://zentity.io/releases/zentity-1.5.0-elasticsearch-7.3.1.zip)
- [Elasticsearch 7.3.0](https://zentity.io/releases/zentity-1.5.0-elasticsearch-7.3.0.zip)
- [Elasticsearch 7.2.1](https://zentity.io/releases/zentity-1.5.0-elasticsearch-7.2.1.zip)
- [Elasticsearch 7.2.0](https://zentity.io/releases/zentity-1.5.0-elasticsearch-7.2.0.zip)
- [Elasticsearch 7.1.1](https://zentity.io/releases/zentity-1.5.0-elasticsearch-7.1.1.zip)
- [Elasticsearch 7.1.0](https://zentity.io/releases/zentity-1.5.0-elasticsearch-7.1.0.zip)
- [Elasticsearch 7.0.1](https://zentity.io/releases/zentity-1.5.0-elasticsearch-7.0.1.zip)
- [Elasticsearch 7.0.0](https://zentity.io/releases/zentity-1.5.0-elasticsearch-7.0.0.zip)
- [Elasticsearch 6.8.2](https://zentity.io/releases/zentity-1.5.0-elasticsearch-6.8.2.zip)
- [Elasticsearch 6.8.1](https://zentity.io/releases/zentity-1.5.0-elasticsearch-6.8.1.zip)
- [Elasticsearch 6.8.0](https://zentity.io/releases/zentity-1.5.0-elasticsearch-6.8.0.zip)
- [Elasticsearch 6.7.2](https://zentity.io/releases/zentity-1.5.0-elasticsearch-6.7.2.zip)
- [Elasticsearch 6.7.1](https://zentity.io/releases/zentity-1.5.0-elasticsearch-6.7.1.zip)
- [Elasticsearch 6.7.0](https://zentity.io/releases/zentity-1.5.0-elasticsearch-6.7.0.zip)
- [Elasticsearch 6.6.2](https://zentity.io/releases/zentity-1.5.0-elasticsearch-6.6.2.zip)
- [Elasticsearch 6.6.1](https://zentity.io/releases/zentity-1.5.0-elasticsearch-6.6.1.zip)
- [Elasticsearch 6.6.0](https://zentity.io/releases/zentity-1.5.0-elasticsearch-6.6.0.zip)
- [Elasticsearch 6.5.4](https://zentity.io/releases/zentity-1.5.0-elasticsearch-6.5.4.zip)
- [Elasticsearch 6.5.3](https://zentity.io/releases/zentity-1.5.0-elasticsearch-6.5.3.zip)
- [Elasticsearch 6.5.2](https://zentity.io/releases/zentity-1.5.0-elasticsearch-6.5.2.zip)
- [Elasticsearch 6.5.1](https://zentity.io/releases/zentity-1.5.0-elasticsearch-6.5.1.zip)
- [Elasticsearch 6.5.0](https://zentity.io/releases/zentity-1.5.0-elasticsearch-6.5.0.zip)

### Release notes

- **Breaking change** - Attribute values in the [`"_attributes"`](/docs/entity-resolution/output-specification/#hits.hits._attributes)
object of each document returned by the [Resolution API](/docs/rest-apis/resolution-api)
are now arrays of values instead of single values.
([c2c723b](https://github.com/zentity-io/zentity/commit/c2c723b38903e5c462dacb196c718de366c98d10))

- **Bug fix** - Fixed cases in which null values or missing fields from the
`"_source"` field caused jobs to fail with a validation exception. Null values
and missing fields are now skipped.
([998c04b](https://github.com/zentity-io/zentity/commit/998c04b1c00fe97e95824615fb586e1bb6f3c16b))


## <a name="zentity-1.4.2">zentity-1.4.2</a>

### Download

Select the plugin version that matches your version of Elasticsearch:

- [Elasticsearch 7.3.2](https://zentity.io/releases/zentity-1.4.2-elasticsearch-7.3.2.zip)
- [Elasticsearch 7.3.1](https://zentity.io/releases/zentity-1.4.2-elasticsearch-7.3.1.zip)
- [Elasticsearch 7.3.0](https://zentity.io/releases/zentity-1.4.2-elasticsearch-7.3.0.zip)
- [Elasticsearch 7.2.1](https://zentity.io/releases/zentity-1.4.2-elasticsearch-7.2.1.zip)
- [Elasticsearch 7.2.0](https://zentity.io/releases/zentity-1.4.2-elasticsearch-7.2.0.zip)
- [Elasticsearch 7.1.1](https://zentity.io/releases/zentity-1.4.2-elasticsearch-7.1.1.zip)
- [Elasticsearch 7.1.0](https://zentity.io/releases/zentity-1.4.2-elasticsearch-7.1.0.zip)
- [Elasticsearch 7.0.1](https://zentity.io/releases/zentity-1.4.2-elasticsearch-7.0.1.zip)
- [Elasticsearch 7.0.0](https://zentity.io/releases/zentity-1.4.2-elasticsearch-7.0.0.zip)
- [Elasticsearch 6.8.2](https://zentity.io/releases/zentity-1.4.2-elasticsearch-6.8.2.zip)
- [Elasticsearch 6.8.1](https://zentity.io/releases/zentity-1.4.2-elasticsearch-6.8.1.zip)
- [Elasticsearch 6.8.0](https://zentity.io/releases/zentity-1.4.2-elasticsearch-6.8.0.zip)
- [Elasticsearch 6.7.2](https://zentity.io/releases/zentity-1.4.2-elasticsearch-6.7.2.zip)
- [Elasticsearch 6.7.1](https://zentity.io/releases/zentity-1.4.2-elasticsearch-6.7.1.zip)
- [Elasticsearch 6.7.0](https://zentity.io/releases/zentity-1.4.2-elasticsearch-6.7.0.zip)
- [Elasticsearch 6.6.2](https://zentity.io/releases/zentity-1.4.2-elasticsearch-6.6.2.zip)
- [Elasticsearch 6.6.1](https://zentity.io/releases/zentity-1.4.2-elasticsearch-6.6.1.zip)
- [Elasticsearch 6.6.0](https://zentity.io/releases/zentity-1.4.2-elasticsearch-6.6.0.zip)
- [Elasticsearch 6.5.4](https://zentity.io/releases/zentity-1.4.2-elasticsearch-6.5.4.zip)
- [Elasticsearch 6.5.3](https://zentity.io/releases/zentity-1.4.2-elasticsearch-6.5.3.zip)
- [Elasticsearch 6.5.2](https://zentity.io/releases/zentity-1.4.2-elasticsearch-6.5.2.zip)
- [Elasticsearch 6.5.1](https://zentity.io/releases/zentity-1.4.2-elasticsearch-6.5.1.zip)
- [Elasticsearch 6.5.0](https://zentity.io/releases/zentity-1.4.2-elasticsearch-6.5.0.zip)

### Release notes

- **Bug fix** - Fixed a bug in the logic that determines whether an index in the
entity model should be queried at a given hop in the resolution job. There were
cases observed in which zentity queried an index even though it had not gathered
sufficent attribute values to populate any resolvers. In those cases, zentity
submitted an empty query to Elasticsearch, which caused the resolution job to
fail because an empty query is an invalid syntax.
([431e2d8](https://github.com/zentity-io/zentity/commit/431e2d89a0d756a4d22bc2b86f040ec640754b11))

- **Bug fix** - During a resolution job, when Elasticsearch retrieves a document
that lacks an index field defined in the entity model, zentity now skips that
field and attempt to extract the other fields. Previously, jobs failed whenever
an index field defined in the entity model was missing from any retrieved
documents. But it's entirely valid for documents in Elasticsearch to lack fields
that are defined in the index mapping.
([cbaaa51](https://github.com/zentity-io/zentity/commit/cbaaa51538378611b76b25a64c2abbc6c17239da))

- **Bug fix** - The HTTP response code for a failed resolution job is now 500
instead of 200.
([f4e629c](https://github.com/zentity-io/zentity/commit/f4e629c87a5caf0ef554bb880561a9bc5c790ed2))

- **Feature** - zentity now handles any exception thrown during a resolution job.
zentity allows a Java stack trace and all hits and queries up to the point of
failure to be included in the response when a resolution job fails.
([f4e629c](https://github.com/zentity-io/zentity/commit/f4e629c87a5caf0ef554bb880561a9bc5c790ed2))


## <a name="zentity-1.4.1">zentity-1.4.1</a>

### Download

Select the plugin version that matches your version of Elasticsearch:

- [Elasticsearch 7.3.1](https://zentity.io/releases/zentity-1.4.1-elasticsearch-7.3.1.zip)
- [Elasticsearch 7.3.0](https://zentity.io/releases/zentity-1.4.1-elasticsearch-7.3.0.zip)
- [Elasticsearch 7.2.1](https://zentity.io/releases/zentity-1.4.1-elasticsearch-7.2.1.zip)
- [Elasticsearch 7.2.0](https://zentity.io/releases/zentity-1.4.1-elasticsearch-7.2.0.zip)
- [Elasticsearch 7.1.1](https://zentity.io/releases/zentity-1.4.1-elasticsearch-7.1.1.zip)
- [Elasticsearch 7.1.0](https://zentity.io/releases/zentity-1.4.1-elasticsearch-7.1.0.zip)
- [Elasticsearch 7.0.1](https://zentity.io/releases/zentity-1.4.1-elasticsearch-7.0.1.zip)
- [Elasticsearch 7.0.0](https://zentity.io/releases/zentity-1.4.1-elasticsearch-7.0.0.zip)
- [Elasticsearch 6.8.2](https://zentity.io/releases/zentity-1.4.1-elasticsearch-6.8.2.zip)
- [Elasticsearch 6.8.1](https://zentity.io/releases/zentity-1.4.1-elasticsearch-6.8.1.zip)
- [Elasticsearch 6.8.0](https://zentity.io/releases/zentity-1.4.1-elasticsearch-6.8.0.zip)
- [Elasticsearch 6.7.2](https://zentity.io/releases/zentity-1.4.1-elasticsearch-6.7.2.zip)
- [Elasticsearch 6.7.1](https://zentity.io/releases/zentity-1.4.1-elasticsearch-6.7.1.zip)
- [Elasticsearch 6.7.0](https://zentity.io/releases/zentity-1.4.1-elasticsearch-6.7.0.zip)
- [Elasticsearch 6.6.2](https://zentity.io/releases/zentity-1.4.1-elasticsearch-6.6.2.zip)
- [Elasticsearch 6.6.1](https://zentity.io/releases/zentity-1.4.1-elasticsearch-6.6.1.zip)
- [Elasticsearch 6.6.0](https://zentity.io/releases/zentity-1.4.1-elasticsearch-6.6.0.zip)
- [Elasticsearch 6.5.4](https://zentity.io/releases/zentity-1.4.1-elasticsearch-6.5.4.zip)
- [Elasticsearch 6.5.3](https://zentity.io/releases/zentity-1.4.1-elasticsearch-6.5.3.zip)
- [Elasticsearch 6.5.2](https://zentity.io/releases/zentity-1.4.1-elasticsearch-6.5.2.zip)
- [Elasticsearch 6.5.1](https://zentity.io/releases/zentity-1.4.1-elasticsearch-6.5.1.zip)
- [Elasticsearch 6.5.0](https://zentity.io/releases/zentity-1.4.1-elasticsearch-6.5.0.zip)

### Release notes

- **Feature** - Catch errors returned by Elasticsearch and then fail the job.
Include the error and the query context in the response. Allow errors where the
index was not found, and ignore those indices in subsequent hops.
([3e96b6d](https://github.com/zentity-io/zentity/commit/3e96b6de8ad86429de76cd89a6b7fbc995d3a531))

- **Security** - Updated Jackson dependency to resolve security vulnerabilities
CVE-2019-14379, CVE-2019-14439.
([189e412](https://github.com/zentity-io/zentity/commit/189e41282d17d9b16ce6694dfb45ee9ad6820f01))

- **Other** - Now using JDK 11 instead of JDK 8 to build zentity.
([94c4f90](https://github.com/zentity-io/zentity/commit/94c4f90d76dd1f4bd5b0a6ac5f0cf208f954d6fa))


## <a name="zentity-1.4.0">zentity-1.4.0</a>

### Download

Select the plugin version that matches your version of Elasticsearch:

- [Elasticsearch 7.3.0](https://zentity.io/releases/zentity-1.4.0-elasticsearch-7.3.0.zip)
- [Elasticsearch 7.2.1](https://zentity.io/releases/zentity-1.4.0-elasticsearch-7.2.1.zip)
- [Elasticsearch 7.2.0](https://zentity.io/releases/zentity-1.4.0-elasticsearch-7.2.0.zip)
- [Elasticsearch 7.1.1](https://zentity.io/releases/zentity-1.4.0-elasticsearch-7.1.1.zip)
- [Elasticsearch 7.1.0](https://zentity.io/releases/zentity-1.4.0-elasticsearch-7.1.0.zip)
- [Elasticsearch 7.0.1](https://zentity.io/releases/zentity-1.4.0-elasticsearch-7.0.1.zip)
- [Elasticsearch 7.0.0](https://zentity.io/releases/zentity-1.4.0-elasticsearch-7.0.0.zip)
- [Elasticsearch 6.8.2](https://zentity.io/releases/zentity-1.4.0-elasticsearch-6.8.2.zip)
- [Elasticsearch 6.8.1](https://zentity.io/releases/zentity-1.4.0-elasticsearch-6.8.1.zip)
- [Elasticsearch 6.8.0](https://zentity.io/releases/zentity-1.4.0-elasticsearch-6.8.0.zip)
- [Elasticsearch 6.7.2](https://zentity.io/releases/zentity-1.4.0-elasticsearch-6.7.2.zip)
- [Elasticsearch 6.7.1](https://zentity.io/releases/zentity-1.4.0-elasticsearch-6.7.1.zip)
- [Elasticsearch 6.7.0](https://zentity.io/releases/zentity-1.4.0-elasticsearch-6.7.0.zip)
- [Elasticsearch 6.6.2](https://zentity.io/releases/zentity-1.4.0-elasticsearch-6.6.2.zip)
- [Elasticsearch 6.6.1](https://zentity.io/releases/zentity-1.4.0-elasticsearch-6.6.1.zip)
- [Elasticsearch 6.6.0](https://zentity.io/releases/zentity-1.4.0-elasticsearch-6.6.0.zip)
- [Elasticsearch 6.5.4](https://zentity.io/releases/zentity-1.4.0-elasticsearch-6.5.4.zip)
- [Elasticsearch 6.5.3](https://zentity.io/releases/zentity-1.4.0-elasticsearch-6.5.3.zip)
- [Elasticsearch 6.5.2](https://zentity.io/releases/zentity-1.4.0-elasticsearch-6.5.2.zip)
- [Elasticsearch 6.5.1](https://zentity.io/releases/zentity-1.4.0-elasticsearch-6.5.1.zip)
- [Elasticsearch 6.5.0](https://zentity.io/releases/zentity-1.4.0-elasticsearch-6.5.0.zip)

### Release notes

- **Feature** - Added an optional [`"terms"`](/docs/entity-resolution/input-specification/#terms)
field to the resolution input which allows resolutions jobs to be submitted with
unknown or unstructured input values.
([1f3e452](https://github.com/zentity-io/zentity/commit/1f3e452599be63ebbe68d42297f3248d3e978071))

- **Feature** - Added a `"_query"` field to each object under `"hit"."hits"` and
`"queries"` to indicate which query of which hop that the object relates to.
([ac567bb](https://github.com/zentity-io/zentity/commit/ac567bb15ca6a23ba7abebdf590d448986210c26))

- **Breaking change** - Renamed `"queries"."resolvers"` to [`"queries"."filters"`](/docs/entity-resolution/output-specification/#queries.filters)
and changed its structure.
([1f3e452](https://github.com/zentity-io/zentity/commit/1f3e452599be63ebbe68d42297f3248d3e978071))


## <a name="zentity-1.3.1">zentity-1.3.1</a>

### Download

Select the plugin version that matches your version of Elasticsearch:

- [Elasticsearch 7.2.0](https://zentity.io/releases/zentity-1.3.1-elasticsearch-7.2.0.zip)
- [Elasticsearch 7.1.1](https://zentity.io/releases/zentity-1.3.1-elasticsearch-7.1.1.zip)
- [Elasticsearch 7.1.0](https://zentity.io/releases/zentity-1.3.1-elasticsearch-7.1.0.zip)
- [Elasticsearch 7.0.1](https://zentity.io/releases/zentity-1.3.1-elasticsearch-7.0.1.zip)
- [Elasticsearch 7.0.0](https://zentity.io/releases/zentity-1.3.1-elasticsearch-7.0.0.zip)
- [Elasticsearch 6.8.0](https://zentity.io/releases/zentity-1.3.1-elasticsearch-6.8.0.zip)
- [Elasticsearch 6.7.2](https://zentity.io/releases/zentity-1.3.1-elasticsearch-6.7.2.zip)
- [Elasticsearch 6.7.1](https://zentity.io/releases/zentity-1.3.1-elasticsearch-6.7.1.zip)
- [Elasticsearch 6.7.0](https://zentity.io/releases/zentity-1.3.1-elasticsearch-6.7.0.zip)
- [Elasticsearch 6.6.2](https://zentity.io/releases/zentity-1.3.1-elasticsearch-6.6.2.zip)
- [Elasticsearch 6.6.1](https://zentity.io/releases/zentity-1.3.1-elasticsearch-6.6.1.zip)
- [Elasticsearch 6.6.0](https://zentity.io/releases/zentity-1.3.1-elasticsearch-6.6.0.zip)
- [Elasticsearch 6.5.4](https://zentity.io/releases/zentity-1.3.1-elasticsearch-6.5.4.zip)
- [Elasticsearch 6.5.3](https://zentity.io/releases/zentity-1.3.1-elasticsearch-6.5.3.zip)
- [Elasticsearch 6.5.2](https://zentity.io/releases/zentity-1.3.1-elasticsearch-6.5.2.zip)
- [Elasticsearch 6.5.1](https://zentity.io/releases/zentity-1.3.1-elasticsearch-6.5.1.zip)
- [Elasticsearch 6.5.0](https://zentity.io/releases/zentity-1.3.1-elasticsearch-6.5.0.zip)

### Release notes

- **Bug fix** - When checking the existence of a resolver with a higher weight,
the absence of any attribute should imply that the resolver does not exist.
Until now the boolean logic had checked for the absence of all attributes of the
resolver. This has been corrected to check for the absence of any attribute of
the resolver.
([4d97d39](https://github.com/zentity-io/zentity/commit/4d97d3974ad560d5a8cbb9430b11faf467c1cb91))

- **Bug fix** - When submitting a resolution request with an embedded model and
an entity type, raise an error because the request is ambiguous.
([b45b24a](https://github.com/zentity-io/zentity/commit/b45b24a463836f88213984cc1538e29a1e2e1cbc))

- **Bug fix** - When submitting a resolution request with an embedded model and
no entity type, process the request.
([b45b24a](https://github.com/zentity-io/zentity/commit/b45b24a463836f88213984cc1538e29a1e2e1cbc))

- **Bug fix** - Return an error when an unrecognized field exists in the
resolution request.
([3fdde88](https://github.com/zentity-io/zentity/commit/3fdde88fea9ae0bd5058e0296d253af5c1e7cff4))

- **Security** - Updated Jackson dependency to resolve security vulnerability
CVE-2019-12814.
([a8e006e](https://github.com/zentity-io/zentity/commit/a8e006eb0dd1b964c338c082345d89a3265d9e40))

- **Minor** - Removed redundant "bool" wrapper clauses.
([a1332ce](https://github.com/zentity-io/zentity/commit/a1332cec6ac44561899d8711ab056ee94274bec1))


## <a name="zentity-1.3.0">zentity-1.3.0</a>

### Download

Select the plugin version that matches your version of Elasticsearch:

- [Elasticsearch 7.2.0](https://zentity.io/releases/zentity-1.3.0-elasticsearch-7.2.0.zip)
- [Elasticsearch 7.1.1](https://zentity.io/releases/zentity-1.3.0-elasticsearch-7.1.1.zip)
- [Elasticsearch 7.1.0](https://zentity.io/releases/zentity-1.3.0-elasticsearch-7.1.0.zip)
- [Elasticsearch 7.0.1](https://zentity.io/releases/zentity-1.3.0-elasticsearch-7.0.1.zip)
- [Elasticsearch 7.0.0](https://zentity.io/releases/zentity-1.3.0-elasticsearch-7.0.0.zip)
- [Elasticsearch 6.8.0](https://zentity.io/releases/zentity-1.3.0-elasticsearch-6.8.0.zip)
- [Elasticsearch 6.7.2](https://zentity.io/releases/zentity-1.3.0-elasticsearch-6.7.2.zip)
- [Elasticsearch 6.7.1](https://zentity.io/releases/zentity-1.3.0-elasticsearch-6.7.1.zip)
- [Elasticsearch 6.7.0](https://zentity.io/releases/zentity-1.3.0-elasticsearch-6.7.0.zip)
- [Elasticsearch 6.6.2](https://zentity.io/releases/zentity-1.3.0-elasticsearch-6.6.2.zip)
- [Elasticsearch 6.6.1](https://zentity.io/releases/zentity-1.3.0-elasticsearch-6.6.1.zip)
- [Elasticsearch 6.6.0](https://zentity.io/releases/zentity-1.3.0-elasticsearch-6.6.0.zip)
- [Elasticsearch 6.5.4](https://zentity.io/releases/zentity-1.3.0-elasticsearch-6.5.4.zip)
- [Elasticsearch 6.5.3](https://zentity.io/releases/zentity-1.3.0-elasticsearch-6.5.3.zip)
- [Elasticsearch 6.5.2](https://zentity.io/releases/zentity-1.3.0-elasticsearch-6.5.2.zip)
- [Elasticsearch 6.5.1](https://zentity.io/releases/zentity-1.3.0-elasticsearch-6.5.1.zip)
- [Elasticsearch 6.5.0](https://zentity.io/releases/zentity-1.3.0-elasticsearch-6.5.0.zip)

### Release notes

- **Breaking change** - Renamed `"priorty"` to `"weight"` in the resolver objects.
([117f38f](https://github.com/zentity-io/zentity/commit/117f38f3844f82247110a093230743f68fb078a1))


## <a name="zentity-1.2.0">zentity-1.2.0</a>

### Download

Select the plugin version that matches your version of Elasticsearch:

- [Elasticsearch 7.2.0](https://zentity.io/releases/zentity-1.2.0-elasticsearch-7.2.0.zip)
- [Elasticsearch 7.1.1](https://zentity.io/releases/zentity-1.2.0-elasticsearch-7.1.1.zip)
- [Elasticsearch 7.1.0](https://zentity.io/releases/zentity-1.2.0-elasticsearch-7.1.0.zip)
- [Elasticsearch 7.0.1](https://zentity.io/releases/zentity-1.2.0-elasticsearch-7.0.1.zip)
- [Elasticsearch 7.0.0](https://zentity.io/releases/zentity-1.2.0-elasticsearch-7.0.0.zip)
- [Elasticsearch 6.8.0](https://zentity.io/releases/zentity-1.2.0-elasticsearch-6.8.0.zip)
- [Elasticsearch 6.7.2](https://zentity.io/releases/zentity-1.2.0-elasticsearch-6.7.2.zip)
- [Elasticsearch 6.7.1](https://zentity.io/releases/zentity-1.2.0-elasticsearch-6.7.1.zip)
- [Elasticsearch 6.7.0](https://zentity.io/releases/zentity-1.2.0-elasticsearch-6.7.0.zip)
- [Elasticsearch 6.6.2](https://zentity.io/releases/zentity-1.2.0-elasticsearch-6.6.2.zip)
- [Elasticsearch 6.6.1](https://zentity.io/releases/zentity-1.2.0-elasticsearch-6.6.1.zip)
- [Elasticsearch 6.6.0](https://zentity.io/releases/zentity-1.2.0-elasticsearch-6.6.0.zip)
- [Elasticsearch 6.5.4](https://zentity.io/releases/zentity-1.2.0-elasticsearch-6.5.4.zip)
- [Elasticsearch 6.5.3](https://zentity.io/releases/zentity-1.2.0-elasticsearch-6.5.3.zip)
- [Elasticsearch 6.5.2](https://zentity.io/releases/zentity-1.2.0-elasticsearch-6.5.2.zip)
- [Elasticsearch 6.5.1](https://zentity.io/releases/zentity-1.2.0-elasticsearch-6.5.1.zip)
- [Elasticsearch 6.5.0](https://zentity.io/releases/zentity-1.2.0-elasticsearch-6.5.0.zip)

### Release notes

- **Feature** - Added an optional [`"_explanation"`](/docs/entity-resolution/output-specification/#hits.hits._explanation)
field to each document in the response object of the [Resolution API](/docs/rest-apis/resolution-api).
This field explains which resolvers caused a document to match, and more specifically,
which input value matched which indexed value using which matcher and params.
([08a2ffc](https://github.com/zentity-io/zentity/commit/08a2ffcaac266aeab9bf63a688955c04d33ecf4b))


## <a name="zentity-1.1.0">zentity-1.1.0</a>

### Download

Select the plugin version that matches your version of Elasticsearch:

- [Elasticsearch 7.2.0](https://zentity.io/releases/zentity-1.1.0-elasticsearch-7.2.0.zip)
- [Elasticsearch 7.1.1](https://zentity.io/releases/zentity-1.1.0-elasticsearch-7.1.1.zip)
- [Elasticsearch 7.1.0](https://zentity.io/releases/zentity-1.1.0-elasticsearch-7.1.0.zip)
- [Elasticsearch 7.0.1](https://zentity.io/releases/zentity-1.1.0-elasticsearch-7.0.1.zip)
- [Elasticsearch 7.0.0](https://zentity.io/releases/zentity-1.1.0-elasticsearch-7.0.0.zip)
- [Elasticsearch 6.8.0](https://zentity.io/releases/zentity-1.1.0-elasticsearch-6.8.0.zip)
- [Elasticsearch 6.7.2](https://zentity.io/releases/zentity-1.1.0-elasticsearch-6.7.2.zip)
- [Elasticsearch 6.7.1](https://zentity.io/releases/zentity-1.1.0-elasticsearch-6.7.1.zip)
- [Elasticsearch 6.7.0](https://zentity.io/releases/zentity-1.1.0-elasticsearch-6.7.0.zip)
- [Elasticsearch 6.6.2](https://zentity.io/releases/zentity-1.1.0-elasticsearch-6.6.2.zip)
- [Elasticsearch 6.6.1](https://zentity.io/releases/zentity-1.1.0-elasticsearch-6.6.1.zip)
- [Elasticsearch 6.6.0](https://zentity.io/releases/zentity-1.1.0-elasticsearch-6.6.0.zip)
- [Elasticsearch 6.5.4](https://zentity.io/releases/zentity-1.1.0-elasticsearch-6.5.4.zip)
- [Elasticsearch 6.5.3](https://zentity.io/releases/zentity-1.1.0-elasticsearch-6.5.3.zip)
- [Elasticsearch 6.5.2](https://zentity.io/releases/zentity-1.1.0-elasticsearch-6.5.2.zip)
- [Elasticsearch 6.5.1](https://zentity.io/releases/zentity-1.1.0-elasticsearch-6.5.1.zip)
- [Elasticsearch 6.5.0](https://zentity.io/releases/zentity-1.1.0-elasticsearch-6.5.0.zip)

### Release notes

- **Feature** - Introduced the concept of resolver priority.
([a57958d](https://github.com/zentity-io/zentity/commit/a57958dda8a1525a7d988890a21481d24212d8a8))

- **Breaking change** - Changed the structure of [`"queries"."resolvers"."tree"`](/docs/entity-resolution/output-specification/#queries.resolvers.tree)
in the response object of the [Resolution API]((/docs/rest-apis/resolution-api)).
([0d76da0](https://github.com/zentity-io/zentity/commit/0d76da05a810eb58b9537e1545dc259a3aa90a53))


## <a name="zentity-1.0.3">zentity-1.0.3</a>

### Download

Select the plugin version that matches your version of Elasticsearch:

- [Elasticsearch 7.2.0](https://zentity.io/releases/zentity-1.0.3-elasticsearch-7.2.0.zip)
- [Elasticsearch 7.1.1](https://zentity.io/releases/zentity-1.0.3-elasticsearch-7.1.1.zip)
- [Elasticsearch 7.1.0](https://zentity.io/releases/zentity-1.0.3-elasticsearch-7.1.0.zip)
- [Elasticsearch 7.0.1](https://zentity.io/releases/zentity-1.0.3-elasticsearch-7.0.1.zip)
- [Elasticsearch 7.0.0](https://zentity.io/releases/zentity-1.0.3-elasticsearch-7.0.0.zip)
- [Elasticsearch 6.8.0](https://zentity.io/releases/zentity-1.0.3-elasticsearch-6.8.0.zip)
- [Elasticsearch 6.7.2](https://zentity.io/releases/zentity-1.0.3-elasticsearch-6.7.2.zip)
- [Elasticsearch 6.7.1](https://zentity.io/releases/zentity-1.0.3-elasticsearch-6.7.1.zip)
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
