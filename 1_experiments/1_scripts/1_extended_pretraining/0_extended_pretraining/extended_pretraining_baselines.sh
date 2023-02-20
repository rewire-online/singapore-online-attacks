#!/bin/bash

strings=(
	# xlm-roberta-base
	indolem/indobert-base-uncased
	indolem/indobertweet-base-uncased
	# bert-base-multilingual-uncased
	# bert-base-multilingual-cased
	# cardiffnlp/twitter-xlm-roberta-base
)
for s in "${strings[@]}"; do
	model_name=${s##*/}
	echo "Running extended pretraining on $model_name"
	python -m mlm --model_name_or_path $s --use_special_tokens True --train_file data/dso_unlabelled_sample_100000.csv --max_seq_length 128 --output_dir outputs/${model_name}_100k --overwrite_output_dir True --do_train --save_total_limit 2 --gradient_accumulation_steps 1 --num_train_epochs 1 --data_seed 123 --seed 123 --line_by_line True --per_device_train_batch_size 4 --overwrite_cache True
	
	echo "Saving model to s3"
	rm -R -- outputs/${model_name}_100k/*/
	python -m save_to_s3 --model_name ${model_name}_100k --model_folder outputs/${model_name}_100k
	
	echo "Removing local model files"
	rm -rf outputs/${model_name}_100k
done
