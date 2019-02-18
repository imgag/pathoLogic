import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    samples: [],
    filterForDate: null,
    filterForId: null
  },
  getters: {
    samples (state) {
      return state.samples
    }
  },
  mutations: {
    addSamples (state, samples) {
      state.samples = samples
    },
    addStatus (state, status) {
      let sample = state.samples.find((s) => s.id === status.id)
      let index = state.samples.indexOf(sample)
      state.samples[index] = {
        ...sample,
        status: status.status
      }
    }
  }
})
