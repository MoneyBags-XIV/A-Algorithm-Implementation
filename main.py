import os
from time import sleep


class Pixel():
    def __init__(self, number, x, y):
        self.is_passable = True if number != 1 else False
        self.is_end = True if number == 3 else False
        self.is_start = True if number == 2 else False

        self.explored = False

        self.x = x
        self.y = y
        
        self.g_cost = 0
        self.h_cost = 0
        self.f_cost = 0

        self.origin_pixel = None

        self.on_path = False

        self.display_color = self.set_display_color()

    def set_display_color(self):
        if self.is_end or self.is_start or self.on_path:
            return "\u001b[44m"
        elif not self.is_passable:
            return "\u001b[47;1m"
        elif self.explored:
            return "\u001b[41m"
        elif self.f_cost:
            return "\u001b[42m"
        return "\u001b[40m"
    
    def set_g_cost(self, pixel):

        if self.explored or not self.is_passable:
            return
        
        x_dis = self.x - pixel.x
        y_dis = self.y - pixel.y

        ans = ((x_dis**2 + y_dis**2)**(1/2)) + pixel.g_cost

        if not self.g_cost or ans < self.g_cost:
            self.g_cost = ans
            self.origin_pixel = pixel

    def set_h_cost(self, end_x, end_y):

        if not self.is_passable:
            return

        x_dis = self.x - end_x
        y_dis = self.y - end_y

        self.h_cost = (x_dis**2 + y_dis**2)**(1/2)
    
    def set_f_cost(self):

        if self.explored or not self.is_passable:
            return

        self.f_cost = self.g_cost + self.h_cost


class Map():
    def __init__(self,file):
        self.file = file
        self.get_csv_data()

        self.end = self.get_end()
        self.start = self.get_start()
        
        self.end_x = self.end.x
        self.end_y = self.end.y

        self.start_x = self.start.x
        self.start_y = self.start.y

    def a_star(self, step_time):
        print('\n'*(len(self.map)+4))
        pixel_to_explore = self.start

        pixel_to_explore.explored = True

        self.update_adjacent_pixels(pixel_to_explore)
        self.display_algorithm_frame()
        sleep(step_time)

        while True:
            pixel_to_explore = self.get_pixel_to_explore()

            pixel_to_explore.explored = True

            self.update_adjacent_pixels(pixel_to_explore)
            self.display_algorithm_frame()

            sleep(step_time)

            if pixel_to_explore == self.end:
                break
        
        pixel = self.end.origin_pixel

        while True:
            pixel.on_path = True
            pixel.display_color = pixel.set_display_color()
            self.display_algorithm_frame()
            sleep(step_time)

            pixel = pixel.origin_pixel

            if pixel == self.start:
                break

    def display_algorithm_frame(self):
        ans = ""

        ans += "\u001b[47;1m  \u001b[0m" * (len(self.map[0]) + 2) + '\n'

        for y in self.map:
            ans += "\u001b[47;1m  \u001b[0m"
            for x in y:
                ans += x.display_color + "  " + "\u001b[0m"
            ans += '\u001b[47;1m  \u001b[0m\n'
        
        overwrite_escape_code = "\033[F"*(len(self.map)+2)

        ans += "\u001b[47;1m  \u001b[0m" * (len(self.map[0]) + 2)

        ans = overwrite_escape_code + ans

        print(ans)
    
    def get_pixel_to_explore(self):
        lowest_f_cost = 0

        for y in self.map:
            for x in y:
                if not lowest_f_cost or x.f_cost < lowest_f_cost:
                    if x.f_cost and not x.explored:
                        lowest_f_cost = x.f_cost
        
        lowest_f_cost_candidates = []
        
        for y in self.map:
            for x in y:
                if x.f_cost == lowest_f_cost and not x.explored:
                    lowest_f_cost_candidates.append(x)
        
        lowest_h_cost = 0

        for pixel in lowest_f_cost_candidates:
            if not lowest_h_cost or pixel.h_cost < lowest_h_cost:
                lowest_h_cost = pixel.h_cost
        
        lowest_h_cost_candidates = []

        for pixel in lowest_f_cost_candidates:
            if pixel.h_cost == lowest_h_cost:
                lowest_h_cost_candidates.append(pixel)
        
        return  lowest_h_cost_candidates[0]

    def update_adjacent_pixels(self, origin_pixel):

        adjacent_pixels = self.get_adjacent_pixels(origin_pixel)
        origin_pixel.display_color = origin_pixel.set_display_color()

        for pixel in adjacent_pixels:
            pixel.set_h_cost(self.end_x, self.end_y)
            pixel.set_g_cost(origin_pixel)
            pixel.set_f_cost()
            pixel.display_color = pixel.set_display_color()

    def get_adjacent_pixels(self, pixel):
        ans = []

        for i in range(9):
            if i == 4:
                continue

            y = pixel.y + (i//3)-1
            x = pixel.x + (i%3)-1

            try:
                if x >= 0 and y >= 0:
                    ans.append(self.map[y][x])
            except:
                pass
        
        return ans

    def get_end(self):

        for y in self.map:
            for x in y:
                if x.is_end:
                    return x
                
    def get_start(self):

        for y in self.map:
            for x in y:
                if x.is_start:
                    return x

    
    def __str__(self):

        ans = ""

        for y in self.map:
            for x in y:
                char = "  "
                if x.is_start:
                    ans += "\u001b[42m" + char + "\u001b[0m"
                elif x.is_end:
                    ans += "\u001b[41m" + char + "\u001b[0m"
                elif x.is_passable:
                    ans += "\u001b[40m" + char + "\u001b[0m"
                else:
                    ans += "\u001b[47;1m" + char + "\u001b[0m"
            ans += '\n'
        
        return ans
    
    def get_csv_data(self):
        with open(self.file, 'r') as f:
            self.map = []
            for i, line in enumerate(f):
                line = line.split(',')
                self.map.append([Pixel(int(x), j, i) for j, x in enumerate(line)])
        
        self.x = len(self.map[0])
        self.y = len(self.map)


def get_file_selection():

    files = [f for f in os.listdir('.') if os.path.isfile(f) and "map" in f]

    print("Which file?")
    
    for i, file in enumerate(files):
        print(str(i+1) + ") " + file)
    
    while True:
        ans = input(">>> ")
        try:
            ans = int(ans)
        
        except:
            continue

        if ans - 1 >= len(files) or ans - 1 < 0:
            continue

        break

    ans = files[ans - 1]

    return ans


def main():

    file = get_file_selection()
    map = Map(file)
    # time_interval = input("")
    map.a_star(0)


if __name__ == "__main__":
    main()