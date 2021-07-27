<template>
  <div>
    <span>Key</span>
    <select v-model="key">
        <option v-for="note in notes" v-bind:key="note">{{note}}</option>
    </select>
    <span>BPM</span>
    <input v-model.number="bpm" type="number">
    <button @click="generate">Generate</button>
    <span>{{melodyTab}}</span>
    <button @click="play" v-if="melodyTab && !playing">Play</button>
    <button @click="stop" v-if="melodyTab && playing">Stop</button>
  </div>
</template>

<script>
    import * as Tone from 'tone'
    export default{
        asyncData() {
            return {
                key: 'C',
                notes: ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"],
                bpm: 120,
                melody: [],
                melodyTab: "",
                playing: false,
                node: null
            }
        },
        methods: {
            generate() {
                let scale = [2, 2, 1, 2, 2, 2, 1]
                let idx = this.notes.indexOf(this.key)
                let sixteenth = 60/(this.bpm*4)
                let keys = []
                for (let jump of scale) {
                    keys.push(this.notes[idx])
                    idx = (idx + jump)%12
                }
                this.melody = []
                this.melodyTab = ""
                let note = keys[Math.floor(Math.random() * keys.length)] + this.randInt(4, 5) 
                let time = 0 
                this.melody.push({note: note, time: time, action: "start"})
                this.melodyTab += note + " "
                let started = true
                for(let i = 0; i < 31; i++) {
                    time += sixteenth
                    let rand = Math.random()
                    if (rand < 0.2 && started) {
                        this.melody.push({note: note, time: time, action: "stop"})
                        started = false
                        this.melodyTab += "/ "
                    } else if(rand < 0.6) {
                        if(started) {
                            this.melody.push({note: note, time: time, action: "stop"})
                        }
                        note = keys[Math.floor(Math.random() * keys.length)] + this.randInt(4, 5)
                        this.melody.push({note: note, time: time, action: "start"})
                        started = true
                        this.melodyTab += note + " "
                    } else {
                        this.melodyTab += "-> "
                    }
                }
                if(started) {
                    this.melody.push({note: note, time: time+sixteenth, action: "stop"})
                }
                console.log(this.melody)
            },
            play() {
                console.log(this.melody[this.melody.length-1].time)
                const synth = new Tone.PolySynth(Tone.Synth).toDestination();
                if(this.node) {
                    this.node.dispose()
                }
                this.node = new Tone.Loop(time => {
                    for(let action of this.melody) {
                        if(action.action == "start") {
                            synth.triggerAttack(action.note, time + action.time)
                        } else {
                            synth.triggerRelease(action.note, time + action.time)
                        }
                    }
                }, this.melody[this.melody.length-1].time).start(0)
                Tone.Transport.start()
                this.playing=true
            },
            stop() {
                Tone.Transport.stop()
                this.playing=false
            },
            randInt(min, max) {
                min = Math.ceil(min);
                max = Math.floor(max);
                return Math.floor(Math.random() * (max - min + 1)) + min;
            }
        }
    }
</script>

