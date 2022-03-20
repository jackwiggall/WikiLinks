<template>
  <div id="inputSrcDest" class="p-4 mt-3 bg-light rounded container">
    <dir class="row">
      <div id="inputSrc" class="form-group col-lg">
        <label>Start Article</label>
        <input
          v-model="src"
          @keyup.enter="submit(src, dest)"
          placeholder="Univerity Of Dundee"
          type="text"
          class="form-control"
        >
      </div>
      <div id="inputDest" class="container col-lg">
        <label>End Article</label>
        <input
          v-model="dest"
          @keyup.enter="submit(src, dest)"
          placeholder="Aberdeen"
          type="text"
          class="form-control"
        >
      </div>
      <div id="submit" container="col-lg btn-block">
        <button type="submit" @click="submit(src, dest)" class="btn btn-primary btn-lg mt-2 ml-4">Submit Query</button>
      </div>
    </dir>
  </div>
</template>

<style scoped>
  *{
    font-family: Georgia, serif;
    font-weight: lighter;
  }
  p {
    display: inline;
    margin-right: 5px;
  }
  input[type=text] {
    width: 300px; 
  }
  #inputSrcDest {
    display: flex;
    justify-content: center;
    font-family: Georgia, serif;
    font-weight: lighter;
    font-size: 20px;
  }
  #submit {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
  }
</style>

<script>
export default {
  name: 'InputSrcDest',
  props: [

  ],
  methods: {
    submit: function(src, dest) {
      if (src && dest)
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
