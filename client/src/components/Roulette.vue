<template>
    <section class="vue-winwheel">
        <div class="mobile-container">
            <div class="wheel-wrapper">
                <div class="canvas-wrapper">
                    <canvas id="canvas" width="310" height="310">
                        <p style="{color: white}" align="center">Sorry, your browser doesn't support canvas. Please try with another browser.</p>
                    </canvas>
                </div>
                <div class="button-wrapper">
                    <a class="btn btn-play" href="#" @click.prevent="startSpin()" v-if="ready && !loadingPrize && !wheelSpinning">SPIN!</a>
                </div>
            </div>
        </div>
        <h2 v-if="modalPrize">Et c'est un <span>{{prizeName}}</span> !!</h2>
    </section>
</template>


<script>
import * as Winwheel from "../Winwheel"

export default {
    name: 'VueWinWheel',
    props: {
        segments: Array,
        prizeNumber: Number,
        ready: Boolean,
    },
    data () {
        return {
            loadingPrize: false,
            theWheel: null,
            modalPrize: false,
            wheelPower: 1,
            wheelSpinning: false,
            prizeName: '',
            WinWheelOptions: {
                textFontSize: 14,
                outterRadius: 410,
                innerRadius: 25,
                lineWidth: 8,
            }
        }
    },
    methods: {
        showPrize () {
            this.modalPrize = true
        },
        hidePrize () {
            this.modalPrize = false
        },
        startSpin () {
            if (this.wheelSpinning === false) {
                this.hidePrize()
                this.theWheel = new Winwheel.Winwheel({
                    ...this.WinWheelOptions,
                    numSegments: this.segments.length,
                    segments: this.segments,
                    animation: {
                        type: 'spinToStop',
                        duration: 5,
                        spins: 5,
                        callbackFinished: this.onFinishSpin
                    }
                })

                let stopAt = this.theWheel.getRandomForSegment(this.prizeNumber)
                this.theWheel.animation.stopAngle = stopAt
                this.loadingPrize = false
                this.theWheel.startAnimation()
                this.wheelSpinning = false
            }
        },
        resetWheel () {
            this.theWheel = new Winwheel.Winwheel({
                ...this.WinWheelOptions,
                numSegments: this.segments.length,
                segments: this.segments,
                animation: {
                    type: 'spinToStop',
                    duration: 1,
                    spins: 2,
                }
            })

            this.theWheel.animation.stopAngle = 0
            this.theWheel.startAnimation()
            
            this.wheelSpinning = false // Reset to false to power buttons and spin can be clicked again.
        },
        initSpin () {
            this.loadingPrize = true
            this.resetWheel()
            this.loadingPrize = false
        },
        onFinishSpin (indicatedSegment) {
            this.prizeName = indicatedSegment.text
            this.showPrize()
        }
    },
    mounted () {
        this.initSpin()
    },
}

</script>

<style scoped>
.vue-winwheel {
	text-align: center;
	background-image: url('/static/img/obstacle-run/bg-spinner-mobile.svg');
	background-size: cover;
	background-position: center bottom;
	background-repeat: no-repeat;
    display: flexbox;
}
.vue-winwheel span {
	color: #b32656;
}
.vue-winwheel h2 {
	margin: 0;
}
.vue-winwheel #modalSpinwheel.custom-modal .content-wrapper .content {
	width: calc(100vw - 30px);
	padding-top: 52px;
}
.vue-winwheel #modalSpinwheel.custom-modal .content-wrapper .content h2 {
	text-transform: uppercase;
	color: #b32656;
	margin-bottom: 16px;
	margin-top: 0;
	font-family: 'Avenir', Helvetica, Arial, sans-serif;
	font-size: 18px;
	letter-spacing: 1.1px;
	margin: 0;
}
.vue-winwheel canvas#canvas {
	position: relative;
}
.vue-winwheel .canvas-wrapper {
	position: relative;
}
.vue-winwheel .canvas-wrapper:after {
	content: '';
	display: block;
	width: 42px;
	background: #c4376f;
	height: 42px;
	position: absolute;
	left: calc(50% - 25px);
	margin: auto;
	border-radius: 100%;
	top: calc(50% - 29px);
	border: 5px solid white;
	box-sizing: content-box;
}
.vue-winwheel .canvas-wrapper:before {
	content: '';
	display: block;
	width: 310px;
	background: #0f0f0f;
	height: 310px;
	position: absolute;
	left: 0;
	right: 0;
	margin: 0 auto;
	border-radius: 100%;
	top: 0;
}
.vue-winwheel .wheel-wrapper {
	position: relative;
}
.vue-winwheel .wheel-wrapper:before {
	content: '';
	width: 62px;
	height: 47px;
	position: absolute;
	top: -10px;
	left: calc(50% - 31px);
	right: 0;
	display: block;
	z-index: 99999;
	background-image: url('../assets/spinner-marker.svg');
	background-repeat: no-repeat;
	background-size: contain;
	background-position: center;
}
.vue-winwheel .wheel-wrapper .button-wrapper {
	margin: 10px auto;
	display: flex;
	flex-direction: column;
	align-items: center;
	justify-content: center;
	width: 231px;
}
.vue-winwheel .wheel-wrapper .btn.btn-play {
	padding: 0 58px !important;
	background: #c4376f;
	height: 40px;
	line-height: 40px;
	color: white;
	font-weight: bold;
	text-decoration: none;
	border-radius: 2px;
	font-family: 'Avenir', Helvetica, Arial, sans-serif;
	letter-spacing: 2px;
}
</style>