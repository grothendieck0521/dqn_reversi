#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import random
import copy

class CPU1:
    def __init__(self, board):
        self.board = board
        
        self.evaluation = np.array([
                                    [30 , -12,  0, -1, -1,  0, -12,  30],
                                    [-12, -15, -3, -3, -3, -3, -15, -12],
                                    [  0,  -3,  0, -1, -1,  0, -3,    0],
                                    [ -1,  -3, -1, -1, -1, -1, -3,   -1],
                                    [ -1,  -3, -1, -1, -1, -1, -3,   -1],
                                    [  0,  -3,  0, -1, -1,  0, -3,    0],
                                    [-12, -15, -3, -3, -3, -3, -15, -12],
                                    [30 , -12,  0, -1, -1,  0, -12,  30]
                                    ])
    def action_func(self):
        positions = self.board.get_put_all()
        
        eval = -9999
        acts = []
        
        for position in positions:
            tmp_eval = self._action_func(position)

            if eval < tmp_eval:
                eval = tmp_eval
                acts = [position]
            elif eval == tmp_eval:
                acts.append(position)

        index = random.randint(0, len(acts) - 1)
        act = acts[index]
        x = act[0]
        y = act[1]
        
        return (x * self.board.SIZE + y)

    def _action_func(self, position):
        b = copy.deepcopy(self.board)
        turn = b.turn
        
        b.put(position)
    
        black_eval = (self.evaluation * b.get_black_board()).sum()
        white_eval = (self.evaluation * b.get_white_board()).sum()
        
        copy.deepcopy(b)
        
        if turn == b.BLACK:
            return black_eval - white_eval
        else:
            return white_eval - black_eval
