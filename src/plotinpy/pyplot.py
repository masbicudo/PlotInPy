from . pandas import _check_is_dataframe
from . styling import build_break_style_info
from . utils import _Result

def plot_bars_with_breaks(dataset, breaks, ax=None, bar_group_width=0.8, y_step=100, style="^", style_inv=False, break_args=None, debug=False, **kwargs):
    # reference: https://stackoverflow.com/questions/53642861/broken-axis-slash-marks-inside-bar-chart-in-matplotlib
    import numpy as np
    import matplotlib.pyplot as plt

    is_df = _check_is_dataframe(dataset)
    if is_df:
        df = dataset
        dataset = []
        for s_name in df:
            dataset.append(df[s_name])
    else:
        dataset = [dataset]

    from matplotlib.transforms import Bbox
    from matplotlib.patches import Rectangle
    from matplotlib.patches import Polygon
    import matplotlib.transforms as trans

    brk_count = len(breaks) + 1
    min_val = 0
    max_val = df.values.max() if is_df else np.array(dataset).max()
    if (debug): print(f"brk_count={brk_count}, min_val={min_val}, max_val={max_val}")
    ints = []
    hs = []
    sum_breaks = 0
    for i in range(brk_count - 1):
        sum_breaks += breaks[i][1] - breaks[i][0]
    for i in range(brk_count):
        base = breaks[brk_count - 2 - i][1] if i < brk_count - 1 else min_val
        if (debug): print(f"brk_count={brk_count}")
        top  = breaks[brk_count - 1 - i][0] if i > 0             else max_val + 0.1*(max_val - min_val - sum_breaks)
        ints.append((base, top))
        if (debug): print(f"base={base}, top={top}")
        hs.append(top - base)
    hs = np.array(hs)
    hs = hs/hs.min()

    plt_count = len(dataset)
    width = bar_group_width/plt_count

    if ax is None:
        ax = plt.gca()
    fig = ax.get_figure()
    subplotspec = ax.get_subplotspec()
    subgridspec = subplotspec.subgridspec(ncols=1, nrows=brk_count, height_ratios=hs)
    ax.remove()
    ax = None
    axes = []
    if debug: print(subgridspec[0, 0])
    for i in range(brk_count):
        subplotspec = subgridspec[brk_count - i - 1, 0]
        if i == 0:
            axes.append(fig.add_subplot(subplotspec))
        else:
            axN = fig.add_subplot(subplotspec, sharex=axes[0])
            axN.axes.get_xaxis().set_visible(False)
            axes.append(axN)
    axes = list(reversed(axes))


    style_points = build_break_style_info(style)
    style_points_inv = np.concatenate(([[0,0]], style_points - [0, 1], [[1,0]]), axis=0)
    style_points = np.concatenate(([[0,0]], style_points, [[1,0]]), axis=0)
    if style_inv:
        _ = style_points
        style_points = style_points_inv*[1,-1]
        style_points_inv = _*[1,-1]
    if (debug): print(f"style_points_inv={style_points_inv}")
    segments_screen_coords = []
    seg_colors = []

    for i, ax in enumerate(axes):
        if i < brk_count - 1: ax.spines['bottom'].set_visible(False)
        if i > 0: ax.spines['top'].set_visible(False)
        ax.tick_params(axis='x',which='both',bottom=False)
        ax.set_facecolor((0, 0, 0, 0))
        base = ints[i][0]
        top  = ints[i][1]
        d = 0.1/hs[i]
        if (debug): print(f"base={base}, top={top}")
        ax.set_ylim(base, top)
        ax.set_yticks(np.arange(base, top+0.0000001, y_step))
        bars_groups = []
        for j, points in enumerate(dataset):
            #if j > 0: break
            offs = bar_group_width*(j*2 - plt_count + 1)/(plt_count*2)
            if (debug): print("offs", offs)
            ind = np.arange(len(points))
            if j == 0:
                ax.set_xticks(ind)
                ax.set_xticklabels(points.index if is_df else range(len(dataset[0])))
            if (debug): print(f"points={points}")
            kwargs2 = {**kwargs}
            if is_df: kwargs2["label"] = points.name
            bars = ax.bar(
                ind + offs,
                points.values if is_df else points,
                **kwargs,
                width=width
                )
            bars_groups.append(bars)

        top_seg = []
        bottom_seg = []
        segments_screen_coords.append(top_seg)
        segments_screen_coords.append(bottom_seg)

        t = ax.get_xaxis_transform()
        for j, bars in enumerate(bars_groups):
            for rect in bars:
                x = rect.get_x()
                y = rect.get_y()
                w = rect.get_width()
                h = rect.get_height()
                c = rect.get_facecolor()
                b = rect.get_bbox()
                if (debug): print(f"bbox={b}")

                if (i == 0):
                    seg_colors.append(c)

                # bottom of the top break
                if h >= top:

                    pts = style_points*[w,d] + [x,1]
                    p = Polygon(pts, True, facecolor=c, clip_on=False, transform=t, aa=True, snap=True)
                    ax.add_patch(p)

                    top_seg.append(t.transform([[x,1],[x+w,1]]))
                else:
                    top_seg.append(None)

                # top of the bottom break
                if i < brk_count - 1 and h >= base:

                    pts = style_points_inv*[w,d] + [x,0]
                    p = Polygon(pts, True, facecolor=c, clip_on=False, transform=t, aa=True, snap=True)
                    ax.add_patch(p)

                    bottom_seg.append(t.transform([[x,0],[x+w,0]]))
                else:
                    bottom_seg.append(None)

                if (debug): ax.add_patch(rect)

                # number over the bar
                # TODO: this should be optional
                if base < h and h <= top:
                    if (debug): print(f"base={base}, top={top}")
                    if (debug): print("   ", "xy", (x + w / 2, h))
                    ax.annotate('{}'.format(h),
                                xy=(x + w / 2, h),
                                xytext=(0, 3),  # use 3 points offset
                                textcoords="offset points",  # in both directions
                                ha="center", va='bottom')

        if (debug): print(f"seg_colors={seg_colors}")
        if break_args is not None:
            if i > 0:
                t_inv = t.inverted()
                break_top_segs = segments_screen_coords[-3]
                break_bottom_segs = segments_screen_coords[-2]
                for k, (top_seg, bottom_seg, c) in enumerate(zip(break_top_segs, break_bottom_segs, seg_colors)):
                    if top_seg is not None and bottom_seg is not None:
                        pts = [*top_seg, *bottom_seg[::-1]]
                        pts = t_inv.transform(pts)
                        p = Polygon(pts, True, edgecolor=c, facecolor=(0,0,0,0), linewidth=0, clip_on=False, transform=t, aa=True, snap=True, **break_args)
                        ax.add_patch(p)

    # TODO: the result should have a dedicated class
    data = _Result()
    data["figure"] = fig
    data["axes"] = axes
    #data["legend"] = axes[0].legend()
    return data
