[Home](/) / [Documentation](/docs) / Security


# <a name="security"></a>Security

As an API extension plugin for Elasticsearch, zentity inherits the security
settings from the cluster on which it is installed. If Elasticsearch has TLS
and RBAC configured, then communications between the cluster and the node client
used by zentity will be encrypted and any interactions with zentity must be
authenticated and authorized.

> **Note**
>
> [As of Elasticsearch 7.1.0](https://www.elastic.co/guide/en/elasticsearch/reference/7.1/release-highlights-7.1.0.html),
> TLS and RBAC come with the official free distribution of Elasticsearch, which
> is licensed under the Elastic Basic license. Prior to Elasticsearch 7.1.0,
> TLS and RBAC were licensed under a paid commercial license. There are
> additional security features, such as document- and field-level security,
> which remain under that commercial license. zentity is compatible with all of
> those security features because it inherits the security of its environment.

Here is an example of a response from the cluster when an unauthorized user
requests `GET _zentity/models/{entity_model}` to retrieve an entity model:

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

All unauthorized interactions with zentity will produced an error response
similar to the one above.


## <a name="role-configuration"></a>Role Configuration

Below are the permission settings that can be configured for a "zentity" role
with Elastic Security. Roles can be managed in Kibana at `https://KIBANA_HOST:KIBANA_PORT/app/kibana#/management/security/roles`
or through the [Role Management APIs](https://www.elastic.co/guide/en/elasticsearch/reference/current/security-api-roles.html).


### <a name="setup-api-permissions"></a>Setup API Permissions

These permission settings apply to the [Setup API](/docs/rest-apis/setup-api).

**Index Privileges**

- Indices: `.zentity-models`
- Permissions: `create_index`

**Actions Granted**

- `POST _zentity/_setup`


### <a name="models-api-permissions"></a>Models API Permissions

These permission settings apply to the [Models API](/docs/rest-apis/models-api).
A single role can be granted any or all of these permissions.

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

Without security enabled, any user that interacts with the Models API will
create the `.zentity-models` index automatically if it does not already exist.
With security enabled, the user must have the `create_index` permission for the
`.zentity-models` index to be created automatically. Otherwise the user will
receive the following error message:

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


### <a name="resolution-api-permissions"></a>Resolution API Permissions

There are no permissions to be configured directly for the [Resolution API](/docs/rest-apis/resolution-api)
endpoints `GET _zentity/resolution` or `GET _zentity/resolution/{entity_type}`.
These endpoints construct and submit search queries using the Elasticsearch
[Search APIs](https://www.elastic.co/guide/en/elasticsearch/reference/current/search.html).
Therefore, permissions must be configured for each index that the user searches
with zentity. Users can only perform entity resolution if they have the `read`
privilege for every index included in the scope of the request.


## <a name="open-source-elasticsearch"></a>Open Source Elasticsearch

Elasticsearch clusters that lack either the free Elastic Basic license or a paid
commercial license do not have any security mechanisms. Communications are
unencrypted and any user can perform any action on the cluster. Likewise, any
user can perform any action with zentity in an pure open source cluster that has
not been configured with Elastic Security.


&nbsp;

----

#### Continue Reading

|&#8249;|[Bulk Resolution API](/docs/rest-apis/bulk-resolution-api)|||
|:---|:---|---:|---:|
|    |    |    |    |
