import pickle
import os
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
import plotly.express as px
import json
from skimage import io

#you can plot ba point on images from here by choosing the same frame for f (L19) and img (L30) parameters
def pickle_read(filename):
    with open(filename, "rb") as f:
        data = pickle.load(f)
    return data

#df = pickle_read('./multiview_calib/scripts/ba_pose_3d_df.pickle')
f = open('multiview_calib/json_files/landmarks/landmarks_frame_60.json')
df = json.load(f)
data_frame = {}
data_frame["pose_x"] = []
data_frame["pose_y"] = []

for i in range(len(df["6_3"]["landmarks"])):
    data_frame["pose_x"].append(df["6_3"]["landmarks"][i][0])
    data_frame["pose_y"].append(df["6_3"]["landmarks"][i][1])

#df = pd.DataFrame.from_dict(data_frame)
img = io.imread('../../ozdemir/ffmpegout/6_3/frame00060.jpg')
plt.imshow(img)
plt.scatter(data_frame["pose_x"], data_frame["pose_y"])
plt.show()
plt.savefig("plot6_3_60")
#fig = px.scatter(df, x='pose_x', y='pose_y')

#fig.show()