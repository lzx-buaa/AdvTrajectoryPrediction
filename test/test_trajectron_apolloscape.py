import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from prediction.dataset.apolloscape import ApolloscapeDataset
from prediction.dataset.generate import data_offline_generator
from prediction.model.Trajectron import TrajectronInterface
from prediction.visualize.visualize import *
from test_utils import *

import numpy as np
import copy

DATADIR = "data/trajectron_apolloscape"
DATASET_DIR = "data/dataset/apolloscape"
obs_length = 6
pred_length = 6
attack_length = 6
time_step = 0.5

dataset = ApolloscapeDataset(obs_length, pred_length, time_step)
# dataset.generate_data("test")

api = TrajectronInterface(obs_length, pred_length, pre_load_model=os.path.join(DATADIR, "model"), maps=None)

def test():
    print("Doing prediction on multi-frame tasks")
    normal_multiframe_test(api, os.path.join(DATASET_DIR, "multi_frame", "raw"), os.path.join(DATADIR, "multi_frame", "normal"), attack_length, 
                            figure_dir=os.path.join(DATADIR, "multi_frame", "normal_visualize"), overwrite=True)


def attack_sample(case_id, obj_id, attack_goal):
    attacker = GradientAttacker(obs_length, pred_length, attack_length, api, seed_num=4, iter_num=50, physical_bounds=dataset.bounds)
    
    input_data = load_data(os.path.join(DATASET_DIR, "multi_frame", "raw", "{}.json".format(case_id)))
    # result_path = os.path.join(DATADIR, "multi_frame", "normal", "{}.json".format(case_id))
    # figure_path = os.path.join(DATADIR, "multi_frame", "normal_visualize", "{}.png".format(case_id))
    # test_core(api, input_data, attack_length, result_path, figure_path)

    result_path = os.path.join(DATADIR, "multi_frame", "attack", "{}-{}-{}.json".format(case_id, obj_id, attack_goal))
    figure_path = os.path.join(DATADIR, "multi_frame", "attack_visualize", "{}-{}-{}.png".format(case_id, obj_id, attack_goal))
    adv_attack_core(attacker, input_data, obj_id, attack_goal, result_path, figure_path)


def attack():
    attacker = GradientAttacker(obs_length, pred_length, attack_length, api)

    adv_attack(attacker, os.path.join(DATASET_DIR, "multi_frame", "raw"), os.path.join(DATADIR, "multi_frame", "attack"), os.path.join(DATADIR, "multi_frame", "attack_visualize"), overwrite=True)

# attack()
# test()
attack_sample(125, 1, "ade")