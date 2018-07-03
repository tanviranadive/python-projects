# Task 1: To clean the corpus

from CorpusCleaner import Cleaner

# directory from where the raw corpus is taken
inputrootdir = "/Users/Shraddha/Desktop/IR-Project/cacm/"

# directory where the cleaned corpus is stored
outrootdir = "/Users/Shraddha/Desktop/IR-Project/cleaned_cacm/"

clean = Cleaner()

clean.getCleanCorpus(inputrootdir, outrootdir)