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


## <a name="latest-release">Latest release</a>


### zentity 0.5.0-beta.2

Select the plugin version that aligns with your version of Elasticsearch:

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


## <a name="quick-start">Quick start</a>

Once you have installed Elasticsearch, you can install zentity from a remote URL or a local file.

1. Browse the [releases](/releases).
2. Find a release that matches your version of Elasticsearch. Copy the name of the .zip file.
3. Install the plugin using the `elasticsearch-plugin` script that comes with Elasticsearch.

Example:

`elasticsearch-plugin install https://zentity.io/releases/zentity-0.5.0-beta.2-elasticsearch-6.2.4.zip`

Read the [installation](/docs/installation) docs for more details.

## <a name="next-steps">Next steps</a>

Read the [documentation](/docs) to learn about [entity models](/docs/entity-models),
how to [manage entity models](/docs/rest-apis/models-api), and how to [resolve entities](/docs/rest-apis/resolution-api).
