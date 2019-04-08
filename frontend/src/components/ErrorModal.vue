<template>
    <v-dialog v-model="active" persistent max-width="290" dark>
        <v-card>
            <v-card-title class="headline">An error occurred</v-card-title>
            <v-card-text>{{ errorMessage }}</v-card-text>
            <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="green darken-1" flat @click="$emit('close')">Close</v-btn>
            </v-card-actions>
        </v-card>
    </v-dialog>
</template>

<script>
export default {
    name: "ErrorModal",
    props: {
        active: {
            type: Boolean,
            default: false
        },
        errorMessage: {
            type: String,
            default: "Something went wrong while processing your request. We're sorry for this inconvenience."
        }
    }
}
</script>
