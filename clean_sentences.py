from functools import lru_cache
from typing import Optional
import re
from Levenshtein import distance as levenshtein_distance

redundant_paren = re.compile(r"（.*[^\u4e00-\u9fff]*.*）")
chinese_char = re.compile(r"[\u4e00-\u9fff]")
zing_zis = re.compile(r"尐|爾個|爾件|爾間|爾道|爾種")
punctuations = {'@', '#', '$', '%', '^', '&', '*', '·', '…', '‥', '—', '～', '~', '`', '!',  '(', ')', '-', '_', '{', '}', '[', ']', '|', '\\', ':', ';',
            '"', '\'', '<', '>', ',', '.', '?', '/',
            '！', '：', '；', '“', '”', '‘', '’', '【', '】', '（', '）',
            '「', '」', '﹁', '﹂', '『','』', '《', '》', '？', '，', '。', '、', '／', '＋',
            '〈','〉', '︿', '﹀', '［', '］', '‧'}
alphanum = re.compile(r"[a-zA-Z0-9]")

def filter_punctuations(s: str) -> str:
    return "".join(c for c in s if c not in punctuations)

@lru_cache(maxsize=200)
def filter_alnum(s: str) -> str:
    return "".join(c for c in s if not alphanum.match(c))

def filter_sent(s: str) -> Optional[str]:
    s = redundant_paren.sub("", s)
    if len(s) <= 5:
        return None
    elif len(chinese_char.findall(s)) / len(s) < 0.5:
        return None
    elif not chinese_char.match(s):
        return None
    elif any(not chinese_char.match(c) and not c.isalnum() for c in filter_punctuations(s)):
        return None
    elif s.endswith("，") or s.endswith("."):
        return None
    elif "「」" in s or "『』" in s or "《》" in s or "【】" in s or "()" in s:
        return None
    elif zing_zis.search(s) is not None:
        return None
    elif s.endswith("可以係：") and len(s) <= 10:
        return None
    else:
        return s

from tqdm import tqdm

with open("sentences.txt", "r") as input_file, open("filtered_sentences.txt", "w+") as output_file:
    filtered_lines = []
    for line in tqdm(input_file.read().splitlines()):
        filtered = filter_sent(line)
        if filtered is not None:
            found_similar_line = False
            filtered_no_alnum = filter_alnum(filtered)
            for prev_line in filtered_lines[-100:]:
                if levenshtein_distance(filter_alnum(prev_line), filtered_no_alnum) <= len(prev_line) * 0.1:
                    found_similar_line = True
                    break
            if not found_similar_line:
                filtered_lines.append(filtered)
    for line in filtered_lines:
        output_file.write(line + "\n")
