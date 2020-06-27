import numpy as np
import sys
import os
import facenet
import tensorflow as tf
import configure
import cv2
import time
from sklearn.metrics.pairwise import cosine_similarity as cs
import pickle

class FaceRecognition(object):
	"""docstring for FaceRecognition"""
	def __init__(self):
		super(FaceRecognition, self).__init__()
		self.graph, self.sess = self.load_model()
		self.images_placeholder, self.embeddings, self.phase_train_placeholder = self.load_input(self.graph, self.sess)
		self.start_model()

	def start_model(self):
		img = [np.ones((242, 242, 3))]
		embs = self.embedding_image(img)

	def load_model(self, filename = "model"):
		graph = tf.Graph()
		os.environ["CUDA_VISIBLE_DEVICES"]="0"
		config = tf.ConfigProto()
		config.gpu_options.allow_growth = True
		sess = tf.Session(config=config, graph = graph)
		with graph.as_default():
			with sess.as_default():
				facenet.load_model(filename)
		return graph, sess

	def load_input(self, graph, sess):
		images_placeholder = graph.get_tensor_by_name("input:0")
		embeddings = graph.get_tensor_by_name("embeddings:0")
		phase_train_placeholder = graph.get_tensor_by_name("phase_train:0")
		return images_placeholder, embeddings, phase_train_placeholder

	def embedding_path(self, paths):
		with self.graph.as_default():
			with self.sess.as_default():
				images =  facenet.load_data_paths(paths, False, False, configure.SIZEMODEL)
				feed_dict = {self.images_placeholder: images, self.phase_train_placeholder: False}
				emb_array = self.sess.run(self.embeddings, feed_dict = feed_dict)
		return emb_array

	def embedding_image(self, images_list):
		with self.graph.as_default():
			with self.sess.as_default():
				images = facenet.load_data(images_list, False, False, configure.SIZEMODEL)
				index = 0
				emb_array = []
				while index < images.shape[0]:
					batch = min(images.shape[0] - index, 32)
					img = images[index:index+batch]
					if img.ndim == 3:
						img = img.reshape(1, img.shape[0], img.shape[1], img.shape[2])
					feed_dict = {self.images_placeholder:img, self.phase_train_placeholder:False}
					embs = self.sess.run(self.embeddings, feed_dict = feed_dict)
					emb_array.extend(embs)
					index += batch
				emb_array = np.array(emb_array)
		return emb_array

	def distance_emb(self, emb_array1, emb_array2):
		return np.sum(np.square(np.subtract(emb_array1,emb_array2)))


# images_list = []
# labels = []
# face_recog = FaceRecognition()
# for namefile in os.listdir("database/hung"):
# 	path = os.path.join("database/hung", namefile)
# 	img = cv2.imread(path)
# 	images_list.append(img)
# 	labels.append("hungdv")
# # img_arr = np.array(img_arr)
# arr_embeddings = face_recog.embedding_image(images_list)
# pickle.dump(arr_embeddings, open("data_embeddings", "wb"))
# pickle.dump(labels, open("labels", "wb"))
# arr_embeddings = pickle.load(open("data_embeddings", "rb"))
# labels = pickle.load(open("labels", "rb"))
# print (arr_embeddings.shape)
# print (labels)