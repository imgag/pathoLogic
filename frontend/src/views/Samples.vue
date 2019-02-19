<template>
  <v-layout
    justify-center
    align-top
  >

  <v-flex
    xs20
    mr-2
  >
  <v-autocomplete
      v-model="filter_ids"
      :multiple="true"
      hint="Filter by sample id"
      :items="$store.getters.sample_ids"
      persistent-hint
  />
  </v-flex>

  <v-flex xs12>
    <v-data-table
      :headers="headers"
      :items="$store.getters.samples"
    >
      <template slot="items" slot-scope="props">
        <td v-if="props.item.status === 'finished'">
          <router-link :to="{ name: 'result', params: { id: props.item.id } }">{{ props.item.id }}</router-link>
        </td>
        <td v-else>{{ props.item.id }}</td>
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
      ],
      filter_ids: []
    }
  },
  watch: {
    filter_ids () {
      this.$store.commit('updateFilterIDs', Object.values(this.filter_ids))
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
        "status": "finished"
      })
    } else {
      fetch(`${process.env.ADDR}/samples`).then((response) => response.json()).then((projects) => { // fetch projects
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
