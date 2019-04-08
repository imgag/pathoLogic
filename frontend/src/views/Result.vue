<template>
    <v-layout
        justify-center
        align-top
    >

    <v-flex xs12>
        <p>You can download the results as a zip archive</p>
        <v-btn :href="zip_url">Download archive</v-btn>
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
        fetch(`${vm.$basePath}/result/${vm.$route.params.id}`)
            .then((result) => Promise.resolve(result.json()))
            .then((content) => {
                vm.zip_url = `${vm.$basePath}/download/${content.result.zip_path}`
            })
    }
}
</script>
