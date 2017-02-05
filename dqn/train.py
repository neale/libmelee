#!/usr/bin/python3
import ops
import model
import env
import sys
sys.path.append("..")
import melee
import tensorflow as tf


def train():
    nn = model.DQN(100, .1, .01, "RMSPROP", './cp')
    
    environ = env.Env(nn, nn.epochs)
    environ.run()
    


if __name__ == '__main__':
    train()
