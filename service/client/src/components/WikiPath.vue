<template>
  <div id="path" class="p-3 mt-5 mt-5 bg-light rounded">
    <h1>WikiPath</h1>
      <li v-for="(page, key) in path" :key="key">
          <WikiPage :title=page.title :url=page.url />
      </li>
    {{steps}}
    {{queryTime}}
  </div>

</template>


<style scoped>
#path {
  padding: 1%;
}
li{
  list-style-type: none;
  padding: 1%;
}
</style>

<script>
import WikiPage from './WikiPage.vue'
// import axios from 'axios'

export default {
  name: 'WikiPath',
  props: [
      'path',
      'steps',
      'queryTime',
  ],
  components: {
    WikiPage
  },
}
</script>