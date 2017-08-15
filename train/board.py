#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np

#ゲームボード
class Board():
    def __init__(self, size = 4):
        self.SIZE = size
        self.BLACK = 1
        self.WHITE = -1
    
    # 初期化
    def reset(self):
        self.board = np.zeros((self.SIZE, self.SIZE), dtype=np.float32)
        self.board[int(self.SIZE / 2 - 1)][int(self.SIZE / 2 - 1)] = self.BLACK
        self.board[int(self.SIZE / 2)][int(self.SIZE / 2 - 1)] = self.WHITE
        self.board[int(self.SIZE / 2)][int(self.SIZE / 2)] = self.BLACK
        self.board[int(self.SIZE / 2 - 1)][int(self.SIZE / 2)] = self.WHITE
        
        self.winner = None
        self.missed = False
        self.done = False
        self.turn = self.BLACK
        self.black = 0
        self.white = 0

    # 石を置いてターンを交代する
    def move(self, act, turn = None):
        if turn is None:
            turn = self.turn
            
        if self.put(act):
            self.change_turn()
            self.check_winner()
        else :
            self.winner = turn * -1
            self.missed = True
            self.done = True

    # ターンを変更する
    def change_turn(self):
        self.turn = self.turn * -1

    # 石がおける場所があるかチェックする
    def check_put_all(self, turn = None):
        if turn is None:
            turn = self.turn
            
        for x in range(self.SIZE):
            for y in range(self.SIZE):
                if (self.check_put((x,y), turn)):
                    return True
        return False
        
    # 石がおける場所をすべて取得する
    def get_put_all(self, turn = None):
        if turn is None:
            turn = self.turn
    
        ret = []
    
        for x in range(self.SIZE):
            for y in range(self.SIZE):
                if (self.check_put((x,y), turn)):
                    ret.append((x,y))
        return ret

    # 石を置く
    def put(self, act, turn = None):
        if turn is None:
            turn = self.turn
    
        x = act[0]
        y = act[1]
            
        if (self.board[x][y] != 0):
            return False
    
        ret = False
        ret = self.__put_sub(act, (1, 0), turn) or ret
        ret = self.__put_sub(act, (1, 1), turn) or ret
        ret = self.__put_sub(act, (1, -1), turn) or ret
        ret = self.__put_sub(act, (0, 1), turn) or ret
        ret = self.__put_sub(act, (0, -1), turn) or ret
        ret = self.__put_sub(act, (-1, 0), turn) or ret
        ret = self.__put_sub(act, (-1, 1), turn) or ret
        ret = self.__put_sub(act, (-1, -1), turn) or ret
        
        if ret:
            self.board[act] = turn
       
        return ret
        
    def __put_sub(self, act, direction, turn = None):
        if turn is None:
            turn = self.turn
            
        if (self.__check_put_line(act, direction, turn) == False):
            return False
        x = act[0]
        y = act[1]
        vx = direction[0]
        vy = direction[1]
        
        while True:
            x = x + vx
            y = y + vy

            if (self.board[x][y] == turn * -1):
                self.board[x][y] = turn
            else:
                break;
        
        return True
        

    # 石がおけるかどうかチェックする
    def check_put(self, act, turn = None):
        if turn is None:
            turn = self.turn
            
        x = act[0]
        y = act[1]
            
        if (self.board[x][y] != 0):
            return False
            
        if (self.__check_put_line(act, (1, 0), turn) > 0):
            return True
            
        if (self.__check_put_line(act, (-1, 0), turn) > 0):
            return True

        if (self.__check_put_line(act, (0, 1), turn) > 0):
            return True

        if (self.__check_put_line(act, (0, -1), turn) > 0):
            return True

        if (self.__check_put_line(act, (1, 1), turn) > 0):
            return True

        if (self.__check_put_line(act, (1, -1), turn) > 0):
            return True

        if (self.__check_put_line(act, (-1, 1), turn) > 0):
            return True

        if (self.__check_put_line(act, (-1, -1), turn) > 0):
            return True
            
        return False

        
    def __check_put_line(self, act, direction, turn = None):
        if turn is None:
            turn = self.turn
            
        x = act[0]
        y = act[1]
        vx = direction[0]
        vy = direction[1]
        
        count = 0
        end = 0
        
        if (x < 0 or self.SIZE <= x or
            y < 0 or self.SIZE <= y) :
            return 0
            
        if (self.board[x][y] != 0):
            return 0
        
        while True:
            x = x + vx;
            y = y + vy;
            
            if (0 <= x and x < self.SIZE and
                0 <= y and y < self.SIZE) :

                end = self.board[x][y]
                if (end == turn * -1):
                    count = count + 1
                else:
                    break;
                
            else:
                end = 0
                break;
        if (end == turn and count > 0):
            return count
        else:
            return 0
        

    # 勝敗を判定
    def check_winner(self):
        if self.check_put_all(self.BLACK):
            return
        
        if self.check_put_all(self.WHITE):
            return
            
        count_black = 0
        count_white = 0
        
        for x in range(self.SIZE):
            for y in range(self.SIZE):
                if self.board[x][y] == self.BLACK:
                    count_black = count_black + 1
                elif self.board[x][y] == self.WHITE:
                    count_white = count_white + 1
                    
                    
        if count_black > count_white:
            self.winner = self.BLACK
            self.done = True

        elif count_black < count_white:
            self.winner = self.WHITE
            self.done = True
        else:
            self.winner = 0
            self.done = True
            
        self.black = count_black
        self.white = count_white

    # 黒がおかれている部分を取得する
    def get_black_board(self):
        board = self.board.copy()
        # 白がおいてある部分を0にする
        board[board == self.WHITE] = 0
        return board

    # 白がおかれている部分を取得する
    def get_white_board(self):
        board = self.board.copy()
        # 黒がおいてある部分を0にする
        board[board == self.BLACK] = 0
        board = board * -1;
        return board

    # 置ける場所を取得する
    def get_putable_board(self, turn = None):
        if turn is None:
            turn = self.turn
            
        positions = self.get_put_all(turn)
        
        board = np.zeros((self.SIZE, self.SIZE), dtype=np.float32)
        
        for p in positions:
            board[p] = 1
            
        return board

    def show(self):
        hr = "\n----------------------------------------\n"
        black_count = 0
        white_count = 0
        
        for x in range(self.SIZE):
            print(hr, end='')
            
            for y in range(self.SIZE):
                if y > 0:
                    print("|", end='')
                    
                if self.board[x][y] == self.BLACK:
                    black_count = black_count + 1
                    print(" ○ ", end='')
                elif self.board[x][y] == self.WHITE:
                    white_count = white_count + 1
                    print(" ● ", end='')
                else:
                    n = x * self.SIZE + y
                    if n < 10:
                        print("  ",n, end='')
                    else :
                        print(" ", n, end='')
            
        print(hr, end='')
        print("BLACK = " , black_count, " ,WHITE = ", white_count)