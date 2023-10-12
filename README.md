# 2 Hours Tetris Game

Couple of days ago, I read that some company was asking for a live test consisting on 40 minutes coding Tetris. 
As far as I know, there was no constrains. My first thought was "they are crazy as f***, in 40 minutes, maybe a board+pieces engine".
Then I thought, "maybe in 2 hours...".

Said and done. In 2 hours we have:

### Features 
* A 20*10 board (It looks like this is the original board dimension)
* all tetris pieces fall down as expected
* board collisions
* piece collisions
* piece rotation with pre-rotation collision detection
* full lines gets cleared (Buggy yet)
* basic score
* next piece preview

### Missing features
* Game end and reset
* Fall speed increase as score goes up

### Dependencies:
* pygame for:
  * keyboard events
  * very (very) basic graphics
* numpy for piece matrix rotation
