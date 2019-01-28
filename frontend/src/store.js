import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    projects: [
      {
        "id": 1,
        "email": "lennard.berger@student.uni-tuebingen.de",
        "created_at": new Date(),
        "last_updated": new Date(),
        "status": "created"
      }
    ],
    filterForDate: null,
    filterForId: null
  },
  getters: {
    projects (state) {
      return state.projects
    }
  },
  mutations: {
    addProject (state, project) {
      state.projects.push(project)
    },
    addStatus (state, status) {
      let project = state.projects.find((p) => p.id === status.id)
      let index = state.projects.indexOf(project)
      state.projects[index] = {
        ...project,
        status: {
          ...status.status
        }
      }
    }
  }
})
