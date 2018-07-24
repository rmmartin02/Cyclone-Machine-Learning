from PIL import Image
import numpy as np

tol = 50

im = Image.open('./patVis.jpg')

cropSize = 800
im = im.crop((im.width/2-cropSize/2,im.height/2-cropSize/2,im.width/2+cropSize/2,im.height/2+cropSize/2))

n = np.array(im)
m = np.empty(n.shape).astype(np.uint8)
for i in range(len(n)):
	print(i)
	for j in range(len(n[i])):
		dif1 = int(n[i][j][0])-int(n[i][j][1])
		dif2 = int(n[i][j][0])-int(n[i][j][2])
		if abs(dif1)<tol and abs(dif2)<tol:
			m[i][j] = n[i][j]


p = Image.fromarray(m,'RGB')
p.show()
p.convert('P').save('test.GIF')
p.convert('RGB').save('testFullColor.JPG')