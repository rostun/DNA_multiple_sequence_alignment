DNA Multiple Sequence Alignment(MSA) Challenge

1. The input is at most 50 DNA sequences (i.e, the character set is limited to T/C/G/A) whose length does not exceed 1000 characters. 
2. The sequences are given in FASTA format (https://en.wikipedia.org/wiki/FASTA_format). These sequences are all different fragments of one chromosome. 
3. The specific set of sequences you will get satisfy a very unique property:  there exists a unique way to reconstruct the entire chromosome from these reads by gluing together pairs of reads that overlap by more than half their length. An example set of input strings is attached.
4. The output of your program should be this unique sequence that contains each of the given input strings as a substring.

Compilation (made with python 3.4.0)

1. put combineSequences.py file and example.txt in same folder and open command line from there
2. python combineSequences.py
3. input filename (without extension) and hit enter
4. You will get an output.txt file with compiled DNA sequence as well as a leftover.txt file containing segments I didn't use

Basic Conclusions and Solution

The main part that will affect complexity will probably be determining if a sequence is in another sequence. Since I know that I am guaranteed that ALL unique sequences overlap into one sequence there is a 98% chance a beginning or end chunk of X of a sequence will match with the a chunk X of another sequence. It's just 50 chunks < 1000 characters so I can just check one by one, but down the line if hypothetically I were to incorporate more segments maybe I can optimize the search somehow. Knuth-Morris-Pratt (KMP) algorithm immediately comes to mind, I'm familiar with it from class and know it's a good option when needing to find multiple matches of DNA subsequences. After some googling Boyer Moore seems to stand out as a better inspiration for this situation. It's ideal when text to search is large and there are multiple strings to be searched and searching from the end fits with what we need here (http://www.ijaiem.org/volume1Issue3/IJAIEM-2012-11-02-001.pdf).

My overall approach is to start off with a random sequence A and find other sequences containing A[0-X]. 

while there's more than one sequence 
	If a sequence B contains substring A[0-X] from B[x-z]
		Check for a match starting from A[X+1] and B[z + 1]
			if A ended, delete A and keep sequence B
			if B ended, combine sequence A + B
		else check the next sequence
	made it here with no match? switch to other end of the sequence

At this point (built off of two ends as far as I can go) I know I have the entire piece, so no need to test the other segments

One unknown is how large the length X of which I should test. If the sequences X is too short, the chance of me encountering a "failed" sequence (one that can not be combined with sequence A) goes up. If the sequence X is too long, the chance of me accidentally testing a "dummy" sequence (one that dne in any sequence entirely) goes up. I need a sequence X that minimizes both of those chances, probably know after I implement my search algorithm.

Complexity (asymptotically)

Space
- As the segments increase, the space usage increases in constant time (more links to the list) so probably around O(n)

Time
- Let's say worst case scenario we need to add every single sequence to our chromosome. Let's say we have 4 sequences and the number of comparisons go down by one like below:
	x x x x
	  x x x
	    x x
	      x
- Therefore our code goes through roughly N^2/2 (or taking into account string length m then O(N^2/2*M)) so it does O(N^2) work overall 
