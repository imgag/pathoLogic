<template>
  <v-layout
    justify-center
    align-top
  >
  <v-flex text-xs-center>
    <v-data-table
      :headers="headers"
      :items="$store.getters.samples"
    >
      <template slot="items" slot-scope="props">
        <td>{{ props.item.id }}</td>
        <td>{{ props.item.author_email }}</td>
        <td>{{ props.item.created }}</td>
        <td>{{ props.item.last_updated }}</td>
        <td><status :status="props.item.status"></status></td>
      </template>
    </v-data-table>
  </v-flex>
  </v-layout>
</template>

<script>
import Status from '@/components/Status'
const addr = "http://localhost:4010/v1/"

export default {
  name: 'samples',
  components: {
    Status,
  },
  data () {
    return {
      headers: [
        {
          text: 'Sample ID',
          align: 'left',
          sortable: true,
          value: 'id'
        },
        {
          text: 'Author email',
          align: 'left',
          sortable: true,
          value: 'author_email'
        },
        {
          text: 'Created',
          align: 'left',
          sortable: true,
          value: 'created'
        },
        {
          text: 'Last updated',
          align: 'left',
          sortable: true,
          value: 'last_updated'
        },
        {
          text: 'Status',
          align: 'left',
          sortable: true,
          value: 'status'
        }
      ]
    }
  },
  mounted () {
    let vm = this
    if (window.webpackHotUpdate) {
      vm.$store.commit('addSamples', [{
        "id": 1,
        "author_email": "lennard.berger@student.uni-tuebingen.de",
        "created": new Date().toISOString(),
        "last_updated": new Date().toISOString(),
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
