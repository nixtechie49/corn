<template>
    <div class="content-wrapper" ref="mainContent">
        <section class="content-header">
            <h1>
                <small>欢迎</small>
            </h1>
            <ol class="breadcrumb">
            </ol>
        </section>
        <section class="content">
            <router-view name="content"></router-view>
        </section>
    </div>
</template>
<script>
    module.exports = {
        mounted: function () {
            let ref = this.$refs;
            let height = document.documentElement.clientHeight;
            ref.mainContent.style.height = (height - 101) + 'px';
        }
    }
</script>