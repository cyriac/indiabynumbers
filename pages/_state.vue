<template>
  <div class="wrapper" v-bind:style="{'background-image': 'url(/images/geo/'+code.toLowerCase()+'.jpg)'}">
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
      <h2>HDI</h2>
      <pre><code>{{ hdi }}</code></pre>
      <h2>HIV AWARENESS</h2>
      <pre><code>{{ hiv_awareness }}</code></pre>
    </div>
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
</style>
