from datetime import timedelta

from matplotlib import pyplot as plt
import matplotlib
from scipy.signal import savgol_filter

from users import nl

matplotlib.use('agg')

font_axes = {'fontsize': 24,
             'fontstyle': 'normal'}

font_title = {'fontsize': 30,
              'fontstyle': 'normal'}


def make_chart(list_of_zone, dicts_of_zones, option):
    type_of_measurement = {'hr': f'ЧСС, уд/мин',
                           'power': f'Мощность, Вт'}

    type_of_graph = {'power': 'мощности',
                     'hr': 'пульса'}

    fig, ax = plt.subplots()

    zones = list(list_of_zone.values())
    percents = list(dicts_of_zones.values())

    bar_labels = [f'{percents[0]}%', f'{percents[1]}%', f'{percents[2]}%',
                  f'{percents[3]}%', f'{percents[4]}%', f'{percents[5]}%', f'{percents[6]}%']

    bar_colors = ['tab:gray', 'tab:cyan', 'tab:blue', 'tab:green', 'tab:olive', 'tab:orange',
                  'tab:red']

    ax.bar(zones, percents, label=bar_labels, color=bar_colors, width=0.9, bottom=True)

    ax.set_ylabel('%', fontdict=font_axes)
    ax.set_xlabel(type_of_measurement[option], fontdict=font_axes)
    ax.legend(title='Разбивка по зонам')

    plt.title(f'Распределение по зонам {type_of_graph[f"{option}"]}{nl}', fontdict=font_title)

    fig.set_size_inches(12, 12)

    plt.savefig(f'media/graph_by_{option}.png', facecolor='white', edgecolor='black', dpi=100)


def make_TSS_graph(list_of_date: list, list_of_TSS: list):
    fig, ax = plt.subplots()

    ATL_values = make_ATL_graph(list_of_date, list_of_TSS)
    x_values = list_of_date
    y_values = list_of_TSS
    ATL_values = savgol_filter(ATL_values, 51, 3)

    plt.plot(x_values, y_values, 'ro', color='red', markersize=4)
    plt.plot(x_values, ATL_values, color='magenta', markersize=5)

    ax.set_ylabel('TSS', fontdict=font_axes)
    ax.set_xlabel(f'{nl}Период всех тренировок', fontdict=font_axes)

    plt.title(f'График TSS за все тренировки{nl}', fontdict=font_title)

    fig.set_size_inches(10, 10)
    plt.savefig('media/graph_by_TSS.png', dpi=100)
    return 'ok'


def make_ATL_graph(list_of_date: list, list_of_TSS: list):
    list_ATL = []
    for i in range(len(list_of_date) - 1, -2, -1):
        if i == len(list_of_date) - 1:
            list_ATL.append(0)
        elif list_of_date[i] - list_of_date[i - 1] <= timedelta(days=7):
            list_ATL.append(list_of_TSS[i - 1] + list_of_TSS[i])

    list_ATL.reverse()

    # print(list_of_date)
    # print(list_of_TSS)
    # print(list_ATL)

    return list_ATL

# if __name__ == '__main__':
#     make_TSS_graph()
