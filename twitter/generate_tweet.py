import tensorflow as tf
import numpy as np

bans = []
with open(r"C:\Users\Payton\Documents\CS325\RAPBOT\filter.txt") as f:
    lines = f.readlines()
    for l in lines:
        spl = l.split(",")
        bans.append(spl[0])

def generate_tweet(constant, one_step_model):
    states = None
    next_char = tf.constant([constant])
    result = []

    for n in range(100):
        next_char, states = one_step_model.generate_one_step(next_char, states=states)
        result.append(next_char)

    result = tf.strings.join(result)
    return result[0].numpy().decode('utf-8')

def make_tweet(input):
    one_step = tf.saved_model.load(r"C:\Users\Payton\Documents\CS325\RAPBOT\thug_one_step\one_step")
    tweet = generate_tweet(input, one_step)
    
    while any(word in tweet for word in bans):
        tweet = generate_tweet(input, one_step)

    i = -1
    while i >= -(len(tweet)):
        if tweet[i] == ' ':
            break
        i-=1

    finished = ""
    for c in tweet[:i]:
        try:
            if finished[-1] == " " and c == " ":
                return finished
            else:
                finished+=c
        except:
            finished+=c

    return tweet[:i]
