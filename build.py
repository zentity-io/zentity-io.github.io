import json
import jinja2

env = jinja2.Environment(
    loader = jinja2.FileSystemLoader("templates"),
    variable_start_string = "{$",
    variable_end_string = "$}"
)

PAGES = {
    "/index.html": {
        "template": "base.html",
        "vars": {
            "title": "Entity Resolution for Elasticsearch",
            "meta_description": "..."
        }
    },
    "/docs/index.html": {
        "template": "base.html",
        "vars": {
            "title": "Documentation",
            "meta_description": "..."
        }
    },
    "/releases/index.html": {
        "template": "base.html",
        "vars": {
            "title": "Releases",
            "meta_description": "..."
        }
    }
}

def build_page(page):
    return env.get_template(page["template"]).render(**page["vars"])

def build_pages(pages=PAGES):
    for output, page in pages.iteritems():
        yield build_page(page)
    
    
if __name__ == "__main__":
    for content in build_pages():
        print content