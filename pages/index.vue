<template>
  <div class="wrapper">
    <div class="container">
      <div class="row">
        <div class="col-md-12">
          <h1>India by the numbers!</h1>
          <div v-if="states">
            <div class="row">
              <div class="col-md-6">
                <div class="btn-group" role="group">
                  <button type="button" class="btn" v-bind:class="{'btn-primary': statefilter == '', 'btn-outline-primary': statefilter != ''}" @click="statefilter=''">All</button>
                  <button type="button" class="btn" v-bind:class="{'btn-primary': statefilter == 'state', 'btn-outline-primary': statefilter != 'state'}" @click="statefilter='state'">States</button>
                  <button type="button" class="btn" v-bind:class="{'btn-primary': statefilter == 'Union territory', 'btn-outline-primary': statefilter != 'Union territory'}" @click="statefilter='Union territory'">Union Territories</button>
                </div>
              </div>
              <div class="col-md-6">
                <form class="form-inline">
                  <input type="text" id="search_states" class="form-control mx-sm-3" placeholder="Search" v-model="searchstates">
                </form>
              </div>
            </div>
            <hr class="invisible"/>
            <div class="card-columns">
              <nuxt-link v-for="state in list_states" class="card" :key="state.id" :to="'/'+state.code.toLowerCase()" :style="{ 'background-image': 'url(/images/geo/thumb/' + state.code.toLowerCase() + '.jpg)' }">
                {{ state.subdivision_name }}
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
      searchstates: '',
      statefilter: ''
    }
  },
  async asyncData ({ params }) {
    let { data } = await axios.get(`/json/states_level/states.json`)
    return { states: data }
  },
  computed: {
    list_states () {
      var self = this
      return this.states.filter(function (s) {
        var sname = s.subdivision_name.toLowerCase().replace(' ', '')
        var search = self.searchstates.toLowerCase().replace(' ', '')
        if (self.statefilter !== '' && self.statefilter !== s.subdivision_category) {
          return false
        }
        return sname.indexOf(search) !== -1
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
