# encoding: utf8
from bs4 import BeautifulSoup
from bs4 import NavigableString
from bs4.element import Comment
import math
from functools import reduce 

class ContentExtraction:

    EXCLUDE_TAGS = ("script", "style")

    def extract_content(self, root_node):

        # calc ctdds
        self.calc_composite_text_density_with_density_sum(root_node)

        threshold_node = max(self._nodes, key=(lambda x: x.ds))
        
        # calc threshold
        for node in self._generator_parent(threshold_node, root_node):
            if threshold_node.td > node.td:
                threshold_node = node

            # print("%f, %s" % (threshold_node.td, threshold_node.name))

        self._threshold = threshold_node.td

        self._content_text = ""

        # extract_content
        self._mark_content_recursively(threshold_node)

        return threshold_node

    def _mark_content_recursively(self, node):

        if node.td >= self._threshold:
            tag = self._get_max_density_sum_tag(node)

            tag.is_content = True

            for child in node.children:
                if isinstance(child, NavigableString) and \
                        not isinstance(child, Comment):
                    self._content_text += child.strip()

                if isinstance(child, NavigableString) or \
                        not self._is_target_tag(child):
                    continue

                self._mark_content_recursively(child)

        else:
            node.is_content = False


    def get_content_text(self):
        return self._content_text

    def _get_max_density_sum_tag(self, node):

        tmp_node = node

        for child in node.children:
            if isinstance(child, NavigableString) or \
                    not self._is_target_tag(child):
                continue

            if tmp_node.td < child.td:
                tmp_node = child

        return tmp_node

    def _generator_parent(self, node, root_node):    
        tmp_node = node
        while tmp_node != root_node:
            tmp_node = tmp_node.parent
            yield tmp_node

    def get_nodes(self):
        return self._nodes

    def get_threshold(self):
        return self._threshold

    def calc_composite_text_density_with_density_sum(self, root_node):

        # initialize
        ds = 0.0

        self._nodes = []
        self._lc_base = \
            reduce(lambda x, y: x + len(y.get_text(strip=True)),
                    root_node.find_all("a"),
                    0)
        self._c_base = len(root_node.get_text(strip=True))

        # calc ctdds
        ctdds = self._calc_ctdds_dfs(root_node)

        # calc threshold


    calc_ctdds = calc_composite_text_density_with_density_sum

    @classmethod
    def _is_target_tag(cls, node):
        return not (isinstance(node, Comment) or \
                node.name in cls.EXCLUDE_TAGS)


    def _calc_ctdds_dfs(self, node):

        t = 0
        c = 0
        lt = 0
        lc = 0
        ds = 0.0
        td = 0.0

        # calc ctdds
        if isinstance(node, NavigableString):
            if node.parent.name == "a":
                lc += len(node)

            else:
                c += len(node)

        else:
            for child in node.children:
                if not (isinstance(child, NavigableString) or \
                        self._is_target_tag(child)):
                    continue

                ctdds = self._calc_ctdds_dfs(child)

                if not isinstance(child, NavigableString):

                    if child.name == "a":
                        t += ctdds[0] 
                        lt += ctdds[2] + 1
                    else:
                        t += ctdds[0] + 1
                        lt += ctdds[2]

                c += ctdds[1]
                lc += ctdds[3]
                ds += ctdds[4]

            td += self._calc_composite_text_density(
                        t, c, lt, lc)

            node.td = td
            node.ds = ds
            self._nodes.append(node)

            #print("%s %d %d %d %d %f %f" % (node.name, t, c, lt, lc, td, ds))

        return (t, c, lt, lc, td, ds)

    def _calc_composite_text_density(self, t, c, lt, lc):

        if t < 1:
            t = 1

        if c < 1:
            c = 1

        if lc < 1:
            lc = 1

        if lt < 1:
            lt = 1

        if t < 1:
            t = 1

        clc = c - lc
        if clc < 1:
            clc = 1

        x = float(c * t) / (lc * lt)
        base = float(c * lc) / clc + \
            float(self._lc_base * c) / self._c_base + \
            math.exp(1)

        return float(c) * math.log(x, math.log(base)) / float(t)

