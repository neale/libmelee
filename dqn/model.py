import sys; sys.path.append("..")
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
class DQN(object):
    
    def __init__(self, epochs, lr, l2_reg, optim, weight_path):
        self.epochs        = epochs
        self.learning_rate = lr
        self.weight_decay  = l2_reg
        self.optim         = optim
        self.weight_path   = weight_path

        tf.reset_default_graph()
        self.get_init_tf()

    def get_init_tf(self):
        inputs = tf.placeholder(shape=[1, 17], dtype=tf.float32)
        W      = tf.Variable(tf.random_uniform([17, 5], 0, 0, tf.float32))
        Qout   = tf.matmul(inputs, W)
        pred   = tf.argmax(Qout, 1)
        self.init = tf.global_variables_initializer()

    def train(self):
        with tf.session() as sess:
            sess.run(init)


    def test_env(self):
        return np.random.randint(1, 10)
