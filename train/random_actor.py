#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random


#explorer用のランダム関数オブジェクト
class RandomActor:
    def __init__(self, board):
        self.board = board
        self.random_count = 0
    def random_action_func(self):
        self.random_count += 1
        positions = self.board.get_put_all()
        index = random.randint(0, len(positions) - 1)
        position = positions[index]
        
        x = position[0]
        y = position[1]
        
        return (x * self.board.SIZE + y)
