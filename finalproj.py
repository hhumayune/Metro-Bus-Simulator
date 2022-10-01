from graphics import *
import time
from random import *
import tkinter

'''
=======================================CLASS INITIALIZATIONS AND FUNCTIONS=======================================
'''
station_name = {
    1: "(1) Queen Street",
    2: "(2) Commercial",
    3: "(3) Campus",
    4: "(4) Park Rd",
    5: "(5) City Station",
    6: "(6) General Hospital",
    7: "(7) Riverside",
    8: "(8) Francis International",
    9: "(9) Savanna",
    10: "(10) Crusader Gate",
    11: "(11) Secretariat",
    12: "(12) Paddington"
}

'''
=============================================VEHICLE CLASS FUNCTIONS=============================================
'''

class bus:
    def __init__(self):
        self.route = None
        self.speed = 60
        self.graph = [Circle(Point(0, 0), 3), Text(Point(335, 670), " ")]
        self.seats = 0
        self.capacity = []
        print("\nclass initialized!")

    def assign_route(self, r):
        self.route = r
        print("\nroute assigned!")

    def traverse_route(self, win, skipped):
        print("route traversal starts!")
        self.graph[1] = Text(Point(win.getWidth() / 2, 670), " ")
        self.graph[1].draw(win)
        if self.route is None:
            return
        else:
            message = Text(Point(win.getWidth() / 2, 700), " ")
            message.draw(win)
            message2 = Text(Point(win.getWidth() / 2, 720), " ")
            message2.draw(win)
            print("message drawn out")

            temp = self.route.start
            print("Moving forward!")
            while temp.next_point is not None:
                if is_station(temp) and skip != temp.station_number:
                    message2.undraw()
                    message2 = Text(Point(win.getWidth() / 2, 720), "Next Station: "
                                    + station_name[int(temp.station_number + 1)])
                    message2.draw(win)
                    self.load_unload(temp, win, "f", message, skipped)
                self.move_forward(temp, win, "f")
                temp = temp.next_point

            print("Moving backward!")
            while temp is not self.route.start:
                if is_station(temp) and skip != temp.station_number:
                    message2.undraw()
                    message2 = Text(Point(win.getWidth() / 2, 720), "Next Station: "
                                    + station_name[int(temp.station_number - 1)])
                    message2.draw(win)
                    self.load_unload(temp, win, "r", message, skipped)

                self.move_forward(temp, win, "r")
                temp = temp.previous_point

            if is_station(temp):
                self.load_unload(temp, win, "r", message, skipped)

            print("Traversal Finished!")

    def load_unload(self, node, win, direction, message, skipped):
        print("\nstation: ", node.station_number)
        self.graph[0] = Circle(Point(node.x, node.y), 5)
        self.graph[0].setFill("blue")
        self.graph[0].draw(win)

        if node.station_number == skipped:
            message.undraw()
            message = Text(Point(win.getWidth() / 2, 700), station_name[node.station_number] + " is skipped!")
            message.draw(win)
            time.sleep(0.5)
            message.undraw()
            self.graph[0].undraw()
            return

        message.undraw()
        message = Text(Point(win.getWidth() / 2, 700), "Current Station: " + station_name[node.station_number])
        message.draw(win)

        # unloading passengers
        items = []
        print("Dropped off: ", end='')
        for x in self.capacity:
            if x != node.station_number:
                items.append(x)
                continue
            else:
                print(x, end=', ')
        self.capacity = items[:]
        items.clear()
        print()

        # loading passengers
        print("Picked up: ", end='')
        not_going = []
        if direction == "f":
            for y in node.capacity:
                if y < node.station_number:
                    not_going.append(y)
                else:
                    self.capacity.append(y)
                    print(y, end=', ')

            node.capacity = not_going[:]
        elif direction == "r":
            for y in node.capacity:
                if y > node.station_number:
                    not_going.append(y)
                else:
                    self.capacity.append(y)
                    print(y, end=', ')

            node.capacity = not_going[:]

        not_going.clear()
        print()

        time.sleep(1.5)
        self.graph[1].undraw()
        self.graph[1] = Text(Point(win.getWidth() / 2, 670), "Passengers: " + str(self.capacity))
        self.graph[1].draw(win)

        message.undraw()
        self.graph[0].undraw()
        return

    def move_forward(self, temp, win, direction):
        # assign start and end
        start_point = [temp.x, temp.y]

        if direction == "f":
            end_point = [temp.next_point.x, temp.next_point.y]
        elif direction == "r":
            end_point = [temp.previous_point.x, temp.previous_point.y]

        # prepare position and step
        step_x = int((end_point[0] - start_point[0]) / 20)
        step_y = int((end_point[1] - start_point[1]) / 20)
        cur_position = start_point[:]

        self.graph[0] = Circle(Point(start_point[0], start_point[1]), 5)
        self.graph[0].setFill("red")

        # actual traversal
        while cur_position != end_point:
            # show on screen
            self.graph[0].draw(win)
            time.sleep(1 / self.speed)
            self.graph[0].undraw()
            # change coordinates
            cur_position[0] += step_x
            cur_position[1] += step_y

            self.graph[0] = Circle(Point(cur_position[0], cur_position[1]), 5)
            self.graph[0].setFill("red")


'''
==============================================ROUTE CLASS FUNCTIONS==============================================
'''


class grid_point:
    def __init__(self, x, y, t, c):
        self.type = t
        self.x = x
        self.y = y

        if self.type == 's':
            self.location = [x, y]
            self.capacity = []
            self.station_number = c

        elif self.type == 'r':
            self.location = [x, y]

        self.next_point = None
        self.previous_point = None


class line_route:
    def __init__(self):
        self.start = None
        self.end = None
        self.station_count = 0

    def create_station(self, x, y):
        self.station_count += 1
        new = grid_point(x, y, 's', self.station_count)
        if self.start is None:
            self.start = new
            self.end = new
            return

        temp = self.start
        while temp.next_point is not None:
            temp = temp.next_point

        temp.next_point = new
        new.previous_point = temp
        self.end = new

    def create_road(self, x, y):
        new = grid_point(x, y, 'r', None)
        if self.start is None:
            print("ERROR, No station to start from")
            return

        temp = self.start
        while temp.next_point is not None:
            temp = temp.next_point

        temp.next_point = new
        new.previous_point = temp
        self.end = new

    def remove_road(self):
        temp = self.start
        while temp is not self.end:
            temp = temp.next_point

        self.end = temp.previous_point
        self.end.next_point = None
        print("removed road!")

    def remove_route(self):
        print("Removing route")
        temp = self.start
        while temp is not self.end:
            self.start = temp
            if temp.graph is not None:
                if temp.type == 's':
                    print("station ", temp.station_number, ": ", temp.capacity)
                temp.graph.undraw()
            temp = temp.next_point
            time.sleep(0.08)
        # final station
        if temp.graph is not None:
            print("station ", temp.station_number, ": ", temp.capacity)
            temp.graph.undraw()
        print("Removed route!")

    def replace_node(self):
        temp = self.end.previous_point
        x = temp.x
        y = temp.y

        new = grid_point(x, y, 's', self.station_count)

        self.end = self.end.previous_point
        self.end = new

    def print_route(self, win):
        temp = self.start
        while temp is not None:
            if temp.type == 's':
                temp.graph = Circle(Point(temp.x, temp.y, ), 3)
                temp.graph.setFill("green")
                temp.graph.draw(win)

                # assign random passengers to station
                i = 0
                while i < 10:
                    x = randint(1, self.station_count)
                    if x == temp.station_number:
                        continue
                    else:
                        temp.capacity.append(x)
                        i += 1
                print("station ", temp.station_number, ": ", temp.capacity)

            elif temp.type == 'r':
                temp.graph = Line(Point(temp.previous_point.x, temp.previous_point.y), Point(temp.x, temp.y))
                temp.graph.draw(win)

            temp = temp.next_point
            time.sleep(0.08)


'''
=======================================OUTSIDE FUNCTIONS AND ALGORITHMS=======================================
'''


def create_grid():
    grid = []
    for y in range(1, 18):
        for x in range(1, 18):
            grid.append([x * 40, y * 40])
    return grid


def road_alg(old_cords, route_check):
    option_list = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]
    options = option_list[:]
    length = len(options)
    while length != 0:

        x = int(old_cords[0])
        y = int(old_cords[1])

        # creating a line from old point
        rand = randint(0, length - 1)
        op = options.pop(rand)
        r1 = op[0]
        r2 = op[1]

        x = x + (r1 * 40)
        y = y + (r2 * 40)

        temp = [x, y]  # store coordinates

        for a in range(len(route_check)):
            t1 = route_check[a]
            if temp == t1:
                route_check.pop(a)  # ok theres a free vertex nobody used
                return temp
        length -= 1
    return "Error"


def is_station(node):
    if node.type != 's':
        return False
    else:
        return True


def create_route(grid_list, win, num):
    route_options = grid_list[:]

    line1 = line_route()
    old_cords = route_options.pop(int(len(grid_list) / 2))  # starting point at center of window

    for i in range(0, num - 1):  # will make 'x' total stations     EDITABLE
        line1.create_station(old_cords[0], old_cords[1])

        # create road
        length = randint(3, 7)  # selects a random road length 'y'       DON'T MESS TOO MUCH WITH LENGTH
        for j in range(0, length):
            new_cords = road_alg(old_cords, route_options)  # find coordinates

            while new_cords == "Error":
                line1.remove_road()
                old_cords = [line1.end.x, line1.end.y]
                new_cords = road_alg(old_cords, route_options)

            line1.create_road(new_cords[0], new_cords[1])  # create road to coordinates
            old_cords = new_cords  # new coordinates are now old

    # last station
    line1.create_station(int(old_cords[0]), int(old_cords[1]))

    line1.print_route(win)
    return line1


def skip():
    window2 = tkinter.Tk()
    window2.title("Skip Station")
    window2.geometry('400x400')
    window2.bell()
    window2.configure(bg='white')

    def check():
        num = int(box.get())
        if num <= 8:
            ans.config(text="Station # " + str(box.get()) + " will be skipped.")
            window2.destroy()
            main(num, 8)
        else:
            ans.config(text="Please enter a valid number. Restarting")
            tkinter.messagebox.showerror(title="Invalid Number Entered", message="Please enter a valid number")
            window2.destroy()

    label = tkinter.Label(window2, text='Enter Station Number (1-8)', font=('Helvetica', 18, 'bold'))
    label.pack(pady=40)
    box = tkinter.Entry(window2)
    box.pack(pady=10)
    bt3 = tkinter.Button(window2, text='Enter', fg='white', bg="black", command=check)
    bt3.pack(pady=30)
    bt4 = tkinter.Button(window2, text='View Station List', fg='white', bg="black", command=stationlist)
    bt4.pack(pady=30)
    ans = tkinter.Label(window2)
    ans.pack()


def stationlist():
    window3 = tkinter.Tk()
    window3.title("Station List")
    window3.geometry('400x400')
    window3.bell()
    window3.configure(bg='white')

    for i in range(1, 9):
        ans = tkinter.Label(window3)
        if i == 1:
            ans.pack(pady=10)
        ans.pack(pady=5)
        ans.config(text=str(i) + ". " + station_name[i])


def start():
    main(0)


def stations():  # Customize Number of Stations
    window3 = tkinter.Tk()
    window3.title("Number of Stations")
    window3.configure(bg='white')
    window3.geometry('400x400')
    window3.bell()

    def check():
        num = int(box1.get())

        if 12 >= num > 2:
            ans1.config(text="There will be " + str(box1.get()) + " stations.")
            window3.destroy()
            main(0, num)
        else:
            ans1.config(text="Please enter a valid number. Restarting")
            tkinter.messagebox.showerror(title="Invalid Number Entered", message="Please enter a valid number")
            window3.destroy()

    label = tkinter.Label(window3, text='Enter Number(2-12): ', font=('Helvetica', 18, 'bold'))
    label.pack(pady=40)

    box1 = tkinter.Entry(window3)
    box1.pack(pady=10)
    bt4 = tkinter.Button(window3, text='Enter', width=20, height=2, fg='white', bg="black", command=check)
    bt4.pack(pady=30)
    ans1 = tkinter.Label(window3)
    ans1.pack()


def quitp():
    exit(0)


def GUI():  # Woohoo GUI Ke Shashkay!!
    window1 = tkinter.Tk()
    window1.title("Metro Simulator")
    window1.configure(bg='white')
    window1.geometry('850x600')
    window1.bell()
    l1 = tkinter.Label(window1, text='Welcome to the Metro Simulator!', bg='white', fg='black',
                       font=('Calibri', 30, 'bold'))
    l1.pack(pady=50)
    bt = tkinter.Button(window1, text='Start Route', bd=5, borderwidth=3, width=30, height=2, fg='white', bg="black",
                        command=stations, font=('Calibri', 18, 'bold'))
    bt.pack(pady=20, padx=20)
    bt1 = tkinter.Button(window1, text='Skip Station', bd=5, borderwidth=3, width=30, height=2, fg='white', bg="black",
                         command=skip, font=('Calibri', 18, 'bold'))
    bt1.pack(pady=20, padx=20)
    bt2 = tkinter.Button(window1, text='Quit Program', bd=5, borderwidth=3, width=30, height=2, fg='white', bg="black",
                         command=quitp, font=('Calibri', 18, 'bold'))
    bt2.pack(pady=20, padx=20)
    window1.mainloop()


def main(sk, st_num):  # Starts Program: skip is the Station Number to be skipped
    window = GraphWin('Sim window', 720, 800)

    c1 = Circle(Point(5, 5), 3)
    c1.setFill("black")
    c1.draw(window)

    # window.bell()
    # window.configure(bg='white')

    grid_list = create_grid()
    route = create_route(grid_list, window, st_num)
    bus1 = bus()
    bus1.assign_route(route)
    bus1.traverse_route(window, sk)
    route.remove_route()
    window.close()


GUI()
