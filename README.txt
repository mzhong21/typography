To run the code, Python OpenCV is required (I couldn't figure out a way to include it into the code). Then, to run, simply run "python classifyType.py"

classifyType is the classifier, LoadTrainingData loads the different typography training data into the file training.txt for the classifyType.py module to use.

Input: "python classifyType.py" (the test data files are already included in the code)
Output:
arial
baskerville
georgia
verdana (should be idealsans)
minionpro
timesnewroman
verdana
timesnewroman
verdana
arial
arial (should be idealsans)
timesnewroman (should be baskerville)
verdana
georgia
timesnewroman