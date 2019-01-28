<template>
    <v-chip>{{ status_text }}</v-chip>
</template>

<script>
    export default {
        name: "Status",
        props: {
            status: {
                type: String,
                required: true
            }
        },
        computed: {
            status_text () {
                let text

                if (this.status === 'created') {
                    text = 'Status: created'
                } else if (this.status === 'started') {
                    text = 'Status: Pipeline'
                } else if (this.status === 'finished') {
                    text = 'Status: Done'
                } else {
                    text = 'Status: Error'
                }
                return text
            }
        }
    }
</script>

<style scoped>

</style>