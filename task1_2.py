import matplotlib.pyplot as plt
import numpy as np

from config1 import *

from task1_1 import ModelWithoutQueue


class ModelWithBoundedQueue:
    def __init__(self):
        # controls default text sizes
        plt.rc('font', size=3)

        # fontsize of tick labels
        plt.rc('xtick', labelsize=5)
        plt.rc('ytick', labelsize=5)

        self.model_without_queue = ModelWithoutQueue()

    def get_p_0(self, n, m):
        sum1 = np.sum([np.power(lambd, k) / (np.math.factorial(k) * np.power(mu, k)) for k in range(1, n + 1)])
        sum2 = np.sum([np.power(lambd / (n * mu), l) for l in range(1, m + 1)])

        return 1 / (1 + sum1 + sum2 * np.power(lambd, n) / (np.math.factorial(n) * np.power(mu, n)))

    def get_p_k(self, k, n, m):
        return np.power(lambd, k) / (np.math.factorial(k) * np.power(mu, k)) * self.get_p_0(n, m)

    def get_p_n_plus_l(self, l, n, m):
        return np.power(lambd / (n * mu), l) * self.get_p_k(n, n, m)

    def get_n_busy(self, n, m):
        sum1 = np.sum([k * self.get_p_k(k, n, m) for k in range(1, n + 1)])
        sum2 = np.sum([self.get_p_n_plus_l(l, n, m) for l in range(1, m + 1)])

        return sum1 + n * sum2

    def get_k_load(self, n_busy, n):
        return n_busy / n

    def get_p_Q(self, n, m):
        return np.sum([self.get_p_n_plus_l(l, n, m) for l in range(1, m + 1)])

    def get_Q(self, n, m):
        return np.sum([l * self.get_p_n_plus_l(l, n, m) for l in range(1, m + 1)])

    def get_k_Q(self, Q, m):
        return Q / m

    def plot_on_axes(self, axes, x, y, c='green', label='label', xlabel='xlabel', ylabel='ylabel'):
        axes.plot(x, y, color=c, linestyle='--', linewidth=linewidth_standart, label=label)

        axes.grid()

        axes.legend(loc='best')
        axes.set_xlabel(xlabel)
        axes.set_ylabel(ylabel)

    def solve(self):

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

        # Текущее число операторов
        cur_n = 1

        # Семейство графиков для разных длин очереди при варьировании числа операторов
        fig, axes1 = plt.subplots(nrows=1, ncols=1, figsize=figsize_standart, dpi=dpi_standart)
        fig, axes2 = plt.subplots(nrows=1, ncols=1, figsize=figsize_standart, dpi=dpi_standart)
        fig, axes3 = plt.subplots(nrows=1, ncols=1, figsize=figsize_standart, dpi=dpi_standart)
        fig, axes4 = plt.subplots(nrows=1, ncols=1, figsize=figsize_standart, dpi=dpi_standart)
        fig, axes5 = plt.subplots(nrows=1, ncols=1, figsize=figsize_standart, dpi=dpi_standart)
        fig, axes6 = plt.subplots(nrows=1, ncols=1, figsize=figsize_standart, dpi=dpi_standart)

        cmap = plt.cm.get_cmap(cmap_name_standart, cmap_size)

        # Текущая вероятность отказа в системе без очереди
        cur_p_decline_without_Q = 1.0

        while cur_p_decline_without_Q >= 0.01:
            p_decline_arr = np.array([])
            n_busy_arr = np.array([])
            k_load_arr = np.array([])
            p_Q_arr = np.array([])
            Q_arr = np.array([])
            k_Q_arr = np.array([])

            m_arr = np.array([])
            for cur_m in range(1, M + 1):
                cur_p_decline = self.get_p_n_plus_l(cur_m, cur_n, cur_m)
                cur_n_busy = self.get_n_busy(cur_n, cur_m)
                cur_k_load = self.get_k_load(cur_n_busy, cur_n)
                cur_p_Q = self.get_p_Q(cur_n, cur_m)
                cur_Q = self.get_Q(cur_n, cur_m)
                cur_k_Q = self.get_k_Q(cur_Q, cur_m)

                m_arr = np.append(m_arr, cur_m)

                p_decline_arr = np.append(p_decline_arr, cur_p_decline)
                n_busy_arr = np.append(n_busy_arr, cur_n_busy)
                k_load_arr = np.append(k_load_arr, cur_k_load)
                p_Q_arr = np.append(p_Q_arr, cur_p_Q)
                Q_arr = np.append(Q_arr, cur_Q)
                k_Q_arr = np.append(k_Q_arr, cur_k_Q)

            self.plot_on_axes(axes1, m_arr, p_decline_arr, c=cmap(cur_n), xlabel='Длина очереди m',
                              ylabel='Вероятность отказа p_отк',
                              label='График зависимости p_отк(m), n={}'.format(cur_n))
            self.plot_on_axes(axes2, m_arr, n_busy_arr, c=cmap(cur_n), xlabel='Длина очереди m',
                              ylabel='Мат. ожидание числа занятых операторов n_busy',
                              label='График зависимости n_busy(m), n={}'.format(cur_n))
            self.plot_on_axes(axes3, m_arr, k_load_arr, c=cmap(cur_n), xlabel='Длина очереди m',
                              ylabel='Коэффициент загрузки операторов k_load',
                              label='График зависимости k_load(m), n={}'.format(cur_n))
            self.plot_on_axes(axes4, m_arr, p_Q_arr, c=cmap(cur_n), xlabel='Длина очереди m',
                              ylabel='Вероятность существования очереди p_Q',
                              label='График зависимости p_Q(m), n={}'.format(cur_n))
            self.plot_on_axes(axes5, m_arr, Q_arr, c=cmap(cur_n), xlabel='Длина очереди m',
                              ylabel='Мат. ожидание длины очереди Q',
                              label='График зависимости Q(m), n={}'.format(cur_n))
            self.plot_on_axes(axes6, m_arr, k_Q_arr, c=cmap(cur_n), xlabel='Длина очереди m',
                              ylabel='Коэффициент загрузки операторов k_Q',
                              label='График зависимости k_Q(m), n={}'.format(cur_n))

            cur_n += 1
            cur_p_decline_without_Q = self.model_without_queue.get_p_k(cur_n, cur_n)

        ###################
        # Семейство графиков для разного числа операторов при варьировании длины очереди
        fig, axes7 = plt.subplots(nrows=1, ncols=1, figsize=figsize_standart, dpi=dpi_standart)
        fig, axes8 = plt.subplots(nrows=1, ncols=1, figsize=figsize_standart, dpi=dpi_standart)
        fig, axes9 = plt.subplots(nrows=1, ncols=1, figsize=figsize_standart, dpi=dpi_standart)
        fig, axes10 = plt.subplots(nrows=1, ncols=1, figsize=figsize_standart, dpi=dpi_standart)
        fig, axes11 = plt.subplots(nrows=1, ncols=1, figsize=figsize_standart, dpi=dpi_standart)
        fig, axes12 = plt.subplots(nrows=1, ncols=1, figsize=figsize_standart, dpi=dpi_standart)

        for cur_m in range(1, M + 1):
            cur_p_decline_without_Q = 1.0

            p_decline_arr = np.array([])
            n_busy_arr = np.array([])
            k_load_arr = np.array([])
            p_Q_arr = np.array([])
            Q_arr = np.array([])
            k_Q_arr = np.array([])

            n_arr = np.array([])

            cur_n = 1
            while cur_p_decline_without_Q >= 0.01:
                cur_p_decline = self.get_p_n_plus_l(cur_m, cur_n, cur_m)
                cur_n_busy = self.get_n_busy(cur_n, cur_m)
                cur_k_load = self.get_k_load(cur_n_busy, cur_n)
                cur_p_Q = self.get_p_Q(cur_n, cur_m)
                cur_Q = self.get_Q(cur_n, cur_m)
                cur_k_Q = self.get_k_Q(cur_Q, cur_m)

                n_arr = np.append(n_arr, cur_n)

                p_decline_arr = np.append(p_decline_arr, cur_p_decline)
                n_busy_arr = np.append(n_busy_arr, cur_n_busy)
                k_load_arr = np.append(k_load_arr, cur_k_load)
                p_Q_arr = np.append(p_Q_arr, cur_p_Q)
                Q_arr = np.append(Q_arr, cur_Q)
                k_Q_arr = np.append(k_Q_arr, cur_k_Q)

                cur_n += 1
                cur_p_decline_without_Q = self.model_without_queue.get_p_k(cur_n, cur_n)

            self.plot_on_axes(axes7, n_arr, p_decline_arr, c=cmap(cur_m), xlabel='Число операторов n',
                              ylabel='Вероятность отказа p_отк',
                              label='График зависимости p_отк(n), m={}'.format(cur_m))
            self.plot_on_axes(axes8, n_arr, n_busy_arr, c=cmap(cur_m), xlabel='Число операторов n',
                              ylabel='Мат. ожидание числа занятых операторов n_busy',
                              label='График зависимости n_busy(n), m={}'.format(cur_m))
            self.plot_on_axes(axes9, n_arr, k_load_arr, c=cmap(cur_m), xlabel='Число операторов n',
                              ylabel='Коэффициент загрузки операторов k_load',
                              label='График зависимости k_load(n), m={}'.format(cur_m))
            self.plot_on_axes(axes10, n_arr, p_Q_arr, c=cmap(cur_m), xlabel='Число операторов n',
                              ylabel='Вероятность существования очереди p_Q',
                              label='График зависимости p_Q(n), m={}'.format(cur_m))
            self.plot_on_axes(axes11, n_arr, Q_arr, c=cmap(cur_m), xlabel='Число операторов n',
                              ylabel='Мат. ожидание длины очереди Q',
                              label='График зависимости Q(n), m={}'.format(cur_m))
            self.plot_on_axes(axes12, n_arr, k_Q_arr, c=cmap(cur_m), xlabel='Число операторов n',
                              ylabel='Коэффициент загрузки операторов k_Q',
                              label='График зависимости k_Q(n), m={}'.format(cur_m))

        plt.show()
