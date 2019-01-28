<template>
  <v-app id="inspire" style="background: #fff">
    <v-toolbar color="blue" dark fixed app>
      <v-toolbar-title>metabiom</v-toolbar-title>
    </v-toolbar>
    <v-content>
      <v-container fluid fill-height>
        <v-layout
                justify-center
                align-top
        >
          <v-flex text-xs-center>
            <v-list light>
              <template v-for="(project) in $store.getters.projects">
                <project v-bind="project" v-bind:key="project.id" @startProject="startProject"></project>
              </template>
            </v-list>
          </v-flex>
        </v-layout>
      </v-container>
    </v-content>
    <v-btn
            fab
            bottom
            right
            color="pink"
            dark
            fixed
            @click="dialog = !dialog"
    >
      <v-icon>add</v-icon>
    </v-btn>
    <v-dialog v-model="dialog" width="800px">
      <v-card>
        <v-card-title
              class="grey lighten-4 py-4 title"
        >
          Create project
        </v-card-title>
        <v-container grid-list-sm class="pa-4">
          <v-layout row wrap>
            <v-flex xs6>
              <v-select
                      v-model="draft_project.probe_type"
                      :items="probe_types"
                      label="Probe type"
              ></v-select>
            </v-flex>
            <v-flex xs6>
              <v-text-field
                      v-model="draft_project.email"
                      prepend-icon="mail"
                      placeholder="Email"
              ></v-text-field>
            </v-flex>
            <v-flex xs12>
              <v-text-field
                      prepend-icon="notes"
                      placeholder="Notes"
              ></v-text-field>
            </v-flex>
          </v-layout>
        </v-container>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn flat color="primary" @click="dialog = false">Cancel</v-btn>
          <v-btn flat @click="createProject">Create</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-app>
</template>

<script>
const addr = "http://localhost:8000/v1/"
import Project from '@/components/Project.vue'

export default {
  name: 'App',
  components: {
    Project
  },
  data () {
    return {
      dialog: false,
      probe_types: [
        "Single",
        "Multiple"
      ],
      draft_project: {
        probe_type: "",
        email: ""
      }
    }
  },
  methods: {
    createProject () {
      let vm = this
      fetch(`${addr}/put`, {
        method: 'PUT',
        body: JSON.stringify(vm.draft_project)
      }).then((response) => response.json()).then((project) => {
        vm.$store.commit('addProject', project)
        vm.dialog = false
      })
    },
    startProject (id) {
      let vm = this
      fetch(`${addr}/project/${id}/start`, { // start job
        method: 'PATCH'
      }).then((response) => {
        console.debug(response.status) // eslint-disable-line
        return Promise.resolve()
      }).then(() => { // update status
        fetch(`${addr}/status/${id}`).then((response) => response.json()).then((status) => {
          vm.$store.commit('addStatus', status)
        })
      })
    }
  },
  mounted () {
    let vm = this

    if (window.webpackHotUpdate) {
      vm.$store.commit('addProject', {
        "id": 1,
        "email": "lennard.berger@student.uni-tuebingen.de",
        "created_at": new Date(),
        "last_updated": new Date(),
      })
      vm.$store.commit('addStatus', {
        "id": 1,
        "status": "created"
      })
    } else {
      fetch(`${addr}/project`).then((response) => response.json()).then((projects) => { // fetch projects
        return Promise.resolve(vm.$store.commit('addProjects', projects))
      }).then(() => fetch(`${addr}/status`)).then((response) => response.json()).then((result) => { // fetch status
        result.forEach((status) => {
          vm.$store.commit('addStatus', status)
        })
      })
    }
  }
}
</script>
