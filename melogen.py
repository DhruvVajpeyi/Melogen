import random

notes = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

scale = [2, 2, 1, 2, 2, 2, 1]

key = "F"
idx = notes.index(key)
bpm = 120
sixteenth = 60/(bpm*4)
keys = []
for jump in scale:
    keys.append(notes[idx])
    idx = (idx + jump)%12

melody = []
note = random.choice(keys) + random.choice(["3", "4", "5"])
time = 0 
melody.append((note, time, "start"))
started = True
for i in range(31):
    time += sixteenth
    rand = random.uniform(0, 1)
    if rand < 0.2 and started: #Rest
        melody.append((note, time, "stop"))
        started = False
    elif rand < 0.6: #New note
        if started:
            melody.append((note, time, "stop"))
        note = random.choice(keys) + random.choice(["3", "4", "5"])
        melody.append((note, time, "start"))
        started = True
if started:
    melody.append((note, time+sixteenth, "stop"))
print(melody)