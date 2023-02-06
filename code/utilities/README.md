# High-D Dataset Tools
Repository containing tools for working with the High-D dataset.

# Batch Causal Discovery
Runs causal discovery on a folder of causal scenes.

```
usage: batch_causal_discovery.sh exe_dir reward_metric_threshold input_json_meta_dir input_scene_dir output_json_meta_dir
```
Parameters:
* exe_dir: Directory containing a compiled "highd_json_meta_causal_discovery" exectuable.
* reward_metric_threshold: Minimum reward metric value required for a causal link to be accepted under the reward-based causal discovery variant.
* input_json_meta_dir: Input directory containing JSON files describing causal scene meta information.
* input_scene_dir: Input directory containing scenes in base High-D format. However, it is recommended to use the trimmed scenes that can be output from the extraction script, as the raw files sometimes capture over 10 minutes of footage and the extra unnecessary data slows down the loading speed of scenes.
* output_json_meta_dir: Output directory containing JSON files describing causal scene meta information as well as new information regarding the discovered causal links and the time the causal discovery took to execute.

# Evaluate Performance
Calculates performance metrics for each causal scene based upon the links discovered for it before calculating statistics for these metrics.

```
usage: evaluate_performance.py [-h] input_path_expr output_file_path
```
Parameters:
* input_path_expr: Path expression that describes the selection of JSON output files to take as input. Can contain wildcards.
* output_file_path: File path to output performance statistics JSON file to.
* -h: Displays the help message for the script.
