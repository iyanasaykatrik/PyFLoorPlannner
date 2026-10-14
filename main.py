#IMPORTS
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

#GEOMETRY FUNCTIONS
def room_bounds(roomnum,data_rooms):
    left=data_rooms[roomnum][3]
    right=data_rooms[roomnum][3]+data_rooms[roomnum][1]
    bottom=data_rooms[roomnum][4]
    top=data_rooms[roomnum][4]+data_rooms[roomnum][2]
    return left,right,bottom,top

def room_area(roomnum,data_rooms):
    area=data_rooms[roomnum][1]*data_rooms[roomnum][2]
    return area

def distance(r1,r2,data_rooms):
    room1=room_bounds(r1,data_rooms)
    room2=room_bounds(r2,data_rooms)
    dx=max(room1[0]-room2[1],room2[0]-room1[1],0)
    dy=max(room1[2]-room2[3],room2[2]-room1[3],0)
    return round((dx**2+dy**2)**0.5,2)

#PLOT VALIDATION
def check_plot_valid(plot_x,plot_y,front_setback,rear_setback,left_setback,right_setback):
    valid_dimension=front_setback+rear_setback<plot_y and left_setback+right_setback<plot_x and plot_x>0 and plot_y>0
    valid_input=front_setback>=0 and rear_setback>=0 and left_setback>=0 and right_setback>=0
    if valid_dimension and valid_input:
        return True
    else:
        return False

#ROOM VALIDATION
def check_rooms_valid(data_rooms,plot_x,plot_y,front_setback,rear_setback,left_setback,right_setback):
    for room in data_rooms:
        inside_plot=room[3]+room[1]<=plot_x-right_setback and room[4]+room[2]<=plot_y-rear_setback and room[3]>=left_setback and room[4]>=front_setback
        valid_input=room[1]>0 and room[2]>0
        if not(inside_plot and valid_input):
            print("Invalid room position or dimension")
            return False
    print("All the inputs are valid")
    return True

def check_overlap(data_rooms):
    no_of_rooms=len(data_rooms)
    for i in range(0,no_of_rooms-1):
        for j in range(i+1,no_of_rooms):
            overlap_x=data_rooms[i][3]+data_rooms[i][1]>data_rooms[j][3] and data_rooms[j][3]+data_rooms[j][1]>data_rooms[i][3]
            overlap_y=data_rooms[i][4]+data_rooms[i][2]>data_rooms[j][4] and data_rooms[j][4]+data_rooms[j][2]>data_rooms[i][4]
            if overlap_x and overlap_y:
                print("Rooms ",i+1," and ",j+1,"overlap")
                return False
    return True

#ROOM DISTANCE
def calculate_room_distances(data_rooms):
    room_distances={}
    no_of_rooms=len(data_rooms)
    for i in range(0,no_of_rooms-1):
        for j in range(i+1,no_of_rooms):
            room_distances[f"R{i+1},R{j+1}"]=distance(i,j,data_rooms)
    return room_distances

#SPATIAL RELATIONSHIP
def spatial_relationship(r1,r2,data_rooms):
    room1=room_bounds(r1,data_rooms)
    room2=room_bounds(r2,data_rooms)
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

def calculate_spatial_relationships(data_rooms):
    room_spatial_relationship={}
    no_of_rooms=len(data_rooms)
    for i in range(0,no_of_rooms-1):
        for j in range(i+1,no_of_rooms):
            room_spatial_relationship[f"{j+1} wrt {i+1}"]=spatial_relationship(i,j,data_rooms)
    return room_spatial_relationship

#ROOM CLEARANCE
def min_clearance(r1,r2,d,data_rooms):
    if distance(r1,r2,data_rooms)>=d:
        return True
    else:
        return False

def check_all_clearance(data_rooms,d):
    min_clearance_rooms=[]
    no_of_rooms=len(data_rooms)
    for i in range(0,no_of_rooms-1):
        for j in range(i+1,no_of_rooms):
            if min_clearance(i,j,d,data_rooms):
                min_clearance_rooms.append(f"r{i+1}r{j+1}")
            else:
                return False
    print(min_clearance_rooms)
    return True

#SETBACK DISTANCE
def distance_from_setback(r1,data_rooms,plot_x,plot_y,front_setback,rear_setback,left_setback,right_setback):
    room1=room_bounds(r1,data_rooms)
    distance_left=room1[0]-left_setback
    distance_right=plot_x-right_setback-room1[1]
    distance_bottom=room1[2]-front_setback
    distance_top=plot_y-rear_setback-room1[3]
    return distance_left,distance_right,distance_bottom,distance_top

def calculate_setback_distances(data_rooms,plot_x,plot_y,front_setback,rear_setback,left_setback,right_setback):
    distance_setback={}
    for i in range(0,len(data_rooms)):
        distance_setback[i+1]=distance_from_setback(i,data_rooms,plot_x,plot_y,front_setback,rear_setback,left_setback,right_setback)
    return distance_setback

def check_setback_clearance(distance_setback,setback_clearance):
    setbacks=list(distance_setback.values())
    for i in setbacks:
        if min(i)<setback_clearance:
            return False
    return True

#ROOM DIMENSION CONSTRAINTS
def check_room_dimensions(data_rooms):
    for room in data_rooms:
        area=room[1]*room[2]
        if room[0].lower()=="parking":
            if room[1]>=6 and room[2]>=3:
                pass
            else:
                return False
        elif room[0].lower()=="main bedroom":
            if room[2]>=2.4 and area>=9.5:
                pass
            else:
                return False
        elif room[0].lower()=="secondary bedroom":
            if room[2]>=2.1 and area>=7.5:
                pass
            else:
                return False
        elif room[0].lower()=="kitchen":
            if room[2]>=1.8 and area>=5.0:
                pass
            else:
                return False
        elif room[0].lower()=="bathroom":
            if room[2]>=1.2 and area>=1.8:
                pass
            else:
                return False
        elif room[0].lower()=="wc":
            if room[2]>=0.9 and area>=1.1:
                pass
            else:
                return False
        elif room[0].lower()=="bathroom + wc":
            if room[2]>=1.2 and area>=2.8:
                pass
            else:
                return False
        else:
            print("Invalid room type")
            return False
    return True

#MANDATORY ROOMS
def check_for_existing_rooms(data_rooms):
    mandatory_rooms=["main bedroom","kitchen","bathroom"]
    rooms_found=[]
    for i in mandatory_rooms:
        for room in data_rooms:
            if room[0].lower()==i:
                rooms_found.append(i)
            elif room[0].lower()=="bathroom + wc" and i=="bathroom":
                rooms_found.append("bathroom")
    rooms_found=list(set(rooms_found))
    if len(mandatory_rooms)==len(rooms_found):
        return True
    else:
        return False

#ROOM HEIGHT
def check_min_height(room_height):
    min_room_height=2.75
    if room_height>=min_room_height:
        return True
    else:
        return False

#WINDOW VALIDATION
def check_window_position(roomnum,wall,position,width,height,sill_height,data_rooms,room_height):
    wall=wall.lower()
    if wall=="front" or wall=="back":
        wall_length=data_rooms[roomnum][1]
    elif wall=="left" or wall=="right":
        wall_length=data_rooms[roomnum][2]
    else:
        return False
    if position<0 or width<=0:
        return False
    if position+width>wall_length:
        return False
    if sill_height<0 or height<=0:
        return False
    if sill_height+height>room_height:
        return False
    return True

def check_window_overlap(window):
    for i in range(0,len(window)-1):
        for j in range(i+1,len(window)):
            same_room=window[i][0]==window[j][0]
            same_wall=window[i][2].lower()==window[j][2].lower()
            overlap=window[i][3]+window[i][4]>window[j][3] and window[j][3]+window[j][4]>window[i][3]
            if same_room and same_wall and overlap:
                print(window[i][1],"and",window[j][1],"overlap")
                return False
    return True

#WINDOW AREA
def total_window_area(roomnum,window):
    area=0
    for w in window:
        if w[0]==f"R{roomnum+1}":
            area+=w[4]*w[5]
    return area

def calculate_window_areas(data_rooms,window):
    window_areas={}
    for i in range(0,len(data_rooms)):
        window_areas[f"R{i+1}"]=total_window_area(i,window)
    return window_areas

def calculate_window_floor_ratio(data_rooms,window):
    window_floor_ratio={}
    for i in range(0,len(data_rooms)):
        floor_area=room_area(i,data_rooms)
        window_area=total_window_area(i,window)
        window_floor_ratio[f"R{i+1}"]=round((window_area/floor_area)*100,2)
    return window_floor_ratio

def check_window_area(data_rooms,window):
    for i in range(0,len(data_rooms)):
        room_type=data_rooms[i][0].lower()
        if room_type in ["main bedroom","secondary bedroom","kitchen"]:
            required_area=room_area(i,data_rooms)/6
            actual_area=total_window_area(i,window)
            if actual_area<required_area:
                print(f"Insufficient window area in R{i+1}")
                return False
    return True

#INPUT FUNCTIONS
def get_rooms(no_of_rooms):
    data_rooms=[]
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
    return data_rooms

def get_windows(data_rooms,room_height,sill_height):
    window=[]
    window_input_valid=True
    no_of_rooms=len(data_rooms)
    for i in range(0,no_of_rooms):
        print("FOR ROOM",i+1)
        no_of_windows=int(input("Enter no of windows: "))
        for j in range(0,no_of_windows):
            room_window=[]
            print("FOR WINDOW",j+1)
            room_window.append(f"R{i+1}")
            room_window.append(f"W{j+1}")
            wall=input("Enter the desired wall: ")
            room_window.append(wall)
            position=float(input("Enter window's position: "))
            room_window.append(position)
            width=float(input("Enter window's width: "))
            room_window.append(width)
            height=float(input("Enter window's height: "))
            room_window.append(height)
            if check_window_position(i,wall,position,width,height,sill_height,data_rooms,room_height):
                window.append(room_window)
                print("Window input is valid")
            else:
                print("Invalid window position or dimensions")
                window_input_valid=False
    return window,window_input_valid

#PLOTTING
def plot_layout(data_rooms,plot_x,plot_y,front_setback,rear_setback,left_setback,right_setback):
    fig,ax=plt.subplots()
    for room in data_rooms:
        Room=Rectangle((room[3],room[4]),room[1],room[2],fill=False)
        ax.add_patch(Room)
        ax.text(room[3]+room[1]/2,room[4]+room[2]/2,room[0],ha="center",va="center")
    setback=Rectangle([left_setback,front_setback],plot_x-right_setback-left_setback,plot_y-rear_setback-front_setback,fill=False)
    ax.add_patch(setback)
    ax.set_xlim(0,plot_x)
    ax.set_ylim(0,plot_y)
    ax.set_aspect("equal")
    plt.show()

#MAIN PROGRAM
def main():
    #PLOT INPUT
    plot_x=float(input("Enter length of plot: "))
    plot_y=float(input("Enter breadth of plot: "))
    front_setback=float(input("Enter front setback: "))
    rear_setback=float(input("Enter rear setback: "))
    left_setback=float(input("Enter left setback: "))
    right_setback=float(input("Enter right setback: "))

    #CHECK PLOT
    if not check_plot_valid(plot_x,plot_y,front_setback,rear_setback,left_setback,right_setback):
        print("Invalid setback and plot dimensions")
        return

    #ROOM INPUT
    no_of_rooms=int(input("Enter the number of rooms: "))
    if no_of_rooms<=0:
        print("Number of rooms must be positive")
        return
    data_rooms=get_rooms(no_of_rooms)

    #OTHER INPUTS
    d=float(input("Enter minimum distance b/w rooms: "))
    setback_clearance=float(input("Enter minimum distance from setback: "))
    room_height=float(input("Enter room height: "))
    sill_height=float(input("Enter common window sill height: "))

    #WINDOW INPUT
    window,window_input_valid=get_windows(data_rooms,room_height,sill_height)

    #VALIDATION
    valid_rooms=check_rooms_valid(data_rooms,plot_x,plot_y,front_setback,rear_setback,left_setback,right_setback)
    valid_overlap=check_overlap(data_rooms)
    valid_clearance=check_all_clearance(data_rooms,d)
    distance_setback=calculate_setback_distances(data_rooms,plot_x,plot_y,front_setback,rear_setback,left_setback,right_setback)
    valid_setback=check_setback_clearance(distance_setback,setback_clearance)
    valid_dimensions=check_room_dimensions(data_rooms)
    valid_mandatory=check_for_existing_rooms(data_rooms)
    valid_height=check_min_height(room_height)
    valid_window_overlap=check_window_overlap(window)
    valid_window_area=check_window_area(data_rooms,window)

    if valid_rooms and valid_overlap and valid_clearance and valid_setback and valid_dimensions and valid_mandatory and valid_height and window_input_valid and valid_window_overlap and valid_window_area:
        print("Layout is valid")

        #CALCULATIONS
        room_distances=calculate_room_distances(data_rooms)
        room_spatial_relationship=calculate_spatial_relationships(data_rooms)
        window_areas=calculate_window_areas(data_rooms,window)
        window_floor_ratio=calculate_window_floor_ratio(data_rooms,window)

        print(room_distances)
        print(room_spatial_relationship)
        print(distance_setback)
        print(window_areas)
        print(window_floor_ratio)

        #PLOT
        plot_layout(data_rooms,plot_x,plot_y,front_setback,rear_setback,left_setback,right_setback)
    else:
        print("Invalid layout")

if __name__=="__main__":
    main()

