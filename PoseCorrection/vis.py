import pickle
import os
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt

joints = {0: 'Nose', 1: 'Neck', 2: 'RShoulder', 3: 'RElbow', 4: 'RWrist', 5: 'LShoulder', 6: 'LElbow',7: 'LWrist', 
        8: 'MidHip', 9: 'RHip', 10: 'RKnee', 11: 'RAnkle', 12: 'LHip', 13: 'LKnee', 14: 'LAnkle', 15: 'REye', 
        16: 'LEye', 17: 'REar', 18: 'LEar', 19: 'LBigToe', 20: 'LSmallToe', 21: 'LHeel', 22: 'RBigToe', 
        23: 'RSmallToe', 24: 'RHeel'}
links = {0: [0, 1], 1: [1, 2, 5, 8], 2: [2, 3], 3:[3, 4], 4: [4], 5: [5, 6], 6: [6, 7], 7: [7], 
    8: [8, 9, 12], 9: [9, 10], 10: [10, 11], 11: [11, 22, 24], 12: [12, 13], 13: [13, 14], 
    14: [14, 19, 21], 19: [19], 21: [21], 22: [22], 24: [24]}
img_width = 1920
img_height = 1080

class Visualize():

    def pickle_read(filename):
        with open(filename, "rb") as f:
            data = pickle.load(f)
        return data

    def convert_points(pts):
        pts_bis = []
        for p in pts:
            if p == 19:
                pts_bis.append(15)
            elif p == 21:
                pts_bis.append(16)
            elif p == 22:
                pts_bis.append(17)
            elif p == 24:
                pts_bis.append(18)
            else: 
                pts_bis.append(p)
        return pts_bis
    
    def plotting_im(seqs, N, fig, row, col):

        global joints
        global links
        global img_height
        global img_width

        x = {0: {}, 1: {}}
        y = {0: {}, 1: {}}
        z = {0: {}, 1: {}}
        x_lines = {0: {}, 1: {}}
        y_lines = {0: {}, 1: {}}
        z_lines = {0: {}, 1: {}}

        frames = []

        for i, seq in enumerate(seqs):

            x[i][N] = [a for j, a in enumerate(seq[:,N]) if j//19 == 0]
            y[i][N] = [a for j, a in enumerate(seq[:,N]) if j//19 == 1]
            z[i][N] = [a for j, a in enumerate(seq[:,N]) if j//19 == 2]

            x_lines[i][N] = []
            y_lines[i][N] = []
            z_lines[i][N] = []
            lines_colors = []
            for p1, v in links.items():
                for p2 in v:
                    if p1 != p2:
                        p = Visualize.convert_points([p1, p2])
                        for j in range(2):
                            x_lines[i][N].append(x[i][N][p[j]])
                            y_lines[i][N].append(y[i][N][p[j]])
                            z_lines[i][N].append(z[i][N][p[j]])
                            lines_colors.append(p[i])
                        x_lines[i][N].append(None)                        
                        y_lines[i][N].append(None)
                        z_lines[i][N].append(None)
                        lines_colors.append(15)
                        
        fig.add_trace(go.Scatter3d(x=x[1][N], y=y[1][N], z=z[1][N], mode='markers', name='Joints', hoverinfo='text', 
                                hovertext=list(joints.values()), opacity=0.8, 
                                marker=dict(color='green', size=6)), row=row, col=col)
        
        fig.add_trace(go.Scatter3d(x=x_lines[1][N], y=y_lines[1][N], z=z_lines[1][N], mode='lines', name='Links', 
                                hoverinfo='text', opacity=0.8, line=dict(color='green', width=5)), row=row, col=col)

        fig.add_trace(go.Scatter3d(x=x[0][N], y=y[0][N], z=z[0][N], mode='markers', name='Joints', hoverinfo='text', 
                                hovertext=list(joints.values()), opacity=0.8, 
                                marker=dict(color='red', size=6)), row=row, col=col)
    
        fig.add_trace(go.Scatter3d(x=x_lines[0][N], y=y_lines[0][N], z=z_lines[0][N], mode='lines', name='Links', 
                                hoverinfo='text', opacity=0.8, line=dict(color='red', width=5)), row=row, col=col)

        return fig
    
    def plotting_seq(seqs, fig, row, col, im, frames, Ns):

        global joints
        global links
        global img_height
        global img_width

        x = {0: {}, 1: {}}
        y = {0: {}, 1: {}}
        z = {0: {}, 1: {}}
        x_lines = {0: {}, 1: {}}
        y_lines = {0: {}, 1: {}}
        z_lines = {0: {}, 1: {}}

        for N in range(Ns[im+1]-Ns[im]):
            for i, seq in enumerate(seqs):

                x[i][N] = [a for j, a in enumerate(seq[:,N]) if j//19 == 0]
                y[i][N] = [a for j, a in enumerate(seq[:,N]) if j//19 == 1]
                z[i][N] = [a for j, a in enumerate(seq[:,N]) if j//19 == 2]

                x_lines[i][N] = []
                y_lines[i][N] = []
                z_lines[i][N] = []
                lines_colors = []
                for p1, v in links.items():
                    for p2 in v:
                        if p1 != p2:
                            p = Visualize.convert_points([p1, p2])
                            for j in range(2):
                                x_lines[i][N].append(x[i][N][p[j]])
                                y_lines[i][N].append(y[i][N][p[j]])
                                z_lines[i][N].append(z[i][N][p[j]])
                                lines_colors.append(p[i])
                            x_lines[i][N].append(None)
                            y_lines[i][N].append(None)
                            z_lines[i][N].append(None)
                            lines_colors.append(15)
                            
            data=[go.Scatter3d(x=x[0][N], y=y[0][N], z=z[0][N], mode='markers', name='Joints',
                            hoverinfo='text', hovertext=list(joints.values()), 
                            marker=dict(color='red', size=5)),
                go.Scatter3d(x=x_lines[0][N], y=y_lines[0][N], z=z_lines[0][N], mode='lines', 
                            name='Links', hoverinfo='text', line=dict(color='red', width=5)),
                go.Scatter3d(x=x[1][N], y=y[1][N], z=z[1][N], mode='markers', name='Joints', 
                            hoverinfo='text', hovertext=list(joints.values()), 
                            marker=dict(color='green', size=5)),
                go.Scatter3d(x=x_lines[1][N], y=y_lines[1][N], z=z_lines[1][N], mode='lines', 
                            name='Links', hoverinfo='text', line=dict(color='green', width=5))]
            
            traces = [im * 4, im * 4 + 1, im * 4 + 2, im * 4 + 3]
            frames.append(dict(name=int(Ns[im])+N, data=data, traces=traces))

        fig.add_trace(go.Scatter3d(x=x[0][0], y=y[0][0], z=z[0][0], mode='markers', name='Joints',
                                hoverinfo='text', hovertext=list(joints.values()), 
                                marker=dict(color='red', size=5)), row=row, col=col)
        
        fig.add_trace(go.Scatter3d(x=x_lines[0][0], y=y_lines[0][0], z=z_lines[0][0], mode='lines', 
                                name='Links', hoverinfo='text', line=dict(color='red', width=5)), row=row, col=col)
                            
        fig.add_trace(go.Scatter3d(x=x[1][0], y=y[1][0], z=z[1][0], mode='markers', name='Joints', 
                                hoverinfo='text', hovertext=list(joints.values()), 
                                marker=dict(color='green', size=5)), row=row, col=col)
        
        fig.add_trace(go.Scatter3d(x=x_lines[1][0], y=y_lines[1][0], z=z_lines[1][0], mode='lines', 
                                name='Links', hoverinfo='text', line=dict(color='green', width=5)), row=row, col=col)

        return fig
    

preds = Visualize.pickle_read('Results/pose_3d.pickle')
inputs = preds['inputs_3d']
outputs = preds['pose_corr_3d']
targets = preds['targets_3d']
#inputs = preds['preds']['in']
#outputs = preds['preds']['out']
#targets = preds['preds']['targ']

#fig = make_subplots(rows=2, cols=3, 
#                    specs=[[{'type': 'Scatter3d'}, {'type': 'Scatter3d'}, {'type': 'Scatter3d'}],
#                           [{'type': 'Scatter3d'}, {'type': 'Scatter3d'}, {'type': 'Scatter3d'}]],
#                   horizontal_spacing = 0, vertical_spacing = 0.1)

fig = make_subplots(rows=1, cols=11, 
                    specs=[[{'type': 'Scatter3d'}, {'type': 'Scatter3d'}, {'type': 'Scatter3d'}, {'type': 'Scatter3d'}, {'type': 'Scatter3d'}, {'type': 'Scatter3d'}, {'type': 'Scatter3d'}, {'type': 'Scatter3d'}, {'type': 'Scatter3d'}, {'type': 'Scatter3d'}, {'type': 'Scatter3d'}]],
                   horizontal_spacing = 0, vertical_spacing = 0)

plot = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
frames = []

Ns = [0]
for el in plot:
    Ns.append(inputs[el].shape[1])
Ns = np.cumsum(Ns)

for i, el in enumerate(plot):
    row = 1
    col = i + 1
    #row = i // 3 + 1
    #col = i % 3 + 1
    fig = Visualize.plotting_seq([inputs[el], outputs[el]], fig, row, col, i, frames, Ns)
    
scene = dict(xaxis = dict(range=[-0.9,0.9], 
                                                backgroundcolor="rgb(200, 200, 230)",
                                                showgrid=False,
                                                zeroline=False,
                                                showticklabels=False,
                                                showbackground=True,
                                                visible=False, 
                                                title=''), 
                                   yaxis = dict(range=[-0.9,0.9], 
                                                backgroundcolor="rgb(230, 200, 230)",
                                                showgrid=False,
                                                zeroline=False,
                                                showticklabels=False,
                                                showbackground=True,
                                                visible=False,
                                                title=''), 
                                   zaxis = dict(range=[-0.9,0.9], 
                                                backgroundcolor="rgb(230, 230, 200)",
                                                showgrid=False,
                                                zeroline=False,
                                                showticklabels=False,
                                                showbackground=True,
                                                visible=False,
                                                title=''),
                                   aspectmode='cube')

sliders = [dict(steps= [dict(method= 'animate',
                           args= [[ f'frame{k}'],
                                  dict(mode= 'immediate',
                                  frame= dict(duration=100, redraw= True ),
                                              transition=dict( duration= 0))
                                 ],
                            label='{:d}'.format(k)
                             ) for k in range(len(frames))], 
                transition= dict(duration= 0 ),
                x=0,#slider starting position  
                y=0, 
                currentvalue=dict(font=dict(size=12), 
                                  prefix='Point: ', 
                                  visible=True, 
                                  xanchor= 'center'),  
                len=1.0)
           ]

fig.update(frames=frames)
fig.update_layout(scene=scene, scene1=scene, scene2=scene, scene3=scene, scene4=scene, scene5=scene, scene6=scene, scene7=scene, scene8=scene, scene9=scene, scene10=scene, scene11=scene,
                  height=700, width=1400,
                  showlegend=False, margin=go.layout.Margin(l=0, r=0, b=0, t=0),
                  updatemenus = [dict(type="buttons", 
                                          buttons=[dict(label="Pause", method="animate",
                                                        args=[[None], {"frame": {"duration": 0, "redraw": False},
                                                                      "mode": "immediate",
                                                                      "transition": {"duration": 0}}]),
                                                  dict(label="SQUAT: Correct", method="animate",
                                                        args=[[f'{k}' for k in range(2)], {"frame": {"duration": 1, "redraw": True},
                                                                     "transition": {"duration": 0}}]),
                                                  dict(label="SQUAT: Feet too wide", method="animate",
                                                        args=[[f'{k}' for k in range(Ns[1], Ns[1]+4)], {"frame": {"duration": 2, "redraw": True},
                                                                     "transition": {"duration": 100}}]),
                                                  dict(label="SQUAT: Knees inward", method="animate",
                                                        args=[[f'{k}' for k in range(Ns[2], Ns[2]+6)], {"frame": {"duration": 3, "redraw": True},
                                                                     "transition": {"duration": 0}}]),
                                                  dict(label="SQUAT: Not low enough", method="animate",
                                                        args=[[f'{k}' for k in range(Ns[3], Ns[3]+8)], {"frame": {"duration": 4, "redraw": True},
                                                                     "transition": {"duration": 0}}]),
                                                  dict(label="SQUAT: Front bent", method="animate",
                                                        args=[[f'{k}' for k in range(Ns[4], Ns[4]+10)], {"frame": {"duration": 5, "redraw": True},
                                                                     "transition": {"duration": 0}}]),
                                                  dict(label="SQUAT: Front bent", method="animate",
                                                        args=[[f'{k}' for k in range(Ns[5], Ns[5]+12)], {"frame": {"duration": 6, "redraw": True},
                                                                     "transition": {"duration": 0}}]),
                                                  dict(label="SQUAT: Front bent", method="animate",
                                                        args=[[f'{k}' for k in range(Ns[6], Ns[6]+14)], {"frame": {"duration": 7, "redraw": True},
                                                                     "transition": {"duration": 0}}]),
                                                  dict(label="SQUAT: Front bent", method="animate",
                                                        args=[[f'{k}' for k in range(Ns[7], Ns[7]+16)], {"frame": {"duration": 8, "redraw": True},
                                                                     "transition": {"duration": 0}}]),
                                                  dict(label="SQUAT: Front bent", method="animate",
                                                        args=[[f'{k}' for k in range(Ns[8], Ns[8]+18)], {"frame": {"duration": 9, "redraw": True},
                                                                     "transition": {"duration": 0}}]),
                                                  dict(label="SQUAT: Front bent", method="animate",
                                                        args=[[f'{k}' for k in range(Ns[9], Ns[9]+20)], {"frame": {"duration": 10, "redraw": True},
                                                                     "transition": {"duration": 0}}]),
                                                  dict(label="SQUAT: Front bent", method="animate",
                                                        args=[[f'{k}' for k in range(Ns[10], Ns[10]+24)], {"frame": {"duration": 10, "redraw": True},
                                                                     "transition": {"duration": 0}}])])],
                                          sliders=sliders)


fig.show()
#plt.savefig(fig)
