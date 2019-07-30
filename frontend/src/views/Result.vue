<template>
    <v-layout
        justify-center
        align-top
    >

    <v-flex xs12>
        <p>You can download the results as a zip archive</p>
        <v-btn @click="downloadArchive">Download archive</v-btn>
    </v-flex>

    </v-layout>
</template>

<script>
export default {
    name: 'result',
    data () {
      return {
        zip_url: ''
      }
    },
    mounted () {
      let vm = this
      vm.$store.getters.fetch_defaults(`${vm.$basePath}/result/${vm.$route.params.id}`)
        .then((result) => Promise.resolve(result.json()))
        .then((content) => {
            vm.zip_url = `${vm.$basePath}/download/${content.result.zip_path}`
      })
    },
    methods: {
      downloadArchive() {
        let results_name = `${this.route.params.id}_results.zip`
        this.$store.getters.fetch_defaults(this.zip_url).then((response) => response.blob()).then((blobby) => {
          let anchor = document.createElement('a')
          let objectURL = window.URL.createObjectURL(blobby)

          anchor.href = objectURL
          anchor.download = results_name
          anchor.dispatchEvent(new MouseEvent('click', { bubbles: true, cancelable: true, view: window }))

          window.URL.revokeObjectURL(objectURL)
        })
      }
    }
}
</script>
