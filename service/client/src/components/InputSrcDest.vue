<template>
<div id="inputSrcDest">
  src
  <input v-model="src" type="text">
  dest
  <input v-model="dest" type="text">
  <input type="submit"  @click="submit">
</div>
</template>

<style scoped>
#inputSrcDest {
  background: grey;
}
</style>

<script>
export default {
  name: 'InputSrcDest',
  props: [
    
  ],
  methods: {
    submit: function() {
      console.log("submit");
    }
  }
}
</script>