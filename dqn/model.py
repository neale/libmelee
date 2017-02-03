import melee
import numpy as np
import tensorflow as tf


def actions():
    return melee.techskill.get_actions()

def one_hot_enc(data, key=None):
    
    if type(data) is dict:
        if key:
            l = len(data[key])
            return [bin(i) for i in range(l)]

    if type(data) is list:
        return [bin(i) for i in range(len(data))]

    else: return None

def one_hot_dec(data, store, key=None):

    if type(data) is dict:
        if key:
            return store[key][int(data)]


## TODO set up inputs pixels? actions, neighboring pixels, damage
## ActionsNN -> AugmentingNN with pixels -> output?
## for now we do this: [action1..actionN, opp damage, self damage, current action, 
##                      isJumping]

def get_init_tf():
    inputs = tf.placeholder(shape[1, 17], dtype=tf.int)
    W      = tf.Variable(tf.random_uniform([17, 5], 0, 0, .1))
    Qout   = tf.matmul(inputs, W)
    pred   = tf.argmax(Qout, 1)

    return tf.initialize_all_variables()

y = .99
e = .1
num_episodes = 200;
jList = []
rList = []
with tf.session() as sess:
    sess.run(init)
