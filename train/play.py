#!/usr/bin/env python
# -*- coding: utf-8 -*-

from board import Board
from human import HumanPlayer
from q_function import Q_Function

import chainer
import numpy as np

def main():
    b = Board(8)

    # 環境と行動の次元数
    obs_size = b.SIZE * b.SIZE * 3
    n_actions = b.SIZE * b.SIZE
    
    # Q-functionのセットアップ
    agent_p1 = Q_Function(obs_size, n_actions)
    chainer.serializers.load_npz("result_130000/model.npz", agent_p1)

    human_player = HumanPlayer()
    
    for i in range(10):
        b.reset()
        dqn = np.random.choice([b.BLACK, b.WHITE])
        
        if dqn == b.BLACK:
            print("YOU WHITE")
        else :
            print("YOU BLACK")
        
        while not b.done:
            # 置ける場所があるかチェック
            if (b.check_put_all() == False):
                b.change_turn()
                
            if dqn == b.turn:
                #DQN
                b.show()
                
                if dqn == b.WHITE :
                    b.board = b.board * -1
                    b.change_turn()
                
                X = b.get_black_board()
                Y = b.get_white_board()
                Z = b.get_putable_board()
                with chainer.using_config('train', False):
                    action = agent_p1(np.array([[X, Y, Z]]))
                
                action = action.greedy_actions.data
                
                print(action)
                
                x = int((action) / b.SIZE)
                y = int((action) % b.SIZE)
                
                if dqn == b.WHITE :
                    b.board = b.board * -1
                    b.change_turn()
                
                b.move((x,y))
                
                if b.done == True:
                    b.show()
                    if b.winner == dqn:
                        print("YOU LOSE")
                    elif b.missed:
                        print("DQN Missed")
                    elif b.winner == 0:
                        print("DRAW")
                    else:
                        print("YOU WIN")
                    continue
            else:
                #人間
                b.show()
                action = human_player.act(b)
                x = int((action) / b.SIZE)
                y = int((action) % b.SIZE)
            
                b.move((x,y))

                if b.done == True:
                    b.show()
                    if b.winner == dqn:
                        print("YOU LOSE")
                    elif b.missed:
                        print("DQN Missed")
                    elif b.winner == 0:
                        print("DRAW")
                    else:
                        print("YOU WIN")

if __name__ == '__main__':
    main()