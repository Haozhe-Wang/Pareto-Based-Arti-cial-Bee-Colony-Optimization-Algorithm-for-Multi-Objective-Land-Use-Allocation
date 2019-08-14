try:
    import matplotlib.pyplot as plt
    from matplotlib.font_manager import FontProperties
except:
    raise ImportError("Install 'matplotlib' to plot convergence results.")
import numpy as np

def show(dataSet):
    # font = FontProperties()
    # font.set_size('larger')
    # plt.figure(figsize=(12.5, 4))
    # # x,y=np.array(dataSet[0]),np.array(dataSet[1])
    # x,y = dataSet[0],dataSet[1]
    # plt.scatter(x, y, color='red', label='result')
    # plt.xlabel("水源涵养")
    # plt.ylabel("氮净化")
    # plt.legend(loc="best", prop=font)
    # plt.xlim([0, len(dataSet)])
    # plt.grid()
    # plt.show()
    plt.plot(dataSet[0], dataSet[1], 'ro')
    plt.show()