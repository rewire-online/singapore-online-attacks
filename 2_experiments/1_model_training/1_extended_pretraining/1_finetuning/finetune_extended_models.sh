#!/bin/bash

strings=(
	xlmr_10000-09-01-2023-13-49-33/
    xlmr_100000-09-01-2023-16-29-14/
    xlmr_1000000-10-01-2023-18-35-07/
	xlmr_50000-09-01-2023-14-44-09/
	xlmr_500000-10-01-2023-01-11-32/
	xlmt_10000-13-01-2023-22-34-19/
	xlmt_100000-14-01-2023-01-11-42/
	xlmt_50000-13-01-2023-23-27-07/
	xlmt_500000-14-01-2023-09-56-04/
	xlmt_1000000-15-01-2023-16-42-42/
	bert-base-multilingual-uncased_100k-18-01-2023-16-26-31/
	indobert-base-uncased_100k-18-01-2023-17-51-55/
	indobertweet-base-uncased_100k-18-01-2023-18-36-29/
)

for s in "${strings[@]}"; do
	model_name=(${s//-/ })
	echo ${model_name[0]}    
	echo "Downloading Pretrained Model"
	aws s3 sync s3://rewire-artifacts-storage/$s models/$model_name
	echo "Finetuning Model $model_name"
	python -m finetune_model -n /home/ubuntu/finetune_models/models/$model_name -b 16

	echo "Copying finetuned model files"
	python -m save_to_s3 --model_name $s --model_folder outputs/$model_name

	echo "Removing local model files"
	rm -rf models/$model_name
	rm -rf models/training_cache/$model_name

	echo "Removing finetuned model files"
	rm -rf outputs/$model_name
done
