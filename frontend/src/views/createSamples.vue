<template>

  <v-layout
    justify-center 
    align-start
  >
    <v-form v-model="valid_config">
      <v-flex>
      <h2>Configuration</h2>    
      </v-flex>
      <v-layout 
          ma-3
          column>
        <v-flex
          xs-10
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
            v-model="config.cpu"
            min=1
            max=40
            hint="Number of threads per process"
            :persistent-hint="true"
            :thumb-label="true"
          />
        </v-flex>
        <v-flex xs2 ml-5>      
          <v-text-field
            v-model="config.cpu"
            min=1
            max=40
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
            v-model="config.queue_size"
            min=1
            max=20
            hint="Number of concurrent processes"
            :persistent-hint="true"
            :thumb-label="true"
          />
        </v-flex>
        <v-flex xs2 ml-5>      
          <v-text-field
            v-model="config.queue_size"
            min=1
            max=20
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
            v-model="config.min_contig_length"
            min=1
            max=1000000
            hint="Length curoff for contigs in final result"
            :persistent-hint="true"
            :thumb-label="true"
          />
        </v-flex>
        <v-flex xs2 ml-5>      
          <v-text-field
            v-model="config.min_contig_length"
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
            v-model="config.target_shortread_cov"
            min=1
            max=200
            hint="Target long read coverage after subsampling"
            :persistent-hint="true"
            :thumb-label="true"
          />
        </v-flex>
        <v-flex xs2 ml-5>      
          <v-text-field
            v-model="config.target_shortread_cov"
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
            v-model="config.target_longread_cov"
            min=1
            max=200
            hint="Target long read coverage after subsampling"
            :persistent-hint="true"
            :thumb-label="true"
          />
        </v-flex>
        <v-flex xs2 ml-5>      
          <v-text-field
            v-model="config.target_longread_cov"
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
            v-model="config.est_genome_size"
            min=1
            max=10000000
            hint="Estimated genome size after assembly"
            :persistent-hint="true"
            :thumb-label="true"
          />
        </v-flex>
        <v-flex xs2 ml-5>      
          <v-text-field
            v-model="config.est_genome_size"
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
            v-model="config.seq_padding"
            min=1
            max=10000
            hint="Sequence overlap length during plasmid identification"
            :persistent-hint="true"
            :thumb-label="true"
          />
        </v-flex>
        <v-flex xs2 ml-5>      
          <v-text-field
            v-model="config.seq_padding"
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
            v-model="config.cov_window"
            min=20
            max=5000
            hint="Coverage window size"
            :persistent-hint="true"
            :thumb-label="true"
          />
        </v-flex>
        <v-flex xs2 ml-5>      
          <v-text-field
            v-model="config.cov_window"
            min=20
            max=5000
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
          <v-btn right :disabled="!valid_config && !valid_samples" @click="saveSamples">Save samples</v-btn>
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
export default {
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
        queue_size: 4,
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
      return this.samples.length && this.samples.every((sample) => sample.id !== "sample" && sample.id.length && sample.path_lr.length)
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

      fetch(`${vm.$basePath}/samples`, {
        method: 'POST',
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          config: vm.config,
          samples: samples
        })
      }).then((response) => { // TODO: Add visual feedback
        if (response.status === 200) {
          vm.$store.commit('addSamples', samples.map((sample) => sample.status = 'created'))
        }
        vm.$router.push({name: 'samples'})
      }).catch(() => vm.$router.push({name: 'samples'}))
    }
  }
}
</script>
