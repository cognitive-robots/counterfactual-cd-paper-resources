#!/bin/bash

EXE_DIR=$1
REWARD_DIFF_THRESHOLD=$2
INPUT_JSON_META_DIR=$3
INPUT_TRIMMED_SCENE_DIR=$4
OUTPUT_JSON_META_DIR=$5

if [[ ! -f "${EXE_DIR}/highd_json_meta_causal_discovery" ]]
then
	echo "Invalid Executable Directory: '${EXE_DIR}'"
	exit 1
fi

if ! [[ "${REWARD_DIFF_THRESHOLD}" =~ ^[+-]?[0-9]+\.?[0-9]*$ ]]
then
  echo "Invalid Reward Diff. Threshold: '${REWARD_DIFF_THRESHOLD}'"
  exit 1
fi

if [[ ! -d "${INPUT_JSON_META_DIR}" ]]
then
	echo "Invalid Input JSON Meta Directory: '${INPUT_JSON_META_DIR}'"
	exit 1
fi

if [[ ! -d "${INPUT_TRIMMED_SCENE_DIR}" ]]
then
	echo "Invalid Input Trimmed Scene Directory: '${INPUT_TRIMMED_SCENE_DIR}'"
	exit 1
fi

if [[ ! -d "${OUTPUT_JSON_META_DIR}" ]]
then
	echo "Invalid Output JSON Meta Directory: '${OUTPUT_JSON_META_DIR}'"
	exit 1
fi

echo "Reward Diff. Threshold: ${REWARD_DIFF_THRESHOLD}"
echo "Input JSON Meta Directory: ${INPUT_JSON_META_DIR}"
echo "Input Trimmed Scene Directory: ${INPUT_TRIMMED_SCENE_DIR}"
echo "Output JSON Meta Directory: ${OUTPUT_JSON_META_DIR}"

i=1
count=$(ls ${INPUT_JSON_META_DIR} | wc -l)
for input_json_meta_file_path in ${INPUT_JSON_META_DIR}/*.json
do
  echo "Processing $input_json_meta_file_path ($i of $count)"
  output_json_meta_file_path="${OUTPUT_JSON_META_DIR}/$(basename $input_json_meta_file_path)"
  if [[ -f $output_json_meta_file_path ]]
  then
	  echo "$output_json_meta_file_path already exists, skipping"
  else
	  ${EXE_DIR}/highd_json_meta_causal_discovery ${REWARD_DIFF_THRESHOLD} $input_json_meta_file_path ${INPUT_TRIMMED_SCENE_DIR} $output_json_meta_file_path
  fi
  i=$((i+1))
done
