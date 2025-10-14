from analz.soc_econ.wv_data_2025_utils import WVGDP_2025
from analz.utils.GDPTree import TNode, TNTree
import pandas as pd
import itertools

class Node:
    def __init__(self, linecode, description, lscount):
        self.LineCode = linecode
        self.description = description
        self.space_count = lscount
        self.next = None
        self.prev = None


class DLL:
    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.tuples = self.get_tuples()
        self.head = None
        self.tail = None
        self.build_dl_list()

    def get_tuples(self):
        ld_tuples = self.df.apply(lambda row: (row.LineCode,
                                               row.Description,
                                               DLL.count_leading_spaces(row.Description)),
                                  axis=1)
        return ld_tuples

    def append(self, linecode, description, lscount ):
        new_node = Node(linecode, description, lscount )
        if not self.head:
            self.head = new_node
            self.tail = new_node
        else:
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node

    def prepend(self, linecode, description, lscount ):
        new_node = Node(linecode, description, lscount )
        if not self.head:
            self.head = new_node
            self.tail = new_node
        else:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node

    def insert_after(self, target_data, data):
        new_node = Node(data)
        current = self.head
        while current:
            if current.LineCode == target_data.LineCode:
                new_node.next = current.next
                new_node.prev = current
                if current.next:
                    current.next.prev = new_node
                else:
                    self.tail = new_node
                current.next = new_node
                return
            current = current.next

    def delete(self, node_to_delete: Node):
        current = self.head
        while current:
            if current.LineCode == node_to_delete.LineCode:
                if current.prev:
                    current.prev.next = current.next
                else:
                    self.head = current.next
                if current.next:
                    current.next.prev = current.prev
                else:
                    self.tail = current.prev
                return
            current = current.next

    def traverse_forward(self):
        current = self.head

        while current:
            print(current.LineCode, end=" <-> ")
            current = current.next
        print("None")

    def traverse_backward(self):
        current = self.tail
        while current:
            print(current.LineCode, end=" <-> ")
            current = current.prev
        print("None")

    @classmethod
    def count_leading_spaces(cls, text):
        return int(sum(1 for _ in itertools.takewhile(str.isspace, text))/2)


    def build_dl_list(self):
        for d in self.tuples:
            # transform eah tuple into a Node for insertion into a DoublyLinkedList
            linecount, description, ls_count = d
            self.append(linecount, description, ls_count)




    def get_node_layers(self):
        from collections import Counter


        keys = [0,1,2,3,4,5,6]
        default_value = []

        skeys = [str(k) for k in keys]
        layer_counter = Counter(skeys)
        layers = {k: default_value for k in keys}



        current = self.head
        while current:
            sc = current.space_count
            print(f'Current space_count: {sc}, Current  LineCode: {current.LineCode}, Current Description: {current.description}')

            layers[sc].append(current)
            layer_counter.update(str(current.space_count))
            current = current.next
        return layers, layer_counter


