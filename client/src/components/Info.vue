<template>
    <div class="info small-container">
        <h1>{{ msg }}</h1>
    </div>
</template>

<script>
export default {
    name: "Info",
    props: {
        msg: String
    }
}
</script>