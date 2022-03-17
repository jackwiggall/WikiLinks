<template>
  <div id="path"> 
    <h1>WikiPath</h1>
      <li v-for="(page, key) in path" :key="key">
          <WikiPage :title=page.title :url=page.url />
      </li>
  </div>

</template>


<style scoped>
#path {
  background: red;
}
  
</style>

<script>
import WikiPage from './WikiPage.vue'
// import axios from 'axios'

export default {
  name: 'WikiPath',
  props: [
    'path',
  ],
  components: {
    WikiPage
  },
}
// var test = "tes?t"
</script>