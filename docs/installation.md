[Home](/#/) / [Documentation](/#/docs) / Installation


# Installation


## Step 1. Install Elasticsearch

Download: [https://www.elastic.co/downloads/elasticsearch](https://www.elastic.co/downloads/elasticsearch)


## Step 2. Install zentity

`elasticsearch-plugin install zentity`


## Step 3. Verify installation

**Example request:**

`GET http://localhost:9200/_zentity`

**Example response:**

```javascript
{
  "name": "zentity",
  "description": "Real-time entity resolution for Elasticsearch.",
  "website": "http://zentity.io",
  "version": {
    "zentity": "0.1.1",
    "elasticsearch": "6.2.1"
  }
}
```