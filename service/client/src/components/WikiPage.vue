<template>
  <ul id="page">
    {{title}}
    {{url}}
  </ul>
</template>

<style scoped>
#page {
  background: green;
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