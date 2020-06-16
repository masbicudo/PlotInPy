import plotinpy as pnp
import matplotlib.pyplot as plt

plt.figure()
pnp.plot_bars_with_breaks([1,2,30],[(15,25)])
plt.savefig("img/example1.png")

plt.figure()
pnp.plot_bars_with_breaks([1,2,30, 1000],[(15,25), (50, 975)], style="~~", break_args={"hatch": '///'})
plt.savefig("img/example2.png")
