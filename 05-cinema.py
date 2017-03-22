import json

def readData(dataFileName = 'cinemadata.txt'):
    f = open(dataFileName, 'r', encoding='utf-8')
    data = f.read()
    f.close()
    return data

def pretifyDataAndSave(data):
    '''
    将data美化并且存为json文件
    :param data: python object, 这里为dict
    '''
    with open('cinemadata.json', 'w', encoding='utf-8') as fout:
        fout.write(json.dumps(data, ensure_ascii=False, sort_keys=True, indent=4))     # ensure_ascii=False: 将unicode转中文

def parseData(data):
    data = data['locations']['List']
    for districts in data:
        print(districts)

def main():
    data = json.loads(readData())
    #pretifyDataAndSave(data)
    # 解析、处理data
    parseData(data)

if __name__ == '__main__':
    main()
    