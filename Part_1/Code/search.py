# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util
import searchAgents

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return [s, s, w, s, w, w, s, w]


def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """

    stack = util.Stack()
    visited = set()

    """DFS algorithm"""

    stack.push((problem.getStartState(), []))

    # The stack is composed of the state and the path from the start to this state

    visited = []

    while not stack.isEmpty():

        popItem = stack.pop()

        state = popItem[0]
        path = popItem[1]

        if problem.isGoalState(state):

            return path

        if state not in visited:

            visited.append(state)

            for successorState, successorDir, successorCost in problem.getSuccessors(state):

                new_path = path + [successorDir]

                stack.push((successorState, new_path))


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""

    from util import Queue
    queue = Queue()
    path = []
    allreadyVisit = []
    output = []
    startnode = problem.getStartState()
    allreadyVisit.append(startnode)
    for i in problem.getSuccessors(startnode):
        queue.push([i])

    while not queue.isEmpty():

        path = queue.pop()
        node = path[-1]

        if node[0] not in allreadyVisit:
            allreadyVisit.append(node[0])
            if problem.isGoalState(node[0]) == True:
                print 'goal'
                for i in path:
                    output.append(i[1])
                break
            for successors in problem.getSuccessors(node[0]):
                difchem = path + [successors]
                queue.push(difchem)
    print output
    print 'goal find'

    return output


def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    n = Directions.NORTH
    e = Directions.EAST
    from util import PriorityQueue
    Pqueue = PriorityQueue()
    path = []
    allreadyVisit = []
    difchem = []
    togo = PriorityQueue()
    startnode = (problem.getStartState(), 'null', 0)
    Pqueue.push(startnode, 0)
    node = startnode
    print problem.getStartState()
    while not problem.isGoalState(node[0]):
        node = Pqueue.pop()
        if node[0] not in allreadyVisit:
            allreadyVisit.append(node[0])
            if problem.isGoalState(node[0]) == True:
                break
            for successors in problem.getSuccessors(node[0]):

                coord = successors[0]
                dir = successors[1]
                if successors[0] not in allreadyVisit:
                    difchem = path + [dir]
                    cost = problem.getCostOfActions(difchem)
                    togo.push(difchem, cost)
                    Pqueue.push(successors, cost)

        path = togo.pop()
    output = list()
    for i in path:
        output.append(i)
    for i in range(len(output)):

        if output[i] is 'North':

            output[i] = n

        elif output[i] is 'East':

            output[i] = e

        elif output[i] is 'South':

            output[i] = s
        elif output[i] is 'West':

            output[i] = w
    print output
    return output

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"

    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    n = Directions.NORTH
    e = Directions.EAST
    from util import PriorityQueue
    Pqueue = PriorityQueue()
    path = []
    allreadyVisit = []
    difchem = []
    togo = PriorityQueue()
    startnode = (problem.getStartState(), 'null', 0)
    Pqueue.push(startnode, 0)
    node = startnode
    print problem.getStartState()
    while not problem.isGoalState(node[0]):
        node = Pqueue.pop()
        if node[0] not in allreadyVisit :
            allreadyVisit.append(node[0])
            if problem.isGoalState(node[0]) == True:
                break
            for successors in problem.getSuccessors(node[0]):

                    coord = successors[0]
                    dir = successors[1]
                    if successors[0] not in allreadyVisit:

                        difchem = path + [dir]
                        cost = problem.getCostOfActions(difchem) + heuristic(coord, problem)
                        togo.push(difchem, cost)
                        Pqueue.push(successors, cost)

        path = togo.pop()
    output = list()
    for i in path:
        output.append(i)
    for i in range(len(output)):

        if output[i] is 'North':

            output[i] = n

        elif output[i] is 'East':

            output[i] = e

        elif output[i] is 'South':

            output[i] = s
        elif output[i] is 'West':

            output[i] = w
    print output
    return output





# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
