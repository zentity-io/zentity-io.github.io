[Home](/) / [Documentation](/docs) / Security


# Security

As an API extension plugin for Elasticsearch, zentity inherits the security settings from the cluster on which it is installed.


## X-Pack Security

[X-Pack](https://www.elastic.co/products/x-pack) is a commercial plugin from Elastic, the creators of Elasticsearch and the
Elastic Stack. [X-Pack Security](https://www.elastic.co/products/x-pack/security) is a subset of the plugin that secures an
Elaticsearch cluster by encrypting communications with TLS and enforcing authentication and role-based access control for
clients communicating with the cluster. Likewise, communications between the cluster and the node client used by zentity will
be encrypted and any interactions with zentity must be authenticated and authorized.

Here is an example of a response from the cluster when an unauthorized user requests `GET _zentity/models/{entity_model}`
to retrieve an entity model:

```javascript
{
  "error": {
    "root_cause": [
      {
        "type": "security_exception",
        "reason": "action [indices:data/read/get] is unauthorized for user [USERNAME]"
      }
    ],
    "type": "security_exception",
    "reason": "action [indices:data/read/get] is unauthorized for user [USERNAME]"
  },
  "status": 403
}
```

All unauthorized interactions with zentity will produced an error response similar to the one above.


## X-Pack Security Role Configuration

Below are the permission settings that can be configured for a "zentity" role with X-Pack Security.
Roles can be managed in Kibana at `https://KIBANA_HOST:KIBANA_PORT/app/kibana#/management/security/roles`
or through the [Role Management APIs](https://www.elastic.co/guide/en/elasticsearch/reference/current/security-api-roles.html).


### Models API Permissions

These permission settings apply to the [Models API](/docs/rest-apis/models-api). A single role can
be granted any or all of these permissions. When setting up 

#### Create and update entity models

**Index Privileges**

- Indices: `.zentity-models`
- Permissions: `create` or `write`

**Actions Granted**

- `POST _zentity/models/{entity_type}`
- `PUT _zentity/models/{entity_type}`


#### Read entity models

**Index Privileges**

- Indices: `.zentity-models`
- Permissions: `read`

**Actions Granted**

- `GET _zentity/models`
- `GET _zentity/models/{entity_type}`


#### Delete entity models

**Index Privileges**

- Indices: `.zentity-models`
- Permissions: `delete`

**Actions Granted**

- `DELETE _zentity/models/{entity_type}`


#### Notes

Currently any user that interacts with the Models API must have the `manage` permission for the
`.zentity-models` index due to a check that is performed by the plugin to ensure that the index exists.

Additionally, when requesting any of the Models API endpoints listed above for the first time, zentity will attempt
to create the `.zentity-models` index. This means that the user who submits the first request to any Models API
endpoint must have `create` privilege for the `.zentity-models` index. Otherwise the user will always receive the
following error message:

```javascript
{
  "error": {
    "root_cause": [
      {
        "type": "security_exception",
        "reason": "action [indices:admin/create] is unauthorized for user [USERNAME]"
      }
    ],
    "type": "security_exception",
    "reason": "action [indices:admin/create] is unauthorized for user [USERNAME]"
  },
  "status": 403
}
```

An administrative user should perform the first request using `GET _zentity/models` to create the index.

A dedicated API endpoint to create the `.zentity-models` index is on the development roadmap to simplify these
experiences and allow the administrators to avoid granting the `manage` privilege for the `.zentity-models` index.


### Resolution API Permissions

There are no permissions to be configured for the [Resolution API](/docs/rest-apis/resolution-api) endpoints
`GET _zentity/resolution` or `GET _zentity/resolution/{entity_type}`. These endpoints construct and submit
search queries using the Elasticsearch [Search APIs](https://www.elastic.co/guide/en/elasticsearch/reference/current/search.html).
Therefore, permissions must be configured for each index that the user searches with zentity. Users can only perform
entity resolution if they have the `read` privilege for every index included in the scope of the request.


## Open Source Elasticsearch

Open source Elasticsearch clusters without an X-Pack Security license do not have any security mechanisms.
Communications are unencrypted and any user can perform any action on the cluster. Likewise, any user can
perform any action with zentity in an open source cluster that has not been configured with X-Pack Security.



&nbsp;

----

#### Continue Reading

|&#8249;|[Models API](/docs/rest-apis/models-api)|||
|:---|:---|---:|---:|
|    |    |    |    |
