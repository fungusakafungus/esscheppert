beats = [(0, 1), (0.5, 1), (1.5, 2), (2.0, 1)]
whole_length = 2.5

from pyo64 import * # noqa
server = Server().boot().start()

trigger_table = NewTable(whole_length)
for pos, vol in beats:
    trigger_table.put(
        1.0,
        # convert seconds to samples
        pos=int(server.getSamplingRate() * pos)
    )
trigger_signal = TableRead(
    trigger_table,
    freq=server.getSamplingRate(),
    interp=1,  # no interpolation, so ones stay ones
    loop=1
).play()
test_signal = Noise()
env_table = HannTable()
trigger_env = TrigEnv(trigger_signal, env_table, dur=0.1)
test_signal.mul = trigger_env
test_signal.out()

snd_path = '058full001.wav'
sndt = SndTable(snd_path, stop=0.757)
