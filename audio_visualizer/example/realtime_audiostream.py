__author__ = 'jpong'

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pyaudio
import struct
import scipy.signal as sig


SAVE = 0.0
TITLE = ''
FPS = 25.0

nFFT = 512
BUF_SIZE = 4 * nFFT
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
K = 0.8

def animate(i, line, stream, wf, MAX_y):

    # Read n*nFFT frames from stream, n > 0
    N = max(stream.get_read_available() / nFFT, 1) * nFFT
    data = stream.read(N)

    # Unpack data, LRLRLR...
    y = np.array(struct.unpack("%dh" % (N * CHANNELS), data)) / MAX_y
    y_L = y[::2]
    y_R = y[1::2]

    # Lowpass filter with K
    Y_L = sig.lfilter([0, 1], [1, -K], np.fft.fft(y_L, nFFT))
    Y_R = sig.lfilter([0, 1], [1, -K], np.fft.fft(y_R, nFFT))

    # Sewing FFT of two channels together, DC part uses right channel's
    Y = abs(np.hstack((Y_L[-nFFT/2:-1], Y_R[:nFFT/2])))

    line.set_ydata(Y)

    return line,


def init(line):

    # This data is a clear frame for animation
    line.set_ydata(np.zeros(nFFT - 1))
    return line,


def main():

    fig = plt.figure()

    # Frequency range
    x_f = 1.0 * np.arange(-nFFT / 2 + 1, nFFT / 2) / nFFT * RATE
    ax = fig.add_subplot(111, title=TITLE, xlim=(x_f[0], x_f[-1]),
                       ylim=(0, 2 * np.pi * nFFT**2 / RATE))
    ax.set_yscale('symlog', linthreshy=nFFT**0.5)

    line, = ax.plot(x_f, np.zeros(nFFT - 1))

    # Change x tick labels for left channel
    def change_xlabel(evt):
        labels = [label.get_text().replace(u'\u2212', '')
                  for label in ax.get_xticklabels()]
        ax.set_xticklabels(labels)
        fig.canvas.mpl_disconnect(drawid)
    drawid = fig.canvas.mpl_connect('draw_event', change_xlabel)

    p = pyaudio.PyAudio()
    # Used for normalizing signal. If use paFloat32, then it's already -1..1.
    # Because of saving wave, paInt16 will be easier.
    MAX_y = 2.0**(p.get_sample_size(FORMAT) * 8 - 1)

    frames = None
    wf = None

    stream = p.open(format=FORMAT,
                  channels=CHANNELS,
                  rate=RATE,
                  input=True,
                  frames_per_buffer=BUF_SIZE)

    ani = animation.FuncAnimation(fig, animate, frames,
      init_func=lambda: init(line), fargs=(line, stream, wf, MAX_y),
      interval=1000.0/FPS, blit=True)

    plt.show()

    stream.stop_stream()
    stream.close()
    p.terminate()

if __name__ == '__main__':
    main()
