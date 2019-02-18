<template>
  <v-layout
    justify-center
    align-top
  >
  <v-flex text-xs-center>
    <v-list light>
      <template v-for="(sample) in $store.getters.samples">
        <sample v-bind="sample" v-bind:key="sample.id"></sample>
      </template>
    </v-list>
  </v-flex>
  </v-layout>
</template>

<script>
const addr = "http://localhost:4010/v1/"
import Sample from '@/components/Sample.vue'

export default {
  name: 'samples',
  components: {
    Sample
  },
  mounted () {
    let vm = this
    if (window.webpackHotUpdate) {
      vm.$store.commit('addSamples', [{
        "id": 1,
        "email": "lennard.berger@student.uni-tuebingen.de",
        "created_at": new Date(),
        "last_updated": new Date(),
      }])
      vm.$store.commit('addStatus', {
        "id": 1,
        "status": "created"
      })
    } else {
      fetch(`${addr}/samples`).then((response) => response.json()).then((projects) => { // fetch projects
        return Promise.resolve(vm.$store.commit('addSamples', projects))
      }).then(() => fetch(`${addr}/status`)).then((response) => response.json()).then((result) => { // fetch status
        result.forEach((status) => {
          vm.$store.commit('addStatus', status)
        })
      })
    }
  }
}
</script>
