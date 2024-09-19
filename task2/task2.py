import json
import numpy as np
import pandas as pd

def parse_tree(json_data, parent=None, relations=None):
    if relations is None:
        relations = []

    for node, children in json_data.items():
        if parent is not None:
            relations.append((parent, node))  
        if isinstance(children, dict):
            parse_tree(children, node, relations)
    
    return relations

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

def get_descendants(relations, node):
    descendants = []
    children = [relation[1] for relation in relations if relation[0] == node]

    for child in children:
        descendants.append(child)
        descendants.extend(get_descendants(relations, child))
    
    return descendants

def get_ancestors(relations, node):
    ancestors = []
    parent = [relation[0] for relation in relations if relation[1] == node]

    if parent:
        ancestors.append(parent[0])
        ancestors.extend(get_ancestors(relations, parent[0]))
    
    return ancestors

def task(relations):
    nodes = sorted({relation[0] for relation in relations}.union({relation[1] for relation in relations}))
    matrix = np.zeros((5, len(nodes)))
    
    for i, node in enumerate(nodes):
        # r1
        immediate_children = [relation[1] for relation in relations if relation[0] == node]
        matrix[0, i] = len(immediate_children)
        
        # r2
        immediate_parents = [relation[0] for relation in relations if relation[1] == node]
        matrix[1, i] = len(immediate_parents)
        
        # r3
        all_descendants = get_descendants(relations, node)
        matrix[2, i] = len(all_descendants) - len(immediate_children) 
        
        # r4
        all_ancestors = get_ancestors(relations, node)
        matrix[3, i] = len(all_ancestors) - len(immediate_parents)
        
        # r5
        siblings = get_siblings(relations, node)
        matrix[4, i] = len(siblings)
    
    return matrix, nodes

with open('./task2/test2.json', 'r') as file:
    tree = json.load(file)

relations = parse_tree(tree)
relation_matrix, nodes = task(relations)
row_labels = ['r1: Непосредственное управление', 
              'r2: Непосредственное подчинение', 
              'r3: Опосредованное управление', 
              'r4: Опосредованное подчинение', 
              'r5: Соподчинение на одном уровне']
df = pd.DataFrame(relation_matrix.astype(int), index=row_labels, columns=nodes)

print(df)