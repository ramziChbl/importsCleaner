import re, ast
import argparse
import pprint


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

            # Match "import *"
            #matches = re.search(r'\s*import\s+(\w+\s*,?\s*)+', line)
            #if matches:
            #   print(matches.groups())
            #matches = re.findall(r'\s*import\s+((\w+)\s*,?\s*)+', line)
            #matches = re.findall(r'\s*import\s+((\w+)\s*,?\s*)+', line)
            #'(?m)^(?:from[ ]+(\S+)[ ]+)?import[ ]+(\S+)[ ]*$'
            #if matches:
        #       print(matches)

            
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

                    for nodeName in node.names:
                        print(vars(nodeName))
                        levelNames = nodeName.name.split('.')
                        print(levelNames)
                        if len(levelNames) == 1:
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


                            #print(currentImport)
                    #for n in node.names:
                    #    print(vars(n))
                    #if not node.names[0].asname:
                    #    modules.append(node.names[0].name)
                print()
            
        pprint.pprint(importedModules)
    
