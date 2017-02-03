import ops
import model
import sys
sys.path.append("..")
import melee
import tensorflow as tf

init = get_init_tf()
tf.reset_default_graph()
y = .99  
e = .1                                                                                                                      
num_episodes = 200
jList = []
rList = []
with tf.session() as sess:
sess.run(init)  
