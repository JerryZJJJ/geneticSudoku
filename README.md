Solving Sudoku Heuristically
============================

A Quick Python Script for Teaching
----------------------------------

This script was written quite hastily to show how heuristics work, utilizing a Sudoku puzzle as an example.  

Given a Sudoku puzzle with empty spaces annotated as -1, the program will parse through the puzzle and begin guessing at solutions.  Those solutions that are 'better' (higher scoring) than other solutions will survive while the lower solutions are replaced with either combined high quality solutions or new random ones.  The program outputs the average score of the population as well as the average during runtime to indicate how the 'evolution' is progressing.

Just a note - this is really quickly, hastily written code and needs more documentation.

## To Do: 

- Document Code
- Generate tiepoints to collect statistics during runtime for graphing
