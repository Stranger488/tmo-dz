import math

import matplotlib.pyplot as plt
import numpy as np

from config import *


def get_p_0(n, m):
    sum1 = np.sum([np.power(lambd, k) / (math.factorial(k) * np.power(k)) for k in range(1, n)])
    sum2 = np.sum([np.power(lambd / (n * mu), l) for l in range(1, m)])

    return 1 / (1 + sum1 + sum2 * np.power(lambd, n) / (math.factorial(n) * np.power(mu, n)))


def get_p_k(k, n, m):
    return np.power(lambd, k) / (math.factorial(k) * np.power(mu, k)) * get_p_0(n, m)


def get_p_n_plus_l(l, n, m):
    return np.power(lambd / (n * mu), l) * get_p_k(n, n, m)


def get_n_busy(n, m):
    sum1 = np.sum([k * get_p_k(k, n, m) for k in range(1, n)])
    sum2 = np.sum([get_p_n_plus_l(l, n, m) for l in range(1, m)])

    return sum1 + n * sum2


def get_k_load(n_busy, n):
    return n_busy / n


def get_p_Q(n, m):
    return np.sum([get_p_n_plus_l(l, n, m) for l in range(1, m)])


def get_Q(n, m):
    return np.sum([l * get_p_n_plus_l(l, n, m) for l in range(1, m)])


def get_k_Q(Q, m):
    return Q / m


def plot_on_axes(axes, x, y, c='blue', label='label', xlabel='xlabel', ylabel='ylabel'):
    axes.plot(x, y, color=c, linewidth=linewidth_standart, label=label)

    axes.grid()

    axes.legend(loc='best')
    axes.set_xlabel(xlabel)
    axes.set_ylabel(ylabel)


def solve():

    # Текущая вероятность отказа
    cur_p_decline = 1.0

    # Текущее мат. ожидание числа занятых операторов
    cur_n_busy = 0.0

    # Текущий коэффициент загрузки операторов
    cur_k_load = 0.0

    # Текущая вероятность существования очереди
    cur_p_Q = 0.0

    # Текущее мат. ожидание длины очереди
    cur_Q = 0.0

    # Текущий коэффициент занятости мест в очереди
    cur_k_Q = 0.0

    n_arr = np.array([])

    p_decline_arr = np.array([])
    n_busy_arr = np.array([])
    k_load_arr = np.array([])
    p_Q_arr = np.array([])
    Q_arr = np.array([])
    k_Q_arr = np.array([])

    # Текущее число операторов
    cur_n = 1


    # Семейство графиков для разных длин очереди при варьировании числа операторов
    # controls default text sizes
    plt.rc('font', size=3)

    # fontsize of tick labels
    plt.rc('xtick', labelsize=5)
    plt.rc('ytick', labelsize=5)

    fig, axes1 = plt.subplots(nrows=1, ncols=1, figsize=figsize_standart, dpi=dpi_standart)
    fig, axes2 = plt.subplots(nrows=1, ncols=1, figsize=figsize_standart, dpi=dpi_standart)
    fig, axes3 = plt.subplots(nrows=1, ncols=1, figsize=figsize_standart, dpi=dpi_standart)
    fig, axes4 = plt.subplots(nrows=1, ncols=1, figsize=figsize_standart, dpi=dpi_standart)
    fig, axes5 = plt.subplots(nrows=1, ncols=1, figsize=figsize_standart, dpi=dpi_standart)
    fig, axes6 = plt.subplots(nrows=1, ncols=1, figsize=figsize_standart, dpi=dpi_standart)

    while cur_p_decline >= 0.01:

        p_decline_arr = np.array([])
        n_busy_arr = np.array([])
        k_load_arr = np.array([])
        p_Q_arr = np.array([])
        Q_arr = np.array([])
        k_Q_arr = np.array([])

        m_arr = np.array([])
        for cur_m in range(1, 5):

            cur_p_decline = get_p_k(cur_n, cur_n, cur_m)
            cur_n_busy = get_n_busy(cur_n, cur_m)
            cur_k_load = get_k_load(cur_n_busy, cur_n)
            cur_p_Q = get_p_Q(cur_n, cur_m)
            cur_Q = get_Q(cur_n, cur_m)
            cur_k_Q = get_k_Q(cur_Q, cur_m)

            m_arr = np.append(m_arr, cur_m)

            p_decline_arr = np.append(p_decline_arr, cur_p_decline)
            n_busy_arr = np.append(n_busy_arr, cur_n_busy)
            k_load_arr = np.append(k_load_arr, cur_k_load)
            p_Q_arr = np.append(p_Q_arr, cur_p_Q)
            Q_arr = np.append(Q_arr, cur_Q)
            k_Q_arr = np.append(k_Q_arr, cur_k_Q)

        plot_on_axes(axes1, m_arr, p_decline_arr, c='red', xlabel='Длина очереди m', ylabel='Вероятность отказа p_k',
                     label='График зависимости p_k(m)')
        plot_on_axes(axes2, m_arr, n_busy_arr, c='green', xlabel='Длина очереди m',
                     ylabel='Мат. ожидание числа занятых операторов n_busy',
                     label='График зависимости n_busy(m)')
        plot_on_axes(axes3, m_arr, k_load_arr, c='blue', xlabel='Длина очереди m',
                     ylabel='Коэффициент загрузки операторов k_load',
                     label='График зависимости k_load(n)')
        plot_on_axes(axes4, m_arr, p_Q_arr, c='yellow', xlabel='Длина очереди m',
                     ylabel='Вероятность существования очереди p_Q',
                     label='График зависимости p_Q(m)')
        plot_on_axes(axes5, m_arr, Q_arr, c='pink', xlabel='Длина очереди m',
                     ylabel='Мат. ожидание длины очеред Q',
                     label='График зависимости Q(m)')
        plot_on_axes(axes6, m_arr, k_Q_arr, c='grey', xlabel='Длина очереди m',
                     ylabel='Коэффициент загрузки операторов k_Q',
                     label='График зависимости k_Q(m)')

        cur_n += 1


    # Семейство графиков для числа операторов при варьировании длины очереди
    ### ----

    plt.show()
