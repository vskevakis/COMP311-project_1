# Artificial Intelligence Course
## Project 1 - Path finding algorithms
***This repo is part of our project for the COMP311 course on ECE dept. of the Technical Univerity of Crete. We implemented three different path finding algorithms that find a solution to a graph problem***
## Run
You need to have python3 installed on your computer.
```bash
python3 app.py
```

## Change sample files
Place file on /samples/ folder and change to the file name on line 407.
```python
samples = "samples/sampleGraph1.txt"
```

## Dijkstra Algorithm
Dijkstra's algorithm to find the shortest path between a and b. It picks the unvisited vertex with the lowest distance, calculates the distance through it to each unvisited neighbor, and updates the neighbor's distance if smaller. Mark visited (set to red) when done with neighbors.
![](https://gblobscdn.gitbook.com/assets%2F-LdGcqx-Ay6h4-DM_J08%2F-LdQqBd3uKWBVNik1EzU%2F-LdQqDsb98yf6tUa_Yif%2Fdijkstra.gif?alt=media&token=a2c261f8-3e0a-46ab-a6cc-abe9f6b2b934)
*from schubertng.gitbook.io

## Iterative deepening A* Algorithm
Iterative-deepening-A* works as follows: at each iteration, perform a depth-first search, cutting off a branch when its total cost f(n)=g(n)+h(n) exceeds a given threshold. This threshold starts at the estimate of the cost at the initial state, and increases for each iteration of the algorithm. At each iteration, the threshold used for the next iteration is the minimum cost of all values that exceeded the current threshold.

As in A*, the heuristic has to have particular properties to guarantee optimality (shortest paths). 
![](https://algorithmsinsight.files.wordpress.com/2016/03/ida-star.gif)
*from algorithmsinsight.wordpress.com

## LRT A* Algorithm
Real-time learning A* is very similar to an A* algorithm so its similar to our IDA* too. The main difference is that LRTA* starts with all the heuristic set to 0 (zero) and every time it crosses a road, we update the heuristics with real-time data and not predictions. This algorithm has a small learning curve and it produces acceptable solutions after running for 3 to 5 days.

## License
[MIT](https://choosealicense.com/licenses/mit/)
