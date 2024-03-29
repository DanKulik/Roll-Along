# Roll-Along

Roll Along is a arcade style game created using Pygame.
This game is really simple with currently only three components as its basis.
The user is a red ball that has to navigate a randomly generated maze to get to the other
side of the screen. However smaller blue balls (streamers) move vertically and horizontally that will set you
back to restart if you interact with them. Walls of the maze also restrict your movements to apply extra difficulty.

When running the script you will find that three folders will be created in the directory the script is in.

Background: will allow you to insert multiple image type files that can be set as a backrgound for the game.

Music: Allows you to insert multiple audio file types that will then create a random playlist that will start as you play.

Game_Stats: will contain four .txt files. Three will keep track of your highest run/score based on the three difficulties available; while the other will measure the latency of your computer to try and give a unique rendering speed so as to make the gameplay standard throughout any device used. (This was tested on both Ubuntu 18.04 and Windows 7, however it is still a little buggy and your are more than welcome to edit the code to adjust the rendering parameters or the .txt file itself)

Inside game options include:

Play: press enter to start; press spacebar to pause and unpause game.

Settings: press enter
        Audio: press -r to remove audio, -i to insert playlist, or +- to adjust volume.
        Background: press -r to remove backround (Black Screen/Classic arcade feel), or -i to insert.
        Difficulty: press -e for easy, -m for moderate, -h for hard.
        Reset Hi-score: press -r to reset run/score to 0.
        Return to Main Menu: press enter to return.

Exit - press enter to leave.

All inside game changes by the user should be updated immediately with your difficulty choice and highest run/score indicated in the top
right hand corner. Also during play the right hand corner will indicate the number of runs completed since the start of play.

Changes from Roll Along Version 1 to 2 include faster functions and a decrease of cpu processing of 25% to 3-10% (if background is included or not) This was done by decreasing the fmps(100->24) and increasing all objects' motion velocities.

A Linux version has been added due to the in game music mixer causing high cpu usage. Pressing the f-key will open your default music player and play all the songs from your MUSIC folder. The functions that complete this task may partially or completely fail. Issues include: opening muliple player windows (depending on default player), identifying the wrong PID for the player (this issue is self-solvable by editing the script so as to only identify the player PID by player name). Player's window self-minimization may also not work and volume must be adjusted outside of gameplay.

All in all I hope that you enjoy the gameplay and interact by adding your own favorite game music and backgrounds (however black and white images are preferable. In my experience color images seem to become too distracting) 

If you notice any bugs or possible changes that could/should be added or fixed please feel free to notify me DanKulik.

Much appriciated for your patronage, and have free fun with Roll Along!
