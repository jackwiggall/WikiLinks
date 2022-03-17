<template>
  <div id="inputSrcDest">
    <div id="inputSrc">
      src
      <input v-model="src" type="text" style="background: #E7BB40;">
    </div>
    <div id="inputDest">

    dest
    <input v-model="dest" type="text" style="background: #E7BB40;">
    </div>
    <input type="submit"  @click="submit" style="background: #E7BB40;">
  </div>
  </template>

  <style scoped>
  *{
    font-family: Georgia, serif;
    font-weight: lighter;
  }
  #inputSrc{
    padding-right: 50px;
  }
  #inputDest{
    padding-right: 50px;
  }

  #inputSrcDest {
  background: #E4CC8A;
  display: flex;
  justify-content: center;
  font-family: Georgia, serif;
  font-weight: lighter;
  font-size: 20px;
  padding: 40px;

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
