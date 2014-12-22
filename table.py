from pyo64 import * # noqa

snd_path = ('/srv/media/samples/musicradar-metal-drum-samples/drums acoustic/'
            '058bpm_drums_acoustic/058full001.wav')

server = Server().boot().start()
sndt = SndTable(snd_path, stop=0.77)
