# -*- coding: utf-8 -*-
# sample.py
import urllib
import json
import falcon
import copy

from board import Board
from q_function import Q_Function

import chainer
import numpy as np

agent_p1 = Q_Function()
chainer.serializers.load_npz("model.npz", agent_p1)

class ItemsResource:
    def on_post(self, req, resp):
        params = req.stream.read().decode('utf-8')
        data = urllib.parse.parse_qs(params)
        pieces = data["pieces"][0]
        turn = int(data["turn"][0])

        pieces = pieces.split(",")
        board = np.array(pieces, dtype=np.float32)

        b = Board(8)
        b.board = np.reshape(board, (8,8))
        b.turn = turn

        X = b.get_black_board()
        Y = b.get_white_board()
        Z = b.get_putable_board()

        with chainer.using_config('train', False):
            action = agent_p1(np.array([[X, Y, Z]]))
                
        action = action.greedy_actions.data
        x = int((action) / b.SIZE)
        y = int((action) % b.SIZE)

        items = {
            'title': 'WebAPI(POST)',
            'tags': [
                {
                    'x' : x,
                    'y' : y
                }
            ]
        }
        resp.status = falcon.HTTP_200
        resp.content_type = 'text/plain'
        resp.body = json.dumps(items,ensure_ascii=False)

api = falcon.API()
api.add_route('/reversi_api', ItemsResource())


if __name__ == "__main__":
    from wsgiref import simple_server

    httpd = simple_server.make_server("127.0.0.1", 8008, api)
    httpd.serve_forever()
