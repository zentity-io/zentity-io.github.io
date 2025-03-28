# Standard packages
import binascii
import codecs
import copy
import datetime
import errno
import json
import os
import re
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

RE_VERSION_ELASTICSEARCH = re.compile(r"-elasticsearch-(.+)$")
RE_VERSION_ZENTITY = re.compile(r"^zentity-(.+)-elasticsearch")

SANDBOX_VERSION_ELASTICSEARCH = "8.13.3"
SANDBOX_VERSION_ZENTITY = "1.8.3"
TUTORIAL_VERSION_ELASTICSEARCH = "7.10.1"
TUTORIAL_VERSION_ZENTITY = "1.6.1"

env = jinja2.Environment(
    loader = jinja2.FileSystemLoader("templates"),
    variable_start_string = "{$",
    variable_end_string = "$}"
)

def parse_latest_version(latest_version):
    return {
        "zentity": re.findall(RE_VERSION_ZENTITY, latest_version)[0],
        "elasticsearch": re.findall(RE_VERSION_ELASTICSEARCH, latest_version)[0]
    }

class ZentityRenderer(mistune.Renderer):

    def block_code(self, code, lang):
        if not lang:
            return "\n<pre><code>%s</code></pre>\n" % mistune.escape(code)
        lexer = get_lexer_by_name(lang, stripall=True)
        id = f'a{binascii.hexlify(os.urandom(8)).decode('utf-8')}'
        formatter = html.HtmlFormatter()
        formatted = highlight(code, lexer, formatter)
        formatted = """
        <div class="code">
          <button type="button" class="btn btn-sm btn-link copy" data-clipboard-target="#%s">
            <span style="font-size:24px;">&#x2398</span> Copy to clipboard
          </button>
          <span id="%s">%s</span>
        </div>
        """ % ( id, id, formatted )
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

def markdown(filename, args):
    content = ""
    with open(fullpath(filename), "rb") as file:
        content = file.read().decode("utf8")
    markdownEnv = jinja2.Environment(
        loader = jinja2.BaseLoader(),
        variable_start_string = "{$",
        variable_end_string = "$}"
    )
    content = markdownEnv.from_string(content).render(**args)
    markdown = mistune.Markdown(renderer=ZentityRenderer())
    return markdown(content)

def PAGES(args):
    return {
        "/": {
            "vars": {
                "title": "Entity Resolution for Elasticsearch",
                "meta_description": META_DESCRIPTION_GENERIC,
                "meta_description_social": META_DESCRIPTION_GENERIC_SHORT,
                "content": markdown("/index.md", args),
                "home": True
            }
        },
        "/docs": {
            "vars": {
                "title": "Documentation",
                "meta_description": META_DESCRIPTION_GENERIC,
                "meta_description_social": META_DESCRIPTION_GENERIC_SHORT,
                "content": markdown("/docs/index.md", args)
            }
        },
        "/docs/installation": {
            "vars": {
                "title": "Installation",
                "meta_description": META_DESCRIPTION_GENERIC,
                "meta_description_social": META_DESCRIPTION_GENERIC_SHORT,
                "content": markdown("/docs/installation.md", args)
            }
        },
        "/docs/basic-usage": {
            "vars": {
                "title": "Basic Usage",
                "meta_description": META_DESCRIPTION_GENERIC,
                "meta_description_social": META_DESCRIPTION_GENERIC_SHORT,
                "content": markdown("/docs/basic-usage.md", args)
            }
        },
        "/docs/basic-usage/exact-name-matching": {
            "vars": {
                "title": "Exact Name Matching",
                "meta_description": META_DESCRIPTION_GENERIC,
                "meta_description_social": META_DESCRIPTION_GENERIC_SHORT,
                "content": markdown("/docs/basic-usage/exact-name-matching.md", args)
            }
        },
        "/docs/basic-usage/robust-name-matching": {
            "vars": {
                "title": "Robust Name Matching",
                "meta_description": META_DESCRIPTION_GENERIC,
                "meta_description_social": META_DESCRIPTION_GENERIC_SHORT,
                "content": markdown("/docs/basic-usage/robust-name-matching.md", args)
            }
        },
        "/docs/basic-usage/multiple-attribute-resolution": {
            "vars": {
                "title": "Multiple Attribute Resolution",
                "meta_description": META_DESCRIPTION_GENERIC,
                "meta_description_social": META_DESCRIPTION_GENERIC_SHORT,
                "content": markdown("/docs/basic-usage/multiple-attribute-resolution.md", args)
            }
        },
        "/docs/basic-usage/multiple-resolver-resolution": {
            "vars": {
                "title": "Multiple Resolver Resolution",
                "meta_description": META_DESCRIPTION_GENERIC,
                "meta_description_social": META_DESCRIPTION_GENERIC_SHORT,
                "content": markdown("/docs/basic-usage/multiple-resolver-resolution.md", args)
            }
        },
        "/docs/basic-usage/cross-index-resolution": {
            "vars": {
                "title": "Cross Index Resolution",
                "meta_description": META_DESCRIPTION_GENERIC,
                "meta_description_social": META_DESCRIPTION_GENERIC_SHORT,
                "content": markdown("/docs/basic-usage/cross-index-resolution.md", args)
            }
        },
        "/docs/basic-usage/scoping-resolution": {
            "vars": {
                "title": "Scoping Resolution",
                "meta_description": META_DESCRIPTION_GENERIC,
                "meta_description_social": META_DESCRIPTION_GENERIC_SHORT,
                "content": markdown("/docs/basic-usage/scoping-resolution.md", args)
            }
        },
        "/docs/advanced-usage": {
            "vars": {
                "title": "Advanced Usage",
                "meta_description": META_DESCRIPTION_GENERIC,
                "meta_description_social": META_DESCRIPTION_GENERIC_SHORT,
                "content": markdown("/docs/advanced-usage.md", args)
            }
        },
        "/docs/advanced-usage/scoring-resolution": {
            "vars": {
                "title": "Scoring Resolution",
                "meta_description": META_DESCRIPTION_GENERIC,
                "meta_description_social": META_DESCRIPTION_GENERIC_SHORT,
                "content": markdown("/docs/advanced-usage/scoring-resolution.md", args)
            }
        },
        "/docs/advanced-usage/matcher-parameters": {
            "vars": {
                "title": "Matcher Parameters",
                "meta_description": META_DESCRIPTION_GENERIC,
                "meta_description_social": META_DESCRIPTION_GENERIC_SHORT,
                "content": markdown("/docs/advanced-usage/matcher-parameters.md", args)
            }
        },
        "/docs/advanced-usage/date-attributes": {
            "vars": {
                "title": "Date Attributes",
                "meta_description": META_DESCRIPTION_GENERIC,
                "meta_description_social": META_DESCRIPTION_GENERIC_SHORT,
                "content": markdown("/docs/advanced-usage/date-attributes.md", args)
            }
        },
        "/docs/advanced-usage/payload-attributes": {
            "vars": {
                "title": "Payload Attributes",
                "meta_description": META_DESCRIPTION_GENERIC,
                "meta_description_social": META_DESCRIPTION_GENERIC_SHORT,
                "content": markdown("/docs/advanced-usage/payload-attributes.md", args)
            }
        },
        "/docs/entity-models": {
            "vars": {
                "title": "Entity Models",
                "meta_description": META_DESCRIPTION_GENERIC,
                "meta_description_social": META_DESCRIPTION_GENERIC_SHORT,
                "content": markdown("/docs/entity-models.md", args)
            }
        },
        "/docs/entity-models/specification": {
            "vars": {
                "title": "Entity Model Specification",
                "meta_description": META_DESCRIPTION_GENERIC,
                "meta_description_social": META_DESCRIPTION_GENERIC_SHORT,
                "content": markdown("/docs/entity-models/specification.md", args)
            }
        },
        "/docs/entity-models/tips": {
            "vars": {
                "title": "Entity Modeling Tips",
                "meta_description": META_DESCRIPTION_GENERIC,
                "meta_description_social": META_DESCRIPTION_GENERIC_SHORT,
                "content": markdown("/docs/entity-models/tips.md", args)
            }
        },
        "/docs/entity-resolution": {
            "vars": {
                "title": "Entity Resolution",
                "meta_description": META_DESCRIPTION_GENERIC,
                "meta_description_social": META_DESCRIPTION_GENERIC_SHORT,
                "content": markdown("/docs/entity-resolution.md", args)
            }
        },
        "/docs/entity-resolution/input-specification": {
            "vars": {
                "title": "Entity Resolution Input Specification",
                "meta_description": META_DESCRIPTION_GENERIC,
                "meta_description_social": META_DESCRIPTION_GENERIC_SHORT,
                "content": markdown("/docs/entity-resolution/input.md", args)
            }
        },
        "/docs/entity-resolution/output-specification": {
            "vars": {
                "title": "Entity Resolution Output Specification",
                "meta_description": META_DESCRIPTION_GENERIC,
                "meta_description_social": META_DESCRIPTION_GENERIC_SHORT,
                "content": markdown("/docs/entity-resolution/output.md", args)
            }
        },
        "/docs/rest-apis": {
            "vars": {
                "title": "REST APIs",
                "meta_description": META_DESCRIPTION_GENERIC,
                "meta_description_social": META_DESCRIPTION_GENERIC_SHORT,
                "content": markdown("/docs/rest-apis.md", args)
            }
        },
        "/docs/rest-apis/setup-api": {
            "vars": {
                "title": "Setup API",
                "meta_description": META_DESCRIPTION_GENERIC,
                "meta_description_social": META_DESCRIPTION_GENERIC_SHORT,
                "content": markdown("/docs/rest-apis/setup-api.md", args)
            }
        },
        "/docs/rest-apis/models-api": {
            "vars": {
                "title": "Models API",
                "meta_description": META_DESCRIPTION_GENERIC,
                "meta_description_social": META_DESCRIPTION_GENERIC_SHORT,
                "content": markdown("/docs/rest-apis/models-api.md", args)
            }
        },
        "/docs/rest-apis/bulk-models-api": {
            "vars": {
                "title": "Bulk Models API",
                "meta_description": META_DESCRIPTION_GENERIC,
                "meta_description_social": META_DESCRIPTION_GENERIC_SHORT,
                "content": markdown("/docs/rest-apis/bulk-models-api.md", args)
            }
        },
        "/docs/rest-apis/resolution-api": {
            "vars": {
                "title": "Resolution API",
                "meta_description": META_DESCRIPTION_GENERIC,
                "meta_description_social": META_DESCRIPTION_GENERIC_SHORT,
                "content": markdown("/docs/rest-apis/resolution-api.md", args)
            }
        },
        "/docs/rest-apis/bulk-resolution-api": {
            "vars": {
                "title": "Bulk Resolution API",
                "meta_description": META_DESCRIPTION_GENERIC,
                "meta_description_social": META_DESCRIPTION_GENERIC_SHORT,
                "content": markdown("/docs/rest-apis/bulk-resolution-api.md", args)
            }
        },
        "/docs/security": {
            "vars": {
                "title": "Security",
                "meta_description": META_DESCRIPTION_GENERIC,
                "meta_description_social": META_DESCRIPTION_GENERIC_SHORT,
                "content": markdown("/docs/security.md", args)
            }
        },
        "/releases": {
            "vars": {
                "title": "Releases",
                "meta_description": "Downloads and release notes for zentity.",
                "meta_description_social": META_DESCRIPTION_GENERIC_SHORT,
                "content": markdown("/releases.md", args)
            }
        },
        "/sandbox": {
            "vars": {
                "title": "Sandbox",
                "meta_description": "Download an Elasticsearch development environment preloaded with zentity, analysis plugins, real data, and sample entity models.",
                "meta_description_social": META_DESCRIPTION_GENERIC_SHORT,
                "content": markdown("/sandbox.md", args)
            }
        }
    }

def wipe_build_dir():
    filepath = fullpath("/build")
    print(f"Wiping build directory: {filepath}")
    return shutil.rmtree(filepath)

def copy_assets_dir():
    filepath_from = fullpath("/assets")
    filepath_to = fullpath("/build")
    print(f"Copying assets from: {filepath_from}")
    return copy_tree(filepath_from, filepath_to)

def write_page(uri_path, content):
    filepath = fullpath(f"/build{uri_path}/index.html")
    # Ensure any subdirectories are created
    try:
        os.makedirs(os.path.dirname(filepath))
    except OSError as e:
        if e.errno == errno.EEXIST:
            pass
        else:
            raise
    print(f"Writing file: {filepath}")
    with codecs.open(filepath, "wb", "utf-8") as file:
        file.write(content)

def build_page(page, args={}):
    template = env.get_template(page.get("template", "base.html"))
    vars = copy.deepcopy(page["vars"])
    vars.update(args)
    vars.update({ "now": datetime.datetime.utcnow() })
    return env.get_template(template).render(**vars)

def build_pages(pages, args={}):
    for uri_path, page in pages.items():
        print(f"Building page: {uri_path}")
        content = build_page(page, args)
        write_page(uri_path, content)

def build(args={}):
    pages = PAGES(args)
    wipe_build_dir()
    copy_assets_dir()
    build_pages(pages, args)

if __name__ == "__main__":
    args = {}
    args["test"] = False
    args["latest"] = None
    for arg in sys.argv[1:]:
        if arg == "--test":
            args["test"] = True
        if arg.startswith("--latest="):
            args["latest"] = parse_latest_version(arg.split("=", 1)[1])
    if not args["latest"]:
        print("Missing required --latest argument")
        sys.exit(0)
    if not args["latest"]["zentity"]:
        print("Missing required zentity version in --latest argument")
        sys.exit(0)
    if not args["latest"]["elasticsearch"]:
        print("Missing required elasticsearch version --latest argument")
        sys.exit(0)
    args["sandbox"] = {
        "elasticsearch": SANDBOX_VERSION_ELASTICSEARCH,
        "zentity": SANDBOX_VERSION_ZENTITY
    }
    args["tutorial"] = {
        "elasticsearch": TUTORIAL_VERSION_ELASTICSEARCH,
        "zentity": TUTORIAL_VERSION_ZENTITY
    }
    print(args)
    build(args)
