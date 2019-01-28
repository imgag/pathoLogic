import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    projects: [],
    filterForDate: null,
    filterForId: null
  },
  getters: {
    projects (state) {
      return state.projects
    }
  },
  mutations: {
    addProjects (state, projects) {
      state.projects = projects
    },
    addProject (state, project) {
      state.projects.push(project)
    },
    addStatus (state, status) {
      let project = state.projects.find((p) => p.id === status.id)
      let index = state.projects.indexOf(project)
      state.projects[index] = {
        ...project,
        status: status.status
      }
    }
  }
})
