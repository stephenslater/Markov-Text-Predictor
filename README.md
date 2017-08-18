# Markov-Text-Predictor
Machine-learning text predictor using Markov chains of letter and word sequences
Coded at OpenWest Conference in Sandy, UT 7/15/17

Test using `python3 testmarkov.py`  
Example REPL usage: `python3 markov.py -f ts.txt -s 5`

This will train the model using The Adventures of Tom Sawyer (saved as a text file), and create Markov chains based on 5-letter sequences. Type anything into the REPL, and if it is a string of length <= size (in this case 5 characters), it will predict the result given the frequency of character sequences in *TS*.
