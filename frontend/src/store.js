const OAuth = require('@zalando/oauth2-client-js')
import fetchDefaults from 'fetch-defaults'
import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

const REALM = (process.env.VUE_APP_AUTH_REALM !== undefined && process.env.VUE_APP_AUTH_REALM.length) ? process.env.VUE_APP_AUTH_REALM : 'debug'
const DOMAIN = (process.env.VUE_APP_AUTH_DOMAIN !== undefined) ? process.env.VUE_APP_AUTH_DOMAIN : 'https://auth.imgag.de'
const AUTHORIZATION_URL = `${DOMAIN}/auth/realms/${REALM}/protocol/openid-connect/auth`
const LOGOUT_URL = `${AUTHORIZATION_URL.substring(0, AUTHORIZATION_URL.length - 4)}logout?redirect_uri=${encodeURI(window.origin)}`

let _access_token = null;
if (window.location.hash.startsWith('#state')) { // indicates that we are processing a redirected application
  try {
    let response = new OAuth.Provider({
      id: 'keycloak',
      authorization_url: AUTHORIZATION_URL
    }).parse(window.location.hash)
    _access_token = response.access_token
    window.history.pushState(null, null, '/') // redirect the user back to the initial page
  } catch (err) {
    console.error(err) // eslint-disable-line no-console
  }
} else { // request login
  let request = new OAuth.Request({
    client_id: 'account',
    redirect_uri: location.origin
  })
  let provider = new OAuth.Provider({
    id: 'keycloak',
    authorization_url: AUTHORIZATION_URL
  })

  let uri = provider.requestToken(request)
  provider.remember(request)
  window.location.href = uri // redirect to OAuth provider
}

export default new Vuex.Store({
  state: {
    samples: [],
    sample_filter_by_ids: [],
    access_token: _access_token,
    logout_url: LOGOUT_URL
  },
  getters: {
    fetch_defaults(state) {
      return fetchDefaults(fetch, {
        headers: {Authorization: `Bearer ${state.access_token}`}
      })
    },
    samples (state) {
      return (state.sample_filter_by_ids.length) ? state.samples.filter((s) => {
        return state.sample_filter_by_ids.includes(s.id)
      }) : state.samples
    },
    sample_ids (state) {
      return state.samples.map((s) => s.id)
    }
  },
  mutations: {
    deleteSample (state, id) {
      let sample = state.samples.find((s) => s.id === id)
      let index = state.samples.indexOf(sample)
      state.samples.splice(index, 1)
    },
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
