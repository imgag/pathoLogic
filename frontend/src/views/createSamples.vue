<template>
  <v-layout
    justify-center
    align-start
  >
    <error-modal :active="submissionFailed" @close="submissionFailed = false" :errorMessage="submissionError" v-if="submissionError.length"></error-modal>
    <error-modal :active="submissionFailed" @close="submissionFailed = false" v-else></error-modal>
    <v-form v-model="valid_config">
      <v-flex>
      <h2>Configuration</h2>
      </v-flex>
      <v-layout
          ma-3
          column>
        <v-flex
          xs2
        >
          <v-select
            v-model="config.mode"
            :items="modes"
            hint="Assembly methods"
            :persistent-hint="true"
            solo
          />
        </v-flex>

        <v-flex
          xs2
        >
          <v-switch
            v-model="advanced_options"
            hint="show advanced options"
            :persistent-hint="true"
          >
          </v-switch>
        </v-flex>
      </v-layout>
      <v-divider></v-divider>
      <v-layout
          v-if="advanced_options"
          ma-3
          column
      >
      <v-flex >
      <h3>Advanced options</h3>
      </v-flex>
      <v-layout
        row
      >
        <v-flex xs6>
          <v-slider
            v-model="config.minContigLength"
            min=1
            max=1000000
            hint="Length curoff for contigs in final result"
            :persistent-hint="true"
            :thumb-label="true"
          />
        </v-flex>
        <v-flex xs2 ml-5>
          <v-text-field
            v-model="config.minContigLength"
            min=1
            max=1000000
            type="number"
            class="mt-0"
          />
        </v-flex>
      </v-layout>
      <v-layout
        row
      >
        <v-flex xs6>
          <v-slider
            v-model="config.targetShortReadCov"
            min=1
            max=200
            hint="Target long read coverage after subsampling"
            :persistent-hint="true"
            :thumb-label="true"
          />
        </v-flex>
        <v-flex xs2 ml-5>
          <v-text-field
            v-model="config.targetShortReadCov"
            min=1
            max=200
            type="number"
            class="mt-0"
          />
        </v-flex>
      </v-layout>
      <v-layout
        row
      >
        <v-flex xs6>
          <v-slider
            v-model="config.targetLongReadCov"
            min=1
            max=200
            hint="Target long read coverage after subsampling"
            :persistent-hint="true"
            :thumb-label="true"
          />
        </v-flex>
        <v-flex xs2 ml-5>
          <v-text-field
            v-model="config.targetLongReadCov"
            min=1
            max=200
            type="number"
            class="mt-0"
          />
        </v-flex>
      </v-layout>
      <v-layout
        row
      >
        <v-flex xs6>
          <v-slider
            v-model="config.genomeSize"
            min=1
            max=10000000
            hint="Estimated approximate final genome size of assembled bacteria. Used for coverage calculations"
            :persistent-hint="true"
            :thumb-label="true"
          />
        </v-flex>
        <v-flex xs2 ml-5>
          <v-text-field
            v-model="config.genomeSize"
            min=1
            max=10000000
            type="number"
            class="mt-0"
          />
        </v-flex>
      </v-layout>
      <v-layout
        row
      >
        <v-flex xs6>
          <v-slider
            v-model="config.seqPadding"
            min=1
            max=10000
            hint="Number of bases added at sequence ends to improve alignment quality in plasmid identification"
            :persistent-hint="true"
            :thumb-label="true"
          />
        </v-flex>
        <v-flex xs2 ml-5>
          <v-text-field
            v-model="config.seqPadding"
            min=1
            max=10000
            type="number"
            class="mt-0"
          />
        </v-flex>
      </v-layout>
      <v-layout
        row
      >
        <v-flex xs6>
          <v-slider
            v-model="config.covWindow"
            min=20
            max=5000
            hint="Window size for coverage calculation"
            :persistent-hint="true"
            :thumb-label="true"
          />
        </v-flex>
        <v-flex xs2 ml-5>
          <v-text-field
            v-model="config.covWindow"
            min=20
            max=5000
            type="number"
            class="mt-0"
          />
        </v-flex>
      </v-layout>
      <v-layout>
        <v-flex xs6>
          <v-slider
                  v-model="config.mappingCov"
                  min=20
                  max=200
                  hint="Target average mean coverage"
                  :persistent-hint="true"
                  :thumb-label="true"
          />
        </v-flex>
        <v-flex xs2 ml-5>
          <v-text-field
                  v-model="config.mappingCov"
                  min=20
                  max=200
                  type="number"
                  class="mt-0"
          />
        </v-flex>
      </v-layout>
      <v-layout>
        <v-flex xs6>
          <v-slider
                  v-model="config.minContigLength"
                  min=2000
                  max=1000000
                  hint="Minimum contig length considered plasmid search"
                  :persistent-hint="true"
                  :thumb-label="true"
          />
        </v-flex>
        <v-flex xs2 ml-5>
          <v-text-field
                  v-model="config.minContigLength"
                  min=2000
                  max=1000000
                  type="number"
                  class="mt-0"
          />
        </v-flex>
      </v-layout>
      <v-layout>
        <v-flex xs6>
          <v-slider
                  v-model="config.maxLength"
                  min=2000
                  max=1000000
                  hint="Maximum contig length considered plasmid search"
                  :persistent-hint="true"
                  :thumb-label="true"
          />
        </v-flex>
        <v-flex xs2 ml-5>
          <v-text-field
                  v-model="config.maxLength"
                  min=2000
                  max=1000000
                  type="number"
                  class="mt-0"
          />
        </v-flex>
      </v-layout>
    </v-layout>
      <v-layout>
        <v-flex
          xs12
          mt-2
          mb-2
        >
          <h2>Samples</h2>
        </v-flex>
      </v-layout>

      <v-layout mb-2>
        <v-flex xs-12>
          <div class="dashboard"></div>
        </v-flex>
      </v-layout>

      <v-layout>
        <v-flex
          xs-1
          mr-1
        >
          <v-btn left @click="addSample">Add new sample</v-btn>
        </v-flex>
        <v-flex
          xs-1
          mr-1
        >
          <v-btn right :disabled="!valid_config || !this.samples.length || duplicate_samples()" @click="saveSamples">Save samples</v-btn>
        </v-flex>
      </v-layout>

      <v-data-table
        :headers="headers"
        :items="samples"
      >
      <template slot="items" slot-scope="props">
        <td>
            <v-text-field
                :value="props.item.id"
                @change="props.item.id = $event"
            ></v-text-field>
        </td>
        <td>
          <v-select
              clearable
              v-model="props.item.path_lr"
              :items="available_files"
          ></v-select>
        </td>
        <td>
          <v-select
              clearable
              v-model="props.item.path_sr1"
              :items="available_files"
          ></v-select>
        </td>
        <td>
          <v-select
              clearable
              v-model="props.item.path_sr2"
              :items="available_files"
          ></v-select>
        </td>
      </template>
      </v-data-table>
    </v-form>
  </v-layout>
</template>

<script>
const Uppy = require('@uppy/core')
const XHRUpload = require('@uppy/xhr-upload')
const Dashboard = require('@uppy/dashboard')
import ErrorModal from '@/components/ErrorModal'

require('@uppy/core/dist/style.css')
require('@uppy/dashboard/dist/style.css')

export default {
  name: 'createSample',
  components: {
    ErrorModal
  },
  data () {
    return {
      available_files: [],
      headers: [
        {
          text: 'Sample ID',
          align: 'left',
          sortable: true,
          value: 'id'
        },
        {
          text: 'Path long read',
          sortable: false,
          value: 'path_lr'
        },
        {
          text: 'Path short read 1',
          sortable: false,
          value: 'path_sr1'
        },
        {
          text: 'Path short read 2',
          sortable: false,
          value: 'path_sr2'
        }
      ],
      modes: [
        "all",
        "unicycler",
        "spades",
        "miniasm",
        "canu",
        "flye"
      ],
      advanced_options: false,
      valid_config: false,
      submissionFailed: false,
      submissionError: "",
      config: {
        minContigLength: 2000,
        targetShortReadCov: 150,
        targetLongReadCov: 150,
        genomeSize: 5300000,
        mode: "unicycler",
        seqPadding: 1000,
        covWindow: 50,
        mappingCov: 20,
        minLength: 5000,
        maxLength: 500000
      },
      samples: [

      ]
    }
  },
  mounted () {
    let vm = this
    const uppy = new Uppy({
      debug: true,
      autoProceed: true,
      restrictions: {
        allowedFileTypes: ['.tar', '.zip', '.gz', '.vcf']
      }
    })
    uppy.use(Dashboard, {
      target: '.dashboard',
      trigger: '.UppyModalOpenerBtn',
      inline: true,
      height: 250
    })
    uppy.use(XHRUpload, {
      endpoint: 'http://localhost:8080/v1/upload',
      formData: true,
      fieldName: 'uploaded_file',
      headers: {
        'authorization': `Bearer ${this.$store.state.access_token}`
      }
    })
    uppy.on('complete', result => {
      if (result.successful.length) {
        vm.available_files.push(result.successful.map((s) => s.name))
      }
    })
  },
  methods: {
    duplicate_samples() {
      // copied this code from SO https://stackoverflow.com/a/50481890
      return !this.samples.map((s) => s.id).every(function(elem, i, array){return array.lastIndexOf(elem) === i})
    },
    addSample () {
      this.samples.push({
        id: `sample${Date.now()}`
      })
    },
    saveSamples () {
      let vm = this
      let samples = vm.samples.map((sample) => {
        sample = {
          ...sample,
          path_lr: sample.path_lr[0],
          created: new Date().toISOString(),
          last_updated: new Date().toISOString()
        }
        if (sample.path_sr1 !== undefined) {
          sample.path_sr1 = sample.path_sr1[0]
        }
        if (sample.path_sr2 !== undefined) {
          sample.path_sr2 = sample.path_sr2[0]
        }
        return sample
      })

      vm.$store.getters.fetch_defaults(`${vm.$basePath}/samples`, {
        method: 'POST',
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          config: vm.config,
          samples: samples
        })
      }).then((response) => {
        if (response.status === 200) {
          vm.$store.commit('addSamples', samples.map((sample) => sample.status = 'created'))
          vm.$router.push({name: 'samples'})
        } else {
          response.json().then((err) => {
            vm.submissionError = err.detail
            vm.submissionFailed = true
          }).catch(() => vm.submissionFailed = true)
        }
      }).catch(() => {
        vm.submissionError = ''
        vm.submissionFailed = true
      })
    }
  }
}
</script>
