import json

# Функция парсинга JSON и запись дерева в виде таблицы связей
def parse_tree(json_data, parent=None, relations=None):
    if relations is None:
        relations = []

    for node, children in json_data.items():
        if parent is not None:
            relations.append((parent, node))  
        if isinstance(children, dict):
            parse_tree(children, node, relations)
    
    return relations

# Функция получения братьев узла
def get_siblings(relations, node):

    parent = None
    for relation in relations:
        if relation[1] == node:
            parent = relation[0]
            break
    
    if parent is None:
        return []  

    siblings = [relation[1] for relation in relations if relation[0] == parent and relation[1] != node]
    return siblings

# Функция получения потомков узла
def get_descendants(relations, node):
    descendants = []
    children = [relation[1] for relation in relations if relation[0] == node]

    for child in children:
        descendants.append(child)
        descendants.extend(get_descendants(relations, child))
    
    return descendants


with open('./test.json', 'r') as file:
    tree = json.load(file)

# Парсим дерево
relations = parse_tree(tree)

# Вывод таблицы связей
print("Таблица связей:")
print(relations)

# Получение братьев и потомков для узла 3
node = "3"
print(f"Братья узла {node}: {get_siblings(relations, node)}")
print(f"Потомки узла {node}: {get_descendants(relations, node)}")
