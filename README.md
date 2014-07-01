Spelling Corrector
==================

A spelling corrector based on the noisy channel model.  This program will be able to correct spelling mistakes even if the word is a real dictionary word, but is used in an incorrect context.

## Description ##

The goal of this project was to be able to find and correct words that were mistyped, even if the typed word is a word in the dictionary.  For example, "fifteen minutes" might be mistyped as "fifteen minuets" - Depending on context, "fifteen minutes" is probably the desired phrase.

In order to predict what the intended word is, we want to maximize the probability P (w|x), where w is the actual word and x is the noisy word that the algorithm receives. Using Baye’s Rule we can equivalently maximize the product P (x|w)P (w).  This can be described as a product between the channel model and the dictionary model.  The channel model tells us the probability that a specific word could have turned into the received word, x. The dictionary model tells us the probability of a specific word (or N-gram) w showing up.

In its simplest form, the channel model will give a higher probability for the lowest number of edits (where an edit is an insertion, deletion, substitution, or transposition). However, we can also approach the probability more specifically. One option is to use some training set of labeled mistakes in order to determine which mistakes are more likely. Another option is to develop some heuristic to explain which mistakes are more likely. For example, we would say that a substitution of keys that neighbor each other is more likely than other substitutions.

The dictionary model can also take a simpler or more complicated form. We can look at the probability of a single word showing up, or we can look at the probability of some N-gram showing up. Using a bigram or trigram will give us context and allow us to more intelligently determine the actual word.

## Implementation ##

The first step in the spelling correction process was to produce all words within one edit-distance of each of the words from the input sentence.  This project used one edit-distance as the maximum because in general, about 80\% of all spelling mistakes could be found in that one edit-distance.  If there were reason to assume that the channel was particularly ``noisy,'' the same algorithm could be used to add all words an additional edit-distance away to the candidate list.

After a list of candidate words is generated, each of these words is plugged into the model discussed above.  For each specific edit, the probability of each edit is calculated.  This is done using data from http://norvig.com/ngrams/ which provides the number of each specific edit (for example the number of times ie is typed as ei: ei|ie).  http://norvig.com/ngrams/ also provides a count of all two-letter-grams allowing us to calculate a P(x|w) where $w$ is the actual word and x is the word with noise.

Next we must take the dictionary model into account.  In order to do this we want to look at the 2 bigrams from either side of the candidate word - P(word | prevWord) and P(nextWord | word).  Originally, I was planning on using requests to Google's N-gram database; however, this failed because Google cut me off (Error 429) from performing too many requests.  I found several other large pieces of text and combined them all to create my own bigram probabilities with the help of the NLTK toolbox.  Unfortunately, this results in a significantly smaller corpus than the giant Google database, but still proved to work for the most part.  Additionally, due to the smaller size of the available text, smoothing proved to be more important.

The probabilities of each candidate word and the original word are all computed, and at first the word with the maximum probability is chosen to be the intended word.  In order to properly analyze the results, and edit probability (the channel model) must be assigned to the actual word typed.  I tested several different options of this probability before settling on assigning the typed word with a probability of 1e-7 while other edit probabilities were in the range of 1e-8 to 1e-9.  After correcting some of the words from the first run, the same method is repeated until no more changes are made.  This is performed so that noisy words that are surrounded by other noisy words are also corrected.

The final program outputs the top three possibilities for each word in the sentence, in increasing order of probability.  These are printed for each successive try to edit the sentence. 

## Dependencies ##

* Python 2.7
* NLTK
* http://norvig.com/ngrams/count_2l.txt
* http://norvig.com/ngrams/count_1edit.txt

## How To Run ##

The user inputs to the program a text file with the lines that need correction and an output file.  The user may optionally use an additional argument specifying a directory that contains additional text files for the corpus. Adding more text files may help the program's performance.  For most of my tests I used all the data found at http://corpus.byu.edu/full-text/formats.asp.

python SpellingCorrector.py <Input> <Output> [More Training]

## Sample Results ##

The following is a list of example inputs that were properly corrected by this program with the training files used (the typos are bolded):

I will go to bed in FITEEN minutes
I will go to bed in FFITEEN minutes
I will go to bed in FIFTAEEN minutes
I will go to bed in FIFTAEN minutes
I will go to bed in fifteen MINUETS

Do you NED ANYTING ALSE FRM ME

My house is the one with the porch up FROUNT
Sometimes in the middle of the night I go to WACH tv
If you can read this you must be RAELLY smart
If you can read this you must be really SMRAT
I THING that this is important
he lived on the DESSERT island

