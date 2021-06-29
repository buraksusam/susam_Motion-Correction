from dataset import HV3D
import numpy as np
from opt import Options

def main(opt):
    #print(opt.gt_dir)
    dim_targets = HV3D(opt.gt_dir).targets
    
option = Options().parse()
main(option)