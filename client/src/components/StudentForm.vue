<template>
    <div id="student-form">
        <form @submit.prevent="handleSubmit">
            <label for="username">Username</label>
            <input name="username" v-model="student.username" type="text" />
            <label for="password">Password</label>
            <input name="password" v-model="student.password" type="password" />
            <button>Login</button>
        </form>
    </div>
</template>

<script>
export default {
    name: 'student-form',
    data() {
        return {
            student: {
                username: '',
                password: '',
            },
        }
    },
    methods: {
        handleSubmit() {
            this.$emit('login:student', this.student)
        },
    },
}
</script>

<style scoped>
  form {
    margin-bottom: 2rem;
  }
</style>