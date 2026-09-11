plot_x=float(input("Enter length of plot: "))
plot_y=float(input("Enter breadth of plot: "))

#STORING INFO OF ROOMS
data_rooms=[]
no_of_rooms=int(input("Enter the number of rooms: "))
i=1
while i<=no_of_rooms:
    Roomi=[]
    print("FOR ROOM",i)
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

#CHECKING FOR INVALID INPUTS AND ADDING ROOMS TO THE PLOT

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

fig,ax=plt.subplots()

for room in data_rooms:
    inside_plot=room[2]+room[0]<=plot_x and room[3]+room[1]<=plot_y and room[2]>=0 and room[3]>=0
    valid_input=room[0]>0 and room[1]>0
    if inside_plot and valid_input:
        Room=Rectangle((room[2],room[3]),room[0],room[1],fill=False)
        ax.add_patch(Room)
    else:
        print("Room doesn't fit inside plot or invalid input")    

#CHECK FOR OVERLAP

def check_overlap():
    for i in range(0,no_of_rooms-1):
        for j in range(i+1,no_of_rooms):
            overlap_x=data_rooms[i][2]+data_rooms[i][0]>data_rooms[j][2] and data_rooms[j][2]+data_rooms[j][0]>data_rooms[i][2]
            overlap_y=data_rooms[i][3]+data_rooms[i][1]>data_rooms[j][3] and data_rooms[j][3]+data_rooms[j][1]>data_rooms[i][3]
            if overlap_x and overlap_y:
                print("The rooms overlap")
                return True
            
    print("The rooms doesn't overlap")
    return False

check_overlap()
ax.set_xlim(0,plot_x)
ax.set_ylim(0,plot_y)
ax.set_aspect("equal")
plt.show()