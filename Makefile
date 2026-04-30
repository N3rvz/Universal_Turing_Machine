#Variables par défaut
PYTHON ?= python3
FILE ?= palindrome.txt
WORD ?= 10101

SCRIPT = MT.py

#regle par defaut
all: help

help:
		$(PYTHON) $(SCRIPT) -h

#Questions
q1:
		$(PYTHON) $(SCRIPT) -q 1

q2:
		$(PYTHON) $(SCRIPT) -q 2 -f $(FILE) -w $(WORD)

q3:
		$(PYTHON) $(SCRIPT) -q 3 -f $(FILE) -w $(WORD)

q4:
		$(PYTHON) $(SCRIPT) -q 4 -f $(FILE) -w $(WORD)

q5:
		$(PYTHON) $(SCRIPT) -q 5 -f $(FILE) -w $(WORD)

q6:
		$(PYTHON) $(SCRIPT) -q 6 -f $(FILE) -w $(WORD)

q7:
		$(PYTHON) $(SCRIPT) -q 7 -f $(FILE)

q8:
		$(PYTHON) $(SCRIPT) -q 8 -f $(FILE)

clean:
		rm -rf __pycache__
		rm -f *.pyc
