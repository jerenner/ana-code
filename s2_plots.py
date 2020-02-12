lt.rcParams["figure.figsize"] = 10, 8
plt.rcParams["font.size"     ] = 14
sns.set()
sns.set_style("white")
sns.set_style("ticks")


def s1_control_plots(plots_dir, dst, s1e_range, s1e_bin, s1w_range, s1w_bin, s1h_range, s1h_bin):
    """
    Control plots for S2 signals
    """
