import os

class CodeFinder:
    # finds pats by suffix input and optionally search words
    def __init__(self, path, suffixes):
        self._path = path
        self._suffixes = suffixes
        self._suffixDict = {".py": "Python", ".java": "Java", ".cs": "C#", ".js": "Javascript"}

    # retrieves code paths
    def getMatchesAndStats(self):
        paths = {}
        for suffix in self._suffixes:
            paths[suffix] = [[self._suffixDict[suffix] + " code paths:"], 0, 0] # set title, filecount and size
        for root, dir, files in os.walk(self._path):
            for file in files:
                fileFound = False
                for suffix in self._suffixes:
                    if fileFound == True:
                        break
                    if file.endswith(suffix):
                        fileFound = True
                        path = os.path.join(root, file)

                        file = open(path, encoding='utf-8')
                        lines = file.readlines()
                        file.close()
                        nonEmptyLines = len(list(filter(None, lines))) # don't include empty lines
                        bytes = os.stat(path).st_size

                        paths[suffix][0].append(path)
                        paths[suffix][1] += nonEmptyLines
                        paths[suffix][2] += bytes

        return paths

    # retrieves code paths if all search words are found in code file
    def getMatchesAndStatsWithMultipleMatch(self, searchWords):
        paths = {}
        for suffix in self._suffixes:
            paths[suffix] = [[self._suffixDict[suffix] + " code paths:"], 0, 0]
        for root, dir, files in os.walk(self._path):
            for file in files:
                searchWordFound = False
                for suffix in self._suffixes:
                    if searchWordFound:
                        break
                    if file.endswith(suffix):
                        temp = searchWords.copy()
                        tempCount = 0
                        path = os.path.join(root, file)

                        file = open(path, encoding='utf-8')
                        lines = file.readlines()
                        file.close()
                        for line in lines:
                            if searchWordFound:
                                break
                            words = line.replace(".", " ").replace("(", " ").split()
                            words = [word.lower() for word in words]

                            for word in words:
                                if word in temp:
                                    temp.pop(temp.index(word))
                                    tempCount += 1
                                    # if all searchwords are found in code file, path is added
                                    if tempCount == len(searchWords):
                                        searchWordFound = True
                                        break

                            if searchWordFound:
                                nonEmptyLines = len(list(filter(None, lines)))
                                bytes = os.stat(path).st_size

                                paths[suffix][0].append(path)
                                paths[suffix][1] += nonEmptyLines
                                paths[suffix][2] += bytes

        return paths

    # retrieves code paths if at least one of the search words are found in code file
    def getMatchesAndStatsWithSingleMatch(self, searchWords):
        paths = {}
        for suffix in self._suffixes:
            paths[suffix] = [[self._suffixDict[suffix] + " code paths:"], 0, 0]
        for root, dir, files in os.walk(self._path):
            for file in files:
                searchWordFound = False
                for suffix in self._suffixes:
                    if searchWordFound:
                        break
                    if file.endswith(suffix):
                        path = os.path.join(root, file)

                        file = open(path, encoding='utf-8')
                        lines = file.readlines()
                        file.close()
                        for line in lines:
                            if searchWordFound:
                                break
                            words = line.replace(".", " ").replace("(", " ").split()
                            words = [word.lower() for word in words]

                            for word in searchWords:
                                if word in words:
                                    searchWordFound = True
                                    break

                            if searchWordFound:
                                nonEmptyLines = len(list(filter(None, lines)))
                                bytes = os.stat(path).st_size

                                paths[suffix][0].append(path)
                                paths[suffix][1] += nonEmptyLines
                                paths[suffix][2] += bytes

        return paths

