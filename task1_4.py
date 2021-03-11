import matplotlib.pyplot as plt
import numpy as np

from config1 import *

from task1_1 import ModelWithoutQueue


class ModelWithLeft:
    def __init__(self):
        # controls default text sizes
        plt.rc('font', size=3)

        # fontsize of tick labels
        plt.rc('xtick', labelsize=5)
        plt.rc('ytick', labelsize=5)

        self.model_without_queue = ModelWithoutQueue()

    def get_mult(self, l, n):
        return np.prod([n * mu + i * nu for i in range(1, l + 1)])

    def get_p_0(self, n, M):
        sum1 = np.sum([np.power(lambd, k) / (np.math.factorial(k) * np.power(mu, k)) for k in range(1, n + 1)])
        sum2 = np.sum([np.power(lambd, l) / self.get_mult(l, n) for l in range(1, M + 1)])

        return 1 / (1 + sum1 + sum2 * np.power(lambd, n) / (np.math.factorial(n) * np.power(mu, n)))

    def get_p_k(self, k, n, M):
        return np.power(lambd, k) / (np.math.factorial(k) * np.power(mu, k)) * self.get_p_0(n, M)

    def get_p_n_plus_l(self, l, n, M):
        return np.power(lambd, l) * self.get_p_k(n, n, M) / self.get_mult(l, n)

    def get_n_busy(self, n, M):
        sum1 = np.sum([k * self.get_p_k(k, n, M) for k in range(1, n + 1)])
        sum2 = np.sum([self.get_p_n_plus_l(l, n, M) for l in range(1, n + 1)])

        return sum1 + n * sum2

    def get_k_load(self, n_busy, n):
        return n_busy / n

    def get_p_Q(self, n, M):
        return np.sum([self.get_p_n_plus_l(l, n, M) for l in range(1, M + 1)])

    def get_Q(self, n, M):
        return np.sum([l * self.get_p_n_plus_l(l, n, M) for l in range(1, M + 1)])

    def plot(self, x, y, c='blue', label='label', xlabel='xlabel', ylabel='ylabel'):
        fig, axes = plt.subplots(nrows=1, ncols=1, figsize=figsize_standart, dpi=dpi_standart)

        axes.plot(x, y, color=c, linewidth=linewidth_standart, label=label)

        axes.grid()

        axes.legend(loc='best')
        axes.set_xlabel(xlabel)
        axes.set_ylabel(ylabel)

    def solve(self):

        # Текущее число операторов
        cur_n = 1

        # Текущая вероятность отказа в системе без очереди
        cur_p_decline_without_Q = 1.0

        # Текущее мат. ожидание числа занятых операторов
        cur_n_busy = 0.0

        # Текущий коэффициент загрузки операторов
        cur_k_load = 0.0

        # Текущая вероятность существования очереди
        cur_p_Q = 0.0

        # Текущее мат. ожидание длины очереди
        cur_Q = 0.0

        n_arr = np.array([])
        n_busy_arr = np.array([])
        k_load_arr = np.array([])
        p_Q_arr = np.array([])
        Q_arr = np.array([])

        while cur_p_decline_without_Q >= 0.01:
            cur_n_busy = self.get_n_busy(cur_n, M)
            cur_k_load = self.get_k_load(cur_n_busy, cur_n)
            cur_p_Q = self.get_p_Q(cur_n, M)
            cur_Q = self.get_Q(cur_n, M)

            n_arr = np.append(n_arr, cur_n)

            n_busy_arr = np.append(n_busy_arr, cur_n_busy)
            k_load_arr = np.append(k_load_arr, cur_k_load)
            p_Q_arr = np.append(p_Q_arr, cur_p_Q)
            Q_arr = np.append(Q_arr, cur_Q)

            cur_n += 1
            cur_p_decline_without_Q = self.model_without_queue.get_p_k(cur_n, cur_n)

        self.plot(n_arr, n_busy_arr, c='green', xlabel='Число операторов n',
                  ylabel='Мат. ожидание числа занятых операторов n_busy',
                  label='График зависимости n_busy(n)')
        self.plot(n_arr, k_load_arr, c='blue', xlabel='Число операторов n',
                  ylabel='Коэффициент загрузки операторов k_load',
                  label='График зависимости k_load(n)')
        self.plot(n_arr, p_Q_arr, c='yellow', xlabel='Число операторов n',
                  ylabel='Вероятность существования очереди p_Q',
                  label='График зависимости p_Q(n)')
        self.plot(n_arr, Q_arr, c='pink', xlabel='Число операторов n',
                  ylabel='Мат. ожидание длины очереди Q',
                  label='График зависимости Q(n)')

        plt.show()
