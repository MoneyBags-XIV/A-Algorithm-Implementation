Hello! This is an implementation of the A* Algorithm

There are two files here: the main file is used for rendering the algorithm, and the other one is for generating maps for the algorithm to navigate.
There are no dependacies for running the algorithm, but to create random generated maps I used perlin noise. To auto-make maps, you'll need to pip install perlin_noise.

There are example maps included, but this can work with any map!

At the bottom, where the A* method is called, there is one arg passed in. This is the time in seconds that the algorithm will delay between displaying frames. I would recomend setting this to like 0.3 for the small maps, and much lower for the big ones. 
