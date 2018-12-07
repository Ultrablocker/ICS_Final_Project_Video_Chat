import cv2
import numpy
import io
from PIL import Image

class Feed:
	def __init__(self, name = 'default', action = 1):
		self.cam = cv2.VideoCapture(0)
		self.action = action
		self.name = name

	def set_name(self, name):
		self.name = name

	def set_action(self, action):
		self.action = action

	def get_frame(self):
		# Courtesy of xxx
		null, img = self.cam.read()
		cv2_im = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
		pil_im = Image.fromarray(cv2_im)
		b = io.BytesIO()
		pil_im.save(b, 'jpeg')
		im_bytes = b.getvalue()
		return im_bytes

	def set_frame(self, im_bytes):
# Courtesy of xxx
		pil_bytes = io.BytesIO(frame_bytes)
		pil_image = Image.open(pil_bytes)
		cv_image = cv2.cvtColor(numpy.array(pil_image), cv2.COLOR_RGB2BGR)
		cv2.imshow(self.name, cv_image)
