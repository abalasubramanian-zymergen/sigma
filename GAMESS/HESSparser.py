import sys

fw = open("dft.inp", "w")

hessactive = 0
dataactive = 0

hessblock = []
datablock = []

keysfile = open("keysDFT.gamess", "r") 
keyscontent = keysfile.read()

with open(sys.argv[1]) as fh:
	for line in fh:
		if line.startswith(" $HESS"):
			hessactive = 1
			hessblock = []
			hessblock.append(line)
		elif line.startswith(" $END"):
			if hessactive:
				hessblock.append(line)
			hessactive = 0
		else:
			if hessactive:
				hessblock.append(line)

		if line.startswith(" COORDINATES OF SYMMETRY UNIQUE ATOMS (ANGS)"):
			dataactive = 1
			datablock = []
			datablock.append(" $DATA\n\n C1\n")
		elif line.startswith("--- OPTIMIZED RHF"):
			if dataactive:
				datablock.append(" $END\n")
			dataactive = 0
		else:
			if dataactive > 0 and dataactive < 3:
				dataactive += 1
			elif dataactive != 0:
				datablock.append(line)

fw.write(keyscontent)
fw.write("\n")

for item in datablock:
	fw.write(item)

fw.write("\n")

for item in hessblock:
	fw.write(item)

fw.close()