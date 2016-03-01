__author__ = 'jpong'

import struct

import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
import pyaudio

FPS = 60.0

nFFT = 512
BUF_SIZE = 4 * nFFT
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100

CUTFREQ = 50
MAX_top = 25

def animate(i, line, stream, MAX_y,rs):
    # Softmax for good feature
    softmax = lambda x:MAX_top*2/(1 + np.exp(-x))-(MAX_top)
    # Read n*nFFT frames from stream, n > 0
    N = max(stream.get_read_available() / nFFT, 1) * nFFT
    data = stream.read(N)

    # Unpack data, LRLRLR...
    y = np.array(struct.unpack("%dh" % (N * CHANNELS), data)) / MAX_y
    y_L = y[::2]

    Y_L = np.fft.fft(y_L, nFFT)

    # Sewing FFT of two channels together, DC part uses right channel's
    Y = softmax(np.abs(Y_L)[0:CUTFREQ])

    for h,r in zip(Y,rs):
        r.set_height(h)
    return rs

def init(line,rs):
    # This data is a clear frame for animation
    for h,r in zip(np.zeros(nFFT)[0:CUTFREQ],rs):
        r.set_height(h)
    return rs


def main():
    fig = plt.figure()
    line = plt.bar(range(CUTFREQ), np.zeros(nFFT)[0:CUTFREQ])
    plt.ylim((0, MAX_top))
    plt.xlim((0, CUTFREQ))

    rs = [r for r in line]

    p = pyaudio.PyAudio()
    # Used for normalizing signal. If use paFloat32, then it's already -1..1.
    # Because of saving wave, paInt16 will be easier.
    MAX_y = 2.0 ** (p.get_sample_size(FORMAT) * 8 - 1)

    frames = None

    stream = p.open(format=FORMAT,
                  channels=CHANNELS,
                  rate=RATE,
                  input=True,
                  frames_per_buffer=BUF_SIZE)

    ani = animation.FuncAnimation(
    fig, animate, frames,
    init_func=lambda: init(line,rs), fargs=(line, stream, MAX_y,rs),
    interval=1000.0 / FPS, blit=True
    )

    plt.show()

    stream.stop_stream()
    stream.close()
    p.terminate()

if __name__ == '__main__':
  main()
