<template>
    <div>
        <p>Dashboard</p>
        <p>{{ name }}</p>
    </div>
</template>

<script>
    module.exports = {
        data: function () {
            return {name: 'abc'}
        }
    }
</script>