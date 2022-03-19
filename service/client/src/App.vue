<template>
  <div id="app" class="bg-dark">
      <div class="body">
          <div class="p-3 mb-2 bg-info text-white">
            <img src="../html/logo.png" alt="WikiLinks" title="WikiLinks" />
          </div>	 <!--Banner-->

          <InputSrcDest @submit="findPath" style="margin:3%;" /> <!--Input-->
          <WikiPath :path="path" :queryTime="queryTime" :steps="steps" style="margin:3%;" /> <!--Output-->
      </div>
    <footer class="bg-info">
      <ul> <!--Credits-->
        <li>Made by:</li>
        <li>Elliot Scott</li> 
        <li>Michael Matthew</li>
        <li>Jack Wiggall</li> 
        <li>Nicole Jackson</li>
        <li>Bijoy Shah</li>
      </ul>
    </footer>
  </div>
</template>

<style>
  *{
    margin: 0;
    font-family: Georgia, serif;
    font-weight: lighter;
  }
  html {
      background-color: #383c44;
  }
  img {
    height: auto;
    width: 25%
  }
  footer li{
    display: inline;
    margin-right: 11%;
  }
  footer ul {
    width: 100%;
  }
</style>

<style scoped>
  footer{
    position:absolute;
    bottom:0;
    width: 100%;
    padding: 1%;
  }
  .body {
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
