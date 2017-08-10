<template>
    <div>
        <app-header></app-header>
        <app-body></app-body>
        <app-footer></app-footer>
    </div>
</template>

<script>
    import Header from './layout/header.vue'
    import Body from './layout/body.vue'
    import Footer from './layout/footer.vue'

    module.exports = {
        components: {
            'app-header': Header,
            'app-body': Body,
            'app-footer': Footer,
        }
    }
</script>