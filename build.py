# Standard packages
import json
import os

# Third-party packages
import jinja2
import mistune


env = jinja2.Environment(
    loader = jinja2.FileSystemLoader("templates"),
    variable_start_string = "{$",
    variable_end_string = "$}"
)

def markdown(filename):
    content = ""
    filepath = os.path.dirname(os.path.abspath(__file__)) + "/" + filename
    filepath = filepath.replace("\\", "/")
    with open(filepath, "rb") as file:
        content = file.read()
    return mistune.markdown(content)

PAGES = {
    "/index.html": {
        "vars": {
            "title": "Entity Resolution for Elasticsearch",
            "meta_description": "..."
        }
    },
    "/docs/index.html": {
        "vars": {
            "title": "Documentation",
            "meta_description": "..."
        }
    },
    "/docs/installation": {
        "vars": {
            "title": "Installation",
            "meta_description": "...",
            "content":  markdown("/docs/installation.md")
        }
    },
    "/releases/index.html": {
        "vars": {
            "title": "Releases",
            "meta_description": "..."
        }
    }
}

def build_page(page):
    template = env.get_template(page.get("template", "base.html"))
    return env.get_template(template).render(**page["vars"])

def build_pages(pages=PAGES):
    for output, page in pages.iteritems():
        yield build_page(page)
    
    
if __name__ == "__main__":
    for content in build_pages():
        print content