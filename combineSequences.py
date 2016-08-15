# Rosa Tung
# combineSequences.py
# last modified: 8.3.16

import sys

X = 10 # the length we're testing

def main():	
	# prompt user to open file 
	filename = input("Enter filename with same format as example.txt\n")
	
	# try to open file and read it's contents
	sequences = readFile(filename)

	# if we succeeded
	if sequences != None:

		# build off of one sequence
		checkSequence = sequences[0]
		del sequences[0] # delete it from list 

		# build off of left end of checkSequence
		checkSequence, sequences = buildAlgorithm(checkSequence, sequences, 0) # print(len(sequences))
		# build off of right end of checkSequence
		checkSequence, sequences = buildAlgorithm(checkSequence, sequences, 1) # print(len(sequences))
		
		# write final sequence to file		
		fileCheckSequence = open('output.txt', 'w')
		fileCheckSequence.write(checkSequence)
		fileCheckSequence.close()

		# write leftovers to file as well
		fileCheckList = open('leftovers.txt', 'w')
		for val in sequences:
			fileCheckList.write(val)
			fileCheckList.write("\n")
		fileCheckSequence.close()
	sys.exit(0)

"""
Facilitates the search and adding on of sequences
Input:
	checkSequence: Total sequence so far
	sequences: list of sequences not used yet
	flag: 0-> build off right end 1->build off left end
Output: 
	checkSequence, sequences 
"""
def buildAlgorithm(checkSequence, sequences, flag):
	if flag == 0:
		keySequence = checkSequence[:X] # grab first 10 characters
	else:
		keySequence = checkSequence[-X:] # grab last 10 characters
	# reverse for convenience, puts search value at 0 
	reverseKey = keySequence[::-1] # extended slice O(len(slice))

	idx = 0 # counter for list of sequences
	i = X-1 # counter for each individual sequence

	# Go through and check for a matching sequence
	while idx < len(sequences):
		val = sequences[idx]
		while i < len(val): # Not Boyer Moore, but has the whole word shift , grows O(n)
			# start comparing at the Xth letter of sequence
			cs = val[i] 
			ks = reverseKey[0] # end value of keySequence
			# compare two letters
			if cs == ks: 
				# if they match, compare entire chunks
				if compareTwoSequences(val, reverseKey, i): # grows O(n)
					beforeSequence = keySequence
					"""
					double check they can fit together, then compare
					right or left chunk depending on if we're building 
					off right or left ends
					"""
					if flag == 0: # compare right part of sequence
						if compareOverlap(checkSequence, val, i, 0): # grows O(n)
							checkSequence = overlapSequences(checkSequence, val, i, 0)
							keySequence = checkSequence[:X] # new keySequence
							del sequences[idx] # delete that sequence
							idx = 0 
							# it means we didn't accomplish anything, we're done
							if beforeSequence == keySequence:
								return checkSequence, sequences
							else:
								reverseKey = keySequence[::-1]
					else: # compare left part of sequence
						if compareOverlap(checkSequence, val, i, 1): # grows O(n)
							checkSequence = overlapSequences(checkSequence, val, i, 1)
							keySequence = checkSequence[-X:] # new keySequence
							del sequences[idx] # delete that sequence
							idx = 0 # start idx back to 0
							# don't need to do it this time around
							reverseKey = keySequence[::-1]					
			else:
				# if not, check if cs is in subsequence at all 
				if cs not in reverseKey:
					i+=10 # skip over 10 spaces
			i+=1
		i = X-1 # reset position of i
		idx+=1 # evaluate next sequence 
	return checkSequence, sequences

"""
Checks whether a given sequence exists in a longer sequence 
Input: 
	checkSequence: longer sequence
	reverseKey: short sequence who's length dictates X
	i: index from where to start on longer sequence
Output: 
	True (they match), False (they do not match)
"""
def compareTwoSequences(checkSequence, reverseKey, i):
	cs = checkSequence[i]
	ks = reverseKey[0]

	idx = 0

	# compare starting from i and 0
	while idx < len(reverseKey):
		cs = checkSequence[i]
		ks = reverseKey[idx]
		if cs != ks:
			return False
		else:
			idx+=1
			i-=1
	return True

"""
Checks if a beginning or end chunk of a shorter sequence exists in a longer sequence
Input: 
	checkSequence: longer sequence
	valSequence: shorter sequence
	i: index of starting position for shorter sequence
	flag: 0 (check beginning), 1 (check end)

Output:
	True (they math), False (they do not match)
"""
def compareOverlap(checkSequence, valSequence, i, flag):
	idx = i
	# compare forward
	if flag == 0:
		idx1 = X-1
		while idx < len(valSequence):
			if valSequence[idx] != checkSequence[idx1]:
				return False
			idx+=1
			idx1+=1		
	# compare backward
	else:
		idx1 = len(checkSequence) - 1
		while idx > 0:
			if valSequence[idx] != checkSequence[idx1]:
				return False
			idx-=1
			idx1-=1
	return True

"""
Combined two sequences where they overlap
Input: 
	checkSequence: original sequence 
	val: smaller sequence that will be added to checkSequence
	i: index of val, where overlap starts
	flag: 0 (overlap forwards), 1 (overlap backwards)
Output: 
	new compiled sequence
"""
def overlapSequences(checkSequence, val, i, flag):
	sequenceChunk = ""
	# overlap forward
	if flag == 0:
		idx = 0
		while idx < i-9:
			sequenceChunk = sequenceChunk + val[idx]
			idx+=1
		checkSequence = sequenceChunk + checkSequence
	# overlap backwards
	else:
		idx = i+1
		while idx < len(val):
			sequenceChunk = sequenceChunk + val[idx]
			idx+=1
		checkSequence = checkSequence + sequenceChunk
	return checkSequence

"""
Reads in file to extract sequences and input them into a list
Input: filename
Output: list of sequences or error
"""
def readFile(filename):
	try:
		in_file = open(filename + ".txt", "r")
		print ("File opened successfully\n")
		
		line = in_file.readline() 
		sequenceBlock = "" 
		sequences = [] 

		while line:
			if line[0] == ">":
				if sequenceBlock:
					sequences.append(sequenceBlock) 
					sequenceBlock = "" k
			else:
				sequenceBlock = sequenceBlock + line
			line = in_file.readline().rstrip() # get rid of any trailing whitespaces
		
		sequences.append(sequenceBlock)

		return sequences
		in_file.close()
	except IOError:
		print("Cannot open file! See example.txt\n")
		return None

# run main
if __name__ == "__main__": 
	main()