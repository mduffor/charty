# Charty

Charty is a simple text expansion language/program I created for fun to randomly lookup info in charts/tables and combine the results in interesting ways.

Charty takes an input file defining a series of lookup tables and an output specification.  It then performs weighted table lookup and string substitution to build and return the results.  

This can be utilized for any table you would "roll for" in a pen & paper RPG (or its digital equivalent): encounter table, loot table, random dungeon, etc.  It can even be used for simple random story generation.

I also use this project as example code, because although the code itself is pretty simple, it illustrates some engineering practices that are important.
- **Separation of Concerns** - Configuration, storage & use, and output are separated from one another for easier comprehension and maintenance.
- **Data Driven** - The code itself is simple, but the various use cases are driven by data.  This allows us to both re-use and expand the functionality without having to change, debug, and re-test the code.
- **Generalized** - Although the code follows the Single Responsibility Principle, it is generalized enough to be used in multiple (related) usages.  charty.py is also structured so that it can be used as either a command line utility, or as a python module that other python apps can utilize.
- **Documented** - Good naming conventions for classes, methods, variables, and parameters gets you a lot of the way towards readability of code.  However occasional use of comments and docstrings can certainly also provide additional clarity without destroying the readability of the code.
- **Consistent format** - This code should generally follow the "pythonic" formatting rules.  There are various code formatting styles, and various holy wars that have arisen from them.  The important thing however is that any given piece of code consistently follows the code formatting set out for the project or the studio.

Example output:

```
./charty.py fortune_cookie.chart 
Your fortune reads: "May you someday be carbon neutral."
```
```
./charty.py fortune_cookie.chart 
Your fortune reads: "A closed mouth gathers no feet."
```
```
./charty.py loot_table.chart -c loot_A
a pewter crown
```
```
./charty.py loot_table.chart -c loot_A
a small pile of coins
```
```
./charty.py a_thieving_story.chart -i 4
    As you enter the temple you behold a display case sitting atop an ornate
stand.  You boldly stride up to it. Upon gazing within you notice a small piece
of paper with "A conclusion is simply the place where you got tired of
thinking." written on it. Fortune favors the bold, indeed!
```
```
./charty.py a_thieving_story.chart -i 4
    As you enter the lair you behold a shiny electrum vase sitting atop an
ornate stand.  You boldly stride up to it. Upon gazing within you notice a small
pile of emeralds, a platinum crown, a magic wand, and a broach. Under your
breath you mutter, "I'm going to be rich!"
```
```
./charty.py --help
Usage: charty.py [options]

Options:
  -h, --help            show this help message and exit
  -f FILE, --file=FILE  write results to FILE instead of stdout
  -c CHART, --chart=CHART
                        roll results on specific CHART instead of using the
                        output section
  -i INDENT, --indent=INDENT
                        indent the first line by INDENT spaces
  -w WIDTH, --width=WIDTH
                        wrap the results at WIDTH characters
```
