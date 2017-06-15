# MIT 6.034 Lab 9: Boosting (Adaboost)
# Written by Jessica Noss (jmn), Dylan Holmes (dxh), and 6.034 staff

from math import log as ln
from utils import *


#### BOOSTING (ADABOOST) #######################################################

def initialize_weights(training_points):
    """Assigns every training point a weight equal to 1/N, where N is the number
    of training points.  Returns a dictionary mapping points to weights."""
    N = len(training_points)
    init_weight = make_fraction(1,N)
    output = {}
    for point in training_points:
        output[point] = init_weight
    return  output


def calculate_error_rates(point_to_weight, classifier_to_misclassified):
    """Given a dictionary mapping training points to their weights, and another
    dictionary mapping classifiers to the training points they misclassify,
    returns a dictionary mapping classifiers to their error rates."""
    output={}
    for classifier in classifier_to_misclassified:
        output[classifier]=make_fraction(0)
        for mis_classify in classifier_to_misclassified[classifier]:
            output[classifier]+=point_to_weight[mis_classify]
    return  output

def pick_best_classifier(classifier_to_error_rate, use_smallest_error=True):
    """Given a dictionary mapping classifiers to their error rates, returns the
    best* classifier, or raises NoGoodClassifiersError if best* classifier has
    error rate 1/2.  best* means 'smallest error rate' if use_smallest_error
    is True, otherwise 'error rate furthest from 1/2'."""
    if use_smallest_error:
        a=sorted(classifier_to_error_rate, key= lambda x: (classifier_to_error_rate[x],x))[0]
        if classifier_to_error_rate[a]==make_fraction(1,2):
            raise NoGoodClassifiersError("")
        return a
    else:
        a = sorted(classifier_to_error_rate, key=lambda x: (-abs(classifier_to_error_rate[x]-make_fraction(1,2)), x))[0]
        if classifier_to_error_rate[a]==make_fraction(1,2):
            raise NoGoodClassifiersError("")
        return a


def calculate_voting_power(error_rate):
    """Given a classifier's error rate (a number), returns the voting power
    (aka alpha, or coefficient) for that classifier."""
    if error_rate==make_fraction(0):
        return INF
    elif error_rate==make_fraction(1):
        return -INF
    return 0.5*ln((1-error_rate)/float(error_rate))

def get_overall_misclassifications(H, training_points, classifier_to_misclassified):
    """Given an overall classifier H, a list of all training points, and a
    dictionary mapping classifiers to the training points they misclassify,
    returns a set containing the training points that H misclassifies.
    H is represented as a list of (classifier, voting_power) tuples."""
    mis=[]
    for point in training_points:
        value=make_fraction(0)
        for classifier in H:
            if point in classifier_to_misclassified[classifier[0]]:
                value-=classifier[1]
            else:
                value+=classifier[1]
        if value<=make_fraction(0):
            mis.append(point)
    return set(mis)





def is_good_enough(H, training_points, classifier_to_misclassified, mistake_tolerance=0):
    """Given an overall classifier H, a list of all training points, a
    dictionary mapping classifiers to the training points they misclassify, and
    a mistake tolerance (the maximum number of allowed misclassifications),
    returns False if H misclassifies more points than the tolerance allows,
    otherwise True.  H is represented as a list of (classifier, voting_power)
    tuples."""
    return len(get_overall_misclassifications(H,training_points,classifier_to_misclassified))<=mistake_tolerance


def update_weights(point_to_weight, misclassified_points, error_rate):
    """Given a dictionary mapping training points to their old weights, a list
    of training points misclassified by the current weak classifier, and the
    error rate of the current weak classifier, returns a dictionary mapping
    training points to their new weights.  This function is allowed (but not
    required) to modify the input dictionary point_to_weight."""
    for point in point_to_weight:
        if point in misclassified_points:
            point_to_weight[point] = point_to_weight[point]*make_fraction(1,2)*make_fraction(1,error_rate)
        else:
            point_to_weight[point] = point_to_weight[point] * make_fraction(1, 2) * make_fraction(1, 1-error_rate)
    return point_to_weight

def adaboost(training_points, classifier_to_misclassified,
             use_smallest_error=True, mistake_tolerance=0, max_rounds=INF):
    """Performs the Adaboost algorithm for up to max_rounds rounds.
    Returns the resulting overall classifier H, represented as a list of
    (classifier, voting_power) tuples."""
    H=[]
    point_to_weight=initialize_weights(training_points)
    round=0
    while (not is_good_enough(H,training_points,classifier_to_misclassified,mistake_tolerance)) and round<max_rounds:
        round+=1
        classifier_to_error_rate=calculate_error_rates(point_to_weight,classifier_to_misclassified)
        try:
            best_classifier=pick_best_classifier(classifier_to_error_rate,use_smallest_error)
        except:
            return H
        misclassified_points=classifier_to_misclassified[best_classifier]
        error_rate=classifier_to_error_rate[best_classifier]
        voting_power=calculate_voting_power(error_rate)
        H.append((best_classifier,voting_power))
        point_to_weight=update_weights(point_to_weight,misclassified_points,error_rate)
    return H



#### SURVEY ####################################################################

NAME = ""
COLLABORATORS = ""
HOW_MANY_HOURS_THIS_LAB_TOOK = 0
WHAT_I_FOUND_INTERESTING = ""
WHAT_I_FOUND_BORING = ""
SUGGESTIONS = "I will miss professor Winston"
