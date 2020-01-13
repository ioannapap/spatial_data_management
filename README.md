# ComplexDataManagement_SpatialData_BeijingRestaurants
part1.py Spatial Index creation

part2.py Range-Search Window Selection. We use the grid we created in part1.py to evaluate window selection queries. The program will take as command-line arguments the lower and upper bound of the window in each dimension,
e.g values <x_low> <x_high> <y_low> <y_high>. It should calculate and print the points included in the window.

grid.grd file format: identifier x-coordinate y-coordinate

grid.dir(directory) file format: at its forefront it has the minimum and maximum values on each axis.
In the following lines, for each cell there will be the cell coordinate (e.g (0,0), (0,1) etc.), location in the grid.grd file which contains the first point in the cell and the number of points in cell.

SETUP: (Prerequisite: Python)

This algorithm is implemented in Python3 and runs with the following command line format in Terminal:
>> python3 part1.py 

>> python3 part2.py (and then you give the input values as it says)

Note that, it is necessary for the files to be in the same exact folder and run the above Terminal
commands in that exact folder.
