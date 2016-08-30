# coding=utf-8
import heapq
import random


class TopkHeap(object):
    def __init__(self, k):
        self.k = k
        self.data = []

    def push(self, elem, greater):
        if len(self.data) < self.k:
            heapq.heappush(self.data, elem)
        else:
            topk_small = self.data[0]
            if greater(elem, topk_small):
                heapq.heapreplace(self.data, elem)

    def topk(self):
        return [x for x in reversed([heapq.heappop(self.data) for x in xrange(len(self.data))])]


if __name__ == "__main__":
    print "Hello"
    list_rand = random.sample(xrange(1000000), 100)
    th = TopkHeap(3)
    for i in list_rand:
        th.push(i, lambda x,y: x > y)
    print th.topk()
    print sorted(list_rand, reverse=True)[0:3]