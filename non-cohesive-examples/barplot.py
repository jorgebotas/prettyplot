import seaborn as sns
import matplotlib.pyplot as plt
from typing import Optional, List, Dict
import pandas as pd
from matplotlib.patches import Patch


def prepare_split_data(
    data: pd.DataFrame, 
    x: str, 
    y: str, 
    split_col: str,
    split_order: Optional[List[str]] = None
) -> pd.DataFrame:
    """
    Prepare data for split bar plotting by creating a combined column.
    
    Parameters
    ----------
    data : DataFrame
        Input data
    x : str
        Column name for x-axis grouping
    y : str
        Column name for y-axis values
    split_col : str
        Column name to split bars (e.g., 'label' for celltype/genotype)
    split_order : list, optional
        Order of split values. If provided, data will be sorted to match this order.
    
    Returns
    -------
    DataFrame
        Data with new combined column for proper bar separation
    """
    data = data.copy()
    
    # If split_order is provided, ensure the split column follows that order
    if split_order is not None:
        data[split_col] = pd.Categorical(data[split_col], categories=split_order, ordered=True)
        data = data.sort_values([x, split_col])
    
    # Create a combined column that seaborn will use to separate bars
    data['_plot_group'] = data[x].astype(str) + '_' + data[split_col].astype(str)
    return data


def apply_hatch_to_bars(
    ax: plt.Axes, 
    data: pd.DataFrame,
    split_col: str,
    hatch_mapping: Optional[Dict[str, str]] = None,
    n_x_groups: Optional[int] = None
) -> None:
    """
    Apply hatch patterns to bars based on a split column.
    
    Parameters
    ----------
    ax : plt.Axes
        Axes object containing the bars
    data : DataFrame
        Original data with split column
    split_col : str
        Column name used for splitting
    hatch_mapping : dict, optional
        Mapping from split values to hatch patterns
    n_x_groups : int, optional
        Number of x-axis groups (auto-detected if None)
    """
    if hatch_mapping is None:
        # Default hatch patterns
        unique_vals = data[split_col].unique()
        default_patterns = ['', '///', '\\\\\\', '|||', '---', '+++', 'xxx']
        hatch_mapping = {val: default_patterns[i % len(default_patterns)] 
                        for i, val in enumerate(unique_vals)}
    
    # Get split values in the order specified by hatch_mapping
    split_values = list(hatch_mapping.keys())
    n_splits = len(split_values)
    
    for idx, patch in enumerate(ax.patches):
        if hasattr(patch, 'get_height'):  # Check if it's a bar
            split_idx = idx % n_splits
            split_val = split_values[split_idx]
            patch.set_hatch(hatch_mapping[split_val])


def create_split_legend(
    base_palette: Dict[str, str],
    split_values: List[str],
    hatch_mapping: Dict[str, str],
    linewidth: float = 2,
    split_label: str = "Type"
) -> tuple:
    """
    Create legend handles and labels for split bar plot.
    
    Parameters
    ----------
    base_palette : dict
        Color palette for main groups
    split_values : list
        Values used for splitting bars
    hatch_mapping : dict
        Mapping from split values to hatch patterns
    linewidth : float
        Line width for legend patches
    split_label : str
        Label for the split category
    
    Returns
    -------
    tuple
        (handles, labels) for legend
    """
    handles = []
    labels = []
    
    # Add main color groups
    for name, color in base_palette.items():
        patch = Patch(
            edgecolor=color,
            facecolor='white',
            linewidth=linewidth,
            label=name
        )
        handles.append(patch)
        labels.append(name)
    
    # Add split patterns
    for split_val in split_values:
        patch = Patch(
            edgecolor='.3',
            facecolor='white',
            linewidth=linewidth,
            hatch=hatch_mapping[split_val],
            label=split_val
        )
        handles.append(patch)
        labels.append(split_val)
    
    return handles, labels


def barplot(
        data: pd.DataFrame,
        x: str,
        y: str,
        hue: Optional[str] = None,
        split: Optional[str] = None,
        color: Optional[str] = None,
        ax: Optional[plt.Axes] = None,
        title: str = "",
        xlabel: str = "",
        ylabel: str = "",
        linewidth: float = 2,
        capsize: float = 0.0,
        alpha: float = 0.1,
        figsize: tuple = (4, 4),
        palette: Optional[dict] = None,
        hatch_mapping: Optional[Dict[str, str]] = None,
        errorbar: str = "se",
        gap: float = 0.1,
    ):
    """
    Create a barplot with split bars and hatch patterns.
    
    Parameters
    ----------
    data : DataFrame
        Input data
    x : str
        Column name for x-axis categories
    y : str
        Column name for y-axis values
    hue : str, optional
        Column name for color grouping (typically same as x)
    split : str, optional
        Column name for splitting bars side-by-side with hatch patterns
    color : str, optional
        Single color for all bars
    ax : plt.Axes, optional
        Matplotlib axes object
    title : str
        Plot title
    xlabel : str
        X-axis label
    ylabel : str
        Y-axis label
    linewidth : float
        Width of bar edges
    capsize : float
        Width of error bar caps
    alpha : float
        Transparency of bar fill
    figsize : tuple
        Figure size if creating new figure
    palette : dict, optional
        Color palette mapping
    hatch_mapping : dict, optional
        Mapping from split values to hatch patterns
    errorbar : str
        Error bar type ('se', 'sd', 'ci', etc.)
    gap : float
        Gap between bar groups
    
    Returns
    -------
    ax : plt.Axes
        Matplotlib axes object
    """
    if ax is None:
        _, ax = plt.subplots(figsize=figsize)
    
    plot_data = data.copy()
    
    # If split is specified, prepare the data
    if split is not None:
        # Get split order from hatch_mapping keys if provided
        split_order = list(hatch_mapping.keys()) if hatch_mapping is not None else None
        
        plot_data = prepare_split_data(plot_data, x, y, split, split_order=split_order)
        plot_x = '_plot_group'
        
        # Create default hatch mapping if not provided
        if hatch_mapping is None:
            split_values = data[split].unique()
            default_patterns = ['', '///', '\\\\\\', '|||', '---', '+++']
            hatch_mapping = {val: default_patterns[i % len(default_patterns)] 
                           for i, val in enumerate(split_values)}
    else:
        plot_x = x
    
    # Create the outline bars
    sns.barplot(
        data=plot_data,
        x=plot_x,
        y=y,
        hue=hue if split is None else x,
        fill=False,
        linewidth=linewidth,
        capsize=capsize,
        ax=ax,
        palette=palette,
        err_kws={"linewidth": linewidth},
        errorbar=errorbar,
        gap=gap,
        legend=False,
    )
    
    # Add filled bars with alpha if needed
    if 0 < alpha < 1:
        sns.barplot(
            data=plot_data,
            x=plot_x,
            y=y,
            hue=hue if split is None else x,
            fill=True,
            alpha=alpha,
            linewidth=0,
            capsize=capsize,
            ax=ax,
            palette=palette,
            err_kws={"linewidth": 0},
            errorbar=errorbar,
            gap=gap,
            legend=False,
        )
    
    # Apply hatch patterns if split is used
    if split is not None:
        apply_hatch_to_bars(
            ax=ax,
            data=data,
            split_col=split,
            hatch_mapping=hatch_mapping,
        )
        
        # Clean up x-axis labels to show only main categories
        x_labels = []
        seen = set()
        for label in plot_data['_plot_group']:
            main_label = label.split('_')[0]
            if main_label not in seen:
                x_labels.append(main_label)
                seen.add(main_label)
        
        # Update tick labels
        n_splits = len(data[split].unique())
        tick_positions = []
        for i, label in enumerate(x_labels):
            # Calculate center position for each group
            center = (n_splits * i) + (n_splits - 1) / 2
            tick_positions.append(center)
        
        ax.set_xticks(tick_positions)
        ax.set_xticklabels(x_labels)
    
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    
    return ax