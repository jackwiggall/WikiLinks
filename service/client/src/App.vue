<template>
  <div id="app" class="bg-dark">
      <div class="body">
          <div class="p-2 bg-info text-center">
            <h1>WikiLinks</h1>
          </div>

          <InputSrcDest @submit="findPath"/> <!--Input-->

          <ErrorMessage v-if="showErrorMessage" :message="errorMessage"/>
          <WikiPath v-if="showPath" :path="path" :info="info" :steps="steps"/> <!--Output-->

          <div v-if="showSpinner" class="text-center">
            <div id="spinner" class="spinner-border m-5 text-info text-center" role="status">
            </div>

          </div>


      </div>
    <footer class="bg-info text-center">
        <span>Made by: Elliot Scott, Michael Matthew, Jack Wiggall, Nicole Jackson, Bijoy Shah</span>
    </footer>
  </div>
</template>

<style>
  *{
    margin: 0;
    font-family: Georgia, serif;
    font-weight: lighter;
  }
  img {
    height: auto;
    width: 25%
  }
</style>

<style scoped>
  footer {
    position: fixed;
    bottom: 0;
    width: 100%;
    padding: 20px;
  }
  #spinner {
    width: 30vh;
    height: 30vh;
    font-size: 50px;
  }
</style>

<script>
import WikiPath from './components/WikiPath.vue'
import InputSrcDest from './components/InputSrcDest.vue'
import ErrorMessage from './components/ErrorMessage.vue'


import axios from 'axios'

import { API_LINK_PAGES } from './api_config.js'

var path = [];
var info = {};
var steps = 0;

var showPath = false
var showErrorMessage = false
var errorMessage = ""
var showSpinner = false

export default {
  name: 'App',
  components: {
    WikiPath,
    InputSrcDest,
    ErrorMessage
  },
  methods: {
    findPath: function(src, dest) {
      this.showErrorMessage = false // clear the errors as new submit
      this.showPath = false
      this.showSpinner = true // LOADING...
      axios.post(API_LINK_PAGES, {src: src, dest: dest})
      .then((res) => {
        this.showSpinner = false // LOADED
        const json = res.data;
        if (json.success) {
          // this.path is the variable above 'export default'
          this.path = json.path;
          this.info = json.info;
          this.steps = json.steps;
          this.showPath = true;
        } else {
          // pass to catch(err) function below
          throw {response: res}
        }
      })
      .catch((err) => {
        this.showSpinner = false // LOADED
        this.showErrorMessage = true; // display error message
        const json = err.response.data;
        if (json && json.success == false) { // error response data
          if (json.message === 'Wikipedia title not found') { // title not found
            if (json.notFoundField === 'src') {
              this.errorMessage = `The Wikipedia article "${src}" is not currently indexed in our database`
            } else {
              this.errorMessage = `The Wikipedia article "${dest}" is not currently indexed in our database`
            }
          } else if (json.message === "Search exhausted") {
            this.errorMessage = "No path found or our database is incomplete (probably the latter)"
          } else if (err.response.status === 500) { // server error
            this.errorMessage = "Server error :(";
          } else {
            this.errorMessage = "Error encountered, message: "+json.message
          }
        }
      })
    }
  },
  data() {
    return {
      path: path,
      info: info,
      steps: steps,
      showPath: showPath,
      showErrorMessage: showErrorMessage,
      errorMessage: errorMessage,
      showSpinner: showSpinner
    }
  }
}
</script>
