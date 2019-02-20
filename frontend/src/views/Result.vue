<template>
    <v-layout
        justify-center
        align-top
    >
    <v-flex xs12 mb-2>
        <v-btn :href="statistics_path">Download the statistics</v-btn>
    </v-flex>

    <v-flex xs12>
        <v-btn :href="zip_path">Download full archive</v-btn>
    </v-flex>

    </v-layout>
</template>

<script>
export default {
    name: 'result',
    data () {
        return {
            statistics_path: '',
            zip_path: ''
        }
    },
    mounted () {
        let vm = this
        fetch(`${vm.$basePath}/result/${vm.$route.params.id}`)
            .then((result) => Promise.resolve(result.json()))
            .then((content) => {
                vm.statistics_path = content.statistics_path
                vm.zip_path = content.zip_path
            })
    }
}
</script>
