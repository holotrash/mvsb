import mplayer, time, jack, binascii, thread, os, sys
from random import randint

if not(os.path.isfile("playlist.cfg")):
    print("playlist.cfg not found. run the config tool to generate a playlist file.")
    sys.exit(0)

loadList = open("playlist.cfg").read().split("?")
bgfilename = loadList[0]
#bgfilename = 'blank_screen_long.mkv'
filenames = []
for x in range(1,len(loadList)):
    filenames.append(loadList[x])
#filenames = ['skid_kid.mkv', 'bodybuilding.mkv', '15sec.mkv', 'yuri_gagarin.mkv', '15sec.mkv']
currentVideo = -1 
loadNewVideo = False
noteOn = "90"
nextVidTriggerNote = "6c"

client = jack.Client("mvsb" + str(randint(0,1000)))
midi_in = client.midi_inports.register("midi_in")

p = mplayer.Player("-fs")
p.loadfile(bgfilename)
# p._run_command("pause")
# p._run_command("pause")

def controlVideo():
    global p
    global loadNewVideo
    global filenames
    global currentVideo

    while True:
        if loadNewVideo:
            if currentVideo<(len(filenames)-1):
                currentVideo = currentVideo + 1
            loadNewVideo = False
            p.loadfile(filenames[currentVideo])
            p._run_command("pause")
            p._run_command("pause")
            time.sleep(10)
            p.loadfile(bgfilename)
            #p._run_command("pause")
            #p._run_command("pause")

@client.set_process_callback
def process(frames):
    global filenames
    global currentVideo
    global p
    global loadNewVideo

    for offset, data in midi_in.incoming_midi_events():
        print("incoming midi event ({0}: 0x{1})".format(client.last_frame_time + offset, binascii.hexlify(data).decode()))
        if len(data) == 3:
            status, pitch, vel = bytes(data)
            print("status: " + binascii.hexlify(status).decode() + "\n")
            print("pitch : " + binascii.hexlify(pitch).decode() + "\n")
            print("vel   : " + binascii.hexlify(vel).decode() + "\n")
            if binascii.hexlify(status).decode() == noteOn and binascii.hexlify(pitch).decode() == nextVidTriggerNote: # if you get the change video signal
                loadNewVideo = True 

thread.start_new_thread(controlVideo, ())
with client:
    input()
