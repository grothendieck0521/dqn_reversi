#!/usr/bin/env python
# -*- coding: utf-8 -*-

import chainer
import chainer.functions as F
import chainer.links as L
import chainerrl

class Q_Function(chainer.Chain):
    def __init__(self):
        super().__init__(
            conv1=L.Convolution2D(3, 198, 5, pad=2, stride=1),
            conv2=L.Convolution2D(198, 198, 5, pad=2, stride=1),
            conv3=L.Convolution2D(198, 198, 5, pad=2, stride=1),
            conv4=L.Convolution2D(198, 198, 5, pad=2, stride=1),
            conv5=L.Convolution2D(198, 198, 5, pad=2, stride=1),
            conv6=L.Convolution2D(198, 1, 1, nobias=True),
            biasl1=L.Bias(shape=64)
        )
    def __call__(self, x, test=False):

        h = F.leaky_relu(self.conv1(x))

        h = F.leaky_relu(self.conv2(h))
        
        h = F.leaky_relu(self.conv3(h))

        h = F.leaky_relu(self.conv4(h))
        
        h = F.leaky_relu(self.conv5(h))
        
        h = F.leaky_relu(self.conv6(h))
        
        h = F.reshape(h, (-1, 64))

        h = self.biasl1(h)
        
        return chainerrl.action_value.DiscreteActionValue(h)
        
