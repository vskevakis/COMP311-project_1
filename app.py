# import networkx as nx
import xml.etree.ElementTree as ET
import re
import time
from datetime import datetime
# import matplotlib.pyplot as plt


class Road:
    def __init__(self, name, node_a, node_b, weight):
        self.name = name
        self.node_a = node_a
        self.node_b = node_b
        self.weight = int(weight)
    

class Node:
    def __init__(self, name, neighbours, weight, previous, road_name):
        self.name = name
        self.neighbours = neighbours
        self.weight = weight 
        self.previous = previous
        self.road_name = road_name
    
    def add_neighbour(self, node):
        neigh_list = self.neighbours
        if node not in self.neighbours:
            neigh_list.append(node)
            self.neightbours = neigh_list
        
    def set_weight(self, number):
        self.weight = number
    
    def set_previous(self, node):
        self.previous = node

    def set_roadname(self, road_name):
        self.road_name = road_name


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
            new_node_1 = Node(node_1, [], None, None, None)
            new_node_1.add_neighbour(node_2)
            nodes.append(new_node_1)
        else:
            node = contains(nodes, node_1)
            nodes.remove(node)
            node.add_neighbour(node_2)
            nodes.append(node)
        if not contains(nodes, node_2):
            new_node_2 = Node(node_2, [], None, None, None)
            new_node_2.add_neighbour(node_1)
            nodes.append(new_node_2)
        else:
            node = contains(nodes, node_2)
            nodes.remove(node)
            node.add_neighbour(node_1)
            nodes.append(node)

    return roads, nodes

def weight_func(roads, node_1, node_2, pred_traffic):
    lowest_weight = 999
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
    Implementing a dijkstra algorith to find the shortest path. 
    \n Returns path[list], total_weight, visited_nodes

    ''' 
    visited_nodes = 0 
    priority_queue = []
    for node in nodes:
        # print(node.name)
        if node.name == source:
            node.set_weight(0)
        else:
            node.set_weight(9999)
        node.set_previous(None)
        priority_queue.append(node)

    while priority_queue:
        # Finding node with minimum weight
        min_weight = 9999
        u_node = None
        for node in priority_queue:
            if node.weight < min_weight:
                u_node = node
        visited_nodes += 1
        priority_queue.remove(u_node)

        # Terminate function
        if u_node.name == destination:
            path = []
            total_weight = u_node.weight
            while u_node.previous:
                path = [u_node.road_name] + path
                u_node = u_node.previous
            return path, total_weight, visited_nodes

        for neighbour in u_node.neighbours:
            # Finding neighbour node object
            for node in nodes:
                if node.name == neighbour:
                    neighbour_node = node
                    break
            [road_name, weight] = weight_func(roads, u_node.name, neighbour_node.name, pred_traffic)
            alt = u_node.weight + weight
            if alt < neighbour_node.weight:
                neighbour_node.set_weight(alt)
                neighbour_node.set_previous(u_node)
                neighbour_node.set_roadname(road_name)
        






def main():
    '''
    This is gonna be our main
    '''
    samples = "samples/sampleGraph2.txt"
    results = "results.txt"

    # Deleting previous results file content
    f = open(results, "w")
    f.close()


    [source, dest] = parse_sourcedest(samples)
    [roads, nodes] = parse_roads(samples)
    [pred_days, actual_days] = parse_days(samples)

    # Running Dijkstra and writing to results file
    for i in range(0, len(pred_days)):
        starting_time = datetime.now()
        # print(Dijkstra(roads, nodes, source, dest, pred_days[i]))
        # print(Dijkstra(roads, nodes, source, dest, actual_days[i]))
        dijkstra_pred_path, dijkstra_pred_weight, dijkstra_pred_vnodes = Dijkstra(roads, nodes, source, dest, pred_days[i])
        dijkstra_actual_path, dijkstra_actual_weight, dijkstra_actual_vnodes = Dijkstra(roads, nodes, source, dest, actual_days[i])
        execution_time = datetime.now() - starting_time
        path = str(' -> '.join([str(road) for road in dijkstra_pred_path]))
        f = open(results, "a")
        f.writelines('\nDay '+ str(i+1) +
        '\nDijkstra: ' + 
        '\n Visited Nodes number: ' + str(dijkstra_pred_vnodes) + 
        '\n Execution Time(ms): ' + str(execution_time.microseconds) + 
        '\n Path: ' + path + 
        '\n Predicted Cost: ' + str(round(dijkstra_pred_weight, 2)) + 
        '\n Real Cost: ' + str(round(dijkstra_actual_weight, 2)))
        f.close()

main()

