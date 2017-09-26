<template>
  <div class="container">
    <h1>India by the numbers!</h1>
    <div v-if="states">
      <form class="form-inline">
        <input type="text" id="search_states" class="form-control mx-sm-3" placeholder="Search states" v-model="searchstates">
      </form>
      <hr class="invisible"/>
      <div class="card-columns">
        <nuxt-link v-for="state in list_states" class="card" :key="state.id" :to="'/'+state.code.toLowerCase()" :style="{ 'background-image': 'url(/images/geo/' + state.code.toLowerCase() + '.jpg)' }">
          {{ state.subdivision_name }}
        </nuxt-link>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data () {
    return {
      searchstates: ''
    }
  },
  async asyncData ({ params }) {
    let { data } = await axios.get(`http://localhost:3000/json/states.json`)
    return { states: data }
  },
  computed: {
    list_states () {
      var self = this
      return this.states.filter(function (s) {
        var sname = s.subdivision_name.toLowerCase().replace(' ', '')
        var search = self.searchstates.toLowerCase().replace(' ', '')
        return sname.indexOf(search) !== -1
      })
    }
  }
}
</script>

<style lang="scss">
body {
  background: white url('/images/geo/in.jpg') center center no-repeat fixed;
  background-size: cover;
}
body::before {
  position: fixed;
  right: 0;
  left: 0;
  top: 0;
  display: block;
  height: 100%;
  content: "";
  background: linear-gradient(hsla(0, 0%, 100%, .1), hsla(0, 0%, 100%, 1) 50%, #fff);
  z-index: 1;
}
.container {
  position: relative;
  z-index: 100;
}
h1 {
  padding: 100px 0;
}
.form-inline {
  justify-content: flex-end;
  input {
    margin: 0 !important;
  }
}
.card-columns {
  column-count: 4;
  -webkit-column-count: 4;
}
.card {
  padding: 40px;
  display: inline-block;
  text-align: center;
  background: #333 center center no-repeat;
  background-size: cover;
  color: white;
  &:hover, &:active {
    color: white;
  }
}
</style>
