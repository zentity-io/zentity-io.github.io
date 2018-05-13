# Standard packages
import codecs
import errno
import json
import os
import shutil
from distutils.dir_util import copy_tree

# Third-party packages
import jinja2
import mistune


env = jinja2.Environment(
    loader = jinja2.FileSystemLoader("templates"),
    variable_start_string = "{$",
    variable_end_string = "$}"
)

def fullpath(filename):
    return (os.path.dirname(os.path.abspath(__file__)) + filename).replace("\\", "/")

def markdown(filename):
    content = ""
    with open(fullpath(filename), "rb") as file:
        content = file.read().decode("utf8")
    return mistune.markdown(content)

PAGES = {
    "/index.html": {
        "vars": {
            "title": "Entity Resolution for Elasticsearch",
            "meta_description": "...",
            "content": markdown("/index.md")
        }
    },
    "/docs/index.html": {
        "vars": {
            "title": "Documentation",
            "meta_description": "...",
            "content": markdown("/docs/index.md")
        }
    },
    "/docs/installation": {
        "vars": {
            "title": "Installation",
            "meta_description": "...",
            "content":  markdown("/docs/installation.md")
        }
    },
    "/docs/basic-usage": {
        "vars": {
            "title": "Basic Usage",
            "meta_description": "...",
            "content":  markdown("/docs/basic-usage.md")
        }
    },
    "/docs/entity-models/index.html": {
        "vars": {
            "title": "Entity Models",
            "meta_description": "...",
            "content":  markdown("/docs/entity-models.md")
        }
    },
    "/docs/entity-models/specification": {
        "vars": {
            "title": "Entity Models - Specification",
            "meta_description": "...",
            "content":  markdown("/docs/entity-models/specification.md")
        }
    },
    "/docs/entity-models/tips": {
        "vars": {
            "title": "Entity Models - Tips",
            "meta_description": "...",
            "content":  markdown("/docs/entity-models/tips.md")
        }
    },
    "/docs/rest-apis/index.html": {
        "vars": {
            "title": "REST APIs",
            "meta_description": "...",
            "content":  markdown("/docs/rest-apis.md")
        }
    },
    "/docs/rest-apis/resolution-api": {
        "vars": {
            "title": "REST APIs - Resolution API",
            "meta_description": "...",
            "content":  markdown("/docs/rest-apis/resolution-api.md")
        }
    },
    "/docs/rest-apis/models-api": {
        "vars": {
            "title": "REST APIs - Models API",
            "meta_description": "...",
            "content":  markdown("/docs/rest-apis/models-api.md")
        }
    },
    "/docs/security": {
        "vars": {
            "title": "Security",
            "meta_description": "...",
            "content":  markdown("/docs/security.md")
        }
    },
    "/releases/index.html": {
        "vars": {
            "title": "Releases",
            "meta_description": "...",
            "content": markdown("/releases.md")
        }
    }
}

def wipe_build_dir():
    filepath = fullpath("/build")
    print "Wiping build directory: {}".format(filepath)
    return shutil.rmtree(filepath)

def copy_assets_dir():
    filepath_from = fullpath("/assets")
    filepath_to = fullpath("/build")
    print "Copying assets from: {}".format(filepath_from)
    return copy_tree(filepath_from, filepath_to)
    
def write_page(filename, content):
    filepath = fullpath("/build" + filename)
    # Ensure any subdirectories are created
    try:
        os.makedirs(os.path.dirname(filepath))
    except OSError as e:
        if e.errno == errno.EEXIST:
            pass
        else:
            raise
    print "Writing file: {}".format(filepath)
    with codecs.open(filepath, "wb", "utf-8") as file:
        print >> file, content
        
def build_page(page):
    template = env.get_template(page.get("template", "base.html"))
    return env.get_template(template).render(**page["vars"])

def build_pages(pages=PAGES):
    for output_filename, page in pages.iteritems():
        print "Building page: {}".format(output_filename)
        content = build_page(page)
        write_page(output_filename, content)
        
def build(pages=PAGES):
    wipe_build_dir()
    copy_assets_dir()
    build_pages(pages)
    
if __name__ == "__main__":
    build()
    