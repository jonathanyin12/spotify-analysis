import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns # improves plot aesthetics
from matplotlib.dates import MonthLocator, DateFormatter

def _invert(x, limits):
    """inverts a value x on a scale from
    limits[0] to limits[1]"""
    return limits[1] - (x - limits[0])

def _scale_data(data, ranges):
    """scales data[1:] to ranges[0],
    inverts if the scale is reversed"""
    for d, (y1, y2) in zip(data[1:], ranges[1:]):
        assert (y1 <= d <= y2) or (y2 <= d <= y1)
    x1, x2 = ranges[0]
    d = data[0]
    if x1 > x2:
        d = _invert(d, (x1, x2))
        x1, x2 = x2, x1
    sdata = [d]
    for d, (y1, y2) in zip(data[1:], ranges[1:]):
        if y1 > y2:
            d = _invert(d, (y1, y2))
            y1, y2 = y2, y1
        sdata.append((d-y1) / (y2-y1) 
                     * (x2 - x1) + x1)
    return sdata

class ComplexRadar():
    def __init__(self, fig, variables, ranges,
                 n_ordinate_levels=6):
        angles = np.arange(0, 360, 360./len(variables))

        axes = [fig.add_axes([0.1,0.1,0.9,0.9],polar=True,
                label = "axes{}".format(i)) 
                for i in range(len(variables))]
        l, text = axes[0].set_thetagrids(angles, 
                                         labels=variables)
        for txt, angle in zip(text, angles):
            # txt.set_rotation(angle-90) # TODO: doesn't work
            txt.set_position((-0.1,-0.1)) # move labels outward
        for ax in axes[1:]:
            ax.patch.set_visible(False)
            ax.grid("off")
            ax.xaxis.set_visible(False)
        for i, ax in enumerate(axes):
            grid = np.linspace(*ranges[i], 
                               num=n_ordinate_levels)
            gridlabel = ["{}".format(round(x,2)) 
                         for x in grid]
            if ranges[i][0] > ranges[i][1]:
                grid = grid[::-1] # hack to invert grid
                          # gridlabels aren't reversed
            gridlabel[0] = "" # clean up origin
            ax.set_rgrids(grid, labels=gridlabel,
                         angle=angles[i])
            #ax.spines["polar"].set_visible(False)
            ax.set_ylim(*ranges[i])
        # variables for plotting
        self.angle = np.deg2rad(np.r_[angles, angles[0]])
        self.ranges = ranges
        self.ax = axes[0]
    def plot(self, data, *args, **kw):
        sdata = _scale_data(data, self.ranges)
        return self.ax.plot(self.angle, np.r_[sdata, sdata[0]], *args, **kw)
    def fill(self, data, *args, **kw):
        sdata = _scale_data(data, self.ranges)
        self.ax.fill(self.angle, np.r_[sdata, sdata[0]], *args, **kw)

# ranges = [(0, 1), (0, 1), (0, 1), (0, 1), 
#           (-60, 0), (50, 200), (0, 1), ]            





def timeseries_ridgeplot(df, factor, y, dateCol = 'date', title = '', save_name = None, aspect=20, height=1, labels=None):
    sns.set_theme(style="white", rc={"axes.facecolor": (0, 0, 0, 0)})
    num_factors = len(pd.unique(df[factor]))
    pal = sns.cubehelix_palette(num_factors, rot=-.25, light=.7)
    g = sns.FacetGrid(df, row=factor, hue=factor, aspect=aspect, height=height, palette=pal)

    g.map(plt.fill_between, dateCol, y, alpha=0.9)
    g.map(sns.lineplot, dateCol, y, alpha=1, linewidth=2, color="w")
    g.refline(y=0, linewidth=2, linestyle="-", color=None, clip_on=False)

    def label(x, color, label):
        ax = plt.gca()
        if labels:
            ax.text(-0.05, .25, labels[label], fontweight="bold", color=color,
                    ha="left", va="center", transform=ax.transAxes)
        else:
            ax.text(-0.05, .25, label, fontweight="bold", color=color,
                ha="left", va="center", transform=ax.transAxes)

    ax = plt.gca()
    ax.set_xticklabels(ax.get_xticks(), fontweight='bold', color=pal[num_factors-1])
    ax.axes.xaxis.set_major_locator(MonthLocator(interval=1)) 
    ax.xaxis.set_major_formatter(DateFormatter('%b'))

    g.map(label,factor)
    g.set_titles("")
    g.figure.suptitle(title, fontweight='bold', color=pal[0], fontsize=18)
    g.set(yticks=[], ylabel="", xlabel = "")
    g.figure.subplots_adjust(hspace=-0.7)
    g.despine(bottom=True, left=True)
    plt.show()
    if save_name:
        g.figure.savefig(save_name, dpi=600)
    sns.reset_orig()


def streamgraph(dates, ys, labels, title =''):
    plt.figure(figsize=(30,12))
    ax = plt.gca()
    plt.title(title)
    fig = plt.stackplot(dates, ys, colors= sns.color_palette("muted"), labels = labels, baseline="wiggle")
    ax.axes.xaxis.set_major_locator(MonthLocator(interval=1)) 
    ax.xaxis.set_major_formatter(DateFormatter('%b'))
    plt.legend(loc='upper left')
    plt.ylabel("Mins listened a day")
    ax.get_yaxis().set_visible(False)
    ax.invert_yaxis()
    plt.show()



def convert_to_df(tracks_data, columns):
    df = pd.DataFrame(tracks_data, columns =columns)
    return df



    