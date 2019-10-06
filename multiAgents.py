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
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
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
        return successorGameState.getScore()

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
        '''
        Returns the best action using the max-min algorithm, and self.depth as max depth
        '''
        def minMax(gameState, agentID, depth):
            '''
            Implements the max-min algorithm. 
            '''
            if agentID == gameState.getNumAgents(): #Chechs if agentID is really pacman, and increases depth
                depth += 1
                agentID = 0    
            #Chech if the gameState is a terminal state, or max depth is reached
            if gameState.isWin() or gameState.isLose() or depth == self.depth:
                return scoreEvaluationFunction(gameState), None
            action_values = [] # A list with all the actions and their values
            for action in gameState.getLegalActions(agentID):
                #Appends the value of the action and the action to the list of action values
                action_values.append([minMax(gameState.generateSuccessor(agentID, action), agentID + 1, depth)[0], action])
            if agentID == 0:
                return max(action_values) #Pacman wants to maximize his scoreEvaluation
            else:
                return min(action_values) #The ghosts wants to minimize pacmans scoreEvaluation
            
        return minMax(gameState, 0, 0)[1] #Returns the action with the higest score evaluation

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        '''
        Returns the minimax action using self.depth and self.evaluationFunction, and the alpha- beta algorithm
        '''
        
        def max_value(gameState, alfa, beta, agentID, depth):
            '''
            Tries to find the action maximation the score. Pacman wants to know this.
            '''
            if agentID != 0:
                agentID = 0 #Every time this function is called, it is pacman to move
                depth += 1 #Every time except for the first this function is called, the iteration is one layer down
            best_action = None #The best action so far
            if gameState.isWin() or gameState.isLose() or self.depth == depth: #If this is a terminal state, or max depth is reached
                return scoreEvaluationFunction(gameState), best_action
            
            v = float('-Inf') #The value of the best move so far
            for action in gameState.getLegalActions(agentID):
                #Calculate the value of this move
                min_val = min_value(gameState.generateSuccessor(agentID, action), alfa, beta, agentID + 1, depth)[0]
                if min_val > v: #If this action has a better value then the others checed, this is the new best action
                    v = min_val
                    best_action = action
                if v > beta: #If this condition is true, there is no point in expanding further
                    return v, action
                alfa = max(alfa, v)
            return v, best_action
        
        def min_value(gameState, alfa, beta, agentID, depth):
            '''
            Tries to find the action with the minimal score. The ghosts wants to know this
            '''
            best_action = None #The best action so far
            if gameState.isWin() or gameState.isLose(): #Checking if this is a terminal state
                return scoreEvaluationFunction(gameState), best_action
            
            v = float('Inf') #The value of the best move so far
            #If this is the last ghost, next agent will be pacman, and will search for max values
            if agentID == gameState.getNumAgents() - 1: 
                function = max_value
            else: #Otherwise, the next agent will also be a ghost, and will search for min values
                function = min_value
            for action in gameState.getLegalActions(agentID):
                #Calculate the value of this move
                val = function(gameState.generateSuccessor(agentID, action), alfa, beta, agentID + 1, depth)[0]
                if val < v: #If this action has a better value then the others checed, this is the new best action
                    v = val
                    best_action = action                
                if v < alfa: #If this condition is true, there is no point in expanding further
                    return v, action
                beta = min(beta, v)
            return v, best_action
        
        alfa = float('-Inf') #MAX's best value
        beta = float('Inf') #MIN's best value
        return max_value(gameState, alfa, beta, 0, 0)[1] #Returns an action
        

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
        util.raiseNotDefined()

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
