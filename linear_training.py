import tensorflow as tf
import numpy
rng = numpy.random

# Parameters
learning_rate = 0.001
training_epochs = 100000
display_step = 50
train_X_orig = []
div_orig = []
train_Y_orig = []
traincount = 1

with open('./trainingFile_noTempAndPm') as f:
    for line in f:
        linelist = line.strip('\r\n').split('\t')
        for i in range(len(linelist)):
            linelist[i] = float(linelist[i])
        if linelist[0] - 0.0 < 0.001:
            train_Y_orig.append([1.0])
        else:
            train_Y_orig.append([linelist[0]])
        train_X_orig.append(linelist[1:])

with open('./divs') as f:
    for line in f:
        div = int(line.strip('\r\n'))
        div_orig.append([1.0/div])

# Training Data
train_X = numpy.matrix(train_X_orig)
train_Y = numpy.matrix(train_Y_orig)
train_DIV = numpy.matrix(div_orig)

#W_start = numpy.asarray([[0]]*train_X.shape[1])
#b_start = numpy.asarray([[0]]*train_X.shape[1])
n_samples = train_X.shape[0]

print train_X
print train_Y

# tf Graph Input
X = tf.placeholder("float", [None, train_X.shape[1]])
Y = tf.placeholder("float", [None, 1])
DIV = tf.placeholder("float", [None, 1])

# Create Model

# Set model weights
#W_start = [[0.00124113610945642], [-0.000858253100886941], [0.0004929733695462346], [0.0009669300634413958], [-0.00023777008755132556], [0.0006793635548092425], [0.0008624290348961949], [0.001174046192318201], [0.11375556141138077], [0.0], [-0.00010708131594583392], [-8.602201705798507e-05], [0.00027691933792084455], [0.000666735926643014], [0.007129747420549393], [-0.00017446652054786682], [0.000398186850361526], [0.027286997064948082], [0.0], [-9.400333510711789e-05], [-3.831821959465742e-05], [0.00047708034981042147], [0.0009549997048452497], [-0.0014572753570973873], [-0.00015841849381104112], [0.0005085058510303497], [0.01706511341035366], [0.0], [-5.8086763601750135e-05], [-0.0001870926353149116], [0.00021724984981119633], [0.0008983694715425372], [0.0007742814486846328], [-0.0001580851385369897], [0.000245486618950963]]
#b_start = [0.8289880752563477]
#W = tf.Variable(tf.constant(numpy.float32(numpy.matrix(W_start))))
#b = tf.Variable(tf.constant(numpy.float32(numpy.matrix(b_start))))
W = tf.Variable(tf.truncated_normal([train_X.shape[1], 1]))
b = tf.Variable(tf.truncated_normal([train_X.shape[0], 1]))
# Construct a linear model
#b = tf.Print(b, [b], "Bias: ")
#W = tf.Print(W, [W], "Weight: ")
#X = tf.Print(X, [X], "TF_in: ")
Y_pred = tf.add(tf.matmul(X,W), b)
#Y_pred = b #tf.Variable(tf.random_normal([1]))
#for pow_i in range(1, 4):
#    W = tf.Variable(tf.random_normal([train_X.shape[1], 1]))
#    Y_pred = tf.add(tf.matmul(tf.pow(X, pow_i), W, a_is_sparse = False), Y_pred)
#tf.Print(activation, [activation], "Matmul: ")

# Minimize the squared errors
#cost = tf.reduce_sum(tf.square(Y_pred-Y, 2))  #L2 loss
#cost = tf.reduce_sum(tf.abs(tf.sub(Y, Y_pred)))
cost = tf.reduce_sum(tf.mul(tf.abs( tf.sub(1.0,tf.div(Y_pred, Y)) ), DIV))
#cost = tf.add(cost, tf.mul(1e-6, tf.global_norm([W])))

optimizer = tf.train.AdamOptimizer(learning_rate).minimize(cost) #Gradient descent

# Initializing the variables
init = tf.initialize_all_variables()

mini_batch_size = 128
# Launch the graph
minVal = 1000000000000000000
minW = []
minB = 0.0
with tf.Session() as sess:
    sess.run(init)
    # Fit all training data
    for epoch in range(training_epochs):
        #i_batch = (epoch % n_samples)*mini_batch_size
        #batch = train_X[i_batch:i_batch+mini_batch_size], train_Y[i_batch:i_batch+mini_batch_size], train_DIV[i_batch:i_batch+mini_batch_size]
        #sess.run(optimizer, feed_dict={X: batch[0], Y: batch[1], DIV: batch[2]})
        sess.run(optimizer, feed_dict={X: train_X, Y: train_Y, DIV: train_DIV})

        prev_training_cost = 0.0
        training_cost = sess.run(cost, feed_dict={X: train_X, Y: train_Y, DIV:train_DIV})
        if training_cost < minVal:
            minVal = training_cost 
            minW = sess.run(W)
            minB = sess.run(b)
        #print(training_cost)
        if epoch % display_step == 0:
            print "Epoch:", '%04d' % (epoch+1), " cost=", "{:.9f}".format(sess.run(cost, feed_dict={X: train_X, Y:train_Y, DIV:train_DIV})), \
                    "\nW=", sess.run(W), "\nb=", sess.run(b), "\n"

        if numpy.abs(prev_training_cost - training_cost) < 0.0000001:
            break
        prev_training_cost = training_cost

    print "Optimization Finished!"
    #training_cost = sess.run(cost, feed_dict={X: train_X, Y: train_Y})
    print "Training cost=", minVal, "W=", minW.tolist(), "b=", minB.tolist(), '\n'

