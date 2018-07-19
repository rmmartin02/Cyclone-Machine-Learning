import os
import tensorflow as tf

labels = []
filenames = []
#num = 0
for storm in os.listdir('./images/'):
	directory = './data/{}/STRMSTAT/'.format(storm)
	if os.path.exists(directory):
		stats = os.listdir(directory)
		directory = './images/{}/4KMIRIMG/'.format(storm)
		if os.path.exists(directory):
			for image in os.listdir(directory):
				for stat in stats:
					if image[-16:-5] == stat[-16:-5]:
						with open('./data/{}/STRMSTAT/{}'.format(storm,stat)) as f:
							windSpeed = int(f.readline().split()[4])
						if windSpeed<64:
							labels.append(0)
						else:
							labels.append(1)
						filenames.append('./images/{}/4KMIRIMG/{}'.format(storm,image))
						#num += 1
						#print(num,windSpeed,image)

# Reads an image from a file, decodes it into a dense tensor, and resizes it
# to a fixed shape.
def _parse_function(filename, label):
  image_string = tf.read_file(filename)
  image_decoded = tf.image.decode_gif(image_string)
  image_resized = tf.image.resize_images(image_decoded, [32, 32])
  return image_resized, label

# A vector of filenames.
filenames = tf.constant(filenames)

# `labels[i]` is the label for the image in `filenames[i].
labels = tf.constant(labels)

dataset = tf.data.Dataset.from_tensor_slices((filenames, labels))
dataset = dataset.map(_parse_function)

dataset = dataset.batch(2)

# step 4: create iterator and final input tensor
iterator = dataset.make_one_shot_iterator()
images, labels = iterator.get_next()

# Build a TensorFlow graph that does something with each element.
loss = model_function(next_element)
optimizer = ...  # A <a href="../../tf/train/Optimizer"><code>tf.train.Optimizer</code></a> object.
train_op = optimizer.minimize(loss)

with tf.Session() as sess:
  try:
    while True:
      sess.run(train_op)
  except tf.errors.OutOfRangeError:
    pass

beginTime = time.time()

# Parameter definitions
batch_size = 100
learning_rate = 0.005
max_steps = 1000

# Uncommenting this line removes randomness
# You'll get exactly the same result on each run
# np.random.seed(1)

# Prepare data
data_sets = data_helpers.load_data()

# -----------------------------------------------------------------------------
# Prepare the TensorFlow graph
# (We're only defining the graph here, no actual calculations taking place)
# -----------------------------------------------------------------------------

# Define input placeholders
images_placeholder = tf.placeholder(tf.float32, shape=[None, 3072])
labels_placeholder = tf.placeholder(tf.int64, shape=[None])

# Define variables (these are the values we want to optimize)
weights = tf.Variable(tf.zeros([3072, 2]))
biases = tf.Variable(tf.zeros([2]))

# Define the classifier's result
logits = tf.matmul(images_placeholder, weights) + biases

# Define the loss function
loss = tf.reduce_mean(tf.nn.sparse_softmax_cross_entropy_with_logits(logits=logits,
  labels=labels_placeholder))

# Define the training operation
train_step = tf.train.GradientDescentOptimizer(learning_rate).minimize(loss)

# Operation comparing prediction with true label
correct_prediction = tf.equal(tf.argmax(logits, 1), labels_placeholder)

# Operation calculating the accuracy of our predictions
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

# -----------------------------------------------------------------------------
# Run the TensorFlow graph
# -----------------------------------------------------------------------------

with tf.Session() as sess:
  # Initialize variables
  sess.run(tf.global_variables_initializer())

  # Repeat max_steps times
  for i in range(max_steps):

    # Generate input data batch
    indices = np.random.choice(data_sets['images_train'].shape[0], batch_size)
    images_batch = data_sets['images_train'][indices]
    labels_batch = data_sets['labels_train'][indices]

    # Periodically print out the model's current accuracy
    if i % 100 == 0:
      train_accuracy = sess.run(accuracy, feed_dict={
        images_placeholder: images_batch, labels_placeholder: labels_batch})
      print('Step {:5d}: training accuracy {:g}'.format(i, train_accuracy))

    # Perform a single training step
    sess.run(train_step, feed_dict={images_placeholder: images_batch,
      labels_placeholder: labels_batch})

  # After finishing the training, evaluate on the test set
  test_accuracy = sess.run(accuracy, feed_dict={
    images_placeholder: data_sets['images_test'],
    labels_placeholder: data_sets['labels_test']})
  print('Test accuracy {:g}'.format(test_accuracy))

endTime = time.time()
print('Total time: {:5.2f}s'.format(endTime - beginTime))
