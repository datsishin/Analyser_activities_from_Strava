from matplotlib import pyplot as plt
import matplotlib

matplotlib.use('agg')

# Специальный символ для переноса строки внутри f-строк
nl = '\n'


def make_chart(list_of_zone, dicts_of_zones, option):
    type_of_measurement = {'hr': f'{nl}ЧСС, уд/мин',
                           'power': f'{nl}Мощность, Вт'}

    fig, ax = plt.subplots()

    zones = list(list_of_zone.values())
    percents = list(dicts_of_zones.values())
    bar_labels = [f'{percents[0]}%', f'{percents[1]}%', f'{percents[2]}%',
                  f'{percents[3]}%', f'{percents[4]}%']
    bar_colors = ['tab:grey', 'tab:blue', 'tab:green', 'tab:orange', 'tab:red']

    font_axes = {'fontsize': 18,
                 'fontstyle': 'normal'}

    font_title = {'fontsize': 30,
                  'fontstyle': 'normal'}

    ax.bar(zones, percents, label=bar_labels, color=bar_colors, width=0.9, bottom=True)

    ax.set_ylabel('%', fontdict=font_axes)
    ax.set_xlabel(type_of_measurement[option], fontdict=font_axes)
    ax.legend(title='Разбивка по зонам')

    plt.title(f'Распределение по зонам{nl}', fontdict=font_title)

    fig.set_size_inches(10, 10)

    plt.savefig(f'media/graph_by_{option}.png', facecolor='white', edgecolor='black', dpi=500)
