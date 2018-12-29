import tensorflow as tf
import numpy as np
import FLAGS


def utt_PIT_MSE_for_CNN(y1, y2):
  # for i in range(tf.shape(y1)[0]):
  loss1 = tf.reduce_mean(tf.square(tf.subtract(y1, y2)), [1, 2])
  y1_speaker1, y1_speaker2 = tf.split(y1, 2, axis=-1)
  y1_swaped = tf.concat([y1_speaker2, y1_speaker1], axis=-1)
  loss2 = tf.reduce_mean(tf.square(tf.subtract(y1_swaped, y2)), [1, 2])
  loss = tf.where(tf.less(loss1, loss2), loss1, loss2)
  return tf.reduce_mean(loss)


def utt_PIT_MSE_for_CNN_v2(y1, y2):
  cleaned1, cleaned2 = tf.split(y1, 2, axis=-1)
  labels1, labels2 = tf.split(y2, 2, axis=-1)
  cost1 = tf.reduce_mean(tf.reduce_sum(tf.pow(cleaned1-labels1, 2), 1)
                         + tf.reduce_sum(tf.pow(cleaned2-labels2, 2), 1), 1)
  cost2 = tf.reduce_mean(tf.reduce_sum(tf.pow(cleaned2-labels1, 2), 1)
                         + tf.reduce_sum(tf.pow(cleaned1-labels2, 2), 1), 1)

  idx = tf.cast(cost1 > cost2, tf.float32)
  loss = tf.reduce_sum(idx*cost2+(1-idx)*cost1)
  return loss


def utt_PIT_MSE_for_LSTM(cleaned1, cleaned2, labels1, labels2):
  cost1 = tf.reduce_mean(tf.reduce_sum(tf.pow(cleaned1-labels1, 2), 1)
                         + tf.reduce_sum(tf.pow(cleaned2-labels2, 2), 1), 1)
  cost2 = tf.reduce_mean(tf.reduce_sum(tf.pow(cleaned2-labels1, 2), 1)
                         + tf.reduce_sum(tf.pow(cleaned1-labels2, 2), 1), 1)
  idx = tf.cast(cost1 > cost2, tf.float32)
  return tf.reduce_sum(idx*cost2+(1-idx)*cost1)


def frame_PIT_MSE_for_CNN(y1, y2):
  # for i in range(tf.shape(y1)[0]):
  loss1 = tf.reduce_mean(tf.square(tf.subtract(y1, y2)), axis=2)
  y1_speaker1, y1_speaker2 = tf.split(y1, 2, axis=-1)
  y1_swaped = tf.concat([y1_speaker2, y1_speaker1], axis=-1)
  loss2 = tf.reduce_mean(tf.square(tf.subtract(y1_swaped, y2)), axis=2)
  loss = tf.where(tf.less(loss1, loss2), loss1, loss2)
  return tf.reduce_mean(loss)


def reduce_sum_frame_batchsize_MSE(y1, y2):
  cost = tf.reduce_mean(tf.reduce_sum(tf.pow(y1-y2, 2), 1), 1)
  return tf.reduce_sum(cost)


def reduce_sum_frame_batchsize_MSE_LOW_FS_IMPROVE(y1, y2):
  loss1 = reduce_sum_frame_batchsize_MSE(y1, y2)
  low_frame = 2000
  low_frame_point = int(257*(low_frame/(FLAGS.MIXED_AISHELL_PARAM.FS/2)))
  loss2 = reduce_sum_frame_batchsize_MSE(tf.slice(y1, [0, 0, 0], [-1, -1, low_frame_point]),
                                         tf.slice(y2, [0, 0, 0], [-1, -1, low_frame_point]))
  return loss1+loss2
