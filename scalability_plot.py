import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os, math

scalability_csv = os.path.abspath(os.path.join("output_files", "scalability.csv"))
df = pd.read_csv(scalability_csv)

pivot_table = df.pivot_table(index='services', columns='nodes', values='kwhelectricity')
pivot_table2 = df.pivot_table(index='services', columns='nodes', values='secondsexectime')

X = pivot_table.columns.values  
Y = pivot_table.index.values 
X, Y = np.meshgrid(X, Y)
Z = pivot_table.values   
Z2 = pivot_table2.values  

fig = plt.figure(figsize=(12, 8))
ax1 = fig.add_subplot(121, projection='3d')
ax2 = fig.add_subplot(122, projection='3d')

surface = ax1.plot_surface(X, Y, Z, cmap='viridis', edgecolor='k', alpha=0.9)
surface2 = ax2.plot_surface(X, Y, Z2, cmap='viridis', edgecolor='k', alpha=0.9)

ax1.set_xlabel('Number of Nodes')
ax1.set_ylabel('Number of Services')
ax1.set_zlabel('Energy Consumption')
ax1.set_title('3D Surface Plot of Energy Consumption (kWh)')

ax2.set_xlabel('Number of Nodes')
ax2.set_ylabel('Number of Services')
ax2.set_zlabel('Execution Time')
ax2.set_title('3D Surface Plot of Execution Time (seconds)')

fig.colorbar(surface, ax=ax1, shrink=0.5, aspect=5)
fig.colorbar(surface2, ax=ax2, shrink=0.5, aspect=5)

unique_nodes = df['nodes'].unique()
unique_nodes.sort()

valid_nodes = []
for node in unique_nodes:
    if len(df[df['nodes'] == node]) > 1:
        valid_nodes.append(node)

n_plots = len(valid_nodes)
n_cols = 4
n_rows = math.ceil(n_plots / n_cols)

fig, axes = plt.subplots(n_rows, n_cols, figsize=(4 * n_cols, 4 * n_rows), sharey=True, sharex=True)
axes = axes.flatten()
fig.suptitle('Fixed Nodes - Energy', fontsize=16)

for idx, node in enumerate(valid_nodes):
    subset = df[df['nodes'] == node]
    grouped = subset.groupby('services', as_index=False)['kwhelectricity'].mean()
    services = grouped['services']
    energy = grouped['kwhelectricity']

    axes[idx].plot(services, energy, marker='o', linestyle='-')
    axes[idx].set_title(f'{node} Nodes')
    axes[idx].set_xlabel('Services')
    axes[idx].set_ylabel('Energy (kWh)')
    axes[idx].set_xticks(range(100, 1000 + 1, 100))
    axes[idx].grid(True)

for i in range(len(valid_nodes), len(axes)):
    axes[i].axis('off')

fig2, axes2 = plt.subplots(n_rows, n_cols, figsize=(4 * n_cols, 4 * n_rows), sharey=True, sharex=True)
axes2 = axes2.flatten()
fig2.suptitle('Fixed Nodes - Time', fontsize=16)

for idx, node in enumerate(valid_nodes):
    subset = df[df['nodes'] == node]
    grouped = subset.groupby('services', as_index=False)['secondsexectime'].mean()
    services = grouped['services']
    energy = grouped['secondsexectime']

    axes2[idx].plot(services, energy, marker='o', linestyle='-')
    axes2[idx].set_title(f'{node} Nodes')
    axes2[idx].set_xlabel('Services')
    axes2[idx].set_ylabel('Seconds (s)')
    axes2[idx].set_xticks(range(100, 1000 + 1, 100))
    axes2[idx].grid(True)

for i in range(len(valid_nodes), len(axes2)):
    axes2[i].axis('off')

unique_services = df['services'].unique()
unique_services.sort()

valid_services = []
for service in unique_services:
    if len(df[df['services'] == service]) > 1:
        valid_services.append(service)

n_plots = len(valid_services)
n_cols = 4
n_rows = math.ceil(n_plots / n_cols)

fig3, axes3 = plt.subplots(n_rows, n_cols, figsize=(4 * n_cols, 4 * n_rows), sharey=True, sharex=True)
axes3 = axes3.flatten()
fig3.suptitle('Fixed Services - Energy', fontsize=16)

for idx, service in enumerate(valid_services):
    subset = df[df['services'] == service]
    grouped = subset.groupby('nodes', as_index=False)['kwhelectricity'].mean()
    nodes = grouped['nodes']
    energy = grouped['kwhelectricity']

    axes3[idx].plot(nodes, energy, marker='o', linestyle='-')
    axes3[idx].set_title(f'{service} Services')
    axes3[idx].set_xlabel('Nodes')
    axes3[idx].set_ylabel('Energy (kWh)')
    axes3[idx].set_xticks(range(100, 1000 + 1, 100))
    axes3[idx].grid(True)

for i in range(len(valid_services), len(axes3)):
    axes3[i].axis('off')

fig4, axes4 = plt.subplots(n_rows, n_cols, figsize=(4 * n_cols, 4 * n_rows), sharey=True, sharex=True)
axes4 = axes4.flatten()
fig4.suptitle('Fixed Services - Time', fontsize=16)

for idx, service in enumerate(valid_services):
    subset = df[df['services'] == service]
    grouped = subset.groupby('nodes', as_index=False)['secondsexectime'].mean()
    nodes = grouped['nodes']
    energy = grouped['secondsexectime']

    axes4[idx].plot(nodes, energy, marker='o', linestyle='-')
    axes4[idx].set_title(f'{service} Services')
    axes4[idx].set_xlabel('Nodes')
    axes4[idx].set_ylabel('Seconds (s)')
    axes4[idx].set_xticks(range(100, 1000 + 1, 100))
    axes4[idx].grid(True)

for i in range(len(valid_services), len(axes4)):
    axes4[i].axis('off')

plt.tight_layout()
plt.show()