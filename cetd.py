
from bs4 import BeautifulSoup
from bs4 import NavigableString
from bs4.element import Comment
import math
from functools import reduce 

class ContentExtraction:

    EXCLUDE_TAGS = ("script", "style")

    def extract_content(self, root_node):
        # calc ctdds
        pass

    def get_nodes(self):
        return self._nodes

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
                ctdds = self._calc_ctdds_dfs(child)

                if not isinstance(child, NavigableString):
                    if isinstance(child, Comment) or \
                        child.name in self.EXCLUDE_TAGS:
                        continue

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

            self._nodes.append((node, ds, td))

            print("%s %d %d %d %d %f %f" % (node.name, t, c, lt, lc, td, ds))

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

