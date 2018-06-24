# machine learning & QA system

## environment
* python3.6.4
* GNU Octave, version 4.4.0

## Required Package
```
pip install jieba
pip install pandas
```

## Quick Start
Execute "testml_qa.m" with Octave.

## Complete Operating
Execute "process_data.py" with Python.
We can get output layer node quantity is 318 (remember this number, we will use it later).
```
$ python process_data.py
Process Data: Q_sentences quantity is 420
Process Data: A_sentences quantity is 420
Process Data: Q_keywords quantity is 513
Process Data: A_keywords quantity is 318     <- output layer node quantity
Process Data: Feature encoding ...
Process Data: Finish.
```

Edit "testml_qa.m" two variables:
```
xt = [ ... ];  # replace with "\result\io_dataset.txt" content
k = ... ;      # replace with output layer node quantity (example: 318)
```

Save and execute "testml_qa.m" with Octave.
