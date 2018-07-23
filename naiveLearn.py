import numpy as np
import pickle

def main():

	#correctHur,correctStorm,wrongHur,wrongStorm
	#guessing based on min of sums: 10815 317 23034 152


	filename = './hurr-batches/64_396_center_data_batch'
	with open(filename, 'rb') as f:
		data = pickle.load(f, encoding='latin1')
	filename = './hurr-batches/64_396_center_test_batch'
	with open(filename, 'rb') as f:
		test = pickle.load(f, encoding='latin1')

	mins = [float('inf'),float('inf')]
	maxs = -float('inf')
	zeros = []
	for idx, image in enumerate(data['data']):
		print('{}/{} ({}%)'.format(idx,len( data['labels'] ),(idx/len( data['labels']))*100))
		s =  sum(image)
		if s == 0:
			if data['labels'][idx] == 1:
				zeros.append(data['filenames'][idx])
		elif s<mins[data['labels'][idx]]:
			mins[data['labels'][idx]] = s

	print(mins)
	print(zeros)
	correctHur = 0
	correctStorm = 0
	wrongHur = 0
	wrongStorm = 0
	for idx, image in enumerate(test['data']):
		print('{}/{} ({}%)'.format(idx,len( data['labels'] ),(idx/len( data['labels']))*100))
		s = sum(image)
		if s<mins[1]:
			if data['labels'][idx] == 0:
				correctStorm += 1
			else:
				wrongStorm += 1
		else:
			if data['labels'][idx] == 1:
				correctHur += 1
			else:
				wrongHur += 1
	print(correctHur,correctStorm,wrongHur,wrongStorm)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print()


