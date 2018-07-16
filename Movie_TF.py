import numpy as np
import tensorflow as tf
import mat4py

'''读入文件'''
data = mat4py.loadmat('ratings.mat')
data_y = np.array(data['Y'])
data_r = np.array(data['R'])
movie_name = open('movie_ids.txt').read().splitlines()


def Train_Parameter(alpha, feature, data_y, data_r):
    '''初始化变量'''
    n_m = data_y.shape[0]  # 电影的数量
    n_u = data_y.shape[1]  # 用户的数量
    x = tf.Variable(tf.random_uniform([n_m,feature]),'x')
    theta = tf.Variable(tf.random_uniform([feature,n_u]),'theta')
    y = tf.placeholder(tf.float32,[n_m,n_u])
    r = tf.placeholder(tf.float32, [n_m, n_u])
    predict_y = tf.matmul(x,theta)*r

    '''均值归一化data_y'''
    miu = np.sum(data_y, axis=1, keepdims=True)/len(data_y[0,:])
    data_y = data_y - miu

    '''计算平方差'''
    square_error = tf.sqrt(tf.reduce_sum((predict_y-y)**2))

    '''梯度下降'''
    train_test = tf.train.AdamOptimizer(alpha).minimize(square_error)

    '''写入Tensorboard'''
    writer = tf.summary.FileWriter('log',graph=tf.get_default_graph())
    with tf.name_scope("Loss"):
        tf.summary.scalar("Loss",square_error)
    merged = tf.summary.merge_all()

    '''开始训练'''
    saver = tf.train.Saver()
    with tf.Session() as sess:
        tf.global_variables_initializer().run()
        for i in range(1000):
            _,summary,loss = sess.run([train_test,merged,square_error],{y:data_y, r:data_r})
            writer.add_summary(summary,i)
            print(loss)
        #保存参数
        saver.save(sess,'Parameter/model.ckpt',global_step=1000)
        np.save('Parameter/miu.npy', miu)
        print("模型参数成功保存!")


'''开始推荐'''
def Recommendation(data_y):
    n_m = data_y.shape[0]
    n_u = data_y.shape[1]

    '''读入参数'''
    x = tf.Variable(tf.random_uniform([n_m,feature]),'x')
    theta = tf.Variable(tf.random_uniform([feature,n_u]),'theta')
    saver = tf.train.Saver()
    with tf.Session() as sess:
        saver.restore(sess, 'Parameter/model.ckpt-1000')
        x,theta = sess.run([x,theta])
    miu = np.load('Parameter/miu.npy')
    matirx = np.matmul(x,theta)+miu

    '''
    #得到我对每部电影的评分
    score = np.matmul(My_theta,x.transpose())
    #排序
    origin_list = []
    for i in score[0]:
        origin_list.append(i)
    score.sort()
    sorted_list = []
    for i in range(feature):
        sorted_list.append(origin_list.index(score[0][-(i+1)]))
    print("推荐给你的10部电影:")
    for i in sorted_list:
        print(movie_name[i]+": "+str(origin_list[i]))
    '''

if __name__ == '__main__':
    '''可变参数'''
    feature = 18  # 代表一部电影用来表示的特征数量
    alpha = 0.02  # 学习率
    #Train_Parameter(alpha, feature, data_y, data_r)
    #定义我的偏好矩阵
    My_theta = np.array([[0.5,0.8,0.6,0.9,0.1,0.7,0.1,0.9,-0.2,-0.1,0.4,0.2,0.9,0.7,-0.1,0.5,0.2,0.3]])
    Recommendation(data_y)




