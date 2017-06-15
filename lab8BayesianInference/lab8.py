# MIT 6.034 Lab 8: Bayesian Inference
# Written by Dylan Holmes (dxh), Jessica Noss (jmn), and 6.034 staff

from nets import *


#### ANCESTORS, DESCENDANTS, AND NON-DESCENDANTS ###############################

def get_ancestors(net, var):
    "Return a set containing the ancestors of var"
    parents = list(net.get_parents(var))
    output = list(parents)
    for p in parents:
        output=output+list(get_ancestors(net,p))
    return set(output)

def get_descendants(net, var):
    "Returns a set containing the descendants of var"
    children = list(net.get_children(var))
    output = list(children)
    for c in children:
        output=output+list(get_descendants(net,c))
    return set(output)

def get_nondescendants(net, var):
    "Returns a set containing the non-descendants of var"
    vars=net.get_variables()
    childrens = get_descendants(net,var)
    output=[]
    for v in vars:
        if (not v in childrens) and (not v==var):
            output=output+[v]
    return set(output)

def simplify_givens(net, var, givens):
    """If givens include every parent of var and no descendants, returns a
    simplified list of givens, keeping only parents.  Does not modify original
    givens.  Otherwise, if not all parents are given, or if a descendant is
    given, returns original givens."""

    descendants=get_descendants(net,var)
    parents=net.get_parents(var)

    list_givens=[]
    for given in givens:
        if given in descendants:
            return givens
        list_givens = list_givens + [given]

    set_givens=set(list_givens)

    if parents.issubset(set_givens):
        new_dict={}
        for parent in parents:
            new_dict[parent]=givens[parent]
        if var in list_givens:
            new_dict[var]=givens[var]
        return new_dict
    return givens



#### PROBABILITY ###############################################################

def probability_lookup(net, hypothesis, givens=None):
    "Looks up a probability in the Bayes net, or raises LookupError"
    var=None
    for key in hypothesis:
        var = key
    if not givens is None:
        givens=simplify_givens(net, var, givens)
    try:
        return net.get_probability(hypothesis,givens)
    except:
        raise LookupError("Look up failed")


def probability_joint(net, hypothesis):
    "Uses the chain rule to compute a joint probability"
    P=1
    vars = []
    for key in hypothesis:
        vars= [key] + vars
    vars.sort(key= lambda var: len(get_descendants(net,var)))
    for var in vars:
        assertion = {}
        assertion[var]=hypothesis[var]
        del hypothesis[var]
        P*=probability_lookup(net,assertion,hypothesis)
    return P


def probability_marginal(net, hypothesis):
    "Computes a marginal probability as a sum of joint probabilities"
    P=0
    vars = list(net.get_variables())
    all = net.combinations(vars, constant_bindings=hypothesis)
    for item in all:
        P = P + probability_joint(net,item)
    return P

def probability_conditional(net, hypothesis, givens=None):
    "Computes a conditional probability as a ratio of marginal probabilities"

    try:
        return probability_lookup(net,hypothesis,givens)
    except:
        for key in hypothesis:
            try:
                if not hypothesis[key] == givens[key]:
                    return 0.0
            except:
                pass
        if not givens == None:
            return probability_marginal(net,dict(hypothesis,**givens))/probability_marginal(net,givens)
        return probability_marginal(net, hypothesis) / probability_marginal(net, givens)

def probability(net, hypothesis, givens=None):
    "Calls previous functions to compute any probability"
    return probability_conditional(net,hypothesis,givens)


#### PARAMETER-COUNTING AND INDEPENDENCE #######################################

def number_of_parameters(net):
    "Computes minimum number of parameters required for net"
    total=0
    vars = net.topological_sort()
    for var in vars:
        N = 1
        N=N*(len(net.get_domain(var))-1)
        parents=net.get_parents(var)
        for parent in parents:
            N=N*len(net.get_domain(parent))
        total+=N
    return total


def is_independent(net, var1, var2, givens=None):
    """Return True if var1, var2 are conditionally independent given givens,
    otherwise False.  Uses numerical independence."""
    domain1=net.get_domain(var1)
    domain2=net.get_domain(var2)
    for value1 in domain1:
        for value2 in domain2:
            if not givens == None:
                p12=probability(net,{var1:value1},dict(givens,**{var2:value2}))
            else:
                p12 = probability(net, {var1: value1}, {var2: value2})
            p1 = probability(net, {var1: value1}, givens)
            if not approx_equal(p12, p1, epsilon=0.0000000001):
                return False
    return True

def is_structurally_independent(net, var1, var2, givens=None):
    """Return True if var1, var2 are conditionally independent given givens,
    based on the structure of the Bayes net, otherwise False.
    Uses structural independence only (not numerical independence)."""
    all_vars=[var1,var2]+list(get_ancestors(net,var1))+list(get_ancestors(net,var2))
    try:
        for var in givens:
            all_vars=all_vars+[var]+list(get_ancestors(net,var))
    except:
        pass
    all_vars=set(all_vars)
    subnet=net.subnet(all_vars)
    subnet_copy=net.subnet(all_vars)
    for var in all_vars:
        parents=list(subnet_copy.get_parents(var))
        for i in range(len(parents)):
            for j in range(i+1,len(parents)):
                    subnet.link(parents[i],parents[j])
    subnet=subnet.make_bidirectional()
    try:
        for given in givens:
            subnet.remove_variable(given)
    except:
        pass
    path = subnet.find_path(var1,var2)
    if path==None:
        return True
    return False




#### SURVEY ####################################################################

NAME = ""
COLLABORATORS = ""
HOW_MANY_HOURS_THIS_LAB_TOOK = 0
WHAT_I_FOUND_INTERESTING = ""
WHAT_I_FOUND_BORING = ""
SUGGESTIONS = ""
