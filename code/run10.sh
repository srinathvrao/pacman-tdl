#!/bin/bash
for i in {1..2}
do
	echo "running train"
	python pacman.py -p TrueOnlineSarsaLambdaAgent -a extractor=SimpleExtractor -q -k 6 -x 50 -n 60 -l custom_10_10_3
done
