var renderer = new marked.Renderer();
renderer.code = function(code, lang) {
  return '<pre><code class="hljs ' + lang + '">' + hljs.highlight(lang, code).value + '</code></pre>';
};
renderer.link = function(href, title, text) {
  if (this.options.sanitize) {
    try {
      var prot = decodeURIComponent(unescape(href))
        .replace(/[^\w:]/g, '')
        .toLowerCase();
    } catch (e) {
      return text;
    }
    if (prot.indexOf('javascript:') === 0 || prot.indexOf('vbscript:') === 0 || prot.indexOf('data:') === 0) {
      return text;
    }
  }
  if (this.options.baseUrl && !originIndependentUrl.test(href)) {
    href = resolveUrl(this.options.baseUrl, href);
  }
  var out = '<a href="' + href + '"';
  if (title) {
    out += ' title="' + title + '"';
  }
  if (!href.startsWith("/") && !href.startsWith("https://zentity.io") && !href.startsWith("http://zentity.io"))
    out += ' onclick="to(\'' + href + '\');"';
  out += '>' + text + '</a>';
  return out;
}
renderer.table = function(header, body) {
  return '<table class="table">\n'
    + '  <thead>\n'
    +      header
    + '  </thead>\n'
    + '  <tbody>\n'
    +      body
    + '  </tbody>\n'
    + '</table>\n';
    + '</div>\n';
};
var http_config = {
  'headers': {
    'Cache-Control': "no-cache,no-store,must-revalidate,max-age=-1,private",
    'Expires': '-1',
    'Pragma': 'no-cache'
  }
};

const Home = {
  template: '<div id="home" v-html="marked(markdown, { renderer: renderer })"></div>',
  data() {
    return {
      markdown: ''
    }
  },
  methods: {
    get() {
      const component = this;
      var uri = '/docs/home.md?_timestamp=' + new Date().getTime();
      axios.get(uri, http_config)
        .then(function(response) {
          console.log(response);
          component.markdown = response.data;
        })
        .catch(function(error) {
          console.log(error);
        });
    }
  },
  created() {
    this.get();
  },
  beforeRouteUpdate(to, from, next) {
    this.get();
  }
};

const Docs = {
  template: '<div id="docs" v-html="marked(markdown, { renderer: renderer })"></div>',
  data() {
    return {
      markdown: ''
    }
  },
  methods: {
    get(page, section) {
      const component = this;
      if (!page)
        page = 'index';
      else if (!!section)
        page = page + '/' + section;
      var uri = '/docs/' + page + '.md?_timestamp=' + new Date().getTime();
      console.log(page);
      axios.get(uri, http_config)
        .then(function(response) {
          console.log(response);
          component.markdown = response.data;
        })
        .catch(function(error) {
          console.log(error);
        });
    }
  },
  created() {
    this.get(this.$route.params.page, this.$route.params.section);
  },
  watch: {
    '$route' (to, from) {
        this.get(to.params.page, this.$route.params.section);
    }
  }
};

const Releases = {
  template: '<div id="home" v-html="marked(markdown, { renderer: renderer })"></div>',
  data() {
    return {
      markdown: ''
    }
  },
  methods: {
    get() {
      const component = this;
      var uri = '/docs/releases.md?_timestamp=' + new Date().getTime();
      axios.get(uri, http_config)
        .then(function(response) {
          console.log(response);
          component.markdown = response.data;
        })
        .catch(function(error) {
          console.log(error);
        });
    }
  },
  created() {
    this.get();
  },
  beforeRouteUpdate(to, from, next) {
    this.get();
  }
};

const router = new VueRouter({
  routes: [
    { path: '/', component: Home },
    { path: '/docs', component: Docs },
    { path: '/docs/:page', component: Docs },
    { path: '/docs/:page/:section', component: Docs },
    { path: '/releases', component: Releases },
  ],
  scrollBehavior (to, from, savedPosition) {
    return { x: 0, y: 0 };
  }
});
router.afterEach((to, from) => {
  gtag('config', 'UA-27325874-2', {
    'page_path': to.fullPath
  });
})

const app = new Vue({
  router,
  watch: {
    '$route': function (route) {
      this.$router.push({ path: route.path });
    }
  }
}).$mount('#app');
