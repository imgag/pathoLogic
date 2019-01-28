<template>
    <v-card>
        <v-card-title primary-title>
            <div>
                <h3 class="headline mb-0">Probe #{{ id }}</h3>
                <div>Some more info about the probe, e.g <span>{{ author_email }}</span> wrote this.</div>
                <v-layout row wrap>
                    <v-chip xs6>Last update: {{ last_updated }}</v-chip>
                    <v-chip xs6>Created: {{ created_at }}</v-chip>
                    <div v-if="status">
                        <status :status="status"></status>
                    </div>
                </v-layout>
                <v-card-actions v-if="status">
                    <v-btn flat color="red" v-if="!started" @click="startProject">Start analysis</v-btn>
                </v-card-actions>
            </div>
        </v-card-title>
    </v-card>
</template>

<script>
import Status from '@/components/Status.vue'

export default {
    name: "Project",
    components: {
        Status
    },
    methods: {
        startProject () {
            this.started = true
            this.$emit('startProject', this.id)
        }
    },
    data () {
        return {
          started: false
        }
    },
    props: {
        id: Number,
        author_email: String,
        created_at: Date,
        last_updated: Date,
        status: String
    }
}
</script>

<style scoped>

</style>