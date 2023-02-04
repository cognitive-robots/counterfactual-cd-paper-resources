#!/usr/bin/python3

import copy
import os
import argparse
import json
import glob
import statistics

def calculate_scene_performance(causal_links):
    tp_count = 0
    fp_count = 0
    fn_count = 0

    for cause_str in causal_links:
        cause_id = int(cause_str)
        effect_ids = causal_links[cause_str]
        if cause_id == convoy_head_id:
            if convoy_tail_id in effect_ids:
                tp_count += 1
                fp_count += len(effect_ids) - 1
            else:
                fp_count += len(effect_ids)
                fn_count += 1
        else:
            fp_count += len(effect_ids)

    if causal_links.get(str(convoy_head_id)) is None:
        fn_count += 1

    if len(causal_links) == 0:
        precision = 0
    else:
        precision = tp_count / (tp_count + fp_count)

    recall = tp_count / (tp_count + fn_count)

    f1_score = (2 * tp_count) / (2 * tp_count + fp_count + fn_count)

    return precision, recall, f1_score

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument("input_path_expr")
arg_parser.add_argument("output_file_path")
args = arg_parser.parse_args()

reward_precisions = []
agency_precisions = []
hybrid_precisions = []

reward_recalls = []
agency_recalls = []
hybrid_recalls = []

reward_f1_scores = []
agency_f1_scores = []
hybrid_f1_scores = []

execution_times = []

for input_file_path in glob.glob(args.input_path_expr):
    input_file_basename = os.path.basename(input_file_path)

    with open(input_file_path, "r") as input_file:
        causal_discovery_json = json.load(input_file)

        convoy_head_id = causal_discovery_json["convoy_head_id"]
        convoy_tail_id = causal_discovery_json["convoy_tail_id"]
        independent_id = causal_discovery_json["independent_id"]


        causal_links = causal_discovery_json["reward_causal_links"]

        precision, recall, f1_score = calculate_scene_performance(causal_links)

        reward_precisions.append(precision)
        reward_recalls.append(recall)
        reward_f1_scores.append(f1_score)


        causal_links = causal_discovery_json["agency_causal_links"]

        precision, recall, f1_score = calculate_scene_performance(causal_links)

        agency_precisions.append(precision)
        agency_recalls.append(recall)
        agency_f1_scores.append(f1_score)


        causal_links = causal_discovery_json["hybrid_causal_links"]

        precision, recall, f1_score = calculate_scene_performance(causal_links)

        hybrid_precisions.append(precision)
        hybrid_recalls.append(recall)
        hybrid_f1_scores.append(f1_score)

        execution_times.append(causal_discovery_json["time_elapsed_in_microseconds"] / 1.0e6)


reward_precision_mean = statistics.mean(reward_precisions)
reward_precision_stdev = statistics.stdev(reward_precisions)

agency_precision_mean = statistics.mean(agency_precisions)
agency_precision_stdev = statistics.stdev(agency_precisions)

hybrid_precision_mean = statistics.mean(hybrid_precisions)
hybrid_precision_stdev = statistics.stdev(hybrid_precisions)


reward_recall_mean = statistics.mean(reward_recalls)
reward_recall_stdev = statistics.stdev(reward_recalls)

agency_recall_mean = statistics.mean(agency_recalls)
agency_recall_stdev = statistics.stdev(agency_recalls)

hybrid_recall_mean = statistics.mean(hybrid_recalls)
hybrid_recall_stdev = statistics.stdev(hybrid_recalls)


reward_f1_score_mean = statistics.mean(reward_f1_scores)
reward_f1_score_stdev = statistics.stdev(reward_f1_scores)

agency_f1_score_mean = statistics.mean(agency_f1_scores)
agency_f1_score_stdev = statistics.stdev(agency_f1_scores)

hybrid_f1_score_mean = statistics.mean(hybrid_f1_scores)
hybrid_f1_score_stdev = statistics.stdev(hybrid_f1_scores)


execution_times_mean = statistics.mean(execution_times)
execution_times_stdev = statistics.stdev(execution_times)


with open(args.output_file_path, "w") as output_file:
    performance_evaluation_json = {
        "reward_based": {
            "precision": {
                "mean": reward_precision_mean,
                "stdev": reward_precision_stdev
            },
            "recall": {
                "mean": reward_recall_mean,
                "stdev": reward_recall_stdev
            },
            "f1_score": {
                "mean": reward_f1_score_mean,
                "stdev": reward_f1_score_stdev
            }
        },
        "agency_based": {
            "precision": {
                "mean": agency_precision_mean,
                "stdev": agency_precision_stdev
            },
            "recall": {
                "mean": agency_recall_mean,
                "stdev": agency_recall_stdev
            },
            "f1_score": {
                "mean": agency_f1_score_mean,
                "stdev": agency_f1_score_stdev
            }
        },
        "hybrid_based": {
            "precision": {
                "mean": hybrid_precision_mean,
                "stdev": hybrid_precision_stdev
            },
            "recall": {
                "mean": hybrid_recall_mean,
                "stdev": hybrid_recall_stdev
            },
            "f1_score": {
                "mean": hybrid_f1_score_mean,
                "stdev": hybrid_f1_score_stdev
            }
        },
        "execution_time": {
            "mean": execution_times_mean,
            "stdev": execution_times_stdev
        }
    }
    json.dump(performance_evaluation_json, output_file)
