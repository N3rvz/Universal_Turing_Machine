#Variables par défaut
FILE ?= palindrome.txt
WORD ?= 10101

SCRIPT = MT.py

#regle par defaut
all: help

help:
		python3 $(SCRIPT) -h

#Questions
q1:
		python3 $(SCRIPT) -q 1

q2:
		python3 $(SCRIPT) -q 2 -f $(FILE) -w $(WORD)

q3:
		python3 $(SCRIPT) -q 3 -f $(FILE) -w $(WORD)

q4:
		python3 $(SCRIPT) -q 4 -f $(FILE) -w $(WORD)

q5:
		python3 $(SCRIPT) -q 5 -f $(FILE) -w $(WORD)

q7:
		python3 $(SCRIPT) -q 7 -f $(FILE)

clean:
		rm -rf __pycache__
		rm -f *.pyc
