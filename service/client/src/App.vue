<template>
  <div id="app">


    <div class="body">

          <h1>WIkiLinks</h1>

          <InputSrcDest />
          <WikiPath v-bind:path="[{title: 'God', url: 'wikipedia.com/god'}, {title: 'Elliot', url: 'wiki.com/smelliot'}]" />
    </div>
    <footer>
      <p>made by: Elliot, michael, Jack, Nicole, Bijoy</p>
    </footer>
  </div>
</template>
<style>
*{
  margin: 0;
  background: #E4CC8A;
  font-family: Georgia, serif;
  font-weight: lighter;
}
</style>

<style scoped>


p{
  padding:40px;
}
footer{
  position:absolute;
  bottom:0;
  width: 100%;


  background: #E7BB40;
  padding: 50px;
  padding-top: 100px;
}
h1{
  margin: 4px;
  padding-left: 10px;
  padding-top:10px;
  padding-bottom: 30px;
  background: #E7BB40;
}
.body {
  background:#E4CC8A;
  padding: 12px;
  margin: 0;
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
