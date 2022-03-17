<template>
  <ul id="page">
    {{title}}
    {{url}}
  </ul>
</template>

<style scoped>
#page {
  background: #ECE4B7;
  
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
