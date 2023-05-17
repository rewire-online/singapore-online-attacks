#!/bin/bash

strings=(
    xlmr_100000-09-01-2023-16-29-14/
	xlmt_100000-14-01-2023-01-11-42/
	bert-base-multilingual-uncased_100k-18-01-2023-16-26-31/
	indobert-base-uncased_100k-18-01-2023-17-51-55/
	indobertweet-base-uncased_100k-18-01-2023-18-36-29/
)

for s in "${strings[@]}"; do
	# model_name=${s##*/}

	echo "Downloading finetuned model files"
	# python -m save_to_s3 --model_name $s --model_folder outputs/$model_name
	aws s3 sync s3://rewire-artifacts-storage/$s extended_pretraining_models/$s
done
