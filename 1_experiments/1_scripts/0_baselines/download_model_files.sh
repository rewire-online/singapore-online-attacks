#!/bin/bash

strings=(
	indolem/indobert-base-uncased
	indolem/indobertweet-base-uncased
	bert-base-multilingual-uncased
	bert-base-multilingual-cased
	xlm-roberta-base
	cardiffnlp/twitter-xlm-roberta-base
)

for s in "${strings[@]}"; do
	model_name=${s##*/}

	echo "Downloading finetuned model files"
	# python -m save_to_s3 --model_name $s --model_folder outputs/$model_name
	aws s3 sync s3://rewire-artifacts-storage/$s baseline_models/$model_name
done
