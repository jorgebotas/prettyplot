from typing import Optional
from matplotlib import pyplot as plt
from matplotlib import rcParams
import seaborn as sns
import pandas as pd
from scipy.stats import fisher_exact
from statannotations.Annotator import Annotator

rcParams["pdf.fonttype"] = 42
sns.set_theme("paper", style="white", font="Arial", font_scale=1.6)

def plot_overlap_vs_background(
        setX: set,
        setY: set,
        universe: set,
        labelX: str,
        labelY: str,
        background_label: str = "Background",
        background_color: str = ".5",
        ax: Optional[plt.Axes] = None,
        title: str = "",
        linewidth: int = 2,
        color: str = "blue",
        capsize: float = 0.0,
        alpha: float = 0.1,
        figsize: tuple = (4, 4),
        ylim: Optional[tuple] = None,
        save: Optional[str] = None
    ):
    data = pd.DataFrame(universe, columns=["index"])
    data.set_index("index", inplace=True, drop=False)
    data[labelX] = data.index.isin(setX)
    data[labelX] = data[labelX].apply(
        lambda x: labelX if x else background_label
    )
    data[labelY] = data.index.isin(setY)
    # data[labelY] = data[labelY].apply(
    #     lambda x: labelY if x else background_label
    # )

    order = [labelX, background_label]

    if ax is None:
        fig, ax = plt.subplots(figsize=figsize)

    if alpha > 0:
        sns.barplot(
            data=data,
            x=labelX,
            y=labelY,
            hue=labelX,
            order=order,
            errorbar="se",
            palette = {
                labelX: color,
                background_label: background_color
            },
            capsize=capsize,
            linewidth=linewidth,
            fill=True,
            alpha=alpha,
            err_kws={"linewidth": 0},
            ax=ax,
            legend=False
        )

    sns.barplot(
        data=data,
        x=labelX,
        y=labelY,
        hue=labelX,
        order=order,
        errorbar="se",
        palette = {
            labelX: color,
            background_label: background_color
        },
        capsize=capsize,
        linewidth=linewidth,
        fill=False,
        err_kws={"linewidth": linewidth},
        ax=ax,
        legend=False
    )

    ax.set_xticks([0, 1], labels=[labelX, background_label])#, rotation=30)
    ax.set_xlabel("")
    ax.set_ylabel(f"Proportion of {labelY}")
    ax.set_title(title)

    # Create the 2x2 contingency table
    contingency_table = pd.crosstab(data[labelX], data[labelY])
    odds_ratio, p_value = fisher_exact(contingency_table, alternative="greater")

    pairs = [(labelX, background_label)]
    annotator = Annotator(ax, pairs, data=data, x=labelX, y=labelY, order=order)

    annotator.set_pvalues([p_value])

    annotator.configure(text_format="simple", loc="inside", line_width=1,)

    annotator.annotate()

    if ylim is not None:
        ax.set_ylim(ylim)
    
    # for spine in ax.spines.values():
    #     spine.set_visible(True)
    #     spine.set_color(".3")
    #     spine.set_linewidth(2)

    if save:
        plt.savefig(save, bbox_inches="tight")

    plt.tight_layout()

    return data