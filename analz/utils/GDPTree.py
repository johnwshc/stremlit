
from collections import namedtuple
from analz.utils.wv_data_2025_utils import WVGDP_2025

GIndex = namedtuple('GIndex',['id', 'level'])



#%%

class TupsDict:

    def __init__(self):

        self.wvgdp = WVGDP_2025()
        self.dff = self.wvgdp.dff
        self.dff.LineCode = self.dff.LineCode.apply(lambda x: int(x))  #  convert LinCode to type int
        self.dff['tups'] = self.dff.apply(lambda row: GIndex(row.LineCode, row.layer), axis=1)  # create df.tups varable
        self.tups = list(self.dff.tups.copy(deep=True))
        self.tups_ddict = {}
        for t in self.tups:  #  init tuples_dictionary
            tid = t.id
            level = t.level
            child_ids = []
            self.tups_ddict[tid] = {'level': level, 'child_ids': child_ids}
            child_ids  = self.get_child_ids(t)
            self.tups_ddict[tid]['child_ids'] = child_ids


    def get_child_ids(self, par: GIndex):  # with parent at top of stack list
        cids = []
        for t in self.tups:
            if t.id == par.id:
                ptups = self.tups[t.id:]
                for c in ptups:
                    if c.level <= par.level:
                        return cids
                    elif c.level > par.level + 1:
                        continue
                    elif c.level == par.level + 1: # this is child
                        cids.append(c.id)
                        continue
                    else:

                        return cids
                return cids
        return cids

    def updateChildIds(self, par):
        cids = self.get_child_ids(par)
        self.td[par.id]['child_ids'] = cids

    def get_num_children(self, id):
        return len(self.tups_ddict.get(id).get('child_ids', []))

    def get_level(self, id):
        lev = self.tups_ddict.get(id, None).get('level', None)
        return lev
#%%
# usage:   tdd = TupsDict(tups, tups_ddict)


class TNode:


    def __init__(self, id: int, level: int, child_ids: list):
        self.level = level
        self.id = id
        self.parent = None
        if child_ids:
            self.child_ids = child_ids
        else:
            self.child_ids = []
        self.children = []

    def has_children(self):
        if self.child_ids:
            return True
        else:
            return False


    def find_parent(self, tup: tuple):
        pass

    def setParent(self, parent):
        self.parent = parent

    def add_children(self, data_dict: TupsDict):
        for c in self.child_ids:

            cdata = data_dict.tups_ddict.get(c, None)
            level = cdata.get('level', None)
            chids = cdata.get('child_ids', [])


            child = TNode(c, level, chids)
            child.parent = self
            self.children.append(child)
            child.add_children(data_dict)




    def __str__(self):
        pid = self.parent.id if self.parent else None
        return f"Level: {self.level}, ID: {self.id}, Parent: {pid}, num_children: {len(self.child_ids)}"


class TNTree:

    @classmethod
    def buildTNTreeFactory(cls, td: TupsDict):
        ids = [id for id in td.tups_ddict.keys()]
        root_id = ids[0]
        root_level = td.tups_ddict.get(root_id).get('level', None)
        root_child_ids = td.tups_ddict.get(root_id, None).get('child_ids', [])
        rnode = TNode(root_id, root_level, root_child_ids)
        rnode.child_ids = td.tups_ddict.get(root_id).get('child_ids', [])
        rnode.children = []
        tnt = TNTree(rnode, td)

        return tnt
            

    def __init__(self, rnode: TNode, td: TupsDict):
        self.root = rnode
        self.tups = td

    def __str__(self):
        return f"Tree: {self.root}"

    def traverse(self, node: TNode, level=0):
        if node:
            print(f"id is {node.id}")
            for child in node.children:
                self.traverse(child, level + 1)
        else:
            print(f"done")

    def find_node(self, node, target_id):
        if node is None:
            return None
        if node.id == target_id:
            return node
        for child in node.children:
            r =  self.find_node(child, target_id)
            if isinstance(r, TNode):
                return r
        return None

    def find_layer(self, node:TNode, level: int, lnodes: list):
        if node is None:
            return lnodes
        if node.level == level:
            lnodes.append(node)
        for child in node.children:
            self.find_layer(child, level, lnodes)
        return lnodes

    def find_subtree(self, node: TNode, target_id: int):
        tnode = self.find_node(node, target_id)
        tnt = TNTree(tnode, self.tups)
        tnt.root.parent = None
        return tnt

    def copy_tree(self, node):
        if node is None:
            return None

        # Create a new node with the same value
        new_node = TNode(node.id, node.level, node.child_ids)
        new_node.parent = node.parent
        new_node.children = node.children


        # Recursively copy all children
        for child in node.children:
            new_node.children.append(self.copy_tree(child))

        return new_node
























