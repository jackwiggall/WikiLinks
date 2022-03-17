<template>
<div id="inputSrcDest">
  src
  <input v-model="src" type="text">
  dest
  <input v-model="dest" type="text">
  <input type="submit" @click="submit(src, dest)">
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
    submit: function(src, dest) {
      this.$emit('submit', src, dest)
    }
  },
  data() {
    return {
      src: "",
      dest: "",
    }
  }
}
</script>