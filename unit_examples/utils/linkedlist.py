

class Stack():
	"""堆栈"""
	def __init__(self, max_size):
		self.max_size = max_size
		self.arr = []

	def counts(self):
		return len(self.arr)

	def push(self, item):
		if len(self.arr) == self.max_size:
			print('数据已满，不能存入')
			return None
		self.arr.insert(0, item)
		print('%s存入成功'%item)

	def pull(self):
		return self.arr.pop()

	def full(self):
		if len(self.arr) == self.max_size:
			print('Is Full!!')
		else:
			print('Not Full!!')

	def index_of(self, index):
		return self.arr[index]

	def replace(self, index, item):
		self.arr[index] = item
		print('Done!!')

	def delete(self, index):
		del self.arr[index]


s = Stack(5)
s.counts()


class Node():
	"""地址"""
	def __init__(self, value):
		self.value = value
		self.next = None
		self.head = False
		self.end = False


class LinlkedList():
	"""链表"""
	def __init__(self):
		self.arr = []

	def initlist(self, item):
		node = Node(item[0])
		self.arr.append(node)
		next = node.next
		node.head = True
		for x in range(1,len(item)):
			node = Node(item[x])
			self.arr.append(node)
			node.next = next
			next = node.next
			if x == len(item) - 1:
				node.end = True
		print('创建链表成功！')

	def counts(self):
		print('长度为%s' % len(self.arr))

	def add(self, item):
		node = Node(item)
		node.end = True
		self.arr.append(node)
		self.arr[-2].end = False
		self.arr[-2].next = node
		print('添加成功')

	def index_of(self, index):
		print(self.arr[index].value)

	def remove_item(self, item):
		remove_list = []
		for x in range(len(self.arr)):
			if item == self.arr[x].value:
				self.arr[x-1].next = self.arr[x+1]
				remove_list.append(x)
		for y in remove_list:
			del self.arr[y]
		print('%s删除成功！' % item)

	def remove_all(self):
		self.arr = []
		print('删除全部，成功！')

	def remove_index(self, index):
		if index == 0:
			self.arr[1].head = True
			print('删除成功')
			return None
		elif index == len(self.arr) - 1:
			self.arr[-2].end = True
			print('删除成功')
			return None
		del self.arr[index]
		self.arr[index-1].next = self.arr[index]
		print('删除成功')
		return None

	def update_item(self, item1, item2):
		for x in range(len(self.arr)):
			if item1 == self.arr[x].value:
				self.arr[x].value = item2
				print('修改成功！')
				break

	def look(self):
		total = [x.value for x in self.arr]
		print(total)


l = LinlkedList()
l.initlist([1,2,3,4,5,6])


class Location():
	def __init__(self, value):
		self.value = value
		self.next = None


class LinkTable():
	"""链表没有列表"""
	def __init__(self):
		self.head = Location('head')
		self.end = Location('end')
		self.head.next = self.end

	# def add(self, item):
	# 	obj = Location(item)
	# 	loc = self.head
	# 	while loc.next != self.end:
	# 		loc = loc.next
	# 	loc.next = obj
	# 	obj.next = self.end
	# 	print('添加成功')
	def add(self, item):
		self.insert(self.counts(), item)

	def insert(self, index, item):
		obj = Location(item)
		loc = self.head
		count = 0
		while count != index:
			loc = loc.next
			count += 1
		obj.next = loc.next
		loc.next = obj
		print('添加成功')

	def counts(self):
		count = 0
		obj = self.head
		while obj.next.value != 'end':
			obj = obj.next
			count += 1
		# print('长度为%d'%count)
		return count

	def update(self, item1, item2):
		loc = self.head
		while loc.value != item1:
			loc = loc.next
		loc.value = item2
		print('修改成功')

	def index_of(self, index):
		loc = self.head
		count = 0
		while count != index:
			loc = loc.next
		print(loc.value)

	def remove_by_index(self, index):
		loc = self.head
		count = 0
		while count != index:
			loc = loc.next
			count += 1
		a = loc.next
		loc.next = loc.next.next
		print('删除成功')

	def remove_by_item(self, item):
		loc = self.head
		count = 0
		while loc.next.value != item:
			loc = loc.next
			count += 1
		loc.next = loc.next.next
		print('删除成功')

	def look(self):
		loc = self.head.next
		while loc.value != 'end':
			print(loc.value, end=' ')
			loc = loc.next






li = LinkTable()
li.add(100)
li.add(999)
li.add(666)
li.add(222)
li.remove_by_index(0)
li.look()
li.counts()

def func1():
	print('func1')

def func2():
	print('func2')

def func3():
	print('func3')


d = {'a': func1, 'b': func2, 'c': func3}
d.get('a')()





