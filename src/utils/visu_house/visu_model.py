from xgboost import plot_tree
import matplotlib.pyplot as plt
import pickle

model = pickle.load(open("bg_reg.pkl", "rb"))
plot_tree(model)
plt.show()