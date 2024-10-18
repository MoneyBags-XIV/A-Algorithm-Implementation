Hello! This is an implementation of the A* Algorithm

I learned about this from Sebastian Lague of Coding Adventures.
https://www.youtube.com/watch?v=-L-WgKMFuhE

There are two files here: main.py is used for rendering the algorithm, and the other one is for generating maps for the algorithm to navigate.
There are no dependacies for running the algorithm, but to create random generated maps I used perlin noise. To auto-make maps, you'll need to pip install perlin_noise.

There are example maps included, but this can work with any rectangular map!

At the bottom, where the A* method is called, there is one arg passed in. This is the time in seconds that the algorithm will delay between displaying frames. I would recomend setting this to like 0.3 for the small maps, and much lower for the big ones. 

Also, to display the maps, I used ansi escape codes to overwrite previously printed stuff. If your terminal or wherever you're running this is too small, this won't work.

Enjoy!
