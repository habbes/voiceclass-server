import wave, tempfile, os


def make_wav(data, sample_rate, sample_width, channel_count):
    # write wave to temp file
    temp = tempfile.NamedTemporaryFile(mode='wb', delete=False)
    wf = wave.open(temp)
    wf.setframerate(sample_rate)
    wf.setsampwidth(sample_width)
    wf.setnchannels(channel_count)
    wf.writeframes(data)
    wf.close()
    temp.close()
    # read wave data from temp file
    rf = open(temp.name, 'rb')
    wav_data = rf.read()
    rf.close()
    os.unlink(temp.name)
    return wav_data

