import pickle
import numpy as np
import pandas as pd
import torch
import torch_dct as dct
from torch.utils.data import DataLoader

from dataset import HV3D
from model import GCN_corr, GCN_class
from opt import Options
from utils import get_labels


def get_full_label(raw_labels):
    map_label = {1: 'Correct', 2: 'Feets too wide', 3: 'Knees inward', 4: 'Not low enough', 5: 'Front bended',
                 6: 'Knees pass toes', 7: 'Banana back', 8: 'Rolled back', 9: 'Asymmetric', 10: 'Unknown'}
    acts = [tup[0] for tup in raw_labels]
    full_labels = [map_label[tup[2]] for tup in raw_labels]
    return acts, full_labels


def main_eval(opt):

    is_cuda = torch.cuda.is_available()

    # Create models
    model_corr = GCN_corr(input_feature=opt.dct_n)
    model_class = GCN_class(input_feature=opt.dct_n, hidden_feature=opt.hidden)

    # Load parameters
    model_corr.load_state_dict(torch.load('Results/model_corr.pt'))
    model_class.load_state_dict(torch.load('Results/model_class.pt'))

    if is_cuda:
        model_corr.cuda()
        model_class.cuda()

    model_corr.eval()
    model_class.eval()

    # Load data
    try:
        with open('tmp.pickle', "rb") as f:
            data = pickle.load(f)
        data_test = data['test']
    except FileNotFoundError:
        sets = [[0, 1, 2], [], [3]]
        data_train = HV3D(opt.gt_dir, sets=sets, split=0, is_cuda=is_cuda)
        data_test = HV3D(opt.gt_dir, sets=sets, split=2, is_cuda=is_cuda)
        with open('Data/tmp.pickle', 'wb') as f:
            pickle.dump({'train': data_train, 'test': data_test}, f)

    test_loader = DataLoader(dataset=data_test, batch_size=len(data_test))

    with torch.no_grad():
        for i, (batch_id, inputs, targetsdct) in enumerate(test_loader):

            if is_cuda:
                inputs = inputs.cuda().float()
                targetsdct = targetsdct.cuda().float()
            else:
                inputs = inputs.float()
                targetsdct = targetsdct.float()

            labels = get_labels([test_loader.dataset.inputs_label[int(i)] for i in batch_id], level=1)
            # acts, full_labels = get_full_label([test_loader.dataset.inputs_label[int(i)] for i in batch_id])
            _, pred_in = torch.max(model_class(inputs).data, 1)
            deltas, att = model_corr(inputs)
            _, pred_out = torch.max(model_class(inputs+deltas).data, 1)

    deltas_3d = dct.idct_2d(deltas.cpu())
    inputs_3d = dct.idct_2d(inputs.cpu())
    targets_3d = dct.idct_2d(targetsdct.cpu())
    pose_corr_3d_dict = {}
    pose_corr_3d_dict["inputs_3d"] = inputs_3d
    pose_corr_3d_dict["targets_3d"] = targets_3d
    pose_corr_3d_dict["pose_corr_3d"] = inputs_3d + deltas_3d

    with open("Results/pose_3d_dct15.pickle", "wb") as f:
        pickle.dump(pose_corr_3d_dict, f)
    
    # summary = np.vstack((acts, full_labels, labels.numpy(), pred_in.numpy(), pred_out.numpy())).T
    # summary = pd.DataFrame(summary, columns=['act', 'full label', 'label', 'original', 'corrected'])
    summary = np.vstack((labels.cpu().numpy(), pred_in.cpu().numpy(), pred_out.cpu().numpy())).T
    summary = pd.DataFrame(summary, columns=['label', 'original', 'corrected'])
    summary.to_csv("Results/summary_dct15.csv", compression=None)
    
    count = 0
    total = 0
    map_label = {0: ('SQUAT', 'Correct'), 1: ('SQUAT', 'Feets too wide'), 2: ('SQUAT', 'Knees inward'),
                 3: ('SQUAT', 'Not low enough'), 4: ('SQUAT', 'Front bended'), 5: ('SQUAT', 'Unknown'),
                 6: ('Lunges', 'Correct'), 7: ('Lunges', 'Not low enough'), 8: ('Lunges', 'Knees pass toes'),
                 9: ('Plank', 'Correct'), 10: ('Plank', 'Banana back'), 11: ('Plank', 'Rolled back')}
    corrects = {'SQUAT': 0, 'Lunges': 6, 'Plank': 9}
    results = {'SQUAT': {}, 'Lunges': {}, 'Plank': {}}
    for k, v in map_label.items():
        results[v[0]][v[1]] = {}
        tmp = summary[summary['label'] == k]
        if len(tmp) > 0:
            results[v[0]][v[1]]['original'] = np.sum(tmp['label'] == tmp['original']) / len(tmp) * 100
            results[v[0]][v[1]]['corrected'] = np.sum(tmp['corrected'] == corrects[v[0]]) / len(tmp) * 100
            count = count + np.sum(tmp['corrected'] == corrects[v[0]])
            total = total + len(tmp)

    res = count / total * 100

    return results

if __name__ == "__main__":
    option = Options().parse()
    results = main_eval(option)

print(results)
results_df = pd.DataFrame(results)
results_df.to_csv("Results/results_dct15.csv", compression=None)    
