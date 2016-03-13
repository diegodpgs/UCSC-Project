class A(object):

	def __init__(self,name):
		self.name = name


class B(A):

	def __init__(self,name,age):
		super(B, self).__init__(name)
		self.age = age

	def hi(self):
		print 'ok'





a1 = A('diego')
b1 = B('pedro',28)

print isinstance(a1,B)
