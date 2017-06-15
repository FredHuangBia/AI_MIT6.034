# MIT 6.034 Lab 3: Games
# Written by Dylan Holmes (dxh), Jessica Noss (jmn), and 6.034 staff

from game_api import *
from boards import *
INF = float('inf')

def is_game_over_connectfour(board) :
    "Returns True if game is over, otherwise False."
    if board.count_pieces(current_player=None)==board.num_rows*board.num_cols:
        return True
    else:
        for chain in board.get_all_chains(current_player=None):
            if len(chain) >=4:
                return True
        return False

def next_boards_connectfour(board) :
    """Returns a list of ConnectFourBoard objects that could result from the
    next move, or an empty list if no moves can be made."""
    new_boards=[]
    if is_game_over_connectfour(board):
        return new_boards
    else:
        for i in range(7):
            if not board.is_column_full(i):
                new_boards.append(board.add_piece(i))
        return new_boards

def endgame_score_connectfour(board, is_current_player_maximizer) :
    """Given an endgame board, returns 1000 if the maximizer has won,
    -1000 if the minimizer has won, or 0 in case of a tie."""
    for chain in board.get_all_chains(current_player=False):
        if len(chain)>=4:
            if is_current_player_maximizer:
                return -1000
            else:
                return 1000
    return 0

def endgame_score_connectfour_faster(board, is_current_player_maximizer) :
    """Given an endgame board, returns an endgame score with abs(score) >= 1000,
    returning larger absolute scores for winning sooner."""
    for chain in board.get_all_chains(current_player=False):
        if len(chain)>=4:
            if is_current_player_maximizer:
                return -1000-10*(42-board.count_pieces(current_player=None))
            else:
                return 1000+10*(42-board.count_pieces(current_player=None))
    return 0

def heuristic_connectfour(board, is_current_player_maximizer) :
    """Given a non-endgame board, returns a heuristic score with
    abs(score) < 1000, where higher numbers indicate that the board is better
    for the maximizer."""
    three_maximizer=0
    two_maximizer=0
    three_minimizer=0
    two_minimizer=0
    maximizer=[]
    minimizer=[]
    if is_current_player_maximizer:
        maximizer=board.get_all_chains(current_player=True)
        minimizer=board.get_all_chains(current_player=False)
    elif not is_current_player_maximizer:
        maximizer=board.get_all_chains(current_player=False)
        minimizer=board.get_all_chains(current_player=True)
    for chain in maximizer:
        if len(chain)==3:
            three_maximizer+=1
        elif len(chain)==2:
            two_maximizer+=1
    for chain in minimizer:
        if len(chain)==3:
            three_minimizer+=1
        elif len(chain)==2:
            two_minimizer+=1
    score = 100*(three_maximizer-three_minimizer)+50*(two_maximizer-two_minimizer)
    if score >500:
        score=500
    elif score <-500:
        score=-500
    return score

# Now we can create AbstractGameState objects for Connect Four, using some of
# the functions you implemented above.  You can use the following examples to
# test your dfs and minimax implementations in Part 2.

# This AbstractGameState represents a new ConnectFourBoard, before the game has started:
state_starting_connectfour = AbstractGameState(snapshot = ConnectFourBoard(),
                                 is_game_over_fn = is_game_over_connectfour,
                                 generate_next_states_fn = next_boards_connectfour,
                                 endgame_score_fn = endgame_score_connectfour_faster)

# This AbstractGameState represents the ConnectFourBoard "NEARLY_OVER" from boards.py:
state_NEARLY_OVER = AbstractGameState(snapshot = NEARLY_OVER,
                                 is_game_over_fn = is_game_over_connectfour,
                                 generate_next_states_fn = next_boards_connectfour,
                                 endgame_score_fn = endgame_score_connectfour_faster)

# This AbstractGameState represents the ConnectFourBoard "BOARD_UHOH" from boards.py:
state_UHOH = AbstractGameState(snapshot = BOARD_UHOH,
                                 is_game_over_fn = is_game_over_connectfour,
                                 generate_next_states_fn = next_boards_connectfour,
                                 endgame_score_fn = endgame_score_connectfour_faster)

#### PART 2 ###########################################
# Note: Functions in Part 2 use the AbstractGameState API, not ConnectFourBoard.

def dfs_maximizing(state) :
    """Performs depth-first search to find path with highest endgame score.
    Returns a tuple containing:
     0. the best path (a list of AbstractGameState objects),
     1. the score of the leaf node (a number), and
     2. the number of static evaluations performed (a number)"""

    """if state.is_game_over():
        return ([state], state.get_endgame_score(is_current_player_maximizer=False),1) # maximizer = False here, interesting
    else:
        new_states=state.generate_next_states()
        new_states=sorted(new_states, key = lambda new_state : dfs_maximizing(new_state)[1],reverse = True)
        statistic=0
        for i in new_states:
            statistic+=dfs_maximizing(i)[2]
        return ([state]+dfs_maximizing(new_states[0])[0], dfs_maximizing(new_states[0])[1], statistic)"""
    if state.is_game_over():
        return ([state], state.get_endgame_score(is_current_player_maximizer=False),1)
    else:
        maxvalue=-INF
        maxstate=None
        statistic=0
        for new_state in state.generate_next_states():
            tem=dfs_maximizing(new_state)
            statistic+=tem[2]
            if maxvalue < tem[1]:
                maxstate=new_state
                maxvalue=tem[1]
        return ([state]+dfs_maximizing(maxstate)[0], dfs_maximizing(maxstate)[1], statistic)



def minimax_endgame_search(state, maximize=True) :
    """Performs minimax search, searching all leaf nodes and statically
    evaluating all endgame scores.  Same return type as dfs_maximizing."""
    if state.is_game_over():
        return ([state], state.get_endgame_score(is_current_player_maximizer=maximize),1)
    else:
        if maximize:
            maxvalue=-INF
            maxstate=None
            statistic=0
            for new_state in state.generate_next_states():
                tem=minimax_endgame_search(new_state, not maximize)
                statistic+=tem[2]
                if maxvalue < tem[1]:
                    maxstate=new_state
                    maxvalue=tem[1]
            return ([state]+minimax_endgame_search(maxstate, not maximize)[0], minimax_endgame_search(maxstate, not maximize)[1], statistic)
        else:
            minvalue=INF
            minstate=None
            statistic=0
            for new_state in state.generate_next_states():
                tem=minimax_endgame_search(new_state, not maximize)
                statistic+=tem[2]
                if minvalue > tem[1]:
                    minstate=new_state
                    minvalue=tem[1]
            return ([state]+minimax_endgame_search(minstate, not maximize)[0], minimax_endgame_search(minstate, not maximize)[1], statistic)


# Uncomment the line below to try your minimax_endgame_search on an
# AbstractGameState representing the ConnectFourBoard "NEARLY_OVER" from boards.py:

#pretty_print_dfs_type(minimax_endgame_search(state_NEARLY_OVER))


def minimax_search(state, heuristic_fn=always_zero, depth_limit=INF, maximize=True) :
    "Performs standard minimax search.  Same return type as dfs_maximizing."
    if state.is_game_over():
        return ([state], state.get_endgame_score(is_current_player_maximizer=maximize),1)
    elif depth_limit==0:
        return ([state], heuristic_fn(state.get_snapshot(),maximize),1)
    else:
        if maximize:
            maxvalue=-INF
            maxstate=None
            statistic=0
            for new_state in state.generate_next_states():
                tem=minimax_search(new_state, heuristic_fn, depth_limit-1,not maximize)
                statistic+=tem[2]
                if maxvalue < tem[1]:
                    maxstate=new_state
                    maxvalue=tem[1]
            return ([state]+minimax_search(maxstate, heuristic_fn, depth_limit-1, not maximize)[0],
            minimax_search(maxstate, heuristic_fn, depth_limit-1, not maximize)[1],
            statistic)
        else:
            minvalue=INF
            minstate=None
            statistic=0
            for new_state in state.generate_next_states():
                tem=minimax_search(new_state, heuristic_fn, depth_limit-1,not maximize)
                statistic+=tem[2]
                if minvalue > tem[1]:
                    minstate=new_state
                    minvalue=tem[1]
            return ([state]+minimax_search(minstate, heuristic_fn, depth_limit-1, not maximize)[0],
            minimax_search(minstate, heuristic_fn, depth_limit-1, not maximize)[1],
            statistic)


# Uncomment the line below to try minimax_search with "BOARD_UHOH" and
# depth_limit=1.  Try increasing the value of depth_limit to see what happens:

#pretty_print_dfs_type(minimax_search(state_UHOH, heuristic_fn=heuristic_connectfour, depth_limit=1))


def minimax_search_alphabeta(state, alpha=-INF, beta=INF, heuristic_fn=always_zero,
                             depth_limit=INF, maximize=True) :
    "Performs minimax with alpha-beta pruning.  Same return type as dfs_maximizing."
    #print alpha
    #print beta
    if state.is_game_over():
        return ([state], state.get_endgame_score(is_current_player_maximizer= maximize),1)
    elif depth_limit==0:
        return ([state], heuristic_fn(state.get_snapshot(), maximize),1)
    else:
        if maximize:
            return_states=[]
            #alpha = -INF
            maxstate=None
            statistic=0
            for new_state in state.generate_next_states():
                tem=minimax_search_alphabeta(new_state, alpha, beta, heuristic_fn, depth_limit-1,not maximize)
                statistic += tem[2]
                if tem[1]>alpha:
                    maxstate=new_state
                    alpha=tem[1]
                    return_states=[state]+tem[0]
                #alpha=max(alpha,v)
                if alpha >= beta:
                    return(return_states
                    ,alpha,statistic)
            return (return_states,
            alpha,
            statistic)
        else:
            return_states=[]
            #beta = INF
            minstate=None
            statistic=0
            for new_state in state.generate_next_states():
                tem=minimax_search_alphabeta(new_state, alpha, beta, heuristic_fn, depth_limit-1, not maximize)
                statistic+=tem[2]
                if tem[1] < beta:
                    beta=tem[1]
                    minstate=new_state
                    return_states=[state]+tem[0]
                #beta=min(v,beta)
                if beta <= alpha:
                    return (return_states
                    ,beta,statistic)
            return (return_states,
            beta,
            statistic)


# Uncomment the line below to try minimax_search_alphabeta with "BOARD_UHOH" and
# depth_limit=4.  Compare with the number of evaluations from minimax_search for
# different values of depth_limit.

#pretty_print_dfs_type(minimax_search_alphabeta(state_UHOH, heuristic_fn=heuristic_connectfour, depth_limit=4, maximize=False))


def progressive_deepening(state, heuristic_fn=always_zero, depth_limit=INF,
                          maximize=True) :
    """Runs minimax with alpha-beta pruning. At each level, updates anytime_value
    with the tuple returned from minimax_search_alphabeta. Returns anytime_value."""
    anytime_value = AnytimeValue()   # TA Note: Use this to store values.
    for i in range(depth_limit+1):
        if i>0:
            result=minimax_search_alphabeta(state,heuristic_fn=heuristic_fn, depth_limit=i, maximize=maximize)
            anytime_value.set_value(result)
    return anytime_value

# Uncomment the line below to try progressive_deepening with "BOARD_UHOH" and
# depth_limit=4.  Compare the total number of evaluations with the number of
# evaluations from minimax_search or minimax_search_alphabeta.

#print progressive_deepening(state_UHOH, heuristic_fn=heuristic_connectfour, depth_limit=4)


##### PART 3: Multiple Choice ##################################################

ANSWER_1 = '4'

ANSWER_2 = '1'

ANSWER_3 = '4'

ANSWER_4 = '5'

#pretty_print_dfs_type(dfs_maximizing(state_NEARLY_OVER))
#### SURVEY ###################################################

NAME = ''
COLLABORATORS = ''
HOW_MANY_HOURS_THIS_LAB_TOOK = 0
WHAT_I_FOUND_INTERESTING = ''
WHAT_I_FOUND_BORING = ''
SUGGESTIONS = ''
