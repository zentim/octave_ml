#encoding=utf-8

#
# Create output directory if it not existed.
#

import pathlib
output_dir = 'result'
pathlib.Path(output_dir).mkdir(parents=True, exist_ok=True)

print('Process Data: Output directory is ready ...')



#
# Prepare QA dataset
#

# read raw data
import pandas as pd
input_filename = 'raw_data/QA.xlsx'
sheet = "QA"
df = pd.read_excel(io=input_filename, sheet_name=sheet)

# output QA dataset
output_filename = output_dir + '/qa.txt'
fo = open(output_filename, "w", encoding='utf-8')
for i in range(0, len(df['Q'])):
  fo.writelines(str(df['Q'][i]) + '\n')
  fo.writelines(str(df['A'][i]) + '\n')
fo.close()

print('Process Data: QA dataset is ready ...')



#
# Separate QA dataset
#

import jieba
import jieba.analyse

Q_sentences = []
A_sentences = []

Q_keywords = set()
A_keywords = set()

# read QA dataset
filename = output_dir + '/qa.txt'
with open(filename, encoding='utf-8') as f:
    lines = f.read().split('\n')

for i in range(0, len(lines) - 1):
    if (i % 2 == 0):
        # collect question sentence
        Q_sentences.append(lines[i])
        for x, w in jieba.analyse.textrank(lines[i], withWeight=True):
            # collect question keyword
            if w > 0.6:
              Q_keywords.add(x)
    else:
        # collect answer sentence
        A_sentences.append(lines[i])
        for x, w in jieba.analyse.textrank(lines[i], withWeight=True):
            # collect answer keyword
            if w > 0.6:
              A_keywords.add(x)



#
# Output sentences and keywords
#
def output_file(filename, dataset):
    fo = open(filename, "w", encoding='utf-8')
    for row in dataset:
        fo.writelines(row + '\n')
    fo.close()

output_file(output_dir + '/Q_sentences.txt', Q_sentences)
output_file(output_dir + '/A_sentences.txt', A_sentences)
output_file(output_dir + '/Q_keywords.txt', Q_keywords)
output_file(output_dir + '/A_keywords.txt', A_keywords)

print('Process Data: Q_sentences quantity is', len(Q_sentences))
print('Process Data: A_sentences quantity is', len(A_sentences))
print('Process Data: Q_keywords quantity is', len(Q_keywords))
print('Process Data: A_keywords quantity is', len(A_keywords))



#
# Load keywords
#

result_dir = 'result'

Q_keywords = {}
A_keywords = {}

with open(result_dir + '/Q_keywords.txt', encoding = 'utf-8') as f:
  lines = f.read().split('\n')
for i in range(0, len(lines) - 1):
  Q_keywords[lines[i]] = i

with open(result_dir + '/A_keywords.txt', encoding = 'utf-8') as f:
  lines = f.read().split('\n')
for i in range(0, len(lines) - 1):
  A_keywords[lines[i]] = i



#
# Load sentences
#

Q_sentences = []
A_sentences = []

with open(result_dir + '/Q_sentences.txt', encoding = 'utf-8') as f:
  lines = f.read().split('\n')
for i in range(0, len(lines) - 1):
  Q_sentences.append(lines[i])

with open(result_dir + '/A_sentences.txt', encoding = 'utf-8') as f:
  lines = f.read().split('\n')
for i in range(0, len(lines) - 1):
  A_sentences.append(lines[i])



#
# Feature encoding
#

print('Process Data: Feature encoding ...')

import jieba
import jieba.analyse

# example: [(inputs, outputs)]
dataset = []

inputs = []
outputs = []

for index in range(0, len(Q_sentences) - 1):
  # prepare one row intput
  oneRowInput = []
  for i in range(0, len(Q_keywords)):
    oneRowInput.append(0)

  for x, w in jieba.analyse.textrank(Q_sentences[index], withWeight=True):
    if x in Q_keywords.keys():
      oneRowInput[Q_keywords.get(x)] = 1

  # prepare one row output
  oneRowOutput = []
  for i in range(0, len(A_keywords)):
    oneRowOutput.append(0)

  for x, w in jieba.analyse.textrank(A_sentences[index], withWeight=True):
    if x in A_keywords.keys():
      oneRowOutput[A_keywords.get(x)] = 1

  inputs.append(oneRowInput)
  outputs.append(oneRowOutput)

  dataset.append((tuple(oneRowInput), tuple(oneRowOutput)))
  # example: dataset.append(((0.3, 0.5), (0, 1)))



filename = 'result/io_dataset.txt'
fo = open(filename, "w", encoding='utf-8')
for row in dataset:
    for x in row[0]:
        fo.writelines(str(x) + ' ')
    for y in row[1]:
        fo.writelines(str(y) + ' ')
    fo.writelines('; ')
fo.close()

print('Process Data: Finish.')
