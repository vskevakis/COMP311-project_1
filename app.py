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
    def __init__(self, name, neighbours):
        self.name = name
        self.neighbours = neighbours
    
    def add_neighbour(self, node):
        neigh_list = self.neighbours
        if node not in self.neighbours:
            neigh_list.append(node)
            self.neightbours = neigh_list


def contains(list, attribute):
    for x in list:
        if x.name == attribute:
            return x
    return None

def parse_roads(sample):

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
    lowest_weight = 999
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
            road_ind = road_ind + 1

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
            prediction.append([road, pred_traffic[road_ind]])
            road_ind = road_ind + 1

        actual_days.append(prediction)

    return pred_days, actual_days          


def main():
    '''
    This is gonna be our main
    '''
    starting_time = datetime.now()
    samples = "samples/sampleGraph1.txt"

    [roads, nodes] = parse_roads(samples)
    [pred_days, actual_days] = parse_days(samples)
    
    print(weight_func(roads, "10Node0e", "10Node7e", pred_days[0]))

    ending_time = datetime.now()
    print("Total time " + str(ending_time-starting_time))

main()

