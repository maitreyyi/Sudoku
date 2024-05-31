import SudokuBoard
import Variable
import Domain
import Trail
import Constraint
import ConstraintNetwork
import time
import random
from collections import defaultdict

class BTSolver:

    # ==================================================================
    # Constructors
    # ==================================================================

    def __init__ ( self, gb, trail, val_sh, var_sh, cc ):
        self.network = ConstraintNetwork.ConstraintNetwork(gb)
        self.hassolution = False
        self.gameboard = gb
        self.trail = trail

        self.varHeuristics = var_sh
        self.valHeuristics = val_sh
        self.cChecks = cc

    # ==================================================================
    # Consistency Checks
    # ==================================================================

    # Basic consistency check, no propagation done
    def assignmentsCheck ( self ):
        for c in self.network.getConstraints():
            if not c.isConsistent():
                return False
        return True

    """
        Part 1 TODO: Implement the Forward Checking Heuristic

        This function will do both Constraint Propagation and check
        the consistency of the network

        (1) If a variable is assigned then eliminate that value from
            the square's neighbors.

        Note: remember to trail.push variables before you assign them
        Return: a tuple of a dictionary and a bool. The dictionary contains all MODIFIED variables, mapped to their MODIFIED domain.
                The bool is true if assignment is consistent, false otherwise.
    """
    def forwardChecking ( self ):
        assignedVars = []
        modified_vars = dict()
    
        for v in self.network.variables:
            if v.isAssigned():
                assignedVars.append(v)
        while len(assignedVars) != 0:
            v = assignedVars.pop()
            for neighbor in self.network.getNeighborsOfVariable(v):
                if neighbor.isChangeable and not neighbor.isAssigned() and neighbor.getDomain().contains(v.getAssignment()):
                    self.trail.push(neighbor)
                    neighbor.removeValueFromDomain(v.getAssignment())
                    if neighbor.domain.size() == 0:
                        #backtrack
                        return (modified_vars, False)
                    elif neighbor.domain.size() ==1:
                        self.trail.push(neighbor)
                        neighbor.assignValue(neighbor.domain.values[0])
                        assignedVars.append(neighbor)

                    modified_vars[neighbor] = neighbor.domain
        return (modified_vars, self.network.isConsistent())

    # =================================================================
	# Arc Consistency
	# =================================================================
    def arcConsistency( self ):
        assignedVars = []
        for c in self.network.constraints:
            for v in c.vars:
                if v.isAssigned():
                    assignedVars.append(v)
        while len(assignedVars) != 0:
            av = assignedVars.pop(0)
            for neighbor in self.network.getNeighborsOfVariable(av):
                if neighbor.isChangeable and not neighbor.isAssigned() and neighbor.getDomain().contains(av.getAssignment()):
                    neighbor.removeValueFromDomain(av.getAssignment())
                    if neighbor.domain.size() == 1:
                        neighbor.assignValue(neighbor.domain.values[0])
                        assignedVars.append(neighbor)

    
    """
        Part 2 TODO: Implement both of Norvig's Heuristics

        This function will do both Constraint Propagation and check
        the consistency of the network

        (1) If a variable is assigned then eliminate that value from
            the square's neighbors.

        (2) If a constraint has only one possible place for a value
            then put the value there.

        Note: remember to trail.push variables before you assign them
        Return: a pair of a dictionary and a bool. The dictionary contains all variables 
		        that were ASSIGNED during the whole NorvigCheck propagation, and mapped to the values that they were assigned.
                The bool is true if assignment is consistent, false otherwise.
    """
    def norvigCheck ( self ):
        norvig = {}

        #first strategy of Norvig's: modifying domains after variable assignment
        for unit in self.network.constraints:
            for v in unit.vars:
                if v.isAssigned():
                    for neighbor in self.network.getNeighborsOfVariable(v):
                        if neighbor.isChangeable() and not neighbor.isAssigned() and neighbor.getDomain().contains(v.getAssignment()):
                            self.trail.push(neighbor)
                            neighbor.removeValueFromDomain(v.getAssignment())
                            if neighbor.getDomain().size()==0:
                                #backtrack necessary
                                return (norvig,False)
                            if neighbor.getDomain().size()==1:
                                self.trail.push(neighbor)
                                norvig[neighbor]=neighbor.domain.values[0]
                                neighbor.assignValue(neighbor.domain.values[0])
                             
        
        #second strategy 
        for unit in self.network.constraints:
            for val in range(1, self.gameboard.N+1):
                pos_count = 0
                for v in unit.vars:
                    if pos_count > 1:
                        break #this val won't work
                    if val in v.getDomain().values or v.getAssignment() == val:
                        pos_count +=1
                if pos_count ==1:
                    #find var that satisfies requirement
                    for v in unit.vars:
                        if val in v.getDomain().values and not v.isAssigned() and v.isChangeable:
                            self.trail.push(v)
                            v.assignValue(val)
                            norvig[v] = val
                if pos_count ==0:
                    return (norvig, False)
        
        return (norvig, self.network.isConsistent())
    """
         Optional TODO: Implement your own advanced Constraint Propagation

         Completing the three tourn heuristic will automatically enter
         your program into a tournament.
    """
        
    def getTournCC ( self ):
        return self.norvigCheck()

    # ==================================================================
    # Variable Selectors
    # ==================================================================

    # Basic variable selector, returns first unassigned variable
    def getfirstUnassignedVariable ( self ):
        for v in self.network.variables:
            if not v.isAssigned():
                return v

        # Everything is assigned
        return None

    """
        Part 1 TODO: Implement the Minimum Remaining Value Heuristic

        Return: The unassigned variable with the smallest domain
    """
    def getMRV ( self ):
        min_var = None
        assigned_vars = []

        for c in self.network.constraints:
            for v in c.vars:
                if v.isAssigned():
                    #check neighbors and pick neighbor with smallest domain
                    assigned_vars.append(v)

        for v in assigned_vars:
            for neighbor in self.network.getNeighborsOfVariable(v):
                if neighbor.isChangeable and not neighbor.isAssigned() and (min_var == None or (neighbor.getDomain().size() < min_var.getDomain().size())):
                    min_var = neighbor

        return min_var

    """
        Part 2 TODO: Implement the Minimum Remaining Value Heuristic
                       with Degree Heuristic as a Tie Breaker

        Return: The unassigned variable with the smallest domain and affecting the  most unassigned neighbors.
                If there are multiple variables that have the same smallest domain with the same number of unassigned neighbors, add them to the list of Variables.
                If there is only one variable, return the list of size 1 containing that variable.
    """
    def MRVwithTieBreaker ( self ):
        min_vars = []
        assigned_vars = []
        min_var = self.getMRV()
        
        if min_var == None:
            return [None]

        for c in self.network.constraints:
            for v in c.vars:
                if v.isAssigned():
                    assigned_vars.append(v)

        #iterate through assigned variables to find all that satisfy MRV
        for v in assigned_vars:
            for neighbor in self.network.getNeighborsOfVariable(v):
                if neighbor.isChangeable and not neighbor.isAssigned() and (neighbor.getDomain().size() == min_var.getDomain().size()):
                    min_vars.append(neighbor)
        
        #use degree heuristics if there are ties and return if there are no ties
        if len(min_vars) == 1: 
            return min_vars
        
        max_deg = 0
        assigned_vars = min_vars
        min_vars = []

        #find largest degree
        for v in assigned_vars:
            neighbors = len(self.network.getNeighborsOfVariable(v))
            if neighbors > max_deg:
                max_deg = neighbors

        #make list of min_vars with highest degree and MRV
        for v in assigned_vars:
            neighbors = len(self.network.getNeighborsOfVariable(v))
            if neighbors == max_deg:
                min_vars.append(v)
    
        return min_vars

    """
         Optional TODO: Implement your own advanced Variable Heuristic

         Completing the three tourn heuristic will automatically enter
         your program into a tournament.
     """
    def getTournVar ( self ):
        return self.MRVwithTieBreaker()

    # ==================================================================
    # Value Selectors
    # ==================================================================

    # Default Value Ordering
    def getValuesInOrder ( self, v ):
        values = v.domain.values
        return sorted( values )

    """
        Part 1 TODO: Implement the Least Constraining Value Heuristic

        The Least constraining value is the one that will knock the least
        values out of it's neighbors domain.

        Return: A list of v's domain sorted by the LCV heuristic
                The LCV is first and the MCV is last
    """
    def getValuesLCVOrder ( self, v ):
        #LCV: given a variable, choose least constraining value: the one that rules out the fewest values in the remaining variables
        v_domain = defaultdict(int)
        for val in v.getValues():
            for neighbor in self.network.getNeighborsOfVariable(v):
                if neighbor.isChangeable and not neighbor.isAssigned():
                    if neighbor.getDomain().contains(val):
                        v_domain[val] += neighbor.getDomain().size()-1
                    else:
                        v_domain[val] += neighbor.getDomain().size()
            
                        
        return sorted(v_domain.keys(), key = lambda x: v_domain[x], reverse=True)

    """
         Optional TODO: Implement your own advanced Value Heuristic

         Completing the three tourn heuristic will automatically enter
         your program into a tournament.
     """
    def getTournVal ( self, v ):
        return self.getValuesLCVOrder(v)

    # ==================================================================
    # Engine Functions
    # ==================================================================

    def solve ( self, time_left=600):
        if time_left <= 60:
            return -1

        start_time = time.time()
        if self.hassolution:
            return 0

        # Variable Selection
        v = self.selectNextVariable()

        # check if the assigment is complete
        if ( v == None ):
            # Success
            self.hassolution = True
            return 0

        # Attempt to assign a value
        for i in self.getNextValues( v ):

            # Store place in trail and push variable's state on trail
            self.trail.placeTrailMarker()
            self.trail.push( v )

            # Assign the value
            v.assignValue( i )

            # Propagate constraints, check consistency, recur
            if self.checkConsistency():
                elapsed_time = time.time() - start_time 
                new_start_time = time_left - elapsed_time
                if self.solve(time_left=new_start_time) == -1:
                    return -1
                
            # If this assignment succeeded, return
            if self.hassolution:
                return 0

            # Otherwise backtrack
            self.trail.undo()
        
        return 0

    def checkConsistency ( self ):
        if self.cChecks == "forwardChecking":
            return self.forwardChecking()[1]

        if self.cChecks == "norvigCheck":
            return self.norvigCheck()[1]

        if self.cChecks == "tournCC":
            return self.getTournCC()

        else:
            return self.assignmentsCheck()

    def selectNextVariable ( self ):
        if self.varHeuristics == "MinimumRemainingValue":
            return self.getMRV()

        if self.varHeuristics == "MRVwithTieBreaker":
            return self.MRVwithTieBreaker()[0]

        if self.varHeuristics == "tournVar":
            return self.getTournVar()

        else:
            return self.getfirstUnassignedVariable()

    def getNextValues ( self, v ):
        if self.valHeuristics == "LeastConstrainingValue":
            return self.getValuesLCVOrder( v )

        if self.valHeuristics == "tournVal":
            return self.getTournVal( v )

        else:
            return self.getValuesInOrder( v )

    def getSolution ( self ):
        return self.network.toSudokuBoard(self.gameboard.p, self.gameboard.q)
