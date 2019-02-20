<template>

  <v-layout
    justify-center 
    align-top
  >
    <v-form v-model="valid_config">
      <v-flex
        xs12
      >
        <h2>Config</h2>    
      </v-flex>
      <v-layout>
        <v-flex
          xs3
          mr-2
        >      
          <v-slider
            v-model="config.cpu"
            min=1
            max=40
            hint="Number of threads per process"
            :persistent-hint="true"
            :thumb-label="true"
          />
        </v-flex>

        <v-flex
          xs3
          mr-2
          ml-2
        >
          <v-slider
            v-model="config.queue_size"
            min=1
            max=20
            hint="Number of concurrent processes"
            :persistent-hint="true"
            :thumb-label="true"
          />
        </v-flex>

        <v-flex
          xs4
          ml-2
          mr-2
        >
          <v-select
            v-model="config.mode"
            :items="modes"
            hint="Different assembly methods"
            :persistent-hint="true"
            solo
          />
        </v-flex>

        <v-flex
          xs2
          ml-2
        >
          <v-switch
            v-model="advanced_options"
            hint="Advanced options"
            :persistent-hint="true"
          >
          </v-switch>
        </v-flex>
      </v-layout>

      <v-layout v-if="advanced_options">
        <v-flex
          xs4
          mr-2
        >
          <v-slider
            v-model="config.min_contig_length"
            min=1
            max=1000000
            hint="Length cutoff for contigs in final result"
            :persistent-hint="true"
            :thumb-label="true"
          />
        </v-flex>

        <v-flex
          xs4
          mr-2
          ml-2
        >
          <v-slider
            v-model="target_shortread_cov"
            min=1
            max=200
            hint="Short reads are subsampled to reach this target coverage"
            :persistent-hint="true"
            :thumb-label="true"
          />
        </v-flex>
        <v-flex
          xs4
          ml-2
        >
          <v-slider
            v-model="config.target_longread_cov"
            min=1
            max=200
            hint="Long reads are subsampled to reach this target coverage"
            :persistent-hint="true"
            :thumb-label="true"
          />
        </v-flex>
      </v-layout>

      <v-layout v-if="advanced_options">
        <v-flex
          xs4
          mr-2
        >
          <v-slider
            v-model="config.est_genome_size"
            min=1
            max=10000000
            hint="Estimated approximate final genome size of assembled bacteria. Used for coverage calculations"
            :persistent-hint="true"
            :thumb-label="true"
          />
        </v-flex>

        <v-flex
          xs4
          mr-2
          ml-2
        >
          <v-slider
            v-model="config.seq_padding"
            min=1
            max=10000
            hint="Number of bases added at sequence ends to improve alignment quality in plasmid identification"
            :persistent-hint="true"
            :thumb-label="true"
          />
        </v-flex>

        <v-flex
          xs4
          ml-2
        >
          <v-slider
            v-model="config.cov_window"
            min=20
            max=5000
            hint="Window size for coverage calculation"
            :persistent-hint="true"
            :thumb-label="true"
          />
        </v-flex>
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

      <v-layout>
        <v-flex
          xs-10
          mr-2
        >
          <v-text-field
            v-model="author_email"
            hint="The author email of the samples"
            value="author@med.uni-tuebingen.de"
            :rules="emailRules"
            required
            persistent-hint
            solo
          ></v-text-field>
        </v-flex>

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
          <v-btn right :disabled="!valid_config && !valid_samples" type="submit">Save samples</v-btn>
        </v-flex>
      </v-layout>

      <v-data-table
        :headers="headers"
        :items="samples"
      >
      <template slot="items" slot-scope="props">
        <td> <editable :content="props.item.id"/></td>
        <td class="text-xs-left">
          <input type="file" :value="props.item.path_lr" @change="props.item.path_lr = $event.srcElement.value"/>
        </td>
        <td class="text-xs-left">
          <input type="file" :value="props.item.path_sr1" @change="props.item.path_sr1 = $event.srcElement.value"/>
        </td>
        <td class="text-xs-left">
          <input type="file" :value="props.item.path_sr2" @change="props.item.path_sr2 = $event.srcElement.value"/>
        </td>
      </template>
      </v-data-table>
    </v-form>
  </v-layout>
</template>

<script>
import Editable from '@/components/Editable.vue'

export default {
  components: {
    Editable
  },
  name: 'createSample',
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
      emailRules: [
        v => !!v || 'E-mail is required',
        v => /.+@.+/.test(v) || 'E-mail must be valid'
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
      author_email: "",
      config: {
        cpu: 5,
        queue__size: 4,
        min_contig_length: 2000,
        target_shortread_cov: 150,
        target_longread_cov: 150,
        est_genome_size: 5300000,
        mode: "unicycler",
        seq_padding: 1000,
        cov_window: 50
      },
      samples: [

      ]
    }
  },
  computed: {
    valid_samples () {
      return this.samples.every((s) => {
        return s.id !== '' && s.path_lr !== ''
      }) && this.samples.length
    }
  },
  methods: {
    addSample () {
      this.samples.push({
        id: 'sample',
        path_lr: '',
        path_sr1: '',
        path_sr2: ''
      })
    },
    saveSamples () {
      let vm = this
      let samples = vm.samples.map((sample) => {
        return {
          ...sample,
          author_email: vm.author_email,
          created: new Date().toISOString(),
          last_updated: new Date().toISOString()
        }
      })

      fetch(`${vm.$basePath}/projects`, {
        method: 'POST',
        body: JSON.stringify({
          config: vm.config,
          samples: samples
        })
      }).then((response) => { // TODO: Add visual feedback
        if (response.status == 200) {
          vm.$store.commit('addSamples', samples.map((sample) => sample.status = 'created'))
          vm.$router.push('samples')
        }
      }).catch(() => vm.$router.push('samples'))
    }
  }
}
</script>
