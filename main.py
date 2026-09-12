plot_x=float(input("Enter length of plot: "))
plot_y=float(input("Enter breadth of plot: "))

#STORING INFO OF ROOMS
data_rooms=[]
no_of_rooms=int(input("Enter the number of rooms: "))
i=1
while i<=no_of_rooms:
    Roomi=[]
    print("FOR ROOM",i)
    room_type=input("Enter room type: ")
    Roomi.append(room_type)
    room_x=float(input("Enter length of room: "))
    Roomi.append(room_x)
    room_y=float(input("Enter breadth of room: "))
    Roomi.append(room_y)
    start_x=float(input("Enter the starting x-coordinate: "))
    Roomi.append(start_x)
    start_y=float(input("Enter the starting y-coordinate: "))
    Roomi.append(start_y)
    data_rooms.append(Roomi)
    i+=1
    print(data_rooms)

#CHECKING FOR INVALID INPUTS

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

fig,ax=plt.subplots()
def check_rooms_valid():
    for room in data_rooms:
        inside_plot=room[3]+room[1]<=plot_x and room[4]+room[2]<=plot_y and room[3]>=0 and room[4]>=0
        valid_input=room[1]>0 and room[2]>0
        if not(inside_plot and valid_input):
            print("Invalid room position or dimension")
            return False
    print("All the inputs are valid")
    return True

#CHECK FOR OVERLAP

def check_overlap():
    for i in range(0,no_of_rooms-1):
        for j in range(i+1,no_of_rooms):
            overlap_x=data_rooms[i][3]+data_rooms[i][1]>data_rooms[j][3] and data_rooms[j][3]+data_rooms[j][1]>data_rooms[i][3]
            overlap_y=data_rooms[i][4]+data_rooms[i][2]>data_rooms[j][4] and data_rooms[j][4]+data_rooms[j][2]>data_rooms[i][4]
            if overlap_x and overlap_y:
                print("Rooms ",i+1," and ",j+1,"overlap")
                return False                
    
    return True

#ADDING ROOMS TO PLOT AND RENDERING THE ROOMS
if check_rooms_valid() and check_overlap():
    for room in data_rooms:
        Room=Rectangle((room[3],room[4]),room[1],room[2],fill=False)
        ax.add_patch(Room)
        ax.text(room[3]+room[1]/2,room[4]+room[2]/2,room[0],ha="center",va="center")
    else:
        ax.set_xlim(0,plot_x)
        ax.set_ylim(0,plot_y)
        ax.set_aspect("equal")
        plt.show()
else:
    print("Invalid layout")