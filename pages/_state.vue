<template>
  <div class="container">
    <h1>{{ subdivision_name }}</h1>
    <h2>ID</h2>
    <pre><code>{{id}}</code></pre>
    <h2>CODE</h2>
    <pre><code>{{ code }}</code></pre>
    <h2>STATE</h2>
    <pre><code>{{ states }}</code></pre>
    <h2>AREA</h2>
    <pre><code>{{ area }}</code></pre>
    <h2>POPULATION</h2>
    <pre><code>{{ population }}</code></pre>
  </div>
</template>


<script>
import axios from 'axios'

export default {
  async asyncData ({ params }) {
    let { data } = await axios.get(`http://localhost:3000/json/${params.state}.json`)
    return data
  }
}
</script>

<style lang="scss">
body {
  background: white center center no-repeat;
  background-size: cover;
}
h1 {
  padding: 100px 0;
}
</style>
