# MIT 6.034 Lab 4: Constraint Satisfaction Problems
# Written by Dylan Holmes (dxh), Jessica Noss (jmn), and 6.034 staff

from constraint_api import *
from test_problems import get_pokemon_problem

#### PART 1: WRITE A DEPTH-FIRST SEARCH CONSTRAINT SOLVER

def has_empty_domains(csp) :
    "Returns True if the problem has one or more empty domains, otherwise False"
    variables=csp.unassigned_vars
    for var in variables:
        if len(csp.get_domain(var))==0:
            return True
    return False


def check_all_constraints(csp) :
    """Return False if the problem's assigned values violate some constraint,
    otherwise True"""
    constraints=csp.get_all_constraints()
    for constraint in constraints:
        var1 = constraint.var1
        var2 = constraint.var2
        val1=csp.get_assigned_value(var1)
        val2=csp.get_assigned_value(var2)
        if val1!=None and val2!=None:
            if not constraint.check(val1,val2):
                return False
    return True


def solve_constraint_dfs(problem) :
    """Solves the problem using depth-first search.  Returns a tuple containing:
    1. the solution (a dictionary mapping variables to assigned values), and
    2. the number of extensions made (the number of problems popped off the agenda).
    If no solution was found, return None as the first element of the tuple."""
    agenda=[problem]
    extension=0
    current_prob=agenda.pop(0)
    extension+=1

    #check failure
    if has_empty_domains(current_prob) or (not check_all_constraints(current_prob)):
        return (None, extension)

    #check success
    all_assigned=True
    variables = current_prob.get_all_variables()
    for var in variables:
        if current_prob.get_assigned_value(var)==None:
            all_assigned=False
            break
    if all_assigned:
        return (current_prob.assigned_values,extension)

    #iteration
    next_un_var=current_prob.pop_next_unassigned_var()
    next_domain=current_prob.get_domain(next_un_var)
    new_probs=[]
    for val in next_domain:
        temp=current_prob.copy()
        new_probs.append(temp.set_assigned_value(next_un_var,val))
    agenda=new_probs+agenda
    while (len(agenda)!=0):
        new_prob = agenda.pop(0)
        result=solve_constraint_dfs(new_prob)
        extension+=result[1]
        if not result[0] is None:
            return (result[0],extension)
    return (None,extension)

#### PART 2: DOMAIN REDUCTION BEFORE SEARCH

def eliminate_from_neighbors(csp, var) :
    """Eliminates incompatible values from var's neighbors' domains, modifying
    the original csp.  Returns an alphabetically sorted list of the neighboring
    variables whose domains were reduced, with each variable appearing at most
    once.  If no domains were reduced, returns empty list.
    If a domain is reduced to size 0, quits immediately and returns None."""
    eliminated_vars=[]
    val1s=csp.get_domain(var)
    neighbors=csp.get_neighbors(var)
    for neighbor in neighbors:
        eliminated=False
        constraints=csp.constraints_between(var,neighbor)
        tem=csp.copy()
        neighbor_domain=tem.get_domain(neighbor)

        for val2 in neighbor_domain:
            satisfied=False
            for val1 in val1s:
                good=True
                for constraint in constraints:
                    if not constraint.check(val1,val2):
                        good=False
                        break
                if good:
                    satisfied=True
                    break
            if not satisfied:
                csp.eliminate(neighbor,val2)
                eliminated=True
        if eliminated:
            eliminated_vars.append(neighbor)
            if len(csp.get_domain(neighbor))==0:
                return None
    return sorted(eliminated_vars)

def domain_reduction(csp, queue=None) :
    """Uses constraints to reduce domains, modifying the original csp.
    If queue is None, initializes propagation queue by adding all variables in
    their default order.  Returns a list of all variables that were dequeued,
    in the order they were removed from the queue.  Variables may appear in the
    list multiple times.
    If a domain is reduced to size 0, quits immediately and returns None."""
    if queue==None:
        queue=csp.get_all_variables()
    dequeued=[]
    while len(queue)!=0:
        current_var=queue.pop(0)
        dequeued.append(current_var)
        eliminated=eliminate_from_neighbors(csp,current_var)
        if(eliminated==None):
            return None
        for var in eliminated:
            if not var in queue:
                 queue.append(var)
    return dequeued


# QUESTION 1: How many extensions does it take to solve the Pokemon problem
#    with dfs if you DON'T use domain reduction before solving it?

# Hint: Use get_pokemon_problem() to get a new copy of the Pokemon problem
#    each time you want to solve it with a different search method.


pokemon_problem=get_pokemon_problem()
# domain_reduction(pokemon_problem,None)
# print(solve_constraint_dfs(pokemon_problem)[1])

ANSWER_1 = 20

# QUESTION 2: How many extensions does it take to solve the Pokemon problem
#    with dfs if you DO use domain reduction before solving it?

ANSWER_2 = 6


#### PART 3: PROPAGATION THROUGH REDUCED DOMAINS

def solve_constraint_propagate_reduced_domains(problem) :
    """Solves the problem using depth-first search with forward checking and
    propagation through all reduced domains.  Same return type as
    solve_constraint_dfs."""
    agenda=[problem]
    extension=0
    current_prob=agenda.pop(0)
    extension+=1

    #check failure
    if has_empty_domains(current_prob) or (not check_all_constraints(current_prob)):
        return (None, extension)

    #check success
    all_assigned=True
    variables = current_prob.get_all_variables()
    for var in variables:
        if current_prob.get_assigned_value(var)==None:
            all_assigned=False
            break
    if all_assigned:
        return (current_prob.assigned_values,extension)

    #iteration
    next_un_var=current_prob.pop_next_unassigned_var()
    next_domain=current_prob.get_domain(next_un_var)
    new_probs=[]
    for val in next_domain:
        temp=current_prob.copy()
        new=temp.set_assigned_value(next_un_var,val)

        queue=[next_un_var]
        domain_reduction(new,queue)

        new_probs.append(new)
    agenda=new_probs+agenda
    while (len(agenda)!=0):
        new_prob = agenda.pop(0)
        result=solve_constraint_propagate_reduced_domains(new_prob)
        extension+=result[1]
        if not result[0] is None:
            return (result[0],extension)
    return (None,extension)

# QUESTION 3: How many extensions does it take to solve the Pokemon problem
#    with propagation through reduced domains? (Don't use domain reduction
#    before solving it.)
#print(solve_constraint_propagate_reduced_domains(pokemon_problem)[1])
ANSWER_3 = 7


#### PART 4: PROPAGATION THROUGH SINGLETON DOMAINS

def domain_reduction_singleton_domains(csp, queue=None) :
    """Uses constraints to reduce domains, modifying the original csp.
    Only propagates through singleton domains.
    Same return type as domain_reduction."""
    if queue==None:
        queue=csp.get_all_variables()
    dequeued=[]
    while len(queue)!=0:
        current_var=queue.pop(0)
        dequeued.append(current_var)
        eliminated=eliminate_from_neighbors(csp,current_var)
        if(eliminated==None):
            return None
        pre_add_list=[]
        add_list=[]
        for var in eliminated:
            exist=False
            for varr in queue:
                if var == varr:
                    exist=True
                break
            if not exist:
                pre_add_list.append(var)
        for var in pre_add_list:
            if len(csp.get_domain(var))==1:
                add_list.append(var)
        queue=queue+add_list
    return dequeued

def solve_constraint_propagate_singleton_domains(problem) :
    """Solves the problem using depth-first search with forward checking and
    propagation through singleton domains.  Same return type as
    solve_constraint_dfs."""
    agenda=[problem]
    extension=0
    current_prob=agenda.pop(0)
    extension+=1

    #check failure
    if has_empty_domains(current_prob) or (not check_all_constraints(current_prob)):
        return (None, extension)

    #check success
    all_assigned=True
    variables = current_prob.get_all_variables()
    for var in variables:
        if current_prob.get_assigned_value(var)==None:
            all_assigned=False
            break
    if all_assigned:
        return (current_prob.assigned_values,extension)

    #iteration
    next_un_var=current_prob.pop_next_unassigned_var()
    next_domain=current_prob.get_domain(next_un_var)
    new_probs=[]
    for val in next_domain:
        temp=current_prob.copy()
        new=temp.set_assigned_value(next_un_var,val)

        queue=[next_un_var]
        domain_reduction_singleton_domains(new,queue)

        new_probs.append(new)
    agenda=new_probs+agenda
    while (len(agenda)!=0):
        new_prob = agenda.pop(0)
        result=solve_constraint_propagate_reduced_domains(new_prob)
        extension+=result[1]
        if not result[0] is None:
            return (result[0],extension)
    return (None,extension)

# QUESTION 4: How many extensions does it take to solve the Pokemon problem
#    with propagation through singleton domains? (Don't use domain reduction
#    before solving it.)
#print(solve_constraint_propagate_singleton_domains(pokemon_problem)[1])
ANSWER_4 = 8


#### PART 5: FORWARD CHECKING

def propagate(enqueue_condition_fn, csp, queue=None) :
    """Uses constraints to reduce domains, modifying the original csp.
    Uses enqueue_condition_fn to determine whether to enqueue a variable whose
    domain has been reduced.  Same return type as domain_reduction."""
    if queue==None:
        queue=csp.get_all_variables()
    dequeued=[]
    while len(queue)!=0:
        current_var=queue.pop(0)
        dequeued.append(current_var)
        eliminated=eliminate_from_neighbors(csp,current_var)
        if(eliminated==None):
            return None
        pre_add_list=[]
        add_list=[]
        for var in eliminated:
            exist=False
            for varr in queue:
                if var == varr:
                    exist=True
                break
            if not exist:
                pre_add_list.append(var)
        for var in pre_add_list:
            if enqueue_condition_fn(csp,var):
                add_list.append(var)
        queue=queue+add_list
    return dequeued

def condition_domain_reduction(csp, var) :
    """Returns True if var should be enqueued under the all-reduced-domains
    condition, otherwise False"""
    return True

def condition_singleton(csp, var) :
    """Returns True if var should be enqueued under the singleton-domains
    condition, otherwise False"""
    if len(csp.get_domain(var))==1:
        return True
    return False

def condition_forward_checking(csp, var) :
    """Returns True if var should be enqueued under the forward-checking
    condition, otherwise False"""
    return False


#### PART 6: GENERIC CSP SOLVER

def solve_constraint_generic(problem, enqueue_condition=None) :
    """Solves the problem, calling propagate with the specified enqueue
    condition (a function).  If enqueue_condition is None, uses DFS only.
    Same return type as solve_constraint_dfs."""
    agenda=[problem]
    extension=0
    current_prob=agenda.pop(0)
    extension+=1

    #check failure
    if has_empty_domains(current_prob) or (not check_all_constraints(current_prob)):
        return (None, extension)

    #check success
    all_assigned=True
    variables = current_prob.get_all_variables()
    for var in variables:
        if current_prob.get_assigned_value(var)==None:
            all_assigned=False
            break
    if all_assigned:
        return (current_prob.assigned_values,extension)

    #iteration
    next_un_var=current_prob.pop_next_unassigned_var()
    next_domain=current_prob.get_domain(next_un_var)
    new_probs=[]
    for val in next_domain:
        temp=current_prob.copy()
        new=temp.set_assigned_value(next_un_var,val)

        if not enqueue_condition==None:
            queue=[next_un_var]
            propagate(enqueue_condition,new,queue)

        new_probs.append(new)
    agenda=new_probs+agenda
    while (len(agenda)!=0):
        new_prob = agenda.pop(0)
        result=solve_constraint_generic(new_prob,enqueue_condition)
        extension+=result[1]
        if not result[0] is None:
            return (result[0],extension)
    return (None,extension)

# QUESTION 5: How many extensions does it take to solve the Pokemon problem
#    with DFS and forward checking, but no propagation? (Don't use domain
#    reduction before solving it.)
#print(solve_constraint_generic(pokemon_problem,condition_forward_checking)[1])
ANSWER_5 = 9


#### PART 7: DEFINING CUSTOM CONSTRAINTS

def constraint_adjacent(m, n) :
    """Returns True if m and n are adjacent, otherwise False.
    Assume m and n are ints."""
    if abs(m-n)==1:
        return True
    return False

def constraint_not_adjacent(m, n) :
    """Returns True if m and n are NOT adjacent, otherwise False.
    Assume m and n are ints."""
    if abs(m-n)==1:
        return False
    return True

def all_different(variables) :
    """Returns a list of constraints, with one difference constraint between
    each pair of variables."""
    constraints=[]
    for index,var in enumerate(variables):
        for sub_index in range(index+1,len(variables)):
            var1=var
            var2=variables[sub_index]
            new_constraint=Constraint(var1,var2,constraint_different)
            constraints.append(new_constraint)
    return constraints
#### PART 8: MOOSE PROBLEM (OPTIONAL)

moose_problem = ConstraintSatisfactionProblem(["You", "Moose", "McCain",
                                               "Palin", "Obama", "Biden"])

# Add domains and constraints to your moose_problem here:


# To test your moose_problem AFTER implementing all the solve_constraint
# methods above, change TEST_MOOSE_PROBLEM to True:
TEST_MOOSE_PROBLEM = False


#### SURVEY ###################################################

NAME = ""
COLLABORATORS = ""
HOW_MANY_HOURS_THIS_LAB_TOOK = 0
WHAT_I_FOUND_INTERESTING = ""
WHAT_I_FOUND_BORING = ""
SUGGESTIONS = ""


###########################################################
### Ignore everything below this line; for testing only ###
###########################################################

if TEST_MOOSE_PROBLEM:
    # These lines are used in the local tester iff TEST_MOOSE_PROBLEM is True
    moose_answer_dfs = solve_constraint_dfs(moose_problem.copy())
    moose_answer_propany = solve_constraint_propagate_reduced_domains(moose_problem.copy())
    moose_answer_prop1 = solve_constraint_propagate_singleton_domains(moose_problem.copy())
    moose_answer_generic_dfs = solve_constraint_generic(moose_problem.copy(), None)
    moose_answer_generic_propany = solve_constraint_generic(moose_problem.copy(), condition_domain_reduction)
    moose_answer_generic_prop1 = solve_constraint_generic(moose_problem.copy(), condition_singleton)
    moose_answer_generic_fc = solve_constraint_generic(moose_problem.copy(), condition_forward_checking)
    moose_instance_for_domain_reduction = moose_problem.copy()
    moose_answer_domain_reduction = domain_reduction(moose_instance_for_domain_reduction)
    moose_instance_for_domain_reduction_singleton = moose_problem.copy()
    moose_answer_domain_reduction_singleton = domain_reduction_singleton_domains(moose_instance_for_domain_reduction_singleton)
