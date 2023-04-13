import matplotlib.pyplot as plt
import numpy as np

def bode_plot(f, Z, phase, colors=['C0', 'C1'], xlabel='Frecuencia [Hz]', ylabel1='Impedancia [$\Omega$]', ylabel2='Fase [°]', savefig=None, xlog=True, ylog=False):
    
    fig, axs = plt.subplots(2, 1, sharex=True)

    axs[0].plot(f, Z, colors[0])
    axs[0].set_ylabel(ylabel1)
    if xlog:
        axs[0].set_xscale('log')
    if ylog:
        axs[0].set_yscale('log')
    axs[0].grid()

    axs[1].plot(f, phase, colors[1])
    axs[1].set_ylabel(ylabel2)
    axs[1].set_xlabel(xlabel)
    axs[1].grid()

    plt.tight_layout()
    if savefig:
        plt.savefig(savefig, dpi=400)
    plt.show()