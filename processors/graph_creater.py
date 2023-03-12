from matplotlib import pyplot as plt
import matplotlib

from users import nl

matplotlib.use('agg')
# matplotlib.use('TkAgg')


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

    font_axes = {'fontsize': 24,
                 'fontstyle': 'normal'}

    font_title = {'fontsize': 30,
                  'fontstyle': 'normal'}

    ax.bar(zones, percents, label=bar_labels, color=bar_colors, width=0.9, bottom=True)

    ax.set_ylabel('%', fontdict=font_axes)
    ax.set_xlabel(type_of_measurement[option], fontdict=font_axes)
    ax.legend(title='Разбивка по зонам')

    plt.title(f'Распределение по зонам {type_of_graph[f"{option}"]}{nl}', fontdict=font_title)

    fig.set_size_inches(12, 12)

    plt.savefig(f'media/graph_by_{option}.png', facecolor='white', edgecolor='black', dpi=100)


def make_TSS_graph(list_of_date: list, list_of_TSS: list):
    x_values = list_of_date
    y_values = list_of_TSS

    dates = matplotlib.dates.date2num(x_values)
    plt.plot_date(dates, y_values, color = 'red', markersize = 3)

    plt.savefig('media/graph_by_TSS.png')
    return 'ok'

# if __name__ == '__main__':
#     make_TSS_graph()
