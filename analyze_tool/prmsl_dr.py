# coding: utf-8
import argparse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.font_manager as font_manager


def parse_args() -> dict:
    """parse_args.
    set file path.

    Args:

    Returns:
        dict:
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", help="set ncfile.", type=str)
    p = parser.parse_args()
    args = {"file": p.file}
    return args

args = parse_args()

csvfile = args["file"]
df = pd.read_csv(csvfile, header=0)
#date,lat,lon,prmsl,deeping_rate
date = df["date"]
prmsl = df["prmsl"]
deeping_rate = df["deeping_rate"]


fig = plt.figure(figsize=(15, 6))
ax = fig.add_subplot(111)
plt.rcParams['figure.dpi'] = 300  # 画質
jp_font_path = "/home/tomita/.local/share/fonts/SourceHanCodeJP-Regular.otf"
jp_font = font_manager.FontProperties(fname=jp_font_path, size=14)


# x axis --> datetime
new_xticks = list(range(0, len(date), 5))
ax.xaxis.set_major_locator(ticker.FixedLocator(new_xticks)) # x軸をnew_xticksで置き換える
ax.xaxis.set_ticklabels(date[::5], fontsize=20) # new_xticksの表示を置き換え
plt.xticks(rotation=60)


# plot
ax.plot(date, prmsl,
        marker='.',
        markersize=10,
        markeredgewidth=1.,
        markeredgecolor="k",
        label="pressure [hPa]",
        color="b",
        linestyle="solid",
        )

ax.set_xlabel("date (UTC)", fontsize=24,)
ax.set_ylabel("pressure [hPa]", fontsize=24,)
pressure_ticks = list(range(1020, 940, -10))
plt.yticks(pressure_ticks, fontsize=24)

# 2軸目
ax2 = ax.twinx()
ax2.xaxis.set_major_locator(ticker.FixedLocator(new_xticks)) # x軸をnew_xticksで置き換える
ax2.xaxis.set_ticklabels(date[::5], fontsize=20) # new_xticksの表示を置き換え
ax2.plot(date, deeping_rate,
         marker='.',
         markersize=10,
         markeredgewidth=1.,
          markeredgecolor="k",
          label="deeping rate",
          color="g",
          linestyle="dashed",
          )
#ax2.set_xlabel(, fontsize=10, fontproperties=jp.font)
ax2.set_ylabel("成長率", fontsize=36, fontproperties=jp_font)
dr_ticks = list(np.arange(-1.5, 2.5, 0.5))
plt.yticks(dr_ticks, fontsize=24)

# grid
ax.xaxis.grid(True, which="major",
              linestyle='-', color='#CFCFCF')
ax.yaxis.grid(True, which="major",
              linestyle='-', color='#CFCFCF')

# save fig
plt.rcParams['font.size'] = 24 # label font size
bar_, label = ax.get_legend_handles_labels()
ax.legend(bar_, label, loc='upper left',
          borderaxespad=0, bbox_to_anchor=(0.35, 1.0))
bar_, label = ax2.get_legend_handles_labels()
ax2.legend(bar_, label, loc='upper left',
          borderaxespad=0, bbox_to_anchor=(0.7, 1.0))
fig.savefig("hoge", bbox_inches="tight", pad_inches=0.5)
