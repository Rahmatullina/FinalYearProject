# import the necessary packages
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import SVC
import pickle


def train_model(pathEmbeddings='CloudAndGridREC/output/embeddings.pickle',
				pathRecognizer='CloudAndGridREC/output/recognizer.pickle',
				pathLabelEnc='CloudAndGridREC/output/le.pickle'):
	# load the face embeddings
	print("[INFO] loading face embeddings...")
	data = pickle.loads(open(pathEmbeddings, "rb").read())
	# encode the labels
	print("[INFO] encoding labels...")
	le = LabelEncoder()
	labels = le.fit_transform(data["names"])

	# train the model used to accept the 128-d embeddings of the face and
	# then produce the actual face recognition
	print("[INFO] training model...")
	recognizer = SVC(C=1.0, kernel="linear", probability=True)
	recognizer.fit(data["embeddings"], labels)

	# write the actual face recognition model to disk
	pickle.dump(recognizer, open(pathRecognizer, "wb"))
	# write the label encoder to disk
	pickle.dump(le, open(pathLabelEnc, "wb"))