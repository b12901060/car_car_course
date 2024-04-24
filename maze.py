import csv
import logging
import math
from enum import IntEnum
from typing import List

import numpy as np
import pandas

from node import Direction, Node

log = logging.getLogger(__name__)


class Action(IntEnum):
    ADVANCE = 1
    U_TURN = 2
    TURN_RIGHT = 3
    TURN_LEFT = 4
    HALT = 5


class Maze:
    def __init__(self, filepath: str):
        # TODO : read file and implement a data structure you like
        # For example, when parsing raw_data, you may create several Node objects.
        # Then you can store these objects into self.nodes.
        # Finally, add to nd_dict by {key(index): value(corresponding node)}
        self.raw_data = pandas.read_csv(filepath).values
        self.nodes = []
        self.node_dict = dict()  # key: index, value: the correspond node
        indexs = range(1, len(self.raw_data) + 1)  
        for index in indexs:
            node=Node(index)
            for i in range(4):
                node.set_successor(self.raw_data[index-1][i+1],index,self.raw_data[index-1][i+5])
            self.nodes.append(node)
            self.node_dict[index] = node

    def get_start_point(self):
        if len(self.node_dict) < 2:
            log.error("Error: the start point is not included.")
            return 0
        return self.node_dict[1]

    def get_node_dict(self):
        return self.node_dict

    def BFS(self, node: Node):
        # TODO : design your data structure here for your algorithm
        # Tips : return a sequence of nodes from the node to the nearest unexplored deadend
        return None

    def BFS_2(self, node_from: Node, node_to: Node):
        # TODO : similar to BFS but with fixed start point and end point
        # Tips : return a sequence of nodes of the shortest path
        visited={node_from:True}
        dist={node_from:0}
        i=0
        tmpn=node_to
        tmps={node_from}
        path={node_from:None}
        while i<len(tmps):
            i=i+1;
            for successor in tmps[i].get_successors():
                if successor not in visited:
                    visited.append(successor)
                    visited[successor]=True
                    dist.append(successor)
                    dist[successor]=dist[tmps[i]]+1
                    path.append(successor)
                    path[successor]=tmps[i]
                    tmps.append(successor)
                    if successor == node_to:
                        short_path = [node_to]
                        while tmpn!=node_from:
                            short_path.append(path[tmpn])
                            tmpn = path[tmpn]
                        short_path.reverse()
                        return short_path
                    
        return None

    def getAction(self, car_dir, node_from: Node, node_to: Node):
        # TODO : get the car action
        # Tips : return an action and the next direction of the car if the node_to is the Successor of node_to
        # If not, print error message and return 0
        for successor in node_from.get_succcessors:
            if successor==node_to:
                if car_dir==node_from.get_direction(node_to):
                    return car_dir,1
                elif abs(car_dir-node_from.get_direction(node_to))==1 and car_dir+node_from.get_direction(node_to)!=5:
                    act={}
                    act.append(2)
                    act.append(1)
                    car_dir=node_from.get_direction(node_to)
                    return car_dir,act 
                elif car_dir==1 and node_from.get_direction(node_to)==3 or car_dir==3 and node_from.get_direction(node_to)==2 or car_dir==2 and node_from.get_direction(node_to)==4 or car_dir==4 and node_from.get_direction(node_to)==1:
                    act={}
                    act.append(4)
                    act.append(1)
                    car_dir=node_from.get_direction(node_to)
                    return car_dir,act
                elif car_dir==3 and node_from.get_direction(node_to)==1 or car_dir==2 and node_from.get_direction(node_to)==3 or car_dir==4 and node_from.get_direction(node_to)==2 or car_dir==1 and node_from.get_direction(node_to)==4:
                    act={}
                    act.append(3)
                    act.append(1)
                    car_dir=node_from.get_direction(node_to)
                    return car_dir,act
        return None

    def getActions(self, nodes: List[Node]):
        # TODO : given a sequence of nodes, return the corresponding action sequence
        # Tips : iterate through the nodes and use getAction() in each iteration
        car_dir=0
        act={}
        actions={}
        for i in range(len(List)-1):
            car_dir,act=getAction(car_dir,List[i],List[i+1])
            actions.append(act)
        return None

    def actions_to_str(self, actions):
        # cmds should be a string sequence like "fbrl....", use it as the input of BFS checklist #1
        cmd = "fbrls"
        cmds = ""
        for action in actions:
            cmds += cmd[action - 1]
        log.info(cmds)
        return cmds

    def strategy(self, node: Node):
        return self.BFS(node)

    def strategy_2(self, node_from: Node, node_to: Node):
        return self.BFS_2(node_from, node_to)
