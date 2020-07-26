<template>
    <div id="grade-options">
        <form>
            <label for="grades">Grades</label>
            <select name="grades" v-model="gradeChoice" @change="handleChange">
                <option v-for="grade in grades" :key="grade.id" :value="grade.id">{{ grade.name }}</option>
            </select> 
        </form>
    </div>
</template>

<script>
export default {
    name: "GradeOptions",
    props: {
        grades: Array,
    },
    data() {
        return {
            gradeChoice: "",
        }
    },
    methods: {
        handleChange() {
            this.$emit("change:grade", this.gradeChoice)
        }
    },
}
</script>

<style scoped>
form {
    margin-bottom: 2em;
  }
</style>