import matplotlib.pyplot as plt
import numpy as np

from config2 import *


class ModelProduction:
    def __init__(self):
        # controls default text sizes
        plt.rc('font', size=3)

        # fontsize of tick labels
        plt.rc('xtick', labelsize=5)
        plt.rc('ytick', labelsize=5)

    def get_mult(self, k, N):
        return np.prod([N - x + 1 for x in range(1, k + 1)])

    def get_p_0(self, n, N):
        sum1 = np.sum([self.get_mult(k, N) * np.power(lambd / mu, k) / np.math.factorial(n) for k in range(1, n + 1)])
        sum2 = np.sum([self.get_mult(n, N) * np.power(lambd / mu, n + l) / (np.power(n, l) * np.math.factorial(n)) for l in range(1, N - n + 1)])

        return 1 / (1 + sum1 + sum2)

    def get_p_k(self, k, n, N):
        return self.get_mult(k, N) * np.power(lambd / mu, k) * self.get_p_0(n, N) / np.math.factorial(k)

    def get_p_n_plus_l(self, l, n, N):
        return self.get_mult(n, N) * np.power(lambd / mu, n + l) * self.get_p_0(n, N) / (np.power(n, l) * np.math.factorial(n))

    def get_M_free(self, n, N):
        return np.sum([k * self.get_p_k(k, n, N) for k in range(1, N + 1)])

    def get_M_wait(self, n, N):
        return np.sum([l * self.get_p_n_plus_l(l, n, N) for l in range(1, N - n + 1)])

    def get_P_wait(self, n, N):
        return np.sum([self.get_p_n_plus_l(l, n, N) for l in range(1, N - n + 1)])

    def get_N_adj(self, n, N):
        sum1 = np.sum([k * self.get_p_k(k, n, N) for k in range(1, n + 1)])
        sum2 = n * np.sum([self.get_p_n_plus_l(l, n, N) for l in range(1, N - n + 1)])

        return sum1 + sum2

    def get_k_load(self, n, N_adj):
        return N_adj / n

    def plot(self, x, y, c='blue', label='label', xlabel='xlabel', ylabel='ylabel'):
        fig, axes = plt.subplots(nrows=1, ncols=1, figsize=figsize_standart, dpi=dpi_standart)

        axes.plot(x, y, color=c, linewidth=linewidth_standart, label=label)

        axes.grid()

        axes.legend(loc='best')
        axes.set_xlabel(xlabel)
        axes.set_ylabel(ylabel)

    def solve(self):

        # Текущее мат. ожидание числа простаивающих станков
        cur_M_free = 0.0

        # Текущее мат. ожидание числа станков, ожидающих обслуживания
        cur_M_wait = 0.0

        # Текущая вероятность ожидания обслуживания
        cur_P_wait = 0.0

        # Текущее мат. ожидание числа занятых наладчиков
        cur_N_adj = 0.0

        # Текущий коэффициент занятости наладчиков
        cur_k_load = 0.0

        M_free_arr = np.array([])
        M_wait_arr = np.array([])
        P_wait_arr = np.array([])
        N_adj_arr = np.array([])
        k_load_arr = np.array([])

        n_arr = np.arange(1, N, 1)

        for cur_n in n_arr:
            cur_M_free = self.get_M_free(cur_n, N)
            cur_M_wait = self.get_M_wait(cur_n, N)
            cur_P_wait = self.get_P_wait(cur_n, N)
            cur_N_adj = self.get_N_adj(cur_n, N)
            cur_k_load = self.get_k_load(cur_n, cur_N_adj)

            M_free_arr = np.append(M_free_arr, cur_M_free)
            M_wait_arr = np.append(M_wait_arr, cur_M_wait)
            P_wait_arr = np.append(P_wait_arr, cur_P_wait)
            N_adj_arr = np.append(N_adj_arr, cur_N_adj)
            k_load_arr = np.append(k_load_arr, cur_k_load)

        self.plot(n_arr, M_free_arr, c='green', xlabel='Число наладчиков n',
                  ylabel='Мат. ожидание числа простаивающих станков M_free',
                  label='График зависимости M_free(n)')
        self.plot(n_arr, M_wait_arr, c='blue', xlabel='Число наладчиков n',
                  ylabel='Мат. ожидание числа станков, ожидающих обслуживания M_wait',
                  label='График зависимости M_wait(n)')
        self.plot(n_arr, P_wait_arr, c='yellow', xlabel='Число наладчиков n',
                  ylabel='Вероятность ожидания обслуживания P_wait',
                  label='График зависимости P_wait(n)')
        self.plot(n_arr, N_adj_arr, c='pink', xlabel='Число наладчиков n',
                  ylabel='Мат. ожидание числа занятых наладчиков N_adj',
                  label='График зависимости N_adj(n)')
        self.plot(n_arr, k_load_arr, c='pink', xlabel='Число наладчиков n',
                  ylabel='Коэффициент занятости наладчиков k_load',
                  label='График зависимости k_load(n)')

        plt.show()