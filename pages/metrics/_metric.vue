<template>
  <div class="wrapper">
    <div class="container">
      <h1>{{ metric.toUpperCase() }}</h1>
      <code>
        {{ data }}
      </code>
    </div>
  </div>
</template>


<script>
import axios from '~/plugins/axios'

export default {
  async asyncData ({ params }) {
    let { data } = await axios.get(`/json/metrics_level/${params.metric}.json`)
    return {
      'data': data,
      'metric': params.metric
    }
  }
}
</script>

<style lang="scss">
</style>
