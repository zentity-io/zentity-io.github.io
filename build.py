# Standard packages
import codecs
import copy
import errno
import json
import os
import shutil
import sys
from distutils.dir_util import copy_tree

# Third-party packages
import jinja2
import mistune
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import html


META_DESCRIPTION_GENERIC = "zentity brings entity resolution to Elasticsearch. Connect the hidden fragments of an identity in your data. Fast, scalable, open source."
META_DESCRIPTION_GENERIC_SHORT = "Connect the hidden fragments of an identity in your data. Fast, scalable, open source."

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
        formatted = highlight(code, lexer, formatter)
        formatted = """
        <div class="code">
          <button type="button" class="btn btn-sm btn-link" onclick="$(this).siblings('.highlight').select();document.execCommand('copy');">
            <span style="font-size:24px;">&#x2398</span> Copy to clipboard
          </button>
          %s
        </div>
        """ % formatted
        return formatted
        
    def link(self, link, title, text):
        link = mistune.escape_link(link)
        out = "<a href=\"%s\"" % link
        if title:
            out += " title=\"%s\"" % escape(title, quote=True)
        if not link.startswith("/") and not link.startswith("#") and not link.startswith("https://zentity.io") and not link.startswith("http://zentity.io"):
            out += " onclick=\"to('%s', 'outbound');\"" % link
            out += " class=\"external\""
        elif link.endswith(".zip"):
            out += " onclick=\"to('%s', 'download');\"" % link
        elif link.startswith("#"):
            out += " onclick=\"to(window.location.pathname + '%s', 'internal');\"" % link
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
            "meta_description": META_DESCRIPTION_GENERIC,
            "meta_description_social": META_DESCRIPTION_GENERIC_SHORT,
            "content": markdown("/index.md"),
            "home": True
        }
    },
    "/docs": {
        "vars": {
            "title": "Documentation",
            "meta_description": META_DESCRIPTION_GENERIC,
            "meta_description_social": META_DESCRIPTION_GENERIC_SHORT,
            "content": markdown("/docs/index.md")
        }
    },
    "/docs/installation": {
        "vars": {
            "title": "Installation",
            "meta_description": META_DESCRIPTION_GENERIC,
            "meta_description_social": META_DESCRIPTION_GENERIC_SHORT,
            "content": markdown("/docs/installation.md")
        }
    },
    "/docs/basic-usage": {
        "vars": {
            "title": "Basic Usage",
            "meta_description": META_DESCRIPTION_GENERIC,
            "meta_description_social": META_DESCRIPTION_GENERIC_SHORT,
            "content": markdown("/docs/basic-usage.md")
        }
    },
    "/docs/basic-usage/exact-name-matching": {
        "vars": {
            "title": "Exact Name Matching",
            "meta_description": META_DESCRIPTION_GENERIC,
            "meta_description_social": META_DESCRIPTION_GENERIC_SHORT,
            "content": markdown("/docs/basic-usage/exact-name-matching.md")
        }
    },
    "/docs/basic-usage/robust-name-matching": {
        "vars": {
            "title": "Robust Name Matching",
            "meta_description": META_DESCRIPTION_GENERIC,
            "meta_description_social": META_DESCRIPTION_GENERIC_SHORT,
            "content": markdown("/docs/basic-usage/robust-name-matching.md")
        }
    },
    "/docs/basic-usage/multiple-attribute-resolution": {
        "vars": {
            "title": "Multiple Attribute Resolution",
            "meta_description": META_DESCRIPTION_GENERIC,
            "meta_description_social": META_DESCRIPTION_GENERIC_SHORT,
            "content": markdown("/docs/basic-usage/multiple-attribute-resolution.md")
        }
    },
    "/docs/basic-usage/multiple-resolver-resolution": {
        "vars": {
            "title": "Multiple Resolver Resolution",
            "meta_description": META_DESCRIPTION_GENERIC,
            "meta_description_social": META_DESCRIPTION_GENERIC_SHORT,
            "content": markdown("/docs/basic-usage/multiple-resolver-resolution.md")
        }
    },
    "/docs/basic-usage/cross-index-resolution": {
        "vars": {
            "title": "Cross Index Resolution",
            "meta_description": META_DESCRIPTION_GENERIC,
            "meta_description_social": META_DESCRIPTION_GENERIC_SHORT,
            "content": markdown("/docs/basic-usage/cross-index-resolution.md")
        }
    },
    "/docs/entity-models": {
        "vars": {
            "title": "Entity Models",
            "meta_description": META_DESCRIPTION_GENERIC,
            "meta_description_social": META_DESCRIPTION_GENERIC_SHORT,
            "content": markdown("/docs/entity-models.md")
        }
    },
    "/docs/entity-models/specification": {
        "vars": {
            "title": "Entity Model Specification",
            "meta_description": META_DESCRIPTION_GENERIC,
            "meta_description_social": META_DESCRIPTION_GENERIC_SHORT,
            "content": markdown("/docs/entity-models/specification.md")
        }
    },
    "/docs/entity-models/tips": {
        "vars": {
            "title": "Entity Modeling Tips",
            "meta_description": META_DESCRIPTION_GENERIC,
            "meta_description_social": META_DESCRIPTION_GENERIC_SHORT,
            "content": markdown("/docs/entity-models/tips.md")
        }
    },
    "/docs/entity-resolution": {
        "vars": {
            "title": "Entity Resolution",
            "meta_description": META_DESCRIPTION_GENERIC,
            "meta_description_social": META_DESCRIPTION_GENERIC_SHORT,
            "content": markdown("/docs/entity-resolution.md")
        }
    },
    "/docs/entity-resolution/input-specification": {
        "vars": {
            "title": "Entity Resolution Input Specification",
            "meta_description": META_DESCRIPTION_GENERIC,
            "meta_description_social": META_DESCRIPTION_GENERIC_SHORT,
            "content": markdown("/docs/entity-resolution/input.md")
        }
    },
    "/docs/entity-resolution/output-specification": {
        "vars": {
            "title": "Entity Resolution Output Specification",
            "meta_description": META_DESCRIPTION_GENERIC,
            "meta_description_social": META_DESCRIPTION_GENERIC_SHORT,
            "content": markdown("/docs/entity-resolution/output.md")
        }
    },
    "/docs/rest-apis": {
        "vars": {
            "title": "REST APIs",
            "meta_description": META_DESCRIPTION_GENERIC,
            "meta_description_social": META_DESCRIPTION_GENERIC_SHORT,
            "content": markdown("/docs/rest-apis.md")
        }
    },
    "/docs/rest-apis/setup-api": {
        "vars": {
            "title": "Setup API",
            "meta_description": META_DESCRIPTION_GENERIC,
            "meta_description_social": META_DESCRIPTION_GENERIC_SHORT,
            "content": markdown("/docs/rest-apis/setup-api.md")
        }
    },
    "/docs/rest-apis/models-api": {
        "vars": {
            "title": "Models API",
            "meta_description": META_DESCRIPTION_GENERIC,
            "meta_description_social": META_DESCRIPTION_GENERIC_SHORT,
            "content": markdown("/docs/rest-apis/models-api.md")
        }
    },
    "/docs/rest-apis/resolution-api": {
        "vars": {
            "title": "Resolution API",
            "meta_description": META_DESCRIPTION_GENERIC,
            "meta_description_social": META_DESCRIPTION_GENERIC_SHORT,
            "content": markdown("/docs/rest-apis/resolution-api.md")
        }
    },
    "/docs/security": {
        "vars": {
            "title": "Security",
            "meta_description": META_DESCRIPTION_GENERIC,
            "meta_description_social": META_DESCRIPTION_GENERIC_SHORT,
            "content": markdown("/docs/security.md")
        }
    },
    "/releases": {
        "vars": {
            "title": "Releases",
            "meta_description": "Downloads and release notes for zentity.",
            "meta_description_social": META_DESCRIPTION_GENERIC_SHORT,
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
    args = {}
    args["test"] = False
    for arg in sys.argv[1:]:
        if arg == "--test":
            args["test"] = True
    print args
    build(args=args)
    