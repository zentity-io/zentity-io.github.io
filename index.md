## <a name="overview">Zenful entity resolution</a>

zentity is an **[Elasticsearch](https://www.elastic.co/products/elasticsearch)** plugin for real-time entity
resolution. It aims to be:

- **Simple** - Entity resolution is hard. zentity makes it easy.
- **Fast** - Get results at interactive speeds. From milliseconds to low seconds.
- **Generic** - Resolve anything. People, companies, locations, sessions, and more.
- **Transitive** - Resolve over multiple hops. Recursion finds dynamic identities.
- **Multi-source** - Resolve over multiple indices with disparate mappings.
- **Accommodating** - Operate on data as it exists. No changing or reindexing data.
- **Logical** - Logic is easier to read, troubleshoot, and optimize than statistics.
- **100% Elasticsearch** - Elasticsearch is a great foundation for entity resolution.


## <a name="latest-release">Download the latest release</a>


### zentity-1.3.0

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


## <a name="quick-start">Quick start</a>

Once you have installed Elasticsearch, you can install zentity from a remote URL or a local file.

1. Browse the [releases](/releases).
2. Find a release that matches your version of Elasticsearch. Copy the name of the .zip file.
3. Install the plugin using the `elasticsearch-plugin` script that comes with Elasticsearch.

Example:

`elasticsearch-plugin install https://zentity.io/releases/zentity-1.3.0-elasticsearch-7.2.0.zip`

Read the [installation](/docs/installation) docs for more details.

## <a name="next-steps">Next steps</a>

Read the [documentation](/docs) to learn about [entity models](/docs/entity-models),
how to [manage entity models](/docs/rest-apis/models-api), and how to [resolve entities](/docs/rest-apis/resolution-api).
