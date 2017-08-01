<template>
    <div>
        <app-header></app-header>
        <app-left></app-left>
        <app-content></app-content>
        <app-footer></app-footer>
    </div>
</template>

<script>
    import Header from './layout/header.vue'
    import Left from './layout/left.vue'
    import Content from './layout/content.vue'
    import Footer from './layout/footer.vue'

    module.exports = {
        components: {
            'app-header': Header,
            'app-left': Left,
            'app-content': Content,
            'app-footer': Footer,
        }
    }
</script>