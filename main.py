plot_x=float(input("Enter length of plot: "))
plot_y=float(input("Enter breadth of plot: "))
front_setback=float(input("Enter front setback: "))
rear_setback=float(input("Enter rear setback: "))
left_setback=float(input("Enter left setback: "))
right_setback=float(input("Enter right setback: "))

#CHECK PLOT VALID
def check_plot_valid():
    valid_dimension=front_setback+rear_setback<plot_y and left_setback+right_setback<plot_x and plot_x>0 and plot_y>0
    valid_input=front_setback>=0 and rear_setback>=0 and left_setback>=0 and right_setback>=0
    if valid_dimension and valid_input: 
        return True
        
    else:
        return False
    
#STORING INFO OF ROOMS
if check_plot_valid():
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
else:
    print("Invalid setback and plot dimensions")
    raise SystemExit

#CHECKING FOR INVALID INPUTS
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

fig,ax=plt.subplots()
def check_rooms_valid():
    for room in data_rooms:
        inside_plot=room[3]+room[1]<=plot_x-right_setback and room[4]+room[2]<=plot_y-rear_setback and room[3]>=left_setback and room[4]>=front_setback
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

#DEFINIGN ROOM BOUNDS
def room_bounds(roomnum):
    left   = data_rooms[roomnum][3]
    right  = data_rooms[roomnum][3]+data_rooms[roomnum][1]
    bottom = data_rooms[roomnum][4]
    top    = data_rooms[roomnum][4] + data_rooms[roomnum][2]
    return left,right,bottom,top

#CALCULATING AREA 
def room_area(roomnum):
    area=data_rooms[roomnum][1]*data_rooms[roomnum][2]
    return area

#DISTANCE BETWEEN EACH ROOM 
def distance(r1,r2):
    room1=room_bounds(r1)
    room2=room_bounds(r2)
    dx=max(room1[0]-room2[1],room2[0]-room1[1],0)
    dy=max(room1[2]-room2[3],room2[2]-room1[3],0)
    return round((dx**2+dy**2)**0.5,2)
room_distances={}
for i in range(0,no_of_rooms-1):
    for j in range(i+1,no_of_rooms):
        room_distances[f"R{i+1},R{j+1}"]=distance(i,j)
print(room_distances)

#SPATIAL RELATIONSHIP BW ROOMS
def spatial_relationship(r1,r2):
    room1=room_bounds(r1)
    room2=room_bounds(r2)
    right=room1[1]<room2[0]
    left=room2[1]<room1[0]
    bottom=room1[2]>room2[3]
    top=room2[2]>room1[3]
    relation_list=[]
    if right:
        relation_list.append("right")
    elif left:
        relation_list.append("left")
    if bottom:
        relation_list.append("bottom")
    elif top:
        relation_list.append("top")
    return relation_list
room_spatial_relationship={}
for i in range(0,no_of_rooms-1):
    for j in range(i+1,no_of_rooms):
        room_spatial_relationship[f"{j+1} wrt {i+1}"]=spatial_relationship(i,j)
print(room_spatial_relationship)

#CHECKING MINIMUN DISTANCE B/W ROOMS
d=float(input("Enter minimum distance b/w rooms: "))
def min_clearance(r1,r2,d):
    if distance(r1,r2)>=d:
        return True
    else:
        return False

def check_all_clearance():
    min_clearance_rooms=[]
    for i in range(0,no_of_rooms-1):
        for j in range(i+1,no_of_rooms):
            if min_clearance(i,j,d):
                min_clearance_rooms.append(f"r{i+1}r{j+1}")
            else:
                return False
    print(min_clearance_rooms)
    return True
  
#DISTANCE FROM SETBACK BOUNDARY
def distance_from_setback(r1):
    room1=room_bounds(r1)
    distance_left=room1[0]-left_setback
    distance_right=plot_x-right_setback-room1[1]
    distance_bottom=room1[2]-front_setback
    distance_top=plot_y-rear_setback-room1[3]
    return distance_left,distance_right,distance_bottom,distance_top

distance_setback={}
for i in range(0,no_of_rooms):
    distance_setback[i+1]=distance_from_setback(i)
print(distance_setback)

def check_setback_clearance():
    setbacks=list(distance_setback.values())
    setback_clearance=float(input("Enter minimunm distance from setback: "))
    for i in setbacks:
        if min(i)<setback_clearance:
            return False
    return True 
    
#ADDING ROOMS TO PLOT AND RENDERING THE ROOMS
if check_rooms_valid() and check_overlap() and check_all_clearance() and check_setback_clearance():
    for room in data_rooms:
        Room=Rectangle((room[3],room[4]),room[1],room[2],fill=False)
        ax.add_patch(Room)
        ax.text(room[3]+room[1]/2,room[4]+room[2]/2,room[0],ha="center",va="center")
    else:
        setback=Rectangle([left_setback,front_setback],plot_x-right_setback-left_setback,plot_y-rear_setback-front_setback,fill=False)
        ax.add_patch(setback)
        ax.set_xlim(0,plot_x)
        ax.set_ylim(0,plot_y)
        ax.set_aspect("equal")
        plt.show()
else:
    print("Invalid layout")

#VERIFYING ROOM DIMENSIONS ACC TO NBC2016:
def check_room_dimensions():
    for room in data_rooms:
        if room[0].lower() == "parking":
            if room[1]>=6 and room[2]>=3:
                pass
            else:
                return False

        elif room[0].lower() == "main bedroom":
            if room[2]>=2.4 and room_area(room)>=9.5:
                pass
            else:
                return False

        elif room[0].lower() == "secondary bedroom":
            if room[2]>=2.1 and room_area(room)>=7.5:
                pass
            else:
                return False
            
        elif room[0].lower() == "kitchen":
            if room[2] >= 1.8 and room_area(room) >= 5.0:
                pass
            else:
                return False
            
        elif room[0].lower() == "bathroom":
            if room[2] >= 1.2 and room_area(room) >= 1.8:
                pass
            else:
                return False

        elif room[0].lower() == "wc":
            if room[2] >= 0.9 and room_area(room) >= 1.1:
                pass
            else:
                return False

        elif room[0].lower() == "bathroom + wc":
            if room[2] >= 1.2 and room_area(room) >= 2.8:
                pass
            else:
                return False
        
        else:
            print("Invalid room type")
            return False
    return True