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


### zentity-{$ latest.zentity $}

Select the plugin version that matches your version of Elasticsearch:

- [Elasticsearch 7.16.3](https://zentity.io/releases/zentity-{$ latest.zentity $}-elasticsearch-7.16.3.zip)
- [Elasticsearch 7.16.2](https://zentity.io/releases/zentity-{$ latest.zentity $}-elasticsearch-7.16.2.zip)
- [Elasticsearch 7.16.1](https://zentity.io/releases/zentity-{$ latest.zentity $}-elasticsearch-7.16.1.zip)
- [Elasticsearch 7.15.2](https://zentity.io/releases/zentity-{$ latest.zentity $}-elasticsearch-7.15.2.zip)
- [Elasticsearch 7.15.1](https://zentity.io/releases/zentity-{$ latest.zentity $}-elasticsearch-7.15.1.zip)
- [Elasticsearch 7.15.0](https://zentity.io/releases/zentity-{$ latest.zentity $}-elasticsearch-7.15.0.zip)
- [Elasticsearch 7.14.2](https://zentity.io/releases/zentity-{$ latest.zentity $}-elasticsearch-7.14.2.zip)
- [Elasticsearch 7.14.1](https://zentity.io/releases/zentity-{$ latest.zentity $}-elasticsearch-7.14.1.zip)


## <a name="quick-start">Quick start</a>

Once you have installed Elasticsearch, you can install zentity from a remote URL or a local file.

1. Browse the [releases](/releases).
2. Find a release that matches your version of Elasticsearch. Copy the name of the .zip file.
3. Install the plugin using the `elasticsearch-plugin` script that comes with Elasticsearch.

Example:

`elasticsearch-plugin install https://zentity.io/releases/zentity-{$ latest.zentity $}-elasticsearch-{$ latest.elasticsearch $}.zip`

Read the [installation](/docs/installation) docs for more details.

## <a name="next-steps">Next steps</a>

Read the [documentation](/docs) to learn about [entity models](/docs/entity-models),
how to [manage entity models](/docs/rest-apis/models-api), and how to [resolve entities](/docs/rest-apis/resolution-api).
