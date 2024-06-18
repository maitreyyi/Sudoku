# Sudoku Solver Project

## Overview

This project was done in-class (CS-171) and it involves a sophisticated Sudoku solver designed to handle boards of varying sizes with high efficiency and accuracy. The solver can process:
- 9x9 boards with at least 7 given values,
- 16x16 boards with at least 20 given values, and
- 25x25 boards with at least 30 given values,
  all within a 3-minute time frame, achieving 100% accuracy.

Boards difficulty is classified by the size of board and given values:
- Easy: P = Q = 3, N = 9  with 7 given values
- Intermediate: P = 3, Q = 4, N = 12 with 11 given values
- Hard: P = Q = 4, N = 16 with 20 given values
- Expert: P = Q = 5, N = 25 with 30 given values


## Features

- **Advanced Heuristics**: Utilizes Norvig’s Check, Backtracking, and Constraint Propagation to optimize solving processes for both time and space efficiency.
- **High Performance**: Capable of solving complex puzzles quickly and accurately, as demonstrated by its performance in an in-class tournament.
- **Scalability**: Efficiently handles different board sizes, from standard 9x9 Sudoku puzzles to larger, more complex 25x25 boards.

## Achievements

- **In-Class Tournament**: Ranked in the top 10% among 244 submissions, showcasing the solver's superior performance and efficiency.

## Technical Details

### Algorithms Implemented

1. **Norvig’s Check**: An advanced heuristic approach that systematically narrows down possible values for each cell.
2. **Backtracking**: A methodical search technique that explores all possible solutions and retracts steps when a dead-end is reached.
3. **Constraint Propagation**: Reduces the search space by enforcing rules that must be met, effectively pruning possibilities early in the solving process.

### Technology Stack

- **Language**: Python
- **Libraries**: Utilizes various Python libraries to enhance computational efficiency and handling of large datasets.

## Usage

1. **Clone the Repository**
   ```bash
   git clone https://github.com/maitreyyi/Sudoku-Solver.git
   cd Sudoku-Python-Shell
   ```

2. **Create Boards of Varying Difficulty**
   ```bash
   python3 board_generator.py <File Prefix> <# of boards> <P> <Q> <M>

   the board format is as follows:
   P Q
   # # # ...
   # # # ...
   # # # ...
   ```

3. **Run the Solver**
   ```bash
   python3 bin/Main.py {algorithms of choice: MRV LCV FC} path/to/board/files
   ```

4. **Input Format**
   - The solver expects a text file containing the Sudoku puzzle. Each row should be on a new line with numbers separated by spaces. Zeros (0) represent empty cells.

### Example Input (9x9 Board)
```
5 3 0 0 7 0 0 0 0
6 0 0 1 9 5 0 0 0
0 9 8 0 0 0 0 6 0
8 0 0 0 6 0 0 0 3
4 0 0 8 0 3 0 0 1
7 0 0 0 2 0 0 0 6
0 6 0 0 0 0 2 8 0
0 0 0 4 1 9 0 0 5
0 0 0 0 8 0 0 7 9
```


## Contact

For any questions or feedback, please reach out to maitres@uci.edu.
