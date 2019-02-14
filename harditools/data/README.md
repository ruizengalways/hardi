'bvals' and 'bvecs' are the original gradient files sent to me by Sean. They
assume that all b0s have been averaged into a single file at the beginning 
of the stack. They also assume the data has shape: (110, 150, 74, 145).

The script 'make_new_bfiles.py' generates new gradient files in the same space
but includes all 16 individual b0 volumes in the order of acquisition. I.e., 
1 b0, 9 DWI, 1 b0, 9 DWI, etc. These files assume the data has a shape
(110, 150, 74, 160)

