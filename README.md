# Greedy Snake 2.0

### Greedy Snake 2.0 is a remake of the classic mobile game, Greedy Snake, inspired by the psychological phenomenon called cognitive dissonance. On top of the original game mechanics, this game is introduces a second player whose task is a to prevent the growth of the snake by pressing a relevant key when the snake eats a food item. The game makes use of cognitive dissonance, the discomfort that results from holding two conflicting ideas, to increase the difficulty level and potentially train the dialectical thinking of the player.

<br/>

#### **Game Design:**
- Snake
    - Goal: survive for two minutes and get points by eating food○
    - Winning condition: scored more points than the thwarter at the end of the game
- Thwarter 
    - Goal: gain points by nullifying the food that the snake ate
    - Winning condition: scored more points than the snake at the end of the game


#### **Game Mechanics:**
1. Snake's movement is controlled by the key `UP`, `DOWN`, `LEFT`, `RIGHT`.
2. The snake grows in length whenever it eats a food item.
3. The thwarter prevents the snake's growth by pressing
    `s` when the snake is eating the food from below;
    `w` when the snake is eating the food from above;
    `a` when the snake is eating the food from the right;
    `d` when the snake is eating the food from the left;


#### **How to run Greedy Snake 2.0 locally:**

1. Install Python3 locally.
2. Install the Pygame library using pip: `pip install pygame`
3. Run the game with `python main.py`


#### **How to run tests:**  

1. Install the library `pytest`.
2. Type `pytest` in the terminal. All tests should pass.

