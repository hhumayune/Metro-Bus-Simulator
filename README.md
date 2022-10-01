# Metro Bus Simulator


## -Introduction

The program is divided into two different segments, the first segment contains specific functions which allow the program to create a route using a grid-based system and store its properties into a linked list. The second segment creates a vehicle object, which uses OOP concepts on the linked list to stop at stations and traverse the route efficiently.

Upon starting of program, the user is prompted with a menu where he/she can select the number of stations in the route, or to pre-define which station It must skip. This data is then sent to the route builder function which keeps a two-dimensional list of grid coordinates. The function then creates a linked list object and inserts the first station as node into the linked list. To keep distance after each station, the function inserts a certain number of road nodes which are passed and validated through a road creation algorithm. This procedure is followed until the required number of stations have been placed. The route builder then returns the linked list as a route. After the route is created, the program creates a Bus object and passes the route as its path to allow traversal along the route. The bus will stop at stations and pick all passengers which are to be dropped off on the stations ahead. The traversal goes from start to end, and back to start again by utilizing property of doubly linked list.

After the traversal is complete, the program will automatically clear the route, and return control to the user from the main menu.


## -Libraries Used
- [Graphics.py](https://mcsp.wartburg.edu/zelle/python/graphics.py)
- Tkinter
## Specifications
Here is a brief specification of the route building part of the program:
- i.	Upon creating a simulation window, the program creates a two-dimensional grid using nested for-looping technique. A grid point is placed after a certain number of pixels to keep spaces between vertices.
- ii.	An empty linked list is created, which takes 2 types of nodes (station, road).
- iii.	The first station is created on the center of the grid to keep the route visually centered, however placing the first station anywhere else is still possible and will not break the program.
- iv.	The number of roads between each station is completely modifiable, however it has been set to any random number between range 3 to 7, this random number is re-assigned after every station to produce variance.
- v.	Road creation algorithm takes coordinates of the previous node, and the complete grid list, to assign a new set of coordinates for the next node.
- vi.	The algorithm chooses a step to a nearby vertex using a total of 8 (4 straight and 4 diagonal) options. Step selection is random. The resulting pair of coordinates is verified by checking if it exists or not in the grid list. 
- vii.	If that vertex is already claimed (does not exist in grid list), it will remove the option from the option list and choose another one, until a free vertex is found.
- viii.	If the vertex is not already claimed (exists in grid list), the corresponding coordinate set from the grid list is popped. And the new vertex coordinate is returned for next node.
- ix.	The road creation algorithm will run for each node between each station.
- x.	Each station and road object will be appended to the linked list after they are created.
- xi.	The last station will be placed at the end of the linked list to finish the route.
- xii.	Each node of the route linked list will then be drawn on the screen at their respective coordinates.
- xiii.	All stations will contain a list of passengers, denoted by numbers, of the station they would like to reach.
- xiv.	The route list is passed on to the Bus object. After traversal is finished, the route is deleted.
- xv.	 A dictionary was used to store the station names and the station numbers were set as the key.
- xvi.	A graphical user interface was added through Tkinter, to create a more user-friendly method to customize values such as the number of stations, the road length between stations or the bus speed.

## Traversal Specifications:
- i.	Bus will start traversal from head node.
- ii.	It will traverse on the route till last station and return to first station.
- iii.	On encounter of station node, the Bus will stop and pick/drop passengers.
- iv.	On encounter of road node, the bus will continue traversal.
- v.	Traversal motion is shown on the screen by drawing -> undrawing -> incrementally changing position until position is at next node coordinates.
- vi.	The bus only picks up those passengers who will go to stations next on route.
- vii.	If the bus encounters a station which is meant to be skipped, it will not pick or drop any passengers at that station.
## Screenshots
# Main Menu
-![Main Menu](https://github.com/hhumayune/Metro-Bus-Simulator/blob/main/Main%20Menu.png)
# Station List
-![Station List](https://github.com/hhumayune/Metro-Bus-Simulator/blob/main/Station%20List.png)
# Simulation
-![Simulation](https://github.com/hhumayune/Metro-Bus-Simulator/blob/main/Simulation.png)
# Collaborators
- Syed Ali Raza
- Qalb-e-Ali
- Syed Musaib Hussain
- Muhammad Tayyab
