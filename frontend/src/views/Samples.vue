<template>
  <v-layout
    justify-center
    align-top
  >

  <v-data-table
    :headers="headers"
    :items="$store.getters.samples"
  >
    <error-modal :active="statusChangeFailed"></error-modal>
    <template slot="items" slot-scope="props">
      <td v-if="props.item.status === 'finished'">
        <router-link :to="{ name: 'result', params: { id: props.item.id } }">{{ props.item.id }}</router-link>
      </td>
      <td v-else>{{ props.item.id }}</td>
      <td>{{ props.item.created }}</td>
      <td>{{ props.item.last_updated }}</td>
      <td><status :status="props.item.status"></status></td>
      <td v-if="props.item.status === 'created'">
        <v-checkbox @change="updateSelectedSample(props.item.id, $event)"/>
      </td>
      <td v-else/>
    </template>
    <template slot="footer">
    <td colspan="3">
      <v-autocomplete
        v-model="filter_ids"
        :multiple="true"
        hint="Filter by sample id"
        :items="$store.getters.sample_ids"
        persistent-hint
      />
    </td>
    <td colspan="1">

    </td>
    <td colspan="1">
      <v-btn :disabled="selected_samples.length < 1" @click="startSamples">Start sample(s)</v-btn>
    </td>
  </template>
  </v-data-table>
  </v-layout>
</template>

<script>
import Status from '@/components/Status'
import ErrorModal from '@/components/ErrorModal'

export default {
  name: 'samples',
  components: {
    Status,
    ErrorModal
  },
  data () {
    return {
      selected_samples: [],
      statusChangeFailed: false,
      headers: [
        {
          text: 'Sample ID',
          align: 'left',
          sortable: true,
          value: 'id'
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
        },
        {
          text: 'Selected',
          align: 'left',
          sortable: false,
          value: 'selected'
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
  methods: {
    updateSelectedSample (id, event) {
      if (event) {
        if (!this.selected_samples.includes(id)) this.selected_samples.push(id)
      } else {
        this.selected_samples = this.selected_samples.filter((s) => s !== id)
      }
    },
    startSamples () {
      let vm = this

      vm.$store.getters.fetch_defaults(`${vm.$basePath}/samples/${vm.selected_samples.join(',')}/start`, {
        method: 'PUT'
      }).then((response) => {
        let status = ""
        if (response.status === 200) {
          status = "started"
        } else {
          status = "error"
          vm.statusChangeFailed = true
        }

        vm.selected_samples.forEach((sample) => {
          vm.$store.commit('addStatus', { "id": sample, "status": status })
        })
      }).catch(() => vm.statusChangeFailed = true)
    }
  },
  mounted () {
    let vm = this
      vm.$store.getters.fetch_defaults(`${vm.$basePath}/samples`).then((response) => response.json()).then((projects) => { // fetch projects
        return Promise.resolve(vm.$store.commit('addSamples', projects))
      }).then(() => vm.$store.getters.fetch_defaults(`${vm.$basePath}/status`)).then((response) => response.json()).then((result) => { // fetch status
        result.forEach((status) => {
          vm.$store.commit('addStatus', status)
        })
      })
    }
}
</script>
