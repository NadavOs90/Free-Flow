

class Hanoi(object):
    def __init__(self, size=3):
        self.size = size
        self.left = range(size)
        self.mid = []
        self.right = []

    def print_towers_locations(self, index):
        if isinstance(index, int):
            print 'Index:', index
        else:
            print 'Index:', int(index[::-1], 2)
        for i in range(self.size):
            try:
                left = self.left[i]
            except IndexError:
                left = '-'
            try:
                mid = self.mid[i]
            except IndexError:
                mid = '-'
            try:
                right = self.right[i]
            except IndexError:
                right = '-'
            print (left, mid, right)
        # print self.left, self.mid, self.right

    def move(self, i):
        if i in self.right:
            if self.left == [] or self.left[0] > i:
                self.left = [self.right.pop(0)] + self.left
            else:
                self.mid = [self.right.pop(0)] + self.mid
        elif i in self.mid:
            if self.right == [] or self.right[0] > i:
                self.right = [self.mid.pop(0)] + self.right
            else:
                self.left = [self.mid.pop(0)] + self.left
        elif i in self.left:
            if self.mid == [] or self.mid[0] > i:
                self.mid = [self.left.pop(0)] + self.mid
            else:
                self.right = [self.left.pop(0)] + self.right

    def to_bin_reversed(self, num):
        ans = '0:0{}b'.format(self.size)
        ans = '{' + ans + '}'
        ans = ans.format(num)
        return ans[::-1]

    def solve_iteratively(self):
        index = self.to_bin_reversed(0)
        while len(self.right) < self.size:
            self.print_towers_locations(index)
            next_index = self.to_bin_reversed(int(index[::-1], 2) + 1)
            if len(next_index) > len(index):
                index = '0' + index
            for i in range(len(next_index)):
                if next_index[i] == '1' and index[i] == '0':
                    self.move(i)
            index = next_index
        self.print_towers_locations(index)

    def solve_recursively(self):
        n = self.size
        index = 0
        self.tower(n, self.left, self.mid, self.right, index)

    def tower(self, n, t_from, t_aux, t_to, index):
        if n == 0:
            self.move_rec(t_from, t_to, index)
            self.print_towers_locations(index)
            return
        self.tower(n-1, t_from, t_to, t_aux, index+1)
        self.move_rec(t_from, t_to, index)
        self.tower(n-1, t_aux, t_from, t_to, index+1)

    def move_rec(self, t_from, t_to, index):
        self.print_towers_locations(index)
        t_to = [t_from.pop(0)] + t_to


# Hanoi(5).solve_iteratively()
Hanoi(5).solve_recursively()