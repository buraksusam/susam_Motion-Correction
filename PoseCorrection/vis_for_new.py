import pickle
import json
import os
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt

#This script is to control DCPose outputs

joints = {0: 'Nose', 1: 'BHead', 2: 'THead', 3: 'LEar', 4: 'REar', 5: 'LShoulder', 6: 'RShoulder', 7: 'LElbow', 8: 'RElbow', 9: 'LWrist', 
        10: 'RWrist', 11: 'LHip', 12: 'RHip', 13: 'LKnee', 14: 'RKnee', 15: 'LAnkle', 16: 'RAnkle'}

links = {0: [0, 1], 1: [1, 2, 5, 6, 11, 12], 2: [2], 5: [5, 7], 6: [6, 8], 7: [7, 9], 
    8: [8, 10], 9: [9], 10: [10], 11: [11, 13], 12: [12, 14], 13: [13, 15], 
    14: [14, 16], 15: [15], 16: [16]}

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
    
    
json_file = open('../../../ozdemir/sample_out/6_1/result_GH01161.json')     #here, place the result json file
data_json = json.load(json_file)
pickle_out = open("pickle_data", "wb")
pickle.dump(data_json, pickle_out)
pickle_out.close()

frames = [('Info', '/cvlabdata2/home/ozdemir/samplevideos/6.1/GH010161/00028630.jpg')]      #here, select the frame you want to visualize
cameras = ['6_4']

plt.figure(figsize=(20,20))
for l, f in enumerate(frames):
    for k, cam in enumerate(cameras):
        gt2d = pickle_out[f[0]][f[1]]['2D_gt'][cam]
        
        x2d = [i[0] for k, i in gt2d['p'].items() if k in links.keys()]
        y2d = [i[1] for k, i in gt2d['p'].items() if k in links.keys()]
        c2d = [i for k, i in gt2d['c'].items() if k in links.keys()]
        
        plt.subplot(4, 1, k + 1)
        colors = plt.cm.plasma(np.linspace(0, 1, len(x2d)))
        plt.scatter(x=x2d, y=y2d, c=colors, s=10)
        
        for p1, v in links.items():
            for p2 in v:
                if p1 != p2:
                    p = Visualize.convert_points([p1, p2])
                    if c2d[p[0]] == 1 and c2d[p[1]] == 1:
                        xs = [x2d[p[0]], x2d[p[1]]]
                        ys = [y2d[p[0]], y2d[p[1]]]
                        plt.plot(xs, ys, c=colors[p[0]])
                    
        plt.xticks([])
        plt.yticks([])
        
plt.show()

