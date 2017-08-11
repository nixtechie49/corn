<template>
    <div>
        <content-left></content-left>
        <content-main></content-main>
    </div>
</template>
<script>

    import Key from './key.vue'
    import Main from './main.vue'

    module.exports = {
        components: {
            'content-left': Key,
            'content-main': Main,
        }
    }
</script>