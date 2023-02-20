#!/bin/bash

strings=(
	microsoft/deberta-v3-base
)

for s in "${strings[@]}"; do
	model_name=${s##*/}
	echo "Finetuning Model $model_name"
	python -m finetune_deberta -n $s -b 16

	echo "Copying finetuned model files"
	python -m baseline_save_to_s3 --model_name $s --model_folder outputs/$model_name

	echo "Removing local model files"
	rm -rf models/training_cache/$model_name

	echo "Removing finetuned model files"
	rm -rf outputs/$model_name
done
