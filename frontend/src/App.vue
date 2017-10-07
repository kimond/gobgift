<template>
    <div class="app">
        <div class="page">
            <transition name="fade" mode="out-in">
                <router-view></router-view>
            </transition>
        </div>
    </div>
</template>


<script>
    export default {
        name: 'app',
        metaInfo: {
            title: 'Home',
            titleTemplate: '%s - Gobgift'
        }
    }
</script>

<style>
    .fade-enter {
        opacity: 0;
    }

    .fade-enter-active {
        transition: opacity .5s ease;
    }
</style>
