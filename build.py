# Standard packages
import codecs
import copy
import errno
import json
import os
import shutil
from distutils.dir_util import copy_tree

# Third-party packages
import jinja2
import mistune
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import html


env = jinja2.Environment(
    loader = jinja2.FileSystemLoader("templates"),
    variable_start_string = "{$",
    variable_end_string = "$}"
)

class ZentityRenderer(mistune.Renderer):
    
    def block_code(self, code, lang):
        if not lang:
            return "\n<pre><code>%s</code></pre>\n" % mistune.escape(code)
        lexer = get_lexer_by_name(lang, stripall=True)
        formatter = html.HtmlFormatter()
        return highlight(code, lexer, formatter)
        
    def link(self, link, title, text):
        link = mistune.escape_link(link)
        out = "<a href=\"%s\"" % link
        if title:
            out += " title=\"%s\"" % escape(title, quote=True)
        if not link.startswith("/") and not link.startswith("https://zentity.io") and not link.startswith("http://zentity.io"):
            out += " onclick=\"to('%s');\"" % link
        elif link.endswith(".zip"):
            out += " onclick=\"to('%s');\"" % link
        out += ">%s</a>" % text
        return out
        
    def table(self, header, body):
        return (
            '<table class="table">\n<thead>%s</thead>\n'
            '<tbody>\n%s</tbody>\n</table>\n'
        ) % (header, body)
        
def fullpath(filename):
    return (os.path.dirname(os.path.abspath(__file__)) + filename).replace("\\", "/")

def markdown(filename):
    content = ""
    with open(fullpath(filename), "rb") as file:
        content = file.read().decode("utf8")
    markdown = mistune.Markdown(renderer=ZentityRenderer())
    return markdown(content)

PAGES = {
    "/": {
        "vars": {
            "title": "Entity Resolution for Elasticsearch",
            "meta_description": "...",
            "content": markdown("/index.md"),
            "home": True
        }
    },
    "/docs": {
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
            "content": markdown("/docs/installation.md")
        }
    },
    "/docs/basic-usage": {
        "vars": {
            "title": "Basic Usage",
            "meta_description": "...",
            "content": markdown("/docs/basic-usage.md")
        }
    },
    "/docs/entity-models": {
        "vars": {
            "title": "Entity Models",
            "meta_description": "...",
            "content": markdown("/docs/entity-models.md")
        }
    },
    "/docs/entity-models/specification": {
        "vars": {
            "title": "Entity Models - Specification",
            "meta_description": "...",
            "content": markdown("/docs/entity-models/specification.md")
        }
    },
    "/docs/entity-models/tips": {
        "vars": {
            "title": "Entity Models - Tips",
            "meta_description": "...",
            "content": markdown("/docs/entity-models/tips.md")
        }
    },
    "/docs/rest-apis": {
        "vars": {
            "title": "REST APIs",
            "meta_description": "...",
            "content": markdown("/docs/rest-apis.md")
        }
    },
    "/docs/rest-apis/resolution-api": {
        "vars": {
            "title": "REST APIs - Resolution API",
            "meta_description": "...",
            "content": markdown("/docs/rest-apis/resolution-api.md")
        }
    },
    "/docs/rest-apis/models-api": {
        "vars": {
            "title": "REST APIs - Models API",
            "meta_description": "...",
            "content": markdown("/docs/rest-apis/models-api.md")
        }
    },
    "/docs/security": {
        "vars": {
            "title": "Security",
            "meta_description": "...",
            "content": markdown("/docs/security.md")
        }
    },
    "/releases": {
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
    
def write_page(uri_path, content):
    filepath = fullpath("/build" + uri_path + "/index.html")
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
        
def build_page(page, args={}):
    template = env.get_template(page.get("template", "base.html"))
    vars = copy.deepcopy(page["vars"])
    vars.update(args)
    return env.get_template(template).render(**vars)

def build_pages(pages=PAGES, args={}):
    for uri_path, page in pages.iteritems():
        print "Building page: {}".format(uri_path)
        content = build_page(page, args)
        write_page(uri_path, content)
        
def build(pages=PAGES, args={}):
    wipe_build_dir()
    copy_assets_dir()
    build_pages(pages, args)
    
if __name__ == "__main__":
    build(args={"test": True})
    