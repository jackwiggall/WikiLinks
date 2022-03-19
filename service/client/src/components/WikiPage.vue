<template>
  <ul id="page" class="bg-white">
    <a href="{{url}}">{{title}}</a>
  </ul>
</template>

<style scoped>
#page {
  
}
</style>

<script>
export default {
  name: 'WikiPage',
  props: [
    'title',
    'url'
  ]
}
</script>
