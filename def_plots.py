import matplotlib.pyplot as plt
import seaborn as sns

# Gray bgcolor for the plots
sns.set_style('darkgrid')

# Scatterplot function
def splot(data, x, y, title, hue, xlabel, ylabel, grid):
    sns.scatterplot(data=data, x=x, y=y, hue=hue)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid(grid)
    plt.legend(['-']).remove()
    plt.show()

# Boxplot function
def bplot(data, x, color, lincolor, linwidth, title):
    sns.boxplot(data=data, x=x, color=color, linecolor=lincolor, linewidth=linwidth)
    plt.title(title)
    plt.show()
