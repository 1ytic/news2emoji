include .env
export

.PHONY: prepare-cls prepare-gen upload train-cls train-gen jobs cancel follow events results files clean spacy

prepare-cls:
	openai tools fine_tunes.prepare_data -f data/${CHANNEL}/dataset.jsonl -q
	mkdir -p data/${CHANNEL}/${TASK}/
	mv data/${CHANNEL}/dataset_prepared_*.jsonl data/${CHANNEL}/${TASK}/
	python 3_check.py "data/${CHANNEL}/${TASK}/dataset_prepared_train.jsonl"
	python 3_check.py "data/${CHANNEL}/${TASK}/dataset_prepared_valid.jsonl"

prepare-gen:
	openai tools fine_tunes.prepare_data -f data/${CHANNEL}/dataset.jsonl -q
	python 3_split.py "data/${CHANNEL}/${TASK}/dataset.jsonl"

upload:
	openai api files.create -f data/${CHANNEL}/${TASK}/dataset_prepared_train.jsonl -p fine-tune
	openai api files.create -f data/${CHANNEL}/${TASK}/dataset_prepared_valid.jsonl -p fine-tune

train-cls:
	openai api fine_tunes.create \
	-t ${TRAIN_FILE_ID} \
	-v ${VALID_FILE_ID} \
	--compute_classification_metrics \
	--classification_n_classes 10 \
	--model ${MODEL} \
	--n_epochs 4

train-gen:
	openai api fine_tunes.create \
	-t ${TRAIN_FILE_ID} \
	-v ${VALID_FILE_ID} \
	--model ${MODEL} \
	--n_epochs 1

cancel:
	openai api fine_tunes.cancel -i ${FINE_TUNE_JOB_ID}

follow:
	openai api fine_tunes.follow -i ${FINE_TUNE_JOB_ID}

events:
	openai api fine_tunes.events -i ${FINE_TUNE_JOB_ID}

results:
	openai api fine_tunes.results -i ${FINE_TUNE_JOB_ID} > data/${CHANNEL}/${TASK}/result_${MODEL}.csv

clean:
	openai api files.delete -i ${TRAIN_FILE_ID}
	openai api files.delete -i ${VALID_FILE_ID}

jobs:
	openai api fine_tunes.list

files:
	openai api files.list

spacy:
# preprocess
	python 4_preprocess.py \
		"data/${CHANNEL}/${TASK}/dataset_prepared_train.jsonl" \
		"data/${CHANNEL}/${TASK}/dataset_prepared_train.spacy"
	python 4_preprocess.py \
		"data/${CHANNEL}/${TASK}/dataset_prepared_valid.jsonl" \
		"data/${CHANNEL}/${TASK}/dataset_prepared_valid.spacy"
# configure
	python -m spacy init fill-config ./spacy.cfg data/${CHANNEL}/${TASK}/config.cfg
# train
	python -m spacy train data/${CHANNEL}/${TASK}/config.cfg \
	--output "data/${CHANNEL}/${TASK}/" \
	--paths.train "data/${CHANNEL}/${TASK}/dataset_prepared_train.spacy" \
	--paths.dev "data/${CHANNEL}/${TASK}/dataset_prepared_valid.spacy"
# eval
	python -m spacy evaluate "data/${CHANNEL}/${TASK}/model-best" \
	"data/${CHANNEL}/${TASK}/dataset_prepared_valid.spacy" \
	--output "data/${CHANNEL}/${TASK}/metrics.json"
# accuracy
	python 5_predict.py \
		"data/varlamov_news/classification/model-best" \
		"data/${CHANNEL}/${TASK}/dataset_prepared_valid.jsonl"
