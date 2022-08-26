import matplotlib.pyplot as plt
import numpy as np

fig,ax = plt.subplots(figsize=(8,8))
fig.set_facecolor("white")

ax.grid(linewidth=0.25, zorder=1)

ax.set_title("Sampling of matplotlib")

np.random.seed(402)
x=np.random.uniform(0,1,50)
y=np.random.uniform(0,1,50)

ax.scatter(x,y,
           edgecolors="white",#border to dot
           linewidths=0.5,
           s=400, #size of dot
           zorder=2)#priority on plotting

ax.set_xlim(0,1)
ax.set_ylim(0,1)

plt.tight_layout() #margin
plt.savefig("../../sample", bbox_inches="tight", dpi =300) #image quality
plt.show()