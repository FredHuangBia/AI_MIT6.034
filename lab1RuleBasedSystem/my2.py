# MIT 6.034 Lab 1: Rule-Based Systems
# Written by 6.034 staff

from production import IF, AND, OR, NOT, THEN, DELETE, forward_chain
from data import *

#### Part 1: Multiple Choice #########################################

ANSWER_1 = '2'

ANSWER_2 = '3'

ANSWER_3 = '2'

ANSWER_4 = '0'

ANSWER_5 = '3'

ANSWER_6 = '1'

ANSWER_7 = '0'

#### Part 2: Transitive Rule #########################################

transitive_rule = IF( AND( '(?x) beats (?y)',
                           '(?y) beats (?z)'),
                      THEN( '(?x) beats (?z)') )

# You can test your rule by uncommenting these print statements:
#print forward_chain([transitive_rule], abc_data)
#print forward_chain([transitive_rule], poker_data)
#print forward_chain([transitive_rule], minecraft_data)


#### Part 3: Family Relations #########################################

# Define your rules here:



# Add your rules to this list:
family_rules = [  IF( 'person (?x)',              #self
                      THEN( 'self (?x) (?x)' ) ),
                  IF( AND( 'parent (?x) (?y)',    #sibling
                           'parent (?x) (?z)',
                           NOT( 'self (?y) (?z)') ),
                      THEN( 'sibling (?y) (?z)',
                            'sibling (?z) (?y)') ),
                  IF( 'parent (?x) (?y)',         #child
                      THEN( 'child (?y) (?x)') ),
                  IF( AND( 'parent (?x) (?y)',    #sibling
                           'parent (?z) (?a)',
                           'sibling (?x) (?z)',
                           NOT( 'self (?a) (?y)'),
                           NOT( 'sibling (?y) (?a)'),
                           NOT( 'sibling (?a) (?y)') ),
                      THEN( 'cousin (?a) (?y)',
                            'cousin (?y) (?a)') ),
                  IF( AND( 'parent (?x) (?y)',   #grandparent
                           'parent (?y) (?z)'),
                      THEN( 'grandparent (?x) (?z)') ),
                  IF( 'grandparent (?x) (?y)',
                      THEN( 'grandchild (?y) (?x)' ) ) ]


# Uncomment this to test your data on the Simpsons family:
#print forward_chain(family_rules, simpsons_data, verbose=Fals)

# These smaller datasets might be helpful for debugging:
#print forward_chain(family_rules, sibling_test_data, verbose=True)
#print forward_chain(family_rules, grandparent_test_data, verbose=True)

# The following should generate 14 cousin relationships, representing 7 pairs
# of people who are cousins:
black_family_cousins = [
    relation for relation in
    forward_chain(family_rules, black_data, verbose=False)
    if "cousin" in relation ]

# To see if you found them all, uncomment this line:
#print black_family_cousins


#### Part 4: Backward Chaining #########################################

# Import additional methods for backchaining
from production import PASS, FAIL, match, populate, simplify, variables



def backchain_to_goal_tree(rules, hypothesis):
    #hypothesis is a string
    #rules is a tuple
    #rules[i] is production.IF
    #rules[i].antecedent() is iterable, each is a string
    #the samle is rules[i].consequent
    #AND('','') OR('','') and and or objects
    """
    Takes a hypothesis (string) and a list of rules (list
    of IF objects), returning an AND/OR tree representing the
    backchain of possible statements we may need to test
    to determine if this hypothesis is reachable or not.

    This method should return an AND/OR tree, that is, an
    AND or OR object, whose constituents are the subgoals that
    need to be tested. The leaves of this tree should be strings
    (possibly with unbound variables), *not* AND or OR objects.
    Make sure to use simplify(...) to flatten trees where appropriate.
    """

    result=OR(hypothesis)
    for rule in rules:  #rule is IF
        for consequent in rule.consequent(): #consequent is string
            if match(consequent,hypothesis)!=None:
                table = match(consequent,hypothesis)
                if isinstance(rule.antecedent(),str):
                    result.append(backchain_to_goal_tree(rules,populate(rule.antecedent(),table)))
                elif isinstance(rule.antecedent(),OR):
                    temp=OR()
                    for antecedent in rule.antecedent():
                        temp.append(backchain_to_goal_tree(rules,populate(antecedent,table)))
                    result.append( temp)
                else:
                    temp=AND()
                    for antecedent in rule.antecedent():
                        temp.append(backchain_to_goal_tree(rules,populate(antecedent,table)))
                    result.append( temp)
    return simplify(result)


# Uncomment this to run your backward chainer:
print backchain_to_goal_tree(zookeeper_rules, 'opus is a penguin')



#### Survey #########################################

NAME = None
COLLABORATORS = None
HOW_MANY_HOURS_THIS_LAB_TOOK = None
WHAT_I_FOUND_INTERESTING = ""
WHAT_I_FOUND_BORING = ""
SUGGESTIONS = None


###########################################################
### Ignore everything below this line; for testing only ###
###########################################################

# The following lines are used in the tester. DO NOT CHANGE!
#transitive_rule_poker = forward_chain([transitive_rule], poker_data)
#transitive_rule_abc = forward_chain([transitive_rule], abc_data)
#transitive_rule_minecraft = forward_chain([transitive_rule], minecraft_data)
#family_rules_simpsons = forward_chain(family_rules, simpsons_data)
#family_rules_black = forward_chain(family_rules, black_data)
#family_rules_sibling = forward_chain(family_rules, sibling_test_data)
#family_rules_grandparent = forward_chain(family_rules, grandparent_test_data)
#family_rules_anonymous_family = forward_chain(family_rules, anonymous_family_test_data)
