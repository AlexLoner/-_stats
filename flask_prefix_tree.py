from flask import Flask, request, jsonify, g
import json
import pandas as pd
import re

app = Flask(__name__)
class PrefixTree:
    
    def __init__(self):
        self.tree = [{}]
    
    def insert(self, key):
        '''
        Добавляет key в дерево
        '''
        if not self.check(key):
            mas = self.tree
            for i in key:
                if i in mas[0]:
                    mas = mas[0][i]
                else:
                    mas[0][i] = [{}]
                    mas = mas[0][i]
            mas.append(1)
    
    def check(self, key, check_only=True):
        '''Проверяет присутствует ли  строка в дереве. Если increase = True Увеличивает число обращаение по данной строке на 1'''
        mas = self.tree
        for i in key:
            if i not in mas[0]:
                return False
            else:
                mas = mas[0][i]
        if len(mas) != 1:
            mas[1] += 1
            return True if check_only else (True, mas[1])
        else:
            return False

    def check_part(self, key):
        '''Проверяет наличие подстроки в дереве'''
        mas = self.tree
        for i in key:
            if i not in mas[0]:
                return False
            else:
                mas = mas[0][i]
        return True 

    
    def top_10(self, key):
        
        def f(m, key):
            num = 0
            w = ''
            top = {}
            for i in m[0]:
                if self.check(key + i):
                    num = m[0][i][1]
                    w = key + i
                temp = f(m[0][i], key + i)
                if temp != (0, ''):
                    d[temp[1]] = temp[0]
            return num, w
        m = self.tree
        for i in key:
            m = m[0][i]
        d = dict()
        f(m, key)
        top = [(v, k) for k, v in d.items()]
        top.sort(reverse=True)
        return top[:10]
            
            
def init_prefix_tree(filename):
    #TODO в данном методе загружаем данные из файла. Предположим вормат файла "Строка, чтобы положить в дерево" \t "json значение для ноды" \t частота встречаемости
    filename = 'data'
    data = pd.read_csv(filename, sep="@")
    baobab = PrefixTree()
    for sets in [data.Abstract, data.Title]:
        for row in sets:
            items = re.findall('[a-zA-Z]+', row) # Оставляем только буквы
            for item in items:
                if len(item) > 3:
                    baobab.insert(item.lower())
    return baobab


@app.route("/get_sudgest/<string>", methods=['GET', 'POST'])
def return_sudgest(string):
    #TODO по запросу string вернуть json, c топ-10 саджестами, и значениями из нод  
    tree = init_prefix_tree('data')
    try: 
        res = tree.top_10(string)
    except: 
        res = "Nothing was found"
    return json.dumps(res)

@app.route("/")
def hello():
    return 'Hi there. Try ~/get_sudgest/<string>'
    
if __name__ == "__main__":
    app.run()