import re
def cut_sent(input):
    lines = []
    i = 0
    line = ""
    while i < len(input):
        if input[i] == "「":
            if len(line) > 0:
                lines.append(line)
                line = ""
            line += input[i]
            i += 1
            while i < len(input) and input[i] != "」":
                line += input[i]
                i += 1
            if i < len(input):
                line += input[i]
            lines.append(line)
            line = ""
        else:
            line += input[i]
        i += 1
    if len(line) > 0:
        lines.append(line)
    sents = []
    for line in lines:
        if line.startswith("「"):
            if len(sents) > 0 and not re.match("[。！？\?]", sents[-1][-1]):
                sents[-1] += line
            else:
                sents.append(line)
        elif len(line) > 0:
            line = re.sub('([。！？\?])([^”’」』])', r"\1\n\2", line)  # 单字符断句符
            line = re.sub('(\.{6})([^”’」』])', r"\1\n\2", line)  # 英文省略号
            line = re.sub('(\…{2})([^”’」』])', r"\1\n\2", line)  # 中文省略号
            line = re.sub('([。！？\?][”’」』])([^，。！？\?])', r'\1\n\2', line)
            # 如果双引号前有终止符，那么双引号才是句子的终点，把分句符\n放到双引号后，注意前面的几句都小心保留了双引号
            line = line.rstrip()  # 段尾如果有多余的\n就去掉它
            # 很多规则中会考虑分号;，但是这里我把它忽略不计，破折号、英文双引号等同样忽略，需要的再做些简单调整即可。
            lines = [line for line in line.split("\n") if len(line) > 0]
            if len(lines) > 0 and len(sents) > 0 and re.search("[^。！？\?][”’」』]$", sents[-1]):
                sents[-1] += lines[0]
                sents.extend(lines[1:])
            else:
                sents.extend(lines)
    return sents

from os import listdir
from os.path import isfile, join
dump_file_paths = [f"dump/{f}" for f in listdir("dump") if isfile(join("dump", f))]

import json
from tqdm import tqdm

# https://stackoverflow.com/a/19016117/6798201
import unicodedata
def remove_control_characters(s):
    return "".join(ch for ch in s if unicodedata.category(ch)[0]!="C")

with open("sentences.txt", "w+") as output_file:
    for dump_file_path in tqdm(dump_file_paths):
        # print(f"Processing {dump_file_path}")
        with open(dump_file_path, "r") as input_file:
            for line in input_file.read().splitlines():
                try:
                    article = json.loads(remove_control_characters(line))
                except:
                    print("One line failed to parse")
                for sent in cut_sent(article["text"]):
                    output_file.write(sent + "\n")
    output_file.flush()
