from perlin_noise import PerlinNoise
from random import randint
import os


def create_empty(x,y):    
    
    zeros = [[0]*x]*y
    save_map_to_file(zeros)


def save_map_to_file(map):

    files = [f for f in os.listdir('.') if os.path.isfile(f)]

    numbers = []

    for file in files:
        if "map" in file:
            numbers.append(int(file.split('.')[0][3:]))

    try:
        num = max(numbers)
    except:
        num = 0

    filename = "map" + str(num+1) + ".csv"

    with open(filename, 'w') as file:
        for line in map:
            ans = [str(x) for x in line]
            file.write(','.join(ans)+'\n')


def create_perlin(x,y,threshold):

    """
    Didn't write this perlin noise code. No need to reinvent wheel. Did write everything else, though.
    """

    noise = PerlinNoise(octaves=100, seed=randint(1,10000))
    grid = [[noise([i/(x+1), j/(x+1)]) for j in range(x)] for i in range(y)]

    for i, y in enumerate(grid):
        for j, x in enumerate(y):
            if x > threshold:
                grid[i][j] = 1

            else:
                grid[i][j] = 0
    
    while True:
        x = randint(0,len(grid)//4)
        y = randint(0,len(grid)//4)

        if grid[y][x] == 0:
            grid[y][x] = 2
            break

    while True:
        x = -randint(1,len(grid)//4)
        y = -randint(1,len(grid)//4)

        if grid[y][x] == 0:
            grid[y][x] = 3
            break

    
    save_map_to_file(grid)


def main():
    print("1) Generate Blank Grid\n2) Generate Map Via Perlin Noise\n")
    while True:
        choice = input(">>> ")
        if choice == str(1):
            x = int(input("Width of grid? "))
            y = int(input("Height of grid? "))
            create_empty(x,y)
            break

        elif choice == str(2):
            x = int(input("Width of grid? "))
            y = int(input("Height of grid? "))
            create_perlin(x,y,0.05)
            break


if __name__ == "__main__":
    main()
