import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from prediction.dataset import ApolloscapeDataset
from prediction.dataset.generate import data_offline_generator
from prediction.model.GRIP import GRIPInterface
from prediction.visualize.visualize import *
from prediction.attack.smooth import *
from test_utils import *

import numpy as np
import copy

DATADIR = "data/grip_apolloscape"
obs_length = 6
pred_length = 6
attack_length = 6
time_step = 0.5


def test():
    api = GRIPInterface(obs_length, pred_length, pre_load_model=os.path.join(DATADIR, "model", "model_epoch_0049.pt"))

    print("Generating single frame test data")
    singleframe_data(os.path.join(DATADIR, "single_frame", "raw"), ApolloscapeDataset, obs_length, pred_length, time_step)
    print("Doing prediction on single-frame tasks")
    normal_singleframe_test(api, os.path.join(DATADIR, "single_frame", "raw"), os.path.join(DATADIR, "single_frame", "normal"))
    print("Evaluating single-frame prediction results")
    singleframe_evaluate(os.path.join(DATADIR, "single_frame", "normal"), os.path.join(DATADIR, "single_frame", "normal_report.json"))

    print("Generating multi frame test data")
    multiframe_data(os.path.join(DATADIR, "multi_frame", "raw"), ApolloscapeDataset, obs_length, pred_length, attack_length, time_step)
    print("Doing prediction on multi-frame tasks")
    normal_multiframe_test(api, os.path.join(DATADIR, "multi_frame", "raw"), os.path.join(DATADIR, "multi_frame", "normal"), attack_length)


def visualize():
    # print("Visualizing multi frame test data")
    # raw_multiframe_visualize(os.path.join(DATADIR, "multi_frame", "raw"), os.path.join(DATADIR, "multi_frame", "raw_visualize"))
    print("Visualizing multi frame prediction")
    normal_multiframe_visualize(os.path.join(DATADIR, "multi_frame", "normal"), os.path.join(DATADIR, "multi_frame", "normal_visualize"))


def attack():
    api = GRIPInterface(obs_length, pred_length, pre_load_model=os.path.join(DATADIR, "model", "model_epoch_0049.pt"))
    attacker = GradientAttacker(obs_length, pred_length, attack_length, api)

    adv_attack(attacker, os.path.join(DATADIR, "multi_frame", "raw"), os.path.join(DATADIR, "multi_frame", "attack"), os.path.join(DATADIR, "multi_frame", "attack_visualize"), overwrite=True)


def attack_sample(case_id, obj_id):
    api = GRIPInterface(obs_length, pred_length, pre_load_model=os.path.join(DATADIR, "model", "model_epoch_0049.pt"))
    attacker = GradientAttacker(obs_length, pred_length, attack_length, api)
    result_dir = os.path.join(DATADIR, "multi_frame", "attack")
    figure_dir = os.path.join(DATADIR, "multi_frame", "attack_visualize")
    
    input_data = load_data(os.path.join(DATADIR, "multi_frame", "raw", "{}.json".format(case_id)))

    for attack_goal in ["ade", "fde", "left", "right", "front", "rear"]:
        result_path = os.path.join(result_dir, "{}-{}-{}.json".format(case_id, obj_id, attack_goal))
        figure_path = os.path.join(figure_dir, "{}-{}-{}.png".format(case_id, obj_id, attack_goal))
        adv_attack_core(attacker, input_data, obj_id, attack_goal, result_path, figure_path)


if __name__ == "__main__":
    # test()
    # attack()
    # visualize()
    attack_sample(133, 1)
    # attack()