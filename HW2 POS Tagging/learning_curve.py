import matplotlib.pyplot as plt

# data for the graph
x = [5000,  10000,
     15000, 20000,
     25000, 30000,
     35000, 40000]
y = [0.108258344342797, 0.0814367973676995,
     0.0702943889124311, 0.0656080963182691,
     0.0612707829598425, 0.0571827404840841,
     0.0559862402472767, 0.0540917815389984]


# plot x y data
plt.plot(x,y)

# given plot label
plt.xlabel('Training Dataset Size')
plt.ylabel('Word Error Rate')

# give plot title
plt.title('Error Rate by word')

# give x axis step spec
plt.xticks(x)

# show the graph
plt.show()