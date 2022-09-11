#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re


def count():
    """
    Count the number of CJK characters and
    unique Cantonese characters in the dump
    """
    cjk = 0
    canto = 0
    dump_dir = "dump/"
    for filename in os.listdir(dump_dir):
        with open(dump_dir + filename, "r") as f:
            for line in f:
                canto += sum(
                    m.span()[1] - m.span()[0] + 1
                    for m in re.finditer(canto_unique, line)
                )
                for cp in line:
                    if is_cjk_cp(ord(cp)):
                        cjk += 1
    return (cjk, canto)


canto_unique = re.compile(
    r"[嘅嗰啲咗佢喺咁噉冇啩哋俾畀嚟諗乜嘢閪撚𨳍瞓睇㗎餸𨋢摷喎嚿噃嚡嘥嗮啱揾喐逳噏𢳂岋糴㨃揈撳𥄫攰癐冚孻冧𡃁嚫跣𨃩瀡氹尐㩒𡁵滮誃僆]|"
    + r"[唔毋嘸][係得會好識使洗駛通知到去走]|點[樣會做得]|[琴尋]日|[而依]家|今[下陣]|而今|[真就]係|[邊焉爾][度道個]|[嚇凍冷攝整揩逢淥浸激]親|[我你佢渠][哋地等]|[橫搞打傾諗攞通得唔拆]掂|[冚咸][家屋]"
    + r"屋企|收皮|[邊焉]科"
)


def is_cjk_cp(cp):
    return (
        (0x3400 <= cp <= 0x4DBF)
        or (0x4E00 <= cp <= 0x9FFF)
        or (0xF900 <= cp <= 0xFAFF)
        or (0x20000 <= cp <= 0x2FFFF)
    )


if __name__ == "__main__":
    (cjk, canto) = count()
    print("CJK characters: {:,}".format(cjk))
    print(
        "Unique Cantonese characters: {:,} ({:,}% of all CJK characters)".format(
            canto, round(canto / cjk * 100)
        )
    )
