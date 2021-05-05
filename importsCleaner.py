import re, ast
import argparse
import pprint


def parseCodeLine(line):
    for node in ast.iter_child_nodes(ast.parse(line)):
        if isinstance(node, ast.ImportFrom):
            print('found ImportFrom')
            print('---------------------------')
            print(vars(node))
            print(len(node.names))
            for n in node.names:
                print(vars(n))
            print('---------------------------')
            
            return 2, node
        elif isinstance(node, ast.Import): # excluding the 'as' part of import
            print('found Import')
            print('---------------------------')
            print(vars(node))
            print(len(node.names))
            for n in node.names:
                print(vars(n))
            print('---------------------------')
            
            return 1, node
        else:
            return None
    return None

def addBranch(branch, dictTree):
    levelNames = branch.split('.')
    print(levelNames)

    if len(levelNames) == 1:
        print('Simple Import-----------------------')
        if nodeName.name not in importedModules:
            moduleDict = {
                'asname' : nodeName.asname,
                'refcount' : 1,
                'subs' : []
            }
            importedModules[nodeName.name] = moduleDict
    else: # Multilevel import eg: matplotlib.pyplot
        print('Multilevel Import-----------------------')
        # Insert ancestor if doesn't exist
        ancestorName = levelNames[0]
        if ancestorName not in importedModules:
            moduleDict = {
                'asname' : None,
                'refcount' : 0,
                'subs' : []
                }
            importedModules[ancestorName] = moduleDict

        parentDict = importedModules[ancestorName]
        moduleDict = {}
        for currentModule in levelNames[1:]:
            if currentModule not in parentDict:
                moduleDict = {
                'asname' : None,
                'refcount' : 0,
                'subs' : []
                }
                parentDict['subs'].append({currentModule: moduleDict})
            else:
                moduleDict = parentDict[currentModule]
                pass
            parentDict = moduleDict
        moduleDict['refcount'] += 1
    return None
    

parser = argparse.ArgumentParser(description='Show unused and repeated imports.')
parser.add_argument('filesPath', type=str, nargs='+', help='files to clean')

programArgs = parser.parse_args()

for filePath in programArgs.filesPath:
    print(filePath)
    with open(filePath, 'r') as browsedFile:
        #moduleDict = {}
        importedModules = {}
        for line in browsedFile:

            # Remove leading and trailing characters like : ' ' and '\n'
            line = line.strip()
            result = parseCodeLine(line)

            if not result: # line does not contain an import statement
                continue            
            
            node = result[1]

            if result[0] == 1: # Import
                
                for nodeName in node.names:
                    branch = nodeName.name
                    print('adding {} to dict'.format(branch))
                    addBranch(branch, importedModules)

            elif result[0] ==2: # ImportFrom
                node.module
                for nodeName in node.names:
                    branch = node.module + '.' + nodeName.name
                    print('adding {} to dict'.format(branch))
                    addBranch(branch, importedModules)
                pass
            '''
            for node in ast.iter_child_nodes(ast.parse(line)):
                
                if isinstance(node, ast.ImportFrom):
                    print('ImportFrom')
                    print(vars(node))
                    print(len(node.names))
                    for n in node.names:
                        print(vars(n))
                    if not node.names[0].asname:  # excluding the 'as' part of import
                        modules.append(node.module)
                elif isinstance(node, ast.Import): # excluding the 'as' part of import
                    print('Import')
                    print(vars(node))
                    print(len(node.names))
            '''
            print()
            
        pprint.pprint(importedModules)
