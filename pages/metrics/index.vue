<template>
  <div class="wrapper">
    <div class="container">
      <div class="row">
        <div class="col-md-12">
          <h1>India by the numbers!</h1>
          <div v-if="metrics">
            <hr class="invisible"/>
            <div class="card-columns">
              <input type="text" id="search_states" class="form-control mx-sm-3" placeholder="Search" v-model="searchmetrics">
              <nuxt-link v-for="(metric, index) in metrics_list" class="card" :key=index :to="'/metrics/'+metric">
                {{ metric }}
              </nuxt-link>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from '~/plugins/axios'

export default {
  data () {
    return {
      searchmetrics: ''
    }
  },
  async asyncData ({ params }) {
    let { data } = await axios.get(`/json/metrics_level/metrics_list.json`)
    return { metrics: data }
  },
  computed: {
    metrics_list () {
      var self = this
      return this.metrics.filter(function (s) {
        var valuename = s.toLowerCase().replace(' ', '')
        var search = self.searchmetrics.toLowerCase().replace(' ', '')
        return valuename.indexOf(search) !== -1
      })
    }
  }
}
</script>

<style lang="scss">
.wrapper {
  background-image: url('/images/geo/in.jpg');
}
.form-inline {
  justify-content: flex-end;
  input {
    margin: 0 !important;
  }
}
.card-columns {
  -webkit-column-count: 4;
  column-count: 4;
  overflow: visible;
  @media (max-width: 992px) {
    -webkit-column-count: 3;
    column-count: 3;
  }
  @media (max-width: 768px) {
    -webkit-column-count: 2;
    column-count: 2;
  }
  @media (max-width: 576px) {
    -webkit-column-count: 1;
    column-count: 1;
  }
}
.card {
  margin-top: 1px;
  padding: 55px;
  display: inline-block;
  text-align: center;
  background: #333 center center no-repeat;
  background-size: cover;
  color: white;
  font-weight: bold;
  font-size: 20px;
  border: 0;
  text-shadow: 1px 0px 3px #333;
  transition: all 60ms ease-in-out;
  box-shadow: 0 1px 1px 0 rgba(0,0,0,.1), 0 1px 5px 0 rgba(0,0,0,.1);
  &:hover, &:active {
    color: white;
    box-shadow: 0 7px 14px rgba(50,50,93,.15), 0 3px 6px rgba(0,0,0,.15);
    transform: translateY(-1px);
  }
  @media (max-width: 576px) {
    width: 100%;
  }
}
</style>
