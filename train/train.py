#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import copy

from board import Board
from random_actor import RandomActor
from q_function import Q_Function

import chainer
import chainer.functions as F
import chainer.links as L
import chainer.computational_graph as c
import chainerrl
import numpy as np

def main():
    parser = argparse.ArgumentParser(description='REVERSI')
    parser.add_argument('--gpu', '-g', type=int, default=-1,
                        help='GPU ID (negative value indicates CPU)')
                        
    args = parser.parse_args()
                        
    print('GPU: {}'.format(args.gpu))
    
    # ボードの準備
    b = Board(8)
    
    # explorer用のランダム関数オブジェクトの準備
    ra = RandomActor(b)
    
    # Q-functionとオプティマイザーのセットアップ
    q_func = Q_Function()
    
    if args.gpu >= 0:
        # Make a specified GPU current
        chainer.cuda.get_device_from_id(args.gpu).use()
        q_func.to_gpu()  # Copy the model to the GPU

    optimizer = chainer.optimizers.Adam(eps=1e-2)
    optimizer.setup(q_func)
    
    # 報酬の割引率
    gamma = 0.99
    
    start_epsilon = 1.0
    decay_steps = 5 * 10 ** 5
    
    # Epsilon-greedyを使ってたまに冒険。
    explorer = chainerrl.explorers.LinearDecayEpsilonGreedy(
        start_epsilon=start_epsilon, end_epsilon=0.3, decay_steps=decay_steps, random_action_func=ra.random_action_func)
        
    # Experience ReplayというDQNで用いる学習手法で使うバッファ
    replay_buffer = chainerrl.replay_buffer.ReplayBuffer(capacity=10 ** 6)
    
    # Agentの生成（replay_buffer等を共有する2つ）
    agent_p1 = chainerrl.agents.DoubleDQN(
        q_func, optimizer, replay_buffer, gamma, explorer,
        replay_start_size=500, update_interval=1, gpu = 0,
        target_update_interval=100)
    agent_p2 = chainerrl.agents.DoubleDQN(
        q_func, optimizer, replay_buffer, gamma, explorer,
        replay_start_size=500, update_interval=1, gpu = 0,
        target_update_interval=100)
    
    #学習ゲーム回数
    n_episodes = 10 ** 6
    
    #カウンタの宣言
    miss = 0
    win = 0
    draw = 0
    put = 0
    
    start = 1
    
    #エピソードの繰り返し実行
    for i in range(start, n_episodes + 1):
        b.reset()
        
        reward = 0
        
        agents = [agent_p1, agent_p2]
        
        turn = np.random.choice([0, 1])
        
        last_state = [None, None]
        
        while not b.done:
            # 置ける場所があるかチェック
            if (b.check_put_all() == False):
                #おけないため相手のターンにする
                b.board = b.board * -1
                
                #ターンを切り替え
                turn = 1 if turn == 0 else 0
                
                
            #配置マス取得
            X = b.get_black_board()
            Y = b.get_white_board()
            Z = b.get_putable_board()

            action = agents[turn].act_and_train(np.array([X, Y, Z]), reward)
            
            x = int((action) / b.SIZE)
            y = int((action) % b.SIZE)
            
            #配置を実行
            b.move((x, y))
            
            put = put + 1
            
            #配置の結果、終了時には報酬とカウンタに値をセットして学習
            if b.done == True:
                if b.winner == 1:
                    win += 1
                    reward = (64 + (b.black - b.white)) / 128
                elif b.winner == 0:
                    draw += 1
                    reward = 0
                else:
                    reward = (-64 + (b.black - b.white)) / 128
                
                    
                if b.missed is True:
                    reward = -10
                    miss += 1
                    
                #エピソードを終了して学習
                x = b.get_black_board()
                y = b.get_white_board()
                z = b.get_putable_board()
                agents[turn].stop_episode_and_train(np.array([x, y, z]), reward, True)
                
                    
                #相手もエピソードを終了して学習。
                if agents[1 if turn == 0 else 0].last_state is not None:
                    if b.missed is False:
                        #前のターンでとっておいたlast_stateをaction実行後の状態として渡す
                        last_board = last_state[1 if turn == 0 else 0]
                        x_l = last_board.get_black_board()
                        y_l= last_board.get_white_board()
                        z_l = last_board.get_putable_board()
                    
                        agents[1 if turn == 0 else 0].stop_episode_and_train(np.array([x_l, y_l, z_l]), reward*-1, True)
                    else:
                        # 相手のミスは勝利として学習しないように
                        agents[1 if turn == 0 else 0].stop_episode()
            else:
            
                #学習用にターン最後の状態を退避
                last_state[turn] = copy.deepcopy(b)
                
                #継続のときは盤面の値を反転
                b.board = b.board * -1
                
                #ターンを切り替え
                turn = 1 if turn == 0 else 0
                
                b.change_turn()
    
        #コンソールに進捗表示
        if i % 100 == 0:
            print("episode:", i, " / put:", put , " / rnd:", ra.random_count, " / miss:", miss, " / win:", win, " / draw:", draw, " / statistics:", agent_p1.get_statistics(), " / epsilon:", agent_p1.explorer.epsilon)
            
            #カウンタの初期化
            miss = 0
            win = 0
            draw = 0
            put = 0
            ra.random_count = 0
        if i % 5000 == 0:
            # 5000エピソードごとにモデルを保存
            agent_p1.save("result_" + str(i))
    print("Training finished.")
    
if __name__ == '__main__':
    main()
    