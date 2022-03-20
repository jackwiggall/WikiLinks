<template>
  <div class="bg-warning container mt-4 p-3 ">
    <span>
      ERROR:
      {{message}}
    </span>
  </div>
</template>

<style scoped>
</style>

<script>
export default {
  name: 'ErrorMessage',
  props: [
    'message'
  ]
}
</script>
