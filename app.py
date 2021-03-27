'''
Course: COMP 311 - Artificial Inteligence
Project: Path finding algorithms
Team:
    Konstantinos Revythis - 2012030136
    Skevakis Vasileios - 2012030033

MIT License
'''

import xml.etree.ElementTree as ET
import re
import time,sys
from datetime import datetime


class Road:
    def __init__(self, name, node_a, node_b, weight):
        self.name = name
        self.node_a = node_a
        self.node_b = node_b
        self.weight = int(weight)
    

class Node:
    def __init__(self, name, neighbours):
        self.name = name
        self.neighbours = neighbours
        self.weight = None 
        self.previous = None
        self.road_name = None
        self.heuristic = 0
    
    def add_neighbour(self, node):
        neigh_list = self.neighbours
        if node not in self.neighbours:
            neigh_list.append(node)
            self.neighbours = neigh_list
        
    def set_weight(self, number):
        self.weight = number
    
    def set_previous(self, node):
        self.previous = node

    def set_roadname(self, road_name):
        self.road_name = road_name

    def set_heuristic(self, heuristic):
        self.heuristic = heuristic

def get_node(node_name, nodes_list):
    for node in nodes_list:
        if node.name == node_name:
            return node

def contains(list, attribute):
    '''
    Takes a list and an attribute value and returns
    if the list has a matching attribute value
    '''
    for x in list:
        if x.name == attribute:
            return x
    return None

def parse_sourcedest(sample):
    '''
    Parsing the samples file and returns the source
    and the destination
    '''
    # Reading txt file
    with open(sample, 'r') as file:
        data_txt = file.read()
    # Adding root tags to parse txt as xml
    data = '<root>' + data_txt + '</root>'

    root = ET.fromstring(data)

    source = root.find('Source')
    dest = root.find('Destination')

    return source.text, dest.text

def parse_roads(sample):
    '''
    Parsing the samples file and returns a Roads and 
    a Nodes list
    '''
    # Reading txt file
    with open(sample, 'r') as file:
        data_txt = file.read()
    # Adding root tags to parse txt as xml
    data = '<root>' + data_txt + '</root>'

    root = ET.fromstring(data)

    roadsxml = root.find('Roads')
    roadstxt = roadsxml.text.split("\n")
    # Removing the two empty cells at start and ending of roads
    roadstxt.remove("")
    roadstxt.remove("")    
    roads = []
    nodes = []
    for road in roadstxt:
        attrs = road.split('; ')
        road_name = attrs[0]
        node_1 = attrs[1]
        node_2 = attrs[2]
        weight = attrs[3]
        roads.append(Road(road_name, node_1, node_2, weight))
        if not contains(nodes, node_1):
            new_node_1 = Node(node_1, [])
            new_node_1.add_neighbour(node_2)
            nodes.append(new_node_1)
        else:
            node = contains(nodes, node_1)
            nodes.remove(node)
            node.add_neighbour(node_2)
            nodes.append(node)
        if not contains(nodes, node_2):
            new_node_2 = Node(node_2, [])
            new_node_2.add_neighbour(node_1)
            nodes.append(new_node_2)
        else:
            node = contains(nodes, node_2)
            nodes.remove(node)
            node.add_neighbour(node_1)
            nodes.append(node)

    return roads, nodes

def weight_func(roads, node_1, node_2, pred_traffic):
    '''
    inputs: source, destination, nodes, roads, pred_traffic
    returns: distance, visited, real_path
    This function gets the predicted traffic and two nodes and returns the road 
    and weight which provide the shortest distance between given nodes
    '''
    lowest_weight = float("inf")
    lowest_road = None
    for road in roads:
        if (road.node_a == node_1 and road.node_b == node_2) or (road.node_a == node_2 and road.node_b == node_1):
            for road_p in pred_traffic:
                if road_p[0] == road.name:
                    if road_p[1] == "low":
                        weight = road.weight * 0.9
                    elif road_p[1] == "normal":
                        weight = road.weight
                    else:
                        weight = road.weight * 1.2

                    if (weight < lowest_weight) or (weight == lowest_weight and road.weight < default_weight):
                        lowest_road = road.name
                        lowest_weight = weight
                        default_weight = road.weight
                    break;
    return lowest_road, lowest_weight

def parse_days(sample):
    # Reading txt file
    with open(sample, 'r') as file:
        data_txt = file.read()
    # Adding root tags to parse txt as xml
    data = '<root>' + data_txt + '</root>'

    root = ET.fromstring(data)

    # Parsing Prediction Days
    pred_days = []
    predictionsxml = root.find('Predictions')
    for day in predictionsxml.iter('Day'):
        roads_regex = re.compile(r'\s(.*?);', re.MULTILINE)
        traffic_regex = re.compile(r'; (.*?)\s', re.MULTILINE)
        pred_road = re.findall(roads_regex, day.text)
        pred_traffic = re.findall(traffic_regex, day.text)

        prediction = []
        road_ind = 0
        for road in pred_road:
            prediction.append([road, pred_traffic[road_ind]])
            road_ind += 1

        pred_days.append(prediction)

    # Parsing Actual Days
    actual_days = []
    predictionsxml = root.find('ActualTrafficPerDay')
    for day in predictionsxml.iter('Day'):
        roads_regex = re.compile(r'\s(.*?);', re.MULTILINE)
        traffic_regex = re.compile(r'; (.*?)\s', re.MULTILINE)
        pred_road = re.findall(roads_regex, day.text)
        pred_traffic = re.findall(traffic_regex, day.text)

        prediction = []
        road_ind = 0
        for road in pred_road:
            prediction.append([road,pred_traffic[road_ind]])
            road_ind += 1

        actual_days.append(prediction)

    return pred_days, actual_days        

def Dijkstra(roads, nodes, source, destination, pred_traffic):
    '''
    Implementing a dijkstra algorithm to find the shortest path. 
    \n Returns path[list], total_weight, visited_nodes
    ''' 
    visited_nodes = 0 
    priority_queue = []
    for node in nodes:
        # print(node.name)
        if node.name == source:
            node.set_weight(0)
            priority_queue.append(node)
        else:
            node.set_weight(float("inf"))
        node.set_previous(None)

    while True:
        # Finding node with minimum weight
        min_weight = float("inf")
        u_node = None
        visited_nodes += 1        

        # Terminate function
        u_node = priority_queue[-1]
        if u_node.name == destination:
            path = []
            total_weight = u_node.weight
            while u_node.previous:
                path = [u_node.road_name + '(' + str(round(u_node.weight, 2)) + ')' ] + path
                u_node = u_node.previous
            return path, total_weight, visited_nodes

        for node in priority_queue:
            for neighbour in node.neighbours:
                # Finding neighbour node object with the minimum distance
                neighbour_node = get_node(neighbour, nodes)
                if neighbour_node not in priority_queue:

                    [road_name, weight] = weight_func(roads, node.name, neighbour_node.name, pred_traffic)
                    alt = weight + node.weight
                    if alt < min_weight:
                        min_weight = alt
                        min_node = neighbour_node
                        min_parent = node
                        min_road = road_name
        #if we havent updated the min weight that mins that we dont have any other node to explore 
        #and we havent found our destination
        if min_weight == float("inf"):
            return None, None, None
        #adding the next node to be explored to the priority_queue and update its values(weight and the road chosen to get here)
        min_node.set_weight(min_weight)
        min_node.set_previous(min_parent)
        min_node.set_roadname(min_road)
        priority_queue.append(min_node)
        
        
def IDA_Star(source, destination, nodes, roads, pred_traffic):
    '''
    inputs: source, destination, nodes, roads, pred_traffic
    returns: distance, visited, real_path
    '''
    threshold = 0
    distance = 0
    current_node = get_node(source, nodes)
    threshold = current_node.heuristic
    current_node.set_weight(0)
    current_node.set_roadname("None")
    visited = 0
    while True:
        #we start the search from the beginning with updated threshold
        [distance, visited, real_path] = IDA_Search(visited, 0, threshold, current_node, destination, nodes, roads, pred_traffic, [current_node])
        if distance == float("inf"):
            #this means that the destination node wasnt found since we explored everything 
            return -1, None, None
        elif distance < 0:
            del real_path[0]
            #our final result
            return -distance, visited, real_path
        else:
            # we add a small value to threshold to decrease the iteration/exploration that it also increases the error rate a small percent 
            # trade of accuracy with speed
            threshold = distance + 0.05*distance

def IDA_Search(visited, distance, threshold, current_node, destination, nodes, roads, pred_traffic, path):
    '''
    inputs: distance, threshold, current_node, source, destination, nodes, roads, pred_traffic
    returns: distance, visited, real_path
    '''
    real_path=[]
    current_node = path[-1]
    f = current_node.weight + current_node.heuristic
    #if the node weight plus its heuristic is bigger than the  threshold then we dont wont to exlpore this node yet
    if f > threshold : 
        return f, visited, real_path
    #we found our destination and we  return and we set the distance to negative
    if destination == current_node.name :
        real_path = [current_node.road_name + '(' + str(round(current_node.weight, 2)) + ')' ]
        return -distance, visited, real_path
    #since we skip the above if then we explore a new node and increase the visited nodes
    visited = visited +1
    min = float("inf")
    #we check all the neighbours("children") nodes of the current node
    for succ in current_node.neighbours :
        succ=get_node(succ, nodes)
        #if the are already in the path we ignore them since we have already expolred them and the have a smaller weight because
        #ida works similar to dikjstra that search the shortest path first
        if succ not in path :
            path.append(succ)
            #add it to path and get the weight between the current node an the child
            [road_name, weight] = weight_func(roads, current_node.name, succ.name, pred_traffic)
            succ.set_roadname(road_name)
            succ.set_weight(current_node.weight + weight)
            #recursive cal of ida_search ,
            [distance , visited, real_path] = IDA_Search(visited, succ.weight , threshold, succ, destination, nodes, roads, pred_traffic, path)
            #because at found we set the distance to negative then we recursively pass the bellow if and return
            if distance < 0 :
                real_path = [current_node.road_name + '(' + str(round(current_node.weight, 2)) + ')' ] + real_path
                return distance, visited, real_path
            #keep the smallest distance in the current node exploration to change the threshold value with it
            elif distance < min:
                min = distance
            #remove the current node from the path since we return from  it 
            path.pop()
    return min, visited, real_path


def LRTA_Star(source, destination, nodes, roads, pred_traffic,low_traffic):
    '''
    inputs: source, destination, nodes, roads, pred_traffic,low_traffic
    returns: distance, path, selected_road, visited
    '''
    #setting the starting values
    distance = 0
    selected_road = []
    current_node = get_node(source, nodes)
    current_node.set_weight(0)
    path = [current_node.name]
    visited = 0
    min_estimate = float("inf")
    #while we have a node to explore continue
    while current_node:

        visited += 1
        min_node=None
        min_road=None
        min_estimate = float("inf")
        #if we found the destination return
        if current_node.name == destination:
            return distance,path,selected_road,visited
        #check all the neighour nodes that are not in the path and keep the path with the smallest weight +heuristic
        for neighbour in current_node.neighbours:
            neighbour=get_node(neighbour, nodes)
            if neighbour not in path:
                [road_name, weight] = weight_func(roads, current_node.name, neighbour.name, low_traffic)
                #Our estimation is the current node weight + the distance to the neighbour + neighbours heuristic
                estimate = current_node.weight + weight + neighbour.heuristic
                [road_name, weight] = weight_func(roads, current_node.name, neighbour.name, pred_traffic)
                if estimate < min_estimate:
                    min_estimate = estimate
                    min_node = neighbour
                    min_road = road_name
                    distance = current_node.weight + weight
        if current_node.heuristic<min_estimate:
            #We change the current node heuristic value with the minimume estimate always smaller than the actual distance since we use low traffic
            current_node.set_heuristic(min_estimate)
        #We select the neighbour node with the min estimate and explore it and update its values
        min_node.set_weight(distance)
        current_node=min_node
        try:
            path.append(min_node.name)
        except:
            pass
        selected_road.append(min_road + '(' + str(round(distance,2)) + ')')


def update_progress(progress):
    '''
    Got this function from stackover flow. It creates an progress bar
    https://stackoverflow.com/questions/3160699/python-progress-bar
    '''
    barLength = 10 # Modify this to change the length of the progress bar
    status = ""
    if isinstance(progress, int):
        progress = float(progress)
    if not isinstance(progress, float):
        progress = 0
        status = "error: progress var must be float\r\n"
    if progress < 0:
        progress = 0
        status = "Halt...\r\n"
    if progress >= 1:
        progress = 1
        status = "Done...\r\n"
    block = int(round(barLength*progress))
    text = "\rPercent: [{0}] {1}% {2}".format( "#"*block + "-"*(barLength-block), progress*100, status)
    sys.stdout.write(text)
    sys.stdout.flush()

def main():
    '''
    This is gonna be our main
    '''
    samples = "samples/sampleGraph1.txt"
    results = "a_results.txt"
    results_b = "b_results.txt"

    print("Getting stuff ready... Please wait")

    [source, dest] = parse_sourcedest(samples)
    [roads, nodes] = parse_roads(samples)
    [pred_days, actual_days] = parse_days(samples)


    # Make a new nodes array WITH heuristics from running Dijkstra on every node
    # till our goal. - Will use it for one day for now
    low_traffic = []
    for day in pred_days[0]:
        low_traffic.append([day[0], "low"])

    # Deleting previous results file content
    f = open(results_b, "w")

    full_lrta_sec = 0
    full_lrta_distance = 0
    full_lrta_visited = 0
    # Running Lrta* and writing to results file
    for i in range(0, len(pred_days)):
        starting_time = datetime.now()
        lrta_pred_weight, useless_path, lrta_pred_path, lrta_pred_vnodes = LRTA_Star(source, dest, nodes, roads, pred_days[i],low_traffic)
        execution_time_lrta = datetime.now() - starting_time
        lrta_path = str(' -> '.join([str(road) for road in lrta_pred_path]))
        f.writelines('Day '+ str(i+1) +
        '\nLRTA*: ' + 
        '\n Visited Nodes number: ' + str(lrta_pred_vnodes) + 
        '\n Execution Time(ms): ' + str(execution_time_lrta.microseconds) + 
        '\n Path: ' + lrta_path + 
        '\n Cost: ' + str(round(lrta_pred_weight, 2)) + 
        '\n')
        full_lrta_sec += execution_time_lrta.total_seconds()
        full_lrta_distance += lrta_pred_weight
        full_lrta_visited += lrta_pred_vnodes
    f.close()

    # Setting heuristics for IDA*
    nodes_with_h = []
    for node in nodes:
        path, heuristic, visited = Dijkstra(roads, nodes, node.name, dest, low_traffic)
        node.set_heuristic(heuristic)
        nodes_with_h.append(node)

    # Deleting previous results file content
    # f = open(results, "w")
    # f.close()
    f = open(results, "w")
    full_dijkstra_sec = 0
    full_ida_sec = 0 
    full_dijkstra_distance = 0
    full_ida_distance = 0
    full_dijkstra_visited = 0
    full_ida_visited = 0
    # Running Dijkstra and IDA * and writing to results file
    for i in range(0, len(pred_days)):
        starting_time = datetime.now()
        dijkstra_pred_path, dijkstra_pred_weight, dijkstra_pred_vnodes = Dijkstra(roads, nodes, source, dest, pred_days[i])
        execution_time_dij = datetime.now() - starting_time
        dijkstra_actual_path, dijkstra_actual_weight, dijkstra_actual_vnodes = Dijkstra(roads, nodes, source, dest, actual_days[i])
        starting_time = datetime.now()
        ida_pred_weight, ida_pred_vnodes, ida_pred_path = IDA_Star(source, dest, nodes_with_h, roads, pred_days[i])
        execution_time_ida = datetime.now() - starting_time
        ida_actual_weight, ida_actual_vnodes, ida_actual_path = IDA_Star(source, dest, nodes_with_h, roads, actual_days[i])
        dij_path = str(' -> '.join([str(road) for road in dijkstra_pred_path]))
        ida_path = str(' -> '.join([str(road) for road in ida_pred_path]))
        f.writelines('Day '+ str(i+1) +
        '\nDijkstra: ' + 
        '\n Visited Nodes number: ' + str(dijkstra_pred_vnodes) + 
        '\n Execution Time(ms): ' + str(execution_time_dij.microseconds) + 
        '\n Path: ' + dij_path + 
        '\n Predicted Cost: ' + str(round(dijkstra_pred_weight, 2)) + 
        '\n Real Cost: ' + str(round(dijkstra_actual_weight, 2)) +
        '\nIDA*: ' + 
        '\n Visited Nodes number: ' + str(ida_pred_vnodes) + 
        '\n Execution Time(ms): ' + str(execution_time_ida.microseconds) + 
        '\n Path: ' + ida_path + 
        '\n Predicted Cost: ' + str(round(ida_pred_weight, 2)) + 
        '\n Real Cost: ' + str(round(ida_actual_weight, 2)) +
        '\n')
        full_dijkstra_sec += execution_time_dij.total_seconds()
        full_ida_sec += execution_time_ida.total_seconds()
        full_dijkstra_distance += dijkstra_pred_weight
        full_ida_distance += ida_pred_weight
        full_dijkstra_visited += dijkstra_pred_vnodes
        full_ida_visited += ida_pred_vnodes
    f.close()


    print("\nRunning Dijkstra simulation for 80 days")
    for i in range(100):
        update_progress(i/99.0)
        time.sleep(full_dijkstra_sec/100)
    
    print('Total Time (sec): '+ str(full_dijkstra_sec))
    print("Dijkstra distance average: " + str(full_dijkstra_distance/80))
    print("Dijkstra visited average: " + str(full_dijkstra_visited/80))

    print("\nRunning IDA* simulation for 80 days")
    for i in range(100):
        update_progress(i/99.0)
        time.sleep(full_ida_sec/100)

    print('Total Time (sec): ' + str(full_ida_sec))
    print("IDA* distance average: " + str(full_ida_distance/80))
    print("IDA* visited average: " + str(full_ida_visited/80))


    print("\nRunning LRTA* simulation for 80 days")
    for i in range(100):
        update_progress(i/99.0)
        time.sleep(full_lrta_sec/100)

    print('Total Time (sec): ' + str(full_lrta_sec))
    print("LRTA* distance average: " + str(full_lrta_distance/80))
    print("LRTA* visited average: " + str(full_lrta_visited/80))

    print("\nResults saved on \"" + results + "\" and \"" + results_b + "\"")


main()

