<template>
  <div id="app">
    <h1>App</h1>

    <InputSrcDest @submit="findPath"/>
    <WikiPath :path="path" :queryTime="queryTime" :steps="steps"/>

  </div>
</template>

<style scoped>
#app {
  background: lightblue;
}
</style>

<script>
import WikiPath from './components/WikiPath.vue'
import InputSrcDest from './components/InputSrcDest.vue'
import axios from 'axios'

import { API_LINK_PAGES_DEV } from './api_config.js'

var path = [];
var queryTime = 0;
var steps = 0;

var errDestNotFound = false
var errSrcNotFound = false
var errServerError = false

function resetErrors() {
  errDestNotFound = false
  errSrcNotFound = false
  errServerError = false
}

export default {
  name: 'App',
  components: {
    WikiPath,
    InputSrcDest
  },
  methods: {
    findPath: function(src, dest) {
      resetErrors(); // clear the errors as new submit
      axios.post(API_LINK_PAGES_DEV, {src: src, dest: dest})
      .then((res) => {
        const json = res.data;
        if (json.success) {
          // this.path is the variable above 'export default'
          this.path = json.path;
          this.queryTime = json.queryTime;
        } else {
          // pass to catch(err) function below
          throw {response: res}
        }
      })
      .catch((err) => {
        const json = err.response.data;
        if (json && json.success == false) { // error response data
          if (json.message === 'wikipedia title not found') { // title not found
            if (json.notFoundField === 'src')
              errSrcNotFound = true;
            else
              errDestNotFound = true;
          } else if (err.response.status === 500) { // server error
            errServerError = true;
          }
        }
      })
    }
  },
  data() {
    return {
      path: path,
      queryTime: queryTime,
      steps: steps,
      errDestNotFound: errDestNotFound,
      errSrcNotFound: errSrcNotFound,
      errServerError: errServerError
    }
  }
}
</script>

