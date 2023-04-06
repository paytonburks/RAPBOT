import tensorflow as tf
import numpy as np
import json
import tweepy
import os
from google.cloud import storage
import pathlib

working_dir = pathlib.Path.cwd()
downloads_folder = working_dir.joinpath('GCPDOWNLOAD')
model = None
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]=r"goog_creds.json"

def download_model():
    BUCKET_NAME = "thugger-one-step-bucket"
    PROJECT_ID = "slattbot"

    client = storage.Client(PROJECT_ID)
    bucket = client.get_bucket(BUCKET_NAME)
    blobs = bucket.list_blobs()
    for b in blobs:
        if str(b.name).startswith("thug_one_step/one_step"):
            path_download = downloads_folder.joinpath(b.name)
            if not path_download.parent.exists():
                path_download.parent.mkdir(parents=True)
            b.download_to_filename(str(path_download))

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
    one_step_gcp = tf.saved_model.load(r"C:\Users\Payton\Documents\CS325\RAPBOT\GCPDOWNLOAD\thug_one_step\one_step")
    tweet = generate_tweet(input, one_step_gcp)

    i = -1
    while i >= -(len(tweet)):
        if tweet[i] == ' ':
            break
        i-=1
    return tweet[:i]

def entry_point(request):
    download_model()
    tweet = make_tweet(input=" ")
    print(tweet)

    ck, cs, at, ats = get_keys()
    client = tweepy.Client(consumer_key=ck, consumer_secret=cs, 
                           access_token=at, access_token_secret=ats)
    # response = client.create_tweet(text=tweet)
    # print(response)
