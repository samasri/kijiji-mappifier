file = open('appartmentInfo')

s = set()
for r in file:
	if not r: continue
	r = r.split(' --> ')
	s.add(r[2])

print (len(s))