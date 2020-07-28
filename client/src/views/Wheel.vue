<template>
    <div id="wheel" class="small-container">
        <student-form v-if="!seen" @login:student="loginStudent" @check:student="checkStudent" />
        <font-awesome-icon v-if="seen" @click="handleClick" icon="sync" />
        <font-awesome-icon v-if="seen" @click="disconnect" icon="sign-out-alt" style="margin-left: 25px;" />
        <pulse-loader :loading="loading" />
        <grade-options v-if="seen" :grades="courses" @choose:grade="changeCourse">Courses</grade-options>
        <grade-options v-if="seen && grades.length > 0" :grades="grades" @choose:grade="changeGrade">Grades</grade-options>
        <div ref="container"></div>
        <box v-if="err" :active="true" :type="'warning'">
            <div slot="box-body">{{ msg }}</div>
        </box>
        <roulette v-if="seen && !err" :ready="state" :segments="options" :prizeNumber="prize" :key="rouletteKey"/>
    </div>
</template>

<script>
import StudentForm from "@/components/StudentForm.vue"
import Roulette from "@/components/Roulette.vue"
import GradeOptions from "@/components/GradeOptions.vue"
import PulseLoader from 'vue-spinner/src/PulseLoader.vue'
import Box from 'vue-info-box'

import * as API from '@/services/api'

export default {
    name: "Wheel",
    components: {
        Roulette,
        StudentForm,
        GradeOptions,
        PulseLoader,
        Box
    },
    data() {
        return {
            state: false,
            msg: "",
            err: false,
            loading: false,
            refreshGrades: 0,
            refreshCourses: 0,
            rouletteKey: 0,
            seen: false,
            grades: [],
            courses: [],
            prize: 3,
            options: [
                {
                    textFillStyle: "#fff",
                    fillStyle: "#000",
                    text: "A"
                },
                {
                    textFillStyle: "#000",
                    fillStyle: "#fadede",
                    text: "B"
                },
                {
                    textFillStyle: "#fff",
                    fillStyle: "#000",
                    text: "C"
                },
                {
                    textFillStyle: "#000",
                    fillStyle: "#fadede",
                    text: "D"
                },
                {
                    textFillStyle: "#fff",
                    fillStyle: "#000",
                    text: "E"
                },
                {
                    textFillStyle: "#000",
                    fillStyle: "#fadede",
                    text: "F"
                }
            ]
        }
    },
    methods: {
        loginStudent(student) {
            this.loading = true
            this.err = false
            API.login(student).then(json => {
                if(json.status === 'error')
                    return Promise.reject(json.error)
                return API.courses()
            }).then(json => {
                if(json.status === 'error')
                    return Promise.reject(json.error)
                this.courses = json.items
                this.seen = true
            }).catch(e => {
                this.msg = e
                this.err = true
            }).finally(() => {
                this.loading = false
            });
        },
        checkStudent(cookie) {
            this.loading = true
            this.err = false
            if(cookie !== undefined)
                this.$cookies.set('MoodleSession', cookie, 0)
            API.check().then(json => {
                if(json.status === "error")
                    return Promise.reject(json.error)
                return API.courses()
            }).then(json => {
                if(json.status === 'error')
                    return Promise.reject(json.error)
                this.courses = json.items
                this.seen = true
            }).catch(e => {
                this.msg = e
                this.err = true
            }).finally(() => {
                this.loading = false
            });
        },
        changeCourse(choice) {
            this.loading = true
            this.err = false
            API.grades(choice).then(json => {
                if(json.status === 'error')
                    return Promise.reject(json.error)
                this.grades = json.items
            }).catch(e => {
                this.msg = e
                this.err = true
            }).finally(() => {
                this.loading = false
            });
        },
        changeGrade(grade) {
            this.err = false
            this.state = false
            let found = this.grades.find(elem => elem.id === grade)

            if(found === undefined) {
                this.msg = 'Cannot find the specified course please try another one'
                this.err = true
                return
            } else if(found.grade === undefined || found.grade === '-') {
                this.msg = 'No grade for that course at the moment'
                this.err = true
                return
            }
            
            let range = []
            found.range.split('–').forEach(curr => range.push(parseInt(curr)))
            let note = parseFloat(found.grade)
            let mid = (range[0] + range[1]) / 2
            let step = (range[1] - mid) / 5

            if(note < mid) {
                this.prize = 6
            } else {
                note -= mid
                this.prize = 5 - Math.ceil(note / step)
            }

            if(this.prize === 0) { // Just to adjust so that it can trigger the grade A
                this.prize++
            }

            this.state = true

            this.forceRerender()
        },
        handleClick() {
            this.loading = true
            API.courses().then(json => {
                if(json.status === 'error')
                    return Promise.reject(json.error)
                this.courses = json.items
                this.grades = []
                this.err = false
            }).catch(console.error).finally(() => {
                this.loading = false
            });
        },
        disconnect() {
            this.$cookies.remove('MoodleSession')
            this.seen = false
        },
        forceRerender() {
            this.rouletteKey++
        }
    },
    mounted() {
        if(this.$cookies.isKey('MoodleSession')) {
            this.checkStudent()
        }
    }
}
</script>