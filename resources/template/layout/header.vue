<template>
    <div>
        <header class="main-header">
            <a href="/" class="logo">
            <span class="logo-lg">
                <b>Redis</b>Explorer
            </span>
            </a>
            <nav class="navbar navbar-static-top" role="navigation">
                <div class="navbar-custom-menu">
                    <ul class="nav navbar-nav">
                        <li>
                            <a href="/" v-show="back"><i class="fa fa-arrow-left"></i></a>
                            <a href="/logout" v-show="!back"><i class="fa fa-close"></i></a>
                        </li>
                    </ul>
                </div>
            </nav>
        </header>
    </div>
</template>
<script>
    module.exports = {
        data: function () {
            return {back: false}
        },
        methods: {
            backOrLogout: function () {
                this.back = window.location.hash !== '#/'
            }
        },
        watch: {
            '$route': 'backOrLogout'
        },
    }
</script>