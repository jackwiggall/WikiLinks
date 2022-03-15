<template>
  <div id="app">
    <h1>App</h1>

    <InputSrcDest />
    <WikiPath v-bind:path="[{title: 'God', url: 'wikipedia.com/god'}, {title: 'Elliot', url: 'wiki.com/smelliot'}]" />

  </div>
</template>

<style scoped>
#app {
  background: lightblue;
}
</style>

<script>
import WikiPath from './components/WikiPath.vue'
import InputSrcDest from './components/InputSrcDest.vue'
export default {
  name: 'App',
  components: {
    WikiPath,
    InputSrcDest
  }
}
</script>

