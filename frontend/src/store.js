import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    samples: [],
    sample_filter_by_ids: []
  },
  getters: {
    samples (state) {
      return (state.sample_filter_by_ids.length) ? state.samples.filter((s) => {
        return state.sample_filter_by_ids.includes(s.id)
      }) : state.samples
    },
    sample_ids (state) {
      return state.samples.map((s) => s.id)
    },
    author_emails (state) {
      return new Set(state.samples.map((s) => s.author_email))
    }
  },
  mutations: {
    addSamples (state, samples) {
      state.samples = samples
    },
    addStatus (state, status) {
      let sample = state.samples.find((s) => s.id === status.id)
      let index = state.samples.indexOf(sample)
      state.samples.splice(index, 1, { ...sample, status: status.status })
    },
    updateFilterIDs (state, ids) {
      state.sample_filter_by_ids = ids
    }
  }
})
