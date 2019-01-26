file = open('apartmentInfo')
writer = open('apartmentInfo.csv','w+')

s = set()
for r in file:
	if not r: continue
	r = r.split(' --> ')
	if r[0] == 'Name': writer.write(r[0] + '=' + r[1] + '=' + r[2] + '=' + r[3])
	price = r[1].strip()[1:]
	if price[-3:] != '.00': continue
	price = int(price[:-3].replace(',',''))
	if price > 2000: continue
	writer.write(r[0] + '=' + r[1] + '=' + r[2] + '=' + r[3])