<template>
  <div class="p-3 mt-2 bg-light rounded container">
    <span>
      Path found in {{queryTime}}ms, minumum of {{steps}} step{{steps > 1 ? 's' : '' }} to reach destination
    </span>
      <div v-for="(page,index) in path" :key="page.title">
        <WikiPage :title="page.title" :url="page.url" :index="index" />
      </div>
  </div>

</template>


<style scoped>
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