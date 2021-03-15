import xml.etree.ElementTree as ET
import re

sample = "samples/sampleGraph1.txt"

# Reading txt file
with open(sample, 'r') as file:
    data_txt = file.read()
# Adding root tags to parse txt as xml
data = '<root>' + data_txt + '</root>'

root = ET.fromstring(data)

# Parsing Prediction Days
days_list = []
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

    days_list.append(prediction)

print(days_list)

