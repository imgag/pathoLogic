<template>
    <v-chip :color="color">{{ text }}</v-chip>
</template>

<script>
    export default {
        name: "Status",
        props: {
            status: {
                required: true
            }
        },
        computed: {
            color () {
                let color

                if (this.status === 'started') {
                    color = 'warning'
                } else if (this.status === 'finished') {
                    color = 'success'
                } else if (this.status === 'error') {
                    color = 'error'
                }
                return color
            },
            text () {
                let text

                if (this.status === 'created') {
                    text = 'Created'
                } else if (this.status === 'started') {
                    text = 'Processing'
                } else if (this.status === 'finished') {
                    text = 'Finished'
                } else {
                    text = 'Error'
                }
                return text
            }
        }
    }
</script>
