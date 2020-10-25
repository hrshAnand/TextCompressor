import operator

intSize = 2  # In bytes


def getText():
    f = open("file.txt", "r")
    text = f.read()
    n = len(text)
    print("File read successfull.\nWords Read:", n)
    return text, n


def getMemorySaved(texts):
    count = {}

    for text in texts:
        windowSize = intSize
        while(windowSize < 20):
            for i in range(len(text)-windowSize):
                phase = text[i:i+windowSize]
                if len(phase) > intSize:
                    try:
                        count[phase] += 1
                    except KeyError:
                        count[phase] = 1
            windowSize += 1

    memSaved = {}

    for phase in count:
        if count[phase] * (len(phase) - intSize) - len(phase) > 0:
            memSaved[phase] = count[phase] * \
                (len(phase) - intSize) - len(phase)

    return memSaved


def greedyCompress(texts):
    memSaved = getMemorySaved(texts)
    mx = 0
    bestPhase = ""

    for phase in memSaved:
        if(memSaved[phase] > mx):
            mx = memSaved[phase]
            bestPhase = phase

    if mx > 0:
        newTexts = []

        for text in texts:
            newTexts += text.split(bestPhase)

        saved, phases = greedyCompress(newTexts)
        
        return mx + saved, phases + [bestPhase]

    return 0, []


def gdfsCompress(texts, b):
    memSaved = getMemorySaved(texts)

    if b == 1:
        return greedyCompress(texts)

    branchingFactor = min(b, len(memSaved))

    topMemorySavers = dict(sorted(memSaved.items(
    ), key=operator.itemgetter(1), reverse=True)[:branchingFactor])

    mostSaved = 0
    bestPhases = []

    for phase in topMemorySavers:
        newTexts = []
        for text in texts:
            newTexts += text.split(phase)

        saved, phases = gdfsCompress(newTexts, b-1)

        if mostSaved < topMemorySavers[phase] + saved:
            mostSaved = topMemorySavers[phase] + saved
            bestPhases = phases + [phase]

    return mostSaved, bestPhases


if __name__ == "__main__":
    text, n = getText()

    bytesSaved, phasesCompressed = greedyCompress([text])

    print("Compression using Greedy:", int(
        10000*bytesSaved/n)/100, "%")
    print("Total Phases Compressed", len(phasesCompressed))

    bytesSaved, phasesCompressed = gdfsCompress([text], 4)

    print("Compression using Greedy-DFS:", int(10000*bytesSaved/n)/100, "%")
    print("Total Phases Compressed", len(phasesCompressed))
