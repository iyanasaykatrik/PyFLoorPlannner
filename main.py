plot_x=float(input("Enter length of plot: "))
plot_y=float(input("Enter breadth of plot: "))
room_x1=float(input("Enter length of room1: "))
room_y1=float(input("Enter breadth of room1: "))
room_x2=float(input("Enter length of room2: "))
room_y2=float(input("Enter breadth of room2: "))
start_x1=float(input("Enter the starting x1-coordinate: "))
start_y1=float(input("Enter the starting y1-coordinate: "))
start_x2=float(input("Enter the starting x2-coordinate: "))
start_y2=float(input("Enter the starting y2-coordinate: "))

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

fig, ax=plt.subplots()
plot=Rectangle((0,0),plot_x,plot_y,fill=False)
room1=Rectangle((start_x1,start_y1),room_x1,room_y1,fill=False)
room2=Rectangle((start_x2,start_y2),room_x2,room_y2,fill=False)
ax.add_patch(plot)

#CHECK FOR OVERLAP

def check_overlap(room1,room2):
    s1x,s1y=room1.get_x(),room1.get_y()
    x1,y1=room1.get_width(),room1.get_height()
    s2x,s2y=room2.get_x(),room2.get_y()
    x2,y2=room2.get_width(),room2.get_height()

    overlap_x=s1x+x1>s2x and s2x+x2>s1x
    overlap_y=s1y+y1>s2y and s2y+y2>s1y
    if overlap_x and overlap_y:
        print("The room overlaps")
        return True
    else:
        print("The room doesn't overlap")
        return False

#CHECKING IF ROOM INSIDE PLOT
if (start_x1+room_x1)<=plot_x and (start_y1+room_y1)<=plot_y and (start_x2+room_x2)<=plot_x and (start_y2+room_y2)<=plot_y and 0<=start_x1<=plot_x and 0<=start_y1<=plot_y and 0<=start_x2<=plot_x and 0<=start_y2<=plot_y and start_x1>=0 and start_y1>=0 and start_x2>=0 and start_y2>=0 and room_x1>0 and room_y1>0 and room_x2>0 and room_y2>0 and plot_x>0 and plot_y>0 :
    ax.add_patch(room1)
    ax.add_patch(room2)
    check_overlap(room1,room2)

else:
    print("room doesnt fit inside the plot or invalid dimensions")

ax.set_xlim(0,plot_x)
ax.set_ylim(0,plot_y)
ax.set_aspect("equal")
plt.show()