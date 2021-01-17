import random
import tkinter
import datetime
import math
from datetime import time, date, datetime
from tkinter import *



def get_init_matr(N, M):
    matrix = [[0 for _ in range(M)] for _ in range(N)]
    return matrix


def is_out_of_bounds(move, N, M):
    if move[0] >= N or move[0] < 0 or move[1] >= M or move[1] < 0:
        return True
    return False


def is_candidate_move(board, move, N, M, border_max_size):
    # if move is unavailable
    if board[move[0]][move[1]] != 0:
        return False
    # look for checker in size 2 proximity matrix
    for border_size in range(1, border_max_size):
        # vertical search
        for i in range(move[0] - border_size, move[0] + border_size + 1):
            for direction in [-1, 1]:
                if not is_out_of_bounds((i, move[1] + direction * border_size), N, M):
                    if board[i][move[1] + direction * border_size] != 0:
                        return True
        # horizontal search
        for j in range(move[1] - border_size + 1, move[1] + border_size):
            for direction in [-1, 1]:
                if not is_out_of_bounds((move[0] + direction * border_size, j), N, M):
                    if board[move[0] + direction * border_size][j] != 0:
                        return True
    # False if no checker was found in 2-proximity
    return False


def get_all_candidate_moves(board, N, M, border_max_size):
    all_moves = []
    for i in range(N):
        for j in range(M):
            if is_candidate_move(board, (i, j), N, M, border_max_size):
                all_moves.append([i, j])
    return all_moves


def update_all_moves(all_moves, move):
    all_moves.remove(move)


def make_move(board, turn, move):
    if board[move[0]][move[1]] != 0:
        return False
    board[move[0]][move[1]] = turn

    return True


def undo_move(board, move):
    board[move[0]][move[1]] = 0


def get_streak_state(board, N, M, move, streak_len, direction, turn):
    opponent_count = 0
    i = move[0]
    j = move[1]

    if 0 <= j < M and 0 <= i < N:
        # if there is opponent checker at streak end -> increase count
        if board[i][j] == -turn:
            opponent_count += 1
    # if streak end on board margin
    else:
        opponent_count += 1

    if direction == "left":
        if j - streak_len - 1 >= 0:
            # check if there is opponent checker at streak beginning -> increase count
            if board[i][j - streak_len - 1] == -turn:
                opponent_count += 1
        else:  # if streak starts on board margin
            opponent_count += 1

    if direction == "up":
        if i - streak_len - 1 >= 0:
            if board[i - streak_len - 1][j] == -turn:
                opponent_count += 1
        else:  # if streak starts on board margin
            opponent_count += 1

    if direction == "S-W":
        if i + streak_len + 1 < N and j - streak_len - 1 >= 0:
            if board[i + streak_len + 1][j - streak_len - 1] == -turn:
                opponent_count += 1
        else:
            opponent_count += 1

    if direction == "S-E":
        if i + streak_len + 1 < N and j + streak_len + 1 < M:
            if board[i + streak_len + 1][j + streak_len + 1] == -turn:
                opponent_count += 1
        else:
            opponent_count += 1

    if opponent_count == 0:
        return "open"
    elif opponent_count == 1:
        return "semi-open"
    return "closed"


def stronger_heur2(board, N, M, win_streak):
    if is_game_over(board, 1, win_streak, N, M):
        return -math.inf
    elif is_game_over(board, -1, win_streak, N, M):
        return math.inf
    heur = 0

    for i in range(N):
        ai_horizontal_streak = 0
        human_horizontal_streak = 0
        ai_vertical_streak = 0
        human_vertical_streak = 0
        for j in range(M):
            # current horizontal streak is continued with one checker
            if board[i][j] == -1:
                ai_horizontal_streak += 1
            # current horizontal streak is discontinued
            else:
                # reward streak with length - 1
                if ai_horizontal_streak > 1:
                    streak_state = get_streak_state(board, N, M, (i, j), ai_horizontal_streak, "left", -1)
                    if streak_state == "open":
                        heur += pow(ai_horizontal_streak, 2)
                    elif streak_state == "semi-open":
                        heur += pow(ai_horizontal_streak / 2, 2)
                # reset streak
                ai_horizontal_streak = 0

            # current vertical streak is continued with one checker
            if board[j][i] == -1:
                ai_vertical_streak += 1
            # current vertical streak is discontinued
            else:
                # reward streak with length - 1
                if ai_vertical_streak > 1:
                    streak_state = get_streak_state(board, N, M, (j, i), ai_vertical_streak, "up", -1)
                    if streak_state == "open":
                        heur += pow(ai_vertical_streak, 2)
                    elif streak_state == "semi-open":
                        heur += pow(ai_vertical_streak / 2, 2)
                # reset streak
                ai_vertical_streak = 0

            # current human horizontal streak is continued with one checker
            if board[i][j] == 1:
                human_horizontal_streak += 1
            # current human horizontal streak is discontinued
            else:
                # reward streak with -(length - 1)
                if human_horizontal_streak > 1:
                    streak_state = get_streak_state(board, N, M, (i, j), human_horizontal_streak, "left", 1)
                    if streak_state == "open":
                        heur -= pow(human_horizontal_streak, 2)
                    elif streak_state == "semi-open":
                        heur -= pow(human_horizontal_streak / 2, 2)
                # reset streak
                human_horizontal_streak = 0

            # current human vertical streak is continued with one checker
            if board[j][i] == 1:
                human_vertical_streak += 1
            # current human vertical streak is discontinued
            else:
                # reward streak with -(length - 1)
                if human_vertical_streak > 1:
                    streak_state = get_streak_state(board, N, M, (j, i), human_vertical_streak, "up", 1)
                    if streak_state == "open":
                        heur -= pow(human_vertical_streak, 2)
                    elif streak_state == "semi-open":
                        heur -= pow(human_vertical_streak / 2, 2)
                # reset streak
                human_vertical_streak = 0
        if ai_horizontal_streak > 1:
            streak_state = get_streak_state(board, N, M, (i, M), ai_horizontal_streak, "left", -1)
            if streak_state == "open":
                heur += pow(ai_horizontal_streak, 2)
            elif streak_state == "semi-open":
                heur += pow(ai_horizontal_streak / 2, 2)
        if ai_vertical_streak > 1:
            streak_state = get_streak_state(board, N, M, (N, i), ai_vertical_streak, "up", -1)
            if streak_state == "open":
                heur += pow(ai_vertical_streak, 2)
            elif streak_state == "semi-open":
                heur += pow(ai_vertical_streak / 2, 2)
        if human_horizontal_streak > 1:
            streak_state = get_streak_state(board, N, M, (i, M), human_horizontal_streak, "left", 1)
            if streak_state == "open":
                heur -= pow(human_horizontal_streak, 2)
            elif streak_state == "semi-open":
                heur -= pow(human_horizontal_streak / 2, 2)
        if human_vertical_streak > 1:
            streak_state = get_streak_state(board, N, M, (N, i), human_vertical_streak, "up", 1)
            if streak_state == "open":
                heur -= pow(human_vertical_streak, 2)
            elif streak_state == "semi-open":
                heur -= pow(human_vertical_streak / 2, 2)


    for i in range(N):
        ai_diag2_streak = 0
        human_diag2_streak = 0
        ai_diag_streak = 0
        human_diag_streak = 0
        l = i
        c = 0
        while l >= 0 and c < M:
            if board[l][c] == -1:
                ai_diag2_streak += 1
            else:
                if ai_diag2_streak > 1:
                    streak_state = get_streak_state(board, N, M, (l, c), ai_diag2_streak, "S-W", -1)
                    if streak_state == "open":
                        heur += pow(ai_diag2_streak, 2)
                    elif streak_state == "semi-open":
                        heur += pow(ai_diag2_streak / 2, 2)
                    # reset streak
                ai_diag2_streak = 0

            if board[l][c] == 1:
                human_diag2_streak += 1
            else:
                if human_diag2_streak > 1:
                    streak_state = get_streak_state(board, N, M, (l, c), human_diag2_streak, "S-W", 1)
                    if streak_state == "open":
                        heur -= pow(human_diag2_streak, 2)
                    elif streak_state == "semi-open":
                        heur -= pow(human_diag2_streak / 2, 2)
                    # reset streak
                human_diag2_streak = 0

            if board[l][M - c - 1] == -1:
                ai_diag_streak += 1
            else:
                if ai_diag_streak > 1:
                    streak_state = get_streak_state(board, N, M, (l, c), ai_diag_streak, "S-E", -1)
                    if streak_state == "open":
                        heur += pow(ai_diag_streak, 2)
                    elif streak_state == "semi-open":
                        heur += pow(ai_diag_streak / 2, 2)
                    # reset streak
                ai_diag_streak = 0

            if board[l][M - c - 1] == 1:
                human_diag_streak += 1
            else:
                if human_diag_streak > 1:
                    streak_state = get_streak_state(board, N, M, (l, c), human_diag_streak, "S-E", 1)
                    if streak_state == "open":
                        heur -= pow(human_diag_streak, 2)
                    elif streak_state == "semi-open":
                        heur -= pow(human_diag_streak/2, 2)
                    # reset streak
                human_diag_streak = 0
            c += 1
            l -= 1

        if ai_diag2_streak > 1:
            streak_state = get_streak_state(board, N, M, (l, c), ai_diag2_streak, "S-W", -1)
            if streak_state == "open":
                heur += pow(ai_diag2_streak, 2)
            elif streak_state == "semi-open":
                heur += pow(ai_diag2_streak / 2, 2)
        if human_diag2_streak > 1:
            streak_state = get_streak_state(board, N, M, (l, c), human_diag2_streak, "S-W", 1)
            if streak_state == "open":
                heur -= pow(human_diag2_streak, 2)
            elif streak_state == "semi-open":
                heur -= pow(human_diag2_streak / 2, 2)
        if ai_diag_streak > 1:
            streak_state = get_streak_state(board, N, M, (l, M - c - 1), ai_diag_streak, "S-E", -1)
            if streak_state == "open":
                heur += pow(ai_diag_streak, 2)
            elif streak_state == "semi-open":
                heur += pow(ai_diag_streak / 2, 2)
        if human_diag_streak > 1:
            streak_state = get_streak_state(board, N, M, (l,M - c - 1), human_diag_streak, "S-E", 1)
            if streak_state == "open":
                heur -= pow(human_diag_streak, 2)
            elif streak_state == "semi-open":
                heur -= pow(human_diag_streak / 2, 2)
    return heur

def stronger_heur(board, N, M, win_streak):
    if is_game_over(board, 1, win_streak, N, M):
        return -math.inf
    elif is_game_over(board, -1, win_streak, N, M):
        return math.inf

    heur = 0
    for i in range(N):
        ai_horizontal_streak = 0
        human_horizontal_streak = 0
        ai_vertical_streak = 0
        human_vertical_streak = 0
        for j in range(M):
            # current horizontal streak is continued with one checker
            if board[i][j] == -1:
                ai_horizontal_streak += 1
            # current horizontal streak is discontinued
            else:
                # reward streak with length - 1
                if ai_horizontal_streak > 1:
                    streak_state = get_streak_state(board, N, M, (i, j), ai_horizontal_streak, "left", -1)
                    if streak_state == "open":
                        heur += pow(10, ai_horizontal_streak)
                    elif streak_state == "semi-open":
                        heur += pow(10, ai_horizontal_streak - 1)
                    # heur += ai_horizontal_streak - 1
                # reset streak
                ai_horizontal_streak = 0

            # current vertical streak is continued with one checker
            if board[j][i] == -1:
                ai_vertical_streak += 1
            # current vertical streak is discontinued
            else:
                # reward streak with length - 1
                if ai_vertical_streak > 1:
                    streak_state = get_streak_state(board, N, M, (j, i), ai_vertical_streak, "up", -1)
                    if streak_state == "open":
                        heur += pow(10, ai_vertical_streak)
                    elif streak_state == "semi-open":
                        heur += pow(10, ai_vertical_streak - 1)
                # reset streak
                ai_vertical_streak = 0

            # current human horizontal streak is continued with one checker
            if board[i][j] == 1:
                human_horizontal_streak += 1
            # current human horizontal streak is discontinued
            else:
                # reward streak with -(length - 1)
                if human_horizontal_streak > 1:
                    streak_state = get_streak_state(board, N, M, (i, j), human_horizontal_streak, "left", 1)
                    if streak_state == "open":
                        heur -= pow(10, human_horizontal_streak)
                    elif streak_state == "semi-open":
                        heur -= pow(10, human_horizontal_streak - 1)
                # reset streak
                human_horizontal_streak = 0

            # current human vertical streak is continued with one checker
            if board[j][i] == 1:
                human_vertical_streak += 1
            # current human vertical streak is discontinued
            else:
                # reward streak with -(length - 1)
                if human_vertical_streak > 1:
                    streak_state = get_streak_state(board, N, M, (j, i), human_vertical_streak, "up", 1)
                    if streak_state == "open":
                        heur -= pow(10, human_vertical_streak)
                    elif streak_state == "semi-open":
                        heur -= pow(10, human_vertical_streak - 1)
                # reset streak
                human_vertical_streak = 0
        if ai_horizontal_streak > 1:
            streak_state = get_streak_state(board, N, M, (i, M), ai_horizontal_streak, "left", -1)
            if streak_state == "open":
                heur += pow(10, ai_horizontal_streak)
            elif streak_state == "semi-open":
                heur += pow(10, ai_horizontal_streak - 1)
        if ai_vertical_streak > 1:
            streak_state = get_streak_state(board, N, M, (N, i), ai_vertical_streak, "up", -1)
            if streak_state == "open":
                heur += pow(10, ai_vertical_streak)
            elif streak_state == "semi-open":
                heur += pow(10, ai_vertical_streak - 1)
        if human_horizontal_streak > 1:
            streak_state = get_streak_state(board, N, M, (i, M), human_horizontal_streak, "left", 1)
            if streak_state == "open":
                heur -= pow(10, human_horizontal_streak)
            elif streak_state == "semi-open":
                heur -= pow(10, human_horizontal_streak - 1)
        if human_vertical_streak > 1:
            streak_state = get_streak_state(board, N, M, (N, i), human_vertical_streak, "up", 1)
            if streak_state == "open":
                heur -= pow(10, human_vertical_streak)
            elif streak_state == "semi-open":
                heur -= pow(10, human_vertical_streak - 1)


    for i in range(N):
        ai_diag2_streak = 0
        human_diag2_streak = 0
        ai_diag_streak = 0
        human_diag_streak = 0
        l = i
        c = 0
        while l >= 0 and c < M:
            if board[l][c] == -1:
                ai_diag2_streak += 1
            else:
                if ai_diag2_streak > 1:
                    streak_state = get_streak_state(board, N, M, (l, c), ai_diag2_streak, "S-W", -1)
                    if streak_state == "open":
                        heur += pow(10, ai_diag2_streak)
                    elif streak_state == "semi-open":
                        heur += pow(10, ai_diag2_streak - 1)
                    # reset streak
                ai_diag2_streak = 0

            if board[l][c] == 1:
                human_diag2_streak += 1
            else:
                if human_diag2_streak > 1:
                    streak_state = get_streak_state(board, N, M, (l, c), human_diag2_streak, "S-W", 1)
                    if streak_state == "open":
                        heur -= pow(10, human_diag2_streak)
                    elif streak_state == "semi-open":
                        heur -= pow(10, human_diag2_streak - 1)
                    # reset streak
                human_diag2_streak = 0

            if board[l][M - c - 1] == -1:
                ai_diag_streak += 1
            else:
                if ai_diag_streak > 1:
                    streak_state = get_streak_state(board, N, M, (l, c), ai_diag_streak, "S-E", -1)
                    if streak_state == "open":
                        heur += pow(10, ai_diag_streak)
                    elif streak_state == "semi-open":
                        heur += pow(10, ai_diag_streak - 1)
                    # reset streak
                ai_diag_streak = 0

            if board[l][M - c - 1] == 1:
                human_diag_streak += 1
            else:
                if human_diag_streak > 1:
                    streak_state = get_streak_state(board, N, M, (l, c), human_diag_streak, "S-E", 1)
                    if streak_state == "open":
                        heur -= pow(10, human_diag_streak)
                    elif streak_state == "semi-open":
                        heur -= pow(10, human_diag_streak - 1)
                    # reset streak
                human_diag_streak = 0
            c += 1
            l -= 1

        if ai_diag2_streak > 1:
            streak_state = get_streak_state(board, N, M, (l, c), ai_diag2_streak, "S-W", -1)
            if streak_state == "open":
                heur += pow(10, ai_diag2_streak)
            elif streak_state == "semi-open":
                heur += pow(10, ai_diag2_streak - 1)
        if human_diag2_streak > 1:
            streak_state = get_streak_state(board, N, M, (l, c), human_diag2_streak, "S-W", 1)
            if streak_state == "open":
                heur -= pow(10, human_diag2_streak)
            elif streak_state == "semi-open":
                heur -= pow(10, human_diag2_streak - 1)
        if ai_diag_streak > 1:
            streak_state = get_streak_state(board, N, M, (l, M - c - 1), ai_diag_streak, "S-E", -1)
            if streak_state == "open":
                heur += pow(10, ai_diag_streak)
            elif streak_state == "semi-open":
                heur += pow(10, ai_diag_streak - 1)
        if human_diag_streak > 1:
            streak_state = get_streak_state(board, N, M, (l,M - c - 1), human_diag_streak, "S-E", 1)
            if streak_state == "open":
                heur -= pow(10, human_diag_streak)
            elif streak_state == "semi-open":
                heur -= pow(10, human_diag_streak - 1)

    return heur





def get_minimax_move(board, N, M, depth, turn, win_streak, alpha=-math.inf, beta=math.inf):
    if turn == -1:
        best_choice = [-math.inf, [-1, -1]]
    else:
        best_choice = [math.inf, [-1, -1]]
    if depth <= 0 or is_game_over(board,-turn,win_streak, N, M):
        return [stronger_heur(board, N, M, win_streak), [-1, -1]]


    all_moves = get_all_candidate_moves(board, N, M, 2)
    for move in all_moves:

        make_move(board, turn, move)
        child_node_value = get_minimax_move(board, N, M, depth - 1, -turn, win_streak, alpha, beta)
        child_node_value[1] = move

        undo_move(board, move)
        if turn == -1 and child_node_value[0] > best_choice[0]:
            best_choice = child_node_value
            alpha = best_choice[0]

        if turn == 1 and child_node_value[0] < best_choice[0]:
            best_choice = child_node_value
            beta = best_choice[0]
        if alpha >= beta:
            break

    return best_choice

def get_minimax_move0(board, N, M, depth, turn, win_streak, alpha=-math.inf, beta=math.inf):
    if turn == -1:
        best_choice = [-math.inf, [-1, -1]]
    else:
        best_choice = [math.inf, [-1, -1]]
    if depth <= 0 or is_game_over(board,-turn,win_streak, N, M):
        return [stronger_heur2(board, N, M, win_streak), [-1, -1]]


    all_moves = get_all_candidate_moves(board, N, M, 2)
    for move in all_moves:

        make_move(board, turn, move)
        child_node_value = get_minimax_move0(board, N, M, depth - 1, -turn, win_streak, alpha, beta)
        child_node_value[1] = move

        undo_move(board, move)
        if turn == -1 and child_node_value[0] > best_choice[0]:
            best_choice = child_node_value
            alpha = best_choice[0]

        if turn == 1 and child_node_value[0] < best_choice[0]:
            best_choice = child_node_value
            beta = best_choice[0]
        if alpha >= beta:
            break

    return best_choice


def print_board(board):
    for line in board:
        print(line)


def is_game_over(board, turn, win_streak, N, M):
    # line
    for i in range(N):
        current_length = 0
        for j in range(M):
            if board[i][j] == turn:
                current_length += 1
                if current_length == win_streak:
                    return True
            else:
                current_length = 0
    # column
    for j in range(N):
        current_length = 0
        for i in range(M):
            if board[i][j] == turn:
                current_length += 1
                if current_length == win_streak:
                    return True
            else:
                current_length = 0

    for j in range(N):
        i = 0
        l = -1
        current_length_length = 0
        while (i + l + 1 < N and j + l + 1 < N):
            l += 1
            if board[i + l][j + l] == turn:
                current_length_length += 1
                if current_length_length == win_streak:
                    return True

            else:
                current_length_length = 0
    for i in range(N):
        j = 0
        l = -1
        current_length_length = 0
        while i + l + 1 < N and j + l + 1 < N:
            l += 1
            if board[i + l][j + l] == turn:
                current_length_length += 1
                if current_length_length == win_streak:
                    return True

            else:
                current_length_length = 0

    for j in range(N):
        i = 0
        l = 0
        current_length_length = 0
        while i + l < N and j - l < N:

            if board[i + l][j - l] == turn:
                current_length_length += 1
                if current_length_length == win_streak:
                    return True
            else:
                current_length_length = 0
            l += 1

    for i in range(N):
        j = 3
        l = 0
        current_length_length = 0
        while i + l < N and j - l < N:
            if board[i + l][j - l] == turn:
                current_length_length += 1
                if current_length_length == win_streak:
                    return True
            else:
                current_length_length = 0
            l += 1
    return False

def weak_heursitic(board, N, M):
    moves = get_all_candidate_moves(board, N, M, 2)
    j = random.randint(0, len(moves) - 1)
    return moves[j]


class Game:
    #creating game settings label
    def __init__(self, tk):
        self.diff=1
        self.s1=[None,None]
        self.s2 = [None, None]
        self.s3 = [None, None]
        self.TURN=1
        self.dimensionX = 4
        self.dimensionY = 4
        self.streaks = 5
        self.seconds_left=0
        self.tk = tk
        self.frame = Frame(self.tk)
        self.frame.pack()
        self.won=0
        self.gameStarted=0
        self.gameRestarted=0
        self.beginning = datetime.now()
        self.icons = {
            "plain": PhotoImage(file="icons/tile_plain.gif"),
            "computer": PhotoImage(file="icons/computer.gif"),
            "human": PhotoImage(file="icons/human.gif"),
            "suggestion": PhotoImage(file="icons/suggestion.gif"),
        }
        self.timeLabel=tkinter.Label(self.frame, text = "Time left: unset")
        self.timeLabel.grid(row=self.dimensionX, column=0, columnspan=self.dimensionY)
        self.streaksLabel = tkinter.Label(self.frame, text="How many in a row:")
        var0=StringVar()
        self.streakSP = Spinbox(self.frame, from_=1, to=40,textvariable=var0)
        var0.set(5)
        self.streakSP.grid(row=self.dimensionX + 1, column=10, columnspan=self.dimensionX)
        self.streaksLabel.grid(row=self.dimensionX+1, column=0, columnspan=self.dimensionX)
        self.sizeLabel = tkinter.Label(self.frame, text="Size x:")
        self.sizeLabel.grid(row=self.dimensionX+2, column=0, columnspan=self.dimensionX)
        var = StringVar()
        self.sizeSP = Spinbox(self.frame, from_=7, to=30, textvariable=var)
        var.set(19)
        self.sizeSP.grid(row=self.dimensionX + 2, column=10, columnspan=self.dimensionX)

        self.sizeLabel2 = tkinter.Label(self.frame, text="Level:")
        self.sizeLabel2.grid(row=self.dimensionX + 3, column=0, columnspan=self.dimensionX)
        self.diffSP = Spinbox(self.frame, from_=1, to=3)
        self.diffSP.grid(row=self.dimensionX + 3, column=10, columnspan=self.dimensionX)

        self.timeLimitLabel = tkinter.Label(self.frame, text="Time limit:")
        self.timeLimitLabel.grid(row=self.dimensionX + 4, column=0, columnspan=self.dimensionX)
        self.timeEntry=tkinter.Entry(self.frame)
        self.timeEntry.grid(row=self.dimensionX + 4, column=10, columnspan=self.dimensionX)
        self.startBtn = tkinter.Button(self.frame, text="Start", command=self.start_game)
        self.startBtn.grid(row=self.dimensionX + 5, column=0, columnspan=self.dimensionX)

    def initialize(self):
        self.won=0
        self.frame2 = Frame(self.tk)
        self.frame2.pack()
        self.board = [[None] * self.dimensionY for _ in range(self.dimensionX)]
        self.squares=[[None] * self.dimensionY for _ in range(self.dimensionX)]
        if self.gameStarted:
            for i in range(self.dimensionX):
                for j in range(self.dimensionY):
                    self.squares[i][j] = tkinter.Label(self.frame2, text='    ', image=self.icons["plain"])
                    self.squares[i][j].grid(row=i, column=j)
                    self.squares[i][j].bind('<Button-1>', lambda e, i=i, j=j: self.on_click(i, j, e))
                    self.squares[i][j].bind('<Button-3>', lambda e, i=i, j=j: self.right_click(i, j, e))


        for i in range(self.dimensionX):
            for j in range(self.dimensionY):
                self.board[i][j]=0


    def printBoard(self):
        for i in range(self.dimensionX):
            print(self.board[i])

    def on_click(self,i, j, event):
        print("aici")
        print(self.s1)
        print(self.s2)
        print(self.s3)
        if(self.board[i][j]==0 and self.TURN==1):
            self.unhoverRec()
            print("unhover")
            self.squares[i][j].config(image=self.icons["human"])
            self.board[i][j]=1
            self.TURN=-1
            self.checkGame(1)
            if(self.won==0):
                self.computerMoves(self.diff)
                self.checkGame(-1)
                #self.printBoard()
                self.recommandations()
            #print(self.s1)
            #print(self.s2)
            #print(self.s3)


    def computerMoves(self,difficulty):
        print("the computer moved")
        if(difficulty==1):
            self.computerMoves1()
        if(difficulty==2):
            self.computerMoves2()
        if (difficulty == 3):
            self.computerMoves3()
        self.TURN=1

    def computerMoves1(self):
        print("easy peasy")
        i,j=weak_heursitic(self.board, self.dimensionY, self.dimensionY)
        self.squares[i][j].config(image=self.icons["computer"])
        self.board[i][j]=-1

    def computerMoves2(self):
        comp_move = get_minimax_move0(self.board, self.dimensionX, self.dimensionY, 1 , -1, self.streaks)
        self.squares[comp_move[1][0]][comp_move[1][1]].config(image=self.icons["computer"])
        self.board[comp_move[1][0]][comp_move[1][1]] = -1

    def computerMoves3(self):
        comp_move = get_minimax_move(self.board, self.dimensionX, self.dimensionY, 2, -1,self.streaks)
        self.squares[comp_move[1][0]][comp_move[1][1]].config(image=self.icons["computer"])
        self.board[comp_move[1][0]][comp_move[1][1]] = -1

    def unhoverRec(self):

        if(self.s1[0]!=None and self.s1[1]!=None):
            self.squares[self.s1[0]][self.s1[1]].config(image=self.icons["plain"])
            print("sa")
        if (self.s2[0]!=None and self.s2[1]!=None):
            self.squares[self.s2[0]][self.s2[1]].config(image=self.icons["plain"])
            print("sa")
        if (self.s3[0]!=None and self.s3[1]!=None):
            self.squares[self.s3[0]][self.s3[1]].config(image=self.icons["plain"])
            print("sa")

    def recommandations(self):
        count=0
        while(count<3):
            for j in range(self.dimensionX):
                for i in range(self.dimensionY):
                    if(self.board[i][j]==0 and i+1<self.dimensionX and j+1<self.dimensionY):
                        if(self.board[i][j+1]==1 or self.board[i+1][j]==1 or self.board[i+1][j+1]==1):
                            r=random.randint(1, 10)
                            if(r<3):
                                if(count==0):
                                    self.s1=[i,j]
                                if (count == 1):
                                    self.s2 = [i, j]
                                if (count == 2):
                                    self.s3 = [i, j]
                                count += 1

        if (self.s1[0] != None and self.s1[1] != None):
            self.squares[self.s1[0]][self.s1[1]].config(image=self.icons["suggestion"])
            print("sa")
        if (self.s2[0] != None and self.s2[1] != None):
            self.squares[self.s2[0]][self.s2[1]].config(image=self.icons["suggestion"])
            print("sa")
        if (self.s3[0] != None and self.s3[1] != None):
            self.squares[self.s3[0]][self.s3[1]].config(image=self.icons["suggestion"])
            print("sa")


    def right_click(self,i,j,event):
        self.squares[i][j].config(image=self.icons["computer"])
        self.board[i][j]=-1
        self.printBoard()

    def countdown(self):
        if(self.won==0):
            self.timeLabel['text'] = "Time left: " + str(self.seconds_left)

            if self.seconds_left:
                self.seconds_left -= 1
                self.frame.after(1000, self.countdown)
            else:
                self.gameOverTime()

    def checkGame(self,player):
        #line
        for i in range(self.dimensionX):
            currentLength = 0
            for j in range(self.dimensionY):
                if(self.board[i][j]==player):
                    currentLength+=1
                    if(currentLength==self.streaks):
                        print("SOMEONE WON")
                        self.gameWon(player)
                else:
                    currentLength=0
        #column
        for j in range(self.dimensionX):
            currentLength = 0
            for i in range(self.dimensionY):
                if(self.board[i][j]==player):
                    currentLength+=1
                    if(currentLength==self.streaks):
                        print("SOMEONE WON")
                        self.gameWon(player)
                else:
                    currentLength=0

        #diagonally
        for j in range(self.dimensionY):
            i = 0
            l = -1
            currentLength = 0
            while (i + l+1 < self.dimensionX and j + l+1 < self.dimensionY):
                l+=1
                if (self.board[i+l][j+l] == player):
                    currentLength += 1
                    if (currentLength == self.streaks):
                        print("SOMEONE WON")
                        self.gameWon(player)
                else:
                    currentLength = 0
        for i in range(self.dimensionY):
            j = 0
            l = -1
            currentLength = 0
            while (i + l+1 < self.dimensionX and j + l+1 < self.dimensionY):
                l+=1
                if (self.board[i+l][j+l] == player):
                    currentLength += 1
                    if (currentLength == self.streaks):
                        print("SOMEONE WON")
                        self.gameWon(player)
                else:
                    currentLength = 0

        #secondary diagonally
        for j in range(self.dimensionY):
            i = 0
            l = 0
            currentLength = 0
            while (i + l< self.dimensionX and j -l< self.dimensionY):

                if (self.board[i+l][j-l] == player):
                    currentLength += 1
                    if (currentLength == self.streaks):
                        print("SOMEONE WON")
                        self.gameWon(player)
                else:
                    currentLength = 0
                l += 1
        for i in range(self.dimensionX):
            j = 3
            l = 0
            currentLength = 0
            while (i + l< self.dimensionX and j -l< self.dimensionY):

                if (self.board[i+l][j-l] == player):
                    currentLength += 1
                    if (currentLength == self.streaks):
                        print("SOMEONE WON")
                        self.gameWon(player)
                else:
                    currentLength = 0
                l += 1




    def gameOverTime(self):
        self.timeLabel['text'] ="Game Over"
        for i in range(self.dimensionX):
            for j in range(self.dimensionY):
                self.board[i][j]=88
        win = Toplevel()
        win.wm_title("END")
        l = Label(win, text="Game over! Time limit exceeded")
        l.grid(row=0, column=0)

        b = Button(win, text="Close", command=win.destroy)
        b.grid(row=1, column=0)


    def gameWon(self,player):
        self.won=1
        if(player==1):
            self.timeLabel['text'] = "You won"
        else:
            self.timeLabel['text'] = "The computer won"
        # for i in range(self.dimensionX):
        #     for j in range(self.dimensionY):
        #         self.board[i][j]=88
        win = Toplevel()
        win.wm_title("END")
        if(player==1):
            l = Label(win, text="You won!!!!")
        else:
            l = Label(win, text="You lost :(")
        l.grid(row=0, column=0)

        b = Button(win, text="Close", command=win.destroy)
        b.grid(row=1, column=0)

    def pos_moves(self):
        moves = []
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                if self.board[i][j] == 0:
                    moves.append((i, j))
        return moves

    def get_rnd_mov(self):
        moves = self.pos_moves()
        j = random.randint(0, len(moves) - 1)
        return moves[j]

    #starts/restart the game
    def start_game(self):
        self.won=0
        self.TURN=1
        if(self.timeEntry.get()):
            self.seconds_left = int(self.timeEntry.get())
        else:
            self.seconds_left=100
        self.countdown()
        self.dimensionX=int(self.sizeSP.get())
        self.dimensionY=self.dimensionX
        N=self.dimensionY
        M=self.dimensionY
        self.diff=int(self.diffSP.get())
        self.streaks=int(self.streakSP.get())
        self.gameStarted = 1
        if(self.gameRestarted):
            self.frame2.destroy()
        self.initialize()
        self.gameRestarted=1;


if __name__ == '__main__':
    window = Tk()
    window.title("Minesweeper")
    minesweeper = Game(window)
    window.mainloop()

