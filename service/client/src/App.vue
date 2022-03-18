<template>
  <div id="app">
    <div class="body">
      <h1>WIkiLinks</h1>

      <InputSrcDest @submit="findPath" />
      <WikiPath :path="path" :queryTime="queryTime" :steps="steps"/>
    </div>
    <footer>
      <p>made by: Elliot, Michael, Jack, Nicole, Bijoy</p>
    </footer>
  </div>
</template>

<style>
  *{
    margin: 0;
    background: #E4CC8A;
    font-family: Georgia, serif;
    font-weight: lighter;
  }
</style>

<style scoped>
  p{
    padding:40px;
  }
  footer{
    position:absolute;
    bottom:0;
    width: 100%;


    background: #E7BB40;
    padding: 50px;
    padding-top: 100px;
  }
  h1{
    margin: 4px;
    padding-left: 10px;
    padding-top:10px;
    padding-bottom: 30px;
    background: #E7BB40;
  }
  .body {
    background:#E4CC8A;
    padding: 12px;
    margin: 0;
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
