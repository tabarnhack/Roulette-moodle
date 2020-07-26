<template>
    <div id="student-form">
        <form @submit.prevent="handleSubmit">
            <label for="username">Username</label>
            <input name="username" v-model="student.username" type="text" />
            <label for="password">Password</label>
            <input name="password" v-model="student.password" type="password" />
            <button>Login</button>
        </form>
        OR
        <form @submit.prevent="handleSubmitCookie">
            <label for="cookie">Moodle Session ID</label>
            <input name="cookie" v-model="cookie" type="text" />
            <button>Check</button>
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
            cookie: ''
        }
    },
    methods: {
        handleSubmit() {
            this.$emit('login:student', this.student)
        },
        handleSubmitCookie() {
            this.$emit('check:student', this.cookie)
        },
    },
}
</script>

<style scoped>
  form {
    margin-bottom: 2rem;
  }
</style>