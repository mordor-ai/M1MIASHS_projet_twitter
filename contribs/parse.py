import time
node = {}
start = time.time()
with open('twitter_100M.csv') as f:
    i = 0
    for line in f:
        i += 1
        if i == 1:
            continue
        if i % 100000 == 0:
            print(i/1000000, '%')
            print
        id_ = int(line.replace('\n', '').split(' ')[0])
        if id_ not in node:
            node[id_] = 0
        node[id_] += 1

c = 0
for k,v in node.items():
    if v < 4:
        c += 1

print(c)

print(len(node))
print(time.time()-start)
