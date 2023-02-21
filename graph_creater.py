from matplotlib import pyplot as plt

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

    ax.bar(zones, percents, label=bar_labels, color=bar_colors)

    ax.set_ylabel('%')
    ax.set_xlabel(type_of_measurement[option])
    ax.legend(title='Разбивка по зонам')
    ax.set_title(label=f'Распределение по зонам{nl}')
    fig.set_size_inches(10, 10)

    plt.savefig(f'graph_by_{option}.png', facecolor='white', edgecolor='black', dpi=500)
