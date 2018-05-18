[Home](/) / [Documentation](/docs) / Security


# <a name="security">Security</a>

As an API extension plugin for Elasticsearch, zentity inherits the security settings from the cluster on which it is installed.


## <a name="x-pack-security">X-Pack Security</a>

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


## <a name="role-configuration">X-Pack Security Role Configuration</a>

Below are the permission settings that can be configured for a "zentity" role with X-Pack Security.
Roles can be managed in Kibana at `https://KIBANA_HOST:KIBANA_PORT/app/kibana#/management/security/roles`
or through the [Role Management APIs](https://www.elastic.co/guide/en/elasticsearch/reference/current/security-api-roles.html).


### <a name="setup-api-permissions">Setup API Permissions</a>

These permission settings apply to the [Setup API](/docs/rest-apis/setup-api).

**Index Privileges**

- Indices: `.zentity-models`
- Permissions: `create_index`

**Actions Granted**

- `POST _zentity/_setup`


### <a name="models-api-permissions">Models API Permissions</a>

These permission settings apply to the [Models API](/docs/rest-apis/models-api). A single role can
be granted any or all of these permissions.

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

Without security enabled, any user that interacts with the Models API will create the `.zentity-models`
index automatically if it does not already exist. With security enabled, the user must have the `create_index`
permission for the `.zentity-models` index to be created automatically. Otherwise the user will receive
the following error message:

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

An administrative user should request `POST _zentity/_setup` to create the index.


### <a name="resolution-api-permissions">Resolution API Permissions</a>

There are no permissions to be configured directly for the [Resolution API](/docs/rest-apis/resolution-api)
endpoints `GET _zentity/resolution` or `GET _zentity/resolution/{entity_type}`. These endpoints construct and submit
search queries using the Elasticsearch [Search APIs](https://www.elastic.co/guide/en/elasticsearch/reference/current/search.html).
Therefore, permissions must be configured for each index that the user searches with zentity. Users can only perform
entity resolution if they have the `read` privilege for every index included in the scope of the request.


## <a name="open-source-elasticsearch">Open Source Elasticsearch</a>

Open source Elasticsearch clusters without an X-Pack Security license do not have any security mechanisms.
Communications are unencrypted and any user can perform any action on the cluster. Likewise, any user can
perform any action with zentity in an open source cluster that has not been configured with X-Pack Security.


&nbsp;

----

#### Continue Reading

|&#8249;|[Resolution API](/docs/rest-apis/resolution-api)|||
|:---|:---|---:|---:|
|    |    |    |    |
