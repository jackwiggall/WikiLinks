<template>
  <div class="">
    {{index}} - <a :href="url">{{title}}</a>
  </div>
</template>

<style scoped>
</style>

<script>
export default {
  name: 'WikiPage',
  props: [
    'title',
    'url',
    'index'
  ]
}
</script>
