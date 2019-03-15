import re
#EACH API AND ITS NUMBER OF HITS
with open("/home/mintu/essentials/Smart Retail/ApiKeys", "r") as keys:
    KeyList = keys.read().strip().splitlines()
    ApiCounts = dict.fromkeys(KeyList, 0)
    # uuid=re.compile('\b[0-9a-f]{8}\b-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-\b[0-9a-f]{12}\b')
    for key in ApiCounts:
        with open("/home/mintu/essentials/Smart Retail/logs/Api Lists/apiCalledInaWindow", "r") as inputFile:
            for line in inputFile:
                ExtractedLine = line.split("   ")
                api = ExtractedLine[1].split(" ")
                api[2] = re.sub(r'\b[0-9a-f]{8}\b-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-\b[0-9a-f]{12}\b', '*',
                                api[2])
                api[2] = re.sub(r'^[0-9]{5,15}$', '#', api[2])
                if api[2].__contains__(key):
                    ApiCounts[key] += 1
    inputFile.close()
    for k in ApiCounts:
        print("\nThe number of "+k+ "   api hits: "+str(ApiCounts[k]))
    print(sum(ApiCounts.values()))

