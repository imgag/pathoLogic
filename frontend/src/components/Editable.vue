<template>
    <div contenteditable="true" @input="$emit('update:content', $event.target.innerText)"></div>
</template>

<script>
export default {
    props: ['content'],
    mounted: function () {
        this.$el.innerText = this.content;
    },
    watch: {
        content: function () {
            this.$el.innerText = this.content;
        }
    }
}
</script>
