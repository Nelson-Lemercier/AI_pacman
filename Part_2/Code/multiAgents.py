# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util
import math
from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        #top ratio
        #ghost=100
        #food=5
        #scared= 1000

        weight_ghost=104
        weight_food=4.5
        weight_scared=600
        weight_capsules=20
        score=successorGameState.getScore()
        #(score)

        for x in range(newFood.width):
            for y in range(newFood.height):
                if newFood[x][y]==True :
                    distancefood=manhattanDistance(newPos,(x,y))
                    #if distancefood==0 :
                    #score =score+100+ weight_food/distancefood
                    #else :
                    score = score + weight_food / distancefood

        Capsules=successorGameState.getCapsules()

        for ghost in newGhostStates :
            distanceghost=manhattanDistance(newPos, ghost.getPosition())
            if distanceghost>0 :
                score =score - weight_ghost/distanceghost
            if (ghost.scaredTimer !=0 ) :
                score=score+weight_scared/distanceghost

        #for cap in Capsules :
            #distanceCapsules=manhattanDistance(newPos, cap)
            #score=weight_capsules/distanceCapsules
        return score

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"

        def min_value(gameState, indexagent, depth):
            v = float("inf")

            if depth == self.depth or len(gameState.getLegalActions(indexagent)) == 0 or gameState.isWin() or gameState.isLose():
                return self.evaluationFunction(gameState)

            legalaction = gameState.getLegalActions(indexagent)
            for action in legalaction:

                successors = gameState.generateSuccessor(indexagent, action)

                if indexagent == (gameState.getNumAgents()-1):
                    v = min(v, max_value(successors, depth))
                else:
                    v = min(v, min_value(successors, indexagent+1, depth))
            return v

        def max_value(gameState, depth):
            v = - float("inf")
            currdepth = depth + 1
            if currdepth == self.depth or len(gameState.getLegalActions(0)) == 0 or gameState.isWin() or gameState.isLose():
                return self.evaluationFunction(gameState)

            legalaction = gameState.getLegalActions(0)
            for action in legalaction:
                successor = gameState.generateSuccessor(0, action)
                v = max(v, min_value(successor, 1, currdepth))
            return v

        legal_action = gameState.getLegalActions(0)
        best_action = ''
        best_score = - float("inf")

        for action in legal_action:

            successor = gameState.generateSuccessor(0, action)
            score = min_value(successor, 1, 0)

            if score > best_score:
                best_score = score
                best_action = action

        return best_action

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"

        def min_value(gameState, indexagent, depth, alpha, beta):
            v = float("inf")

            if depth == self.depth or len(gameState.getLegalActions(indexagent)) == 0 or gameState.isWin() or gameState.isLose():
                return self.evaluationFunction(gameState)
            beta_temp = beta
            legalaction = gameState.getLegalActions(indexagent)
            for action in legalaction:

                successors = gameState.generateSuccessor(indexagent, action)

                if indexagent == (gameState.getNumAgents()-1):
                    v = min(v, max_value(successors, depth, alpha, beta_temp))

                    if v < alpha:
                        return v

                    beta_temp = min(beta_temp, v)

                else:
                    v = min(v, min_value(successors, indexagent+1, depth, alpha, beta_temp))

                    if v < alpha:

                        return v

                    beta_temp = min(beta_temp, v)

            return v

        def max_value(gameState, depth, alpha, beta):
            v = - float("inf")
            currdepth = depth + 1

            if currdepth == self.depth or len(gameState.getLegalActions(0)) == 0 or gameState.isWin() or gameState.isLose():
                return self.evaluationFunction(gameState)
            alpha_temp = alpha
            legalaction = gameState.getLegalActions(0)
            for action in legalaction:
                successor = gameState.generateSuccessor(0, action)
                v = max(v, min_value(successor, 1, currdepth, alpha_temp, beta))

                if v > beta:

                    return v

                alpha_temp = max(alpha_temp, v)

            return v

        legal_action = gameState.getLegalActions(0)
        best_action = ''
        best_score = - float("inf")
        alpha = - float("inf")
        beta = float("inf")

        for action in legal_action:

            successor = gameState.generateSuccessor(0, action)
            score = min_value(successor, 1, 0, alpha, beta)

            if score > best_score:
                best_score = score
                best_action = action

            if score > beta:

                return best_action

            alpha = max(alpha, score)

        return best_action

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        def expect_value(gameState, indexagent, depth):
            if depth == self.depth or len(gameState.getLegalActions(indexagent)) == 0 or gameState.isWin() or gameState.isLose():
                return self.evaluationFunction(gameState)

            legalaction = gameState.getLegalActions(indexagent)
            totalvalue = 0
            nbaction = len(legalaction)
            for action in legalaction:

                successors = gameState.generateSuccessor(indexagent, action)

                if indexagent == (gameState.getNumAgents()-1):
                    v = max_value(successors, depth)
                else:
                    v = expect_value(successors, indexagent+1, depth)
                totalvalue += v
            return float(totalvalue)/ float(nbaction)

        def max_value(gameState, depth):
            v = - float("inf")
            currdepth = depth + 1
            if currdepth == self.depth or len(gameState.getLegalActions(0)) == 0 or gameState.isWin() or gameState.isLose():
                return self.evaluationFunction(gameState)

            legalaction = gameState.getLegalActions(0)
            for action in legalaction:
                successor = gameState.generateSuccessor(0, action)
                v = max(v, expect_value(successor, 1, currdepth))
            return v

        legal_action = gameState.getLegalActions(0)
        best_action = ''
        best_score = - float("inf")

        for action in legal_action:

            successor = gameState.generateSuccessor(0, action)
            score = expect_value(successor, 1, 0)

            if score > best_score:
                best_score = score
                best_action = action

        return best_action

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

