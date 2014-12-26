from pyo64 import * # noqa


def play_the_beats(server, beats, whole_length):
    trigger_table = NewTable(whole_length)
    for pos, vol in beats:
        trigger_table.put(
            1.0,
            # convert seconds to samples
            pos=int(server.getSamplingRate() * pos)
        )
    trigger_signal = TableRead(
        trigger_table,
        freq=1 / whole_length,
        interp=1,  # no interpolation, so ones stay ones
        loop=1
    ).play()
    amp = Iter(trigger_signal, choice=[vol for pos, vol in beats])

    snd_path = '32017KICK3.wav'
    sndt = SndTable(snd_path)
    env_table = LinTable([
        (0, 1.0),
        (sndt.getSize(), 1.0),
        (sndt.getSize() + 1, 0.0)
    ])
    trigger_env = TrigEnv(
        trigger_signal,
        env_table,
        dur=sndt.getDur(),
        mul=amp * 0.4)
    #test_signal = Noise()
    #test_signal.mul = trigger_env
    #test_signal.out()
    beat = OscTrig(sndt, trigger_signal,
                   #freq=[sndt.getRate()] * 2, mul=amp * 0.5)
                   freq=[sndt.getRate()] * 2, mul=trigger_env)
    beat.out()
    return beat

if __name__ == '__main__':
    beats = [(0, 1), (0.5, 1), (1.5, 2), (2.0, 1)]
    whole_length = 2.5

    from pyo64 import Server
    server = Server().boot().start()

    beat = play_the_beats(server, beats, whole_length)
