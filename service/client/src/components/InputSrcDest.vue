<template>
  <div id="inputSrcDest" class="p-4 mt-5 bg-light rounded" >
    <div id="inputSrc">
      src
      <input v-model="src" type="text" class="bg-white">
    </div>
    <div id="inputDest">
      dest
      <input v-model="dest" type="text" class="bg-white">
    </div>
    <input type="submit" @click="submit(src, dest)" class="bg-white">
  </div>
  </template>

<style scoped>
  *{
    font-family: Georgia, serif;
    font-weight: lighter;
  }
  #inputSrc, #inputDest{
    padding-right: 2%;
  }
  input[type=text] {
    width: 70%; 
  }
  #inputSrcDest {
    display: flex;
    justify-content: center;
    font-family: Georgia, serif;
    font-weight: lighter;
    font-size: 20px;
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
