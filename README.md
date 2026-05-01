# Turing Machine Simulator & Universal Machine



A comprehensive Python implementation of a multi-tape Turing Machine simulator. This project parses machine definitions directly from the popular [Turing Machine Simulator](https://turingmachinesimulator.com/) format, executes complex multi-tape algorithms, and simulates a Universal Turing Machine with time-bounded execution capabilities to prevent infinite loops.

## Features

* **Multi-Tape Support:** Automatically detects and handles machines with any number of tapes (1 to N) based on the transition definitions.
* **TMSimulator Compatibility:** Parses standard `.txt` files following the `turingmachinesimulator.com` syntax.
* **Universal Machine Encoding:** Translates standard Turing Machines into standard string encodings (`<M>`) and binary Gödel numbers.
* **Time-Bounded Execution:** Prevents infinite loops by simulating a Universal Turing Machine with an adjustable step counter limit.
* **Makefile Automation:** Fully automated via `make` to run tasks, test specific machines, and debug execution steps effortlessly.

## Prerequisites

* Python 3.6 or higher.
* `make` utility installed on your system.
* No external python dependencies required (uses only standard library modules).

## Usage

The project is fully automated using a `Makefile`. You can override default variables like `FILE`, `WORD`, and `STEPS` directly in the command line.

### Basic Syntax
```bash
make q<question_number> [FILE=path/to/machine.txt] [WORD=input_word] [STEPS=max_steps]
```

### Command Examples

**Run a standard simulation (e.g., Unary Multiplication on Q4):**
```bash
make q4 FILE=mult_unaire.txt WORD="11#111"
```

**Run a simulation with step-by-step configuration display (Q5):**
```bash
make q5 FILE=compare.txt WORD="101#110"
```

**Generate the `<M>` encoding and binary representation of a machine (Q8):**
```bash
make q8 FILE=recherche.txt
```

**Run a Time-Bounded Universal Machine Simulation (Q10):**
```bash
make q10 FILE=compare.txt WORD="10#10" STEPS=100
```

### Pre-configured Test Suites (Question 6)

The `Makefile` includes built-in shortcuts to test specific algorithms and edge cases (successes and infinite loops):
```bash
make q6_comp          # Test successful binary comparison
make q6_comp_faux     # Test failing binary comparison (triggers infinite loop)
make q6_search        # Test successful list search
make q6_search_faux   # Test failing list search
make q6_mult_un       # Test unary multiplication
```

## Machine Definition Format

This simulator reads `.txt` files structured as follows:
```text
name: MyMachine
init: q0
accept: qAccept

// Transition format: State, ReadTape1, ReadTape2
q0, 0, _
// NextState, WriteTape1, WriteTape2, MoveTape1, MoveTape2
q0, 0, 0, >, >
```
*Note: Ensure consistent tape counts across all transitions. Supported directions are `>`, `<`, `-`, `R`, `L`.*

## Project Structure

* `MT.py`: The core simulator, parser, and CLI entry point.
* `Makefile`: Task runner for automated testing and execution.
* `MT` class: Represents the formal definition of the Turing Machine.
* `Configuration` class: Tracks the current state, tape contents, and head positions.
