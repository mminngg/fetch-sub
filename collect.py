import base64
import re
import traceback

import requests
import yaml
from bs4 import BeautifulSoup


def build_request(hearder=None):
    http_proxy = {}
    request = requests.session()
    if hearder:
        request.headers.update(hearder)
    request.proxies.update(http_proxy)
    return request

t=set()
node_list=set()

def scrape_node(url):
    try:
        # 发送HTTP请求
        response = build_request().get(url, timeout=2)
        response.raise_for_status()  # 检查请求是否成功
        # 解析HTML内容
        soup = BeautifulSoup(response.text, 'html.parser')
        messages = soup.find_all('div', attrs={'class': 'tgme_widget_message_text js-message_text'})
        node_num=0
        reg = r'((vless|vmess|trojan|ss|ssr|hysteria)://[^\s]+)'
        for message in messages:
            text=message.get_text(separator=' ')
            # print(text)
            nodes=re.findall(reg,text)
            node_num+= len(nodes)
            for node in nodes:
                node_list.add(node[0])
                # print(node[0])
                pass
        if node_num==0:
            t.add(url)
        return
    except requests.RequestException as e:
        print(f"请求错误: {e}")
        return
    except Exception as e:
        print(f"处理错误: {e}")
        traceback.print_exc()
        return



def load_config(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        # 使用 yaml.safe_load() 加载文件内容
        # safe_load() 比 load() 更安全，因为它只解析有限的 YAML 标签
        # 避免执行恶意代码
        data = yaml.safe_load(file)
        url_list=data.get('tgchannel')
        for url in url_list:
            url='https://t.me/s/'+url.replace('https://t.me/','')
            scrape_node(url)


def get_valid_nodes():
    url = 'https://raw.githubusercontent.com/mminngg/speed-test/refs/heads/master/output/base64.txt'
    try:
        response = build_request().get(url)
        response.raise_for_status()
        text=response.text
        text=base64.b64decode(text).decode("utf8").strip()
        text='\n'.join(line for line in text.splitlines() if line.strip())
        return text
    except requests.RequestException as e:
        print(f"请求错误: {e}")
        return ''

if __name__ == "__main__":
    load_config('./config.yaml')
    print('-------')
    for url in t:
        print(url)
    with open('valid_content_all.txt','w+',encoding='utf8') as f:
        # for n in f:
        #     node_list.add(n.strip())
        # f.seek(0)
        text=get_valid_nodes()
        f.write(text)
        f.write('\n')
        for node in node_list:
            f.write(node)
            f.write('\n')




