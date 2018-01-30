#coding=utf-8


#------------
from sklearn import datasets,cross_validation,naive_bayes
import matplotlib.pyplot as plt 

# 可视化手写识别数据集Digit Dataset

def show_digits():
	digits=datasets.load_digits()
	fig=plt.figure()
	for i in xrange(20):
		ax=fig.add_subplot(4,5,i+1)
		ax.imshow(digits.images[i], cmap = plt.cm.gray_r, interpolation='nearest') 
	plt.show()


def load_data():
	digits=datasets.load_digits()
	return cross_validation.train_test_split(digits.data,digits.target,random_state=0)


#show_digits()  


def test_GaussianNB(*data):
    X_train, X_test, y_train, y_test = data
    cls = naive_bayes.GaussianNB()
    cls.fit(X_train, y_train)
    print('GaussianNB Classifier')
    print('Training Score: %.2f' % cls.score(X_train, y_train))
    print('Test Score: %.2f' % cls.score(X_test, y_test))
    


def test_MultinomialNB(*data):
    X_train, X_test, y_train, y_test = data
    cls = naive_bayes.MultinomialNB()
    cls.fit(X_train, y_train)
    print('MultinomialNB Classifier')
    print('Training Score: %.2f' % cls.score(X_train, y_train))
    print('Test Score: %.2f' % cls.score(X_test, y_test))
 


def test_BernoulliNB(*data):
    X_train, X_test, y_train, y_test = data
    cls = naive_bayes.BernoulliNB()
    cls.fit(X_train, y_train)
    print('BernoulliNB Classifier')
    print('Training Score: %.2f' % cls.score(X_train, y_train))
    print('Test Score: %.2f' % cls.score(X_test, y_test))


if __name__ == '__main__':
	

	X_train, X_test, y_train, y_test = load_data()
	
	test_GaussianNB(X_train, X_test, y_train, y_test)
	#X_train, X_test, y_train, y_test = load_data()
	test_MultinomialNB(X_train, X_test, y_train, y_test)    
	#X_train, X_test, y_train, y_test = load_data()
	test_BernoulliNB(X_train, X_test, y_train, y_test)
	cls = naive_bayes.BernoulliNB()
	print cls.fit(X_train, y_train)
	print('Test Score: %.2f' % cls.score(X_test, y_test))
	
	cls.fit(X_test, X_test)
	print('Test Score: %.2f' % cls.score(X_test, y_test))

	
		

