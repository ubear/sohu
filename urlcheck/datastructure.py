#!/usr/bin/env python
# -*- coding=utf8 -*-

# url and its type
class Node(object):
    LINK_A = 1
    LINK_OHTER = 0

    def __init__(self, link, hyperlink_type=LINK_A):
        self.link = link
        self.hypertype = hyperlink_type # <a> or <other>

