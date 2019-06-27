from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import loader

import os
from django.conf import settings

import cntk as C
from cntk.ops.functions import load_model

from PIL import Image
import numpy as np

import re
import base64
import random 
import string

def indexView(request):
	template = loader.get_template('api/index.html')
	context = {}
	return HttpResponse(template.render(context, request))

def convertImage(imgData1, filename):
	imgstr = re.search(r'base64,(.*)', str(imgData1)).group(1)
	img = base64.b64decode(imgstr)
	with open(filename+'.png', 'wb') as output:
		output.write(img)

def predictView(request):

	model = load_model(os.path.join(settings.BASE_DIR, "data/myModel.model"))

	post_data = request.POST.items()

	pd = [p for p in post_data]

	imgData1 = pd[1][0].replace(" ", "+")

	imgData1 += "=" * ((4 - len(imgData1) % 4) % 4)

	filename = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(32)])

	convertImage(imgData1, filename)

	image = Image.open(filename+'.png').convert('1')

	image.thumbnail((28,28), Image.ANTIALIAS)
	
	image_np = np.array(image.getdata()).astype(int)
	image_np_expanded = np.expand_dims(image_np, axis = 0)

	predicted_label_probs = model.eval({model.arguments[0]: image_np_expanded})

	data = np.argmax(predicted_label_probs, axis=1)

	return JsonResponse({"data": str(data[0])})