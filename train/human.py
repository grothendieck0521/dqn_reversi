#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 人間プレイヤー
class HumanPlayer:
    def act(self, board):
        act = ""
        while True:
            try:
                str = "Please enter 0 - %s :" % (board.SIZE * board.SIZE - 1)
                act = input(str)
                act = int(act)
                if act >= 0 and act <= board.SIZE * board.SIZE - 1:
                    x = int((act) / board.SIZE)
                    y = int((act) % board.SIZE)
                    
                    if board.check_put((x, y)):
                        return act
                    else :
                        print("Invalid put")
                else:
                    print("Invalid put")
            except Exception as e:
                print(act,  " is invalid")
