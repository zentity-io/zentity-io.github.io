var renderer = new marked.Renderer();
renderer.code = function(code, lang) {
  return '<pre><code class="hljs ' + lang + '">' + hljs.highlight(lang, code).value + '</code></pre>';
};
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
      axios.get('/docs/home.md')
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
      console.log(page);
      axios.get('/docs/' + page + '.md')
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
      axios.get('/docs/releases.md')
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
