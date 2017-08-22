# -*- coding: utf-8 -*-

import MeCab

mc = MeCab()

text = "私は納豆が好き"

print(mc.parse(text))
