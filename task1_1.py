import math

import matplotlib.pyplot as plt
import numpy as np

from config import *


def get_p_0(n):
    return 1 / (1 + np.sum([np.power(lambd, k) / (math.factorial(k) * np.power(mu, k)) for k in range(1, n)]))


def get_p_k(k, n):
    return np.power(lambd, k) / (math.factorial(k) * np.power(mu, k)) * get_p_0(n)


def get_n_busy(n):
    return np.sum([k * get_p_k(k, n) for k in range(1, n)])


def get_k_load(n_busy, n):
    return n_busy / n


def plot(x, y, c="blue", label="label", xlabel="xlabel", ylabel="ylabel", is_savefig=False):

    # controls default text sizes
    plt.rc('font', size=3)

    # fontsize of tick labels
    plt.rc('xtick', labelsize=5)
    plt.rc('ytick', labelsize=5)

    fig, axes = plt.subplots(nrows=1, ncols=1, figsize=figsize_standart, dpi=dpi_standart)

    axes.plot(x, y, color=c, linewidth=linewidth_standart, label=label)

    axes.grid()

    axes.legend(loc='best')
    axes.set_xlabel(xlabel)
    axes.set_ylabel(ylabel)

    if is_savefig:
        fig.savefig('fig.png', dpi=dpi_standart, bbox_inches='tight')


def solve():

    # Текущеее число операторов
    cur_n = 1

    # Текущая вероятность отказа
    cur_p_decline = 1.0

    # Текущее мат. ожидание числа занятых операторов
    cur_n_busy = 0.0

    # Текущий коэффициент загрузки операторов
    cur_n_load = 0.0

    n_arr = np.array([])
    p_decline_arr = np.array([])
    n_busy_arr = np.array([])
    k_load_arr = np.array([])

    while cur_p_decline >= 0.01:
        cur_p_decline = get_p_k(cur_n, cur_n)
        cur_n_busy = get_n_busy(cur_n)
        cur_n_load = get_k_load(cur_n_busy, cur_n)

        n_arr = np.append(n_arr, cur_n)
        p_decline_arr = np.append(p_decline_arr, cur_p_decline)
        n_busy_arr = np.append(n_busy_arr, cur_n_busy)
        k_load_arr = np.append(k_load_arr, cur_n_load)

        cur_n += 1

    plot(n_arr, p_decline_arr, c='red', xlabel='Число операторов n', ylabel='Вероятность отказа p_k',
         label='График зависимости p_k(n)')
    plot(n_arr, n_busy_arr, c='green', xlabel='Число операторов n', ylabel='Мат. ожидание числа занятых операторов n_busy',
         label='График зависимости n_busy(n)')
    plot(n_arr, k_load_arr, c='blue', xlabel='Число операторов n', ylabel='Коэффициент загрузки операторов k_load',
         label='График зависимости k_load(n)')

    plt.show()
