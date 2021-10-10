# STYLUS CONTROLLED SNAKE GAME

## This whole project can be divided into two subparts:
### a) Creating a snake game using Pygame
**Note: We are now making only the game, will be linked to the original code later** 

The basic operations required while making the game is:
1. Creatinng a game window for the game to play in.
2. Defining a gameloop is suggested so to make the make code more systematic. 
3. Initializing a snk_list in which coordinates of the whole snake piece by piece will be appended.
4. Generating random coodinates of food for the snake after each time food is eaten.
5. It should be noted that food should not come over the hurdles, separate conditions are mentioned.
6. Mentioning the conditions for the arrows key to move the snake in that perticular direction.
7. Creating a list for head and appending every new coordinate of head in the list.
8. Now appending the head into the snk_list.
9. Checking for the collision conditions(with itself and also with boundary).
10. We can set the frame rate according to our choice.

**Now that we have created a simple snake game we can add moving images and hurdles to make it attractive**.

Final code is attached. After implemening all the steps we get the snake game as:
![](https://i.imgur.com/6F8qdX4.png)

### b) Making a stylus controlled snake game.
Our aims will be to detect the direction in which stylus is moving and if we are able to get it then only we have to link it with the game.

 **Approch for detecting the stlyus and then its direction.**
1. To find the upper and lower ranges of HSV values to detect the object which is to be used as Stylus.
2. To find the contours of the object and finally finding out its centroid which will be tracked.
3. To detect the direction we will be making a list and appending 10 consecutive coordinates of stylus moving.
4. Finding the maximum difference of consecutive say x coordinates in the list and if it is greater than 10(significant movement in that perticular direction) then the snake is assigned that direction.

**All the rest necessary information is explained through comments in the code**

**Here is the output of the detection of direction**
![](https://i.imgur.com/NBLDFmk.gif)

**Final output**
![](https://i.imgur.com/nnQYar3.gif)


### Contributers
LOVESH GOYAL



