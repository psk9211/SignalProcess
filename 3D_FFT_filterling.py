__author__ = 'jpong'

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
import scipy.fftpack as fft


def fft2D(x):
    X_temp = np.array([fft.fft(x[i]) for i in range(x.shape[0])])
    X = np.transpose(np.array([fft.fft(np.transpose(X_temp)[i]) for i in range(np.transpose(X_temp).shape[0])]))

    return X

def w2d_hamming(M):
    w1d = np.hamming(100)#using hamming filter
    w2d = np.zeros((100, 100))

    for i in range(100):
        if i >= 50-M and i <= 50+M:
            for j in range(100):
                if j >= 50-M and j <= 50+M:
                    w2d[i][j] = np.sqrt(w1d[i]**2 + w1d[j]**2)

    return w2d

def main():
    fig = plt.figure(1)

    ax = fig.add_subplot(2, 2, 1, projection='3d')
    X, Y = np.mgrid[0:10:0.25, 0:10:0.25]
    Z1 = np.cos(np.pi/4*X+3*np.pi/4*Y)

    surf = ax.plot_surface(X, Y, Z1, cmap='autumn', cstride=2, rstride=2)

    ax = fig.add_subplot(2, 2, 3, projection='3d')
    X, Y = np.mgrid[0:100:1, 0:100:1]
    Z1 = np.cos(np.pi/4*(X-50)+3*np.pi/4*(Y-50))

    surf = ax.plot_surface(X, Y, abs(fft2D(Z1)), cmap='autumn', cstride=2, rstride=2)

    ax = fig.add_subplot(2, 2, 2, projection='3d')
    X, Y = np.mgrid[0:10:0.25, 0:10:0.25]
    Z2 = np.cos(np.pi/4*(X-50))*np.cos(3*np.pi/4*(Y-50))

    surf = ax.plot_surface(X, Y, Z2, cmap='autumn', cstride=2, rstride=2)

    ax = fig.add_subplot(2, 2, 4, projection='3d')
    X, Y = np.mgrid[0:100:1, 0:100:1]
    Z2 = np.cos(np.pi/4*(X-50))*np.cos(3*np.pi/4*(Y-50))

    surf = ax.plot_surface(X, Y, abs(fft2D(Z2)), cmap='autumn', cstride=2, rstride=2)



    fig = plt.figure(2)

    ax = fig.add_subplot(1, 2, 1, projection='3d')
    X, Y = np.mgrid[0:100:1, 0:100:1]
    ohm1 = np.pi/4
    ohm2 = np.pi/2
    h = (ohm1/np.pi*np.sinc(ohm1/np.pi*(X-50))*(ohm2/np.pi*np.sinc(ohm2/np.pi*(Y-50))))

    surf = ax.plot_surface(X, Y, abs(fft2D(h)), cmap='autumn', cstride=2, rstride=2)

    ax = fig.add_subplot(1, 2, 2, projection='3d')
    X, Y = np.mgrid[0:100:1, 0:100:1]
    g = (ohm1/np.pi*ohm2/np.pi)*np.sinc(ohm1/np.pi*(X-50)+ohm2/np.pi*(Y-50))

    surf = ax.plot_surface(X, Y, abs(fft2D(g)), cmap='autumn', cstride=2, rstride=2)



    fig = plt.figure(3)
    #h plot
    ax = fig.add_subplot(2, 2, 1, projection='3d')
    X, Y = np.mgrid[0:100:1, 0:100:1]
    ohm1 = np.pi/4
    ohm2 = np.pi/2
    h = (ohm1/np.pi*np.sinc(ohm1/np.pi*(X-50))*(ohm2/np.pi*np.sinc(ohm2/np.pi*(Y-50))))

    surf = ax.plot_surface(X, Y, abs(fft2D(h)), cmap='autumn', cstride=2, rstride=2)

    ax = fig.add_subplot(2, 2, 2, projection='3d')
    X, Y = np.mgrid[0:100:1, 0:100:1]
    x = np.cos(np.pi/4*(X-50)+np.pi/8*(Y-50))+np.cos(3*np.pi/4*(X-50)+5*np.pi/8*(Y-50))

    surf = ax.plot_surface(X, Y, abs(fft2D(x)), cmap='autumn', cstride=2, rstride=2)

    ax = fig.add_subplot(2, 2, 3, projection='3d')
    X, Y = np.mgrid[0:100:1, 0:100:1]

    w2d = w2d_hamming(12)
    h_f = w2d * h

    surf = ax.plot_surface(X, Y, abs(fft2D(h_f)), cmap='autumn', cstride=2, rstride=2)

    ax = fig.add_subplot(2, 2, 4, projection='3d')
    X, Y = np.mgrid[0:100:1, 0:100:1]

    surf = ax.plot_surface(X, Y, abs(fft2D(h_f)*fft2D(x)), cmap='autumn', cstride=2, rstride=2)

    plt.show()

if __name__ == '__main__':
    main()
