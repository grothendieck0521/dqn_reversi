#!/usr/bin/env python
# -*- coding: utf-8 -*-

from board import Board
from human import HumanPlayer
from q_function import Q_Function
from random_actor import RandomActor
from cpu1 import CPU1

import chainer
import numpy as np

def main():
    b = Board(8)
    
    ra = RandomActor(b)
    cpu1 = CPU1(b)
    
    # Q-functionのセットアップ
    agent_p1 = Q_Function()

    chainer.serializers.load_npz("result_50000/model.npz", agent_p1)

    agent1_win = 0
    agent1_miss = 0
    draw = 0
    
    for i in range(100):
        b.reset()
        dqn = np.random.choice([b.BLACK, b.WHITE])
        
        while not b.done:
            # 置ける場所があるかチェック
            if (b.check_put_all() == False):
                b.change_turn()
                
            if dqn == b.turn:
                # agent1
                
                if dqn == b.WHITE :
                    b.board = b.board * -1
                    b.change_turn()
                
                X = b.get_black_board()
                Y = b.get_white_board()
                Z = b.get_putable_board()
                
                with chainer.using_config('train', False):
                    action = agent_p1(np.array([[X, Y, Z]]))
                
                action = action.greedy_actions.data
                x = int((action) / b.SIZE)
                y = int((action) % b.SIZE)
                
                if dqn == b.WHITE :
                    b.board = b.board * -1
                    b.change_turn()
                
                b.move((x,y))
                
            else:
                # agent2
                #action = ra.random_action_func()
                action = cpu1.action_func()
                x = int((action) / b.SIZE)
                y = int((action) % b.SIZE)
                
                b.move((x,y))
                
            if b.done == True:
                if b.missed:
                    agent1_miss = agent1_miss + 1
                    print("PLAY = ", i , "/ agent missed", b.black, " - ", b.white)
                elif b.winner == dqn:
                    agent1_win = agent1_win + 1
                    print("PLAY = ", i , "/ agent win", b.black, " - ", b.white)
                elif b.winner == dqn * -1:
                    print("PLAY = ", i , "/ random win", b.black, " - ", b.white)
                else:
                    draw = draw + 1
                    print("PLAY = ", i , "/ draw", b.black, " - ", b.white)
    
    print("agent_win = ", agent1_win)
    print("agent_miss = ", agent1_miss)
    print("draw = ", draw)

if __name__ == '__main__':
    main()
    