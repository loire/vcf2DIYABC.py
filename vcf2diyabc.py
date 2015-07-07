#!/usr/bin/python

#Usage: ./vcf2diyabc.py infile.vcf popfile.txt sexratio
# Tool to convert vcf file in diyABC input file for SNP data
# User needs to provide a popfile.txt which specify individuals sex and population of origin (This information is not always present in vcf file.
# popfile must be formated as follow:
#   indiv sex pop
# with as many lines as there is individuals recorded in the vcf file. Individuals name must match the identifiants in the vcf file 
# Additionnaly, the sex ratio must be provided as a float number. Specify 1 for equal sex ratio



import sys

def usage():
    print("##################################################################")
    print("Unix usage:\n./vcf2diyabc.py")
    print("On windows, rigth click on the script file to execute it through a python launcher")
    print(2*"\n")
    print(" Tool to convert vcf file in diyABC input file for SNP data")
    print(" User needs to provide a popfile.tsv which specify individuals sex and population of origin (This information is not always present in vcf file.")
    print(" popfile must be formated as follow:")
    print("\tindiv \\t sex \\t pop")
    print(" with as many lines as there is individuals recorded in the vcf file. Individuals name must match the identifiants in the vcf file ")
    print("sex takes M or F only (or 9 if undefined).")

usage()


vcffile = input('Enter the vcf_filename :')
try:
    open(vcffile,'r')
except IOError:
    print("unable to open "+vcffile)
    usage()
    sys.exit()



indinfof = input('Enter the individual information file :')

try:
    open(indinfof,'r')
except IOError:
    print("unable to open "+indinfof)
    usage()
    sys.exit()

# Parsing informations about individuals
indivinfo={}
for line in open(indinfof,'r'):
    c = line[:-1].split()
    indivinfo[c[0]]=(c[1],c[2])
    # Sex is first elements, pop is second


vcff = open(vcffile,'r')

def parseline(l):
    locusinf=[]
    c = l[:-1].split("\t")
    # Testing for locus type
    idSNP = "A"             # everything that is not in [X,Y,MT] will be an autosome
    if c[0]=="MT":
        idSNP = "M"
    if c[0]=="Y":
        idSNP = "Y"
    if c[0]=="X":
        idSNP="X"
    locusinf.append(idSNP)
    # Here maybe parse information in X,Y and MT chromosome
    
    # Now reject polymorphism if it's not a biallelic SNP
    if len(c[3])>1 or len(c[4])>1:
        return 0
    else:
        for indiv in c[9:]:
            gt = indiv.split(":")[0]
            if len(gt)==1:   # For haploid data ( X male, Y and MT )
                if gt==".":
                    geno = 9
                else:
                    if gt=="0":
                        geno = 1
                    else:
                        geno = 0

            else:
                gt = indiv.split(":")[0]
                if gt[0] not in ["0","1","."] or gt[2] not in ["0","1","."]:
                    print("vcf format incorrect, only 0 and 1 should be present in the GT file for biallelic SNP")
                    print("problematic line:\n"+l)
                    sys.exit()
                if gt[0]=="." or gt[1]==".": # Missing data
                    geno = 9
                else:
                    geno = 2 - int(gt[0]) - int(gt[2])
            locusinf.append(geno) 
    return locusinf

def parsevcf(of):
    mat = [] # Final matrix to print
    loctyp = [] # information on locus type (A, M, Y, or X linked)
    #"Scan file until first entry"
    for line in of:
        if line[0:6]!="#CHROM":
            continue
        else:
            break
    c = line[:-1].split("\t")
    num_indiv = len(c)-9
    ids_indiv = c[9:]
    # The real big loop
    for line in of:
        linfo = parseline(line) # parse information on the locus
        if linfo!=0:        # If locus is informative
            loctyp.append(linfo[0])
            mat.append(linfo[1:])
    return (ids_indiv,loctyp,mat)



print("Parsing "+vcffile+"...")
m = parsevcf(vcff)

indivs = m[0]
locs = m[1]
mat = m[2]

outfilename = ".".join(vcffile.split(".")[:-1])
outfilename = outfilename+".DIYABC.snp"


print("Writing outputfile as: "+outfilename)

fout = open(outfilename,"w")
fout.write("insert title here <NM=$insert_sex_ratio$NF>\n")
tmpstr = "IND\tSEX\tPOP"
for loc in locs:
    tmpstr+="\t"+str(loc)
fout.write(tmpstr+"\n")

iX = [i for i,x in enumerate(locs) if x == 'X']
iY = [i for i,x in enumerate(locs) if x == 'Y']

for cpt in range(len(indivs)):
    ind = indivs[cpt]
    try:
        indivinfo[ind]
    except KeyError:
        print("Indiv is not in population file ! please check entry file for "+ind+"\n")
        sys.exit()
    
    sex = indivinfo[ind][0]
    pop = indivinfo[ind][1]
    tmpstr=ind+"\t"+sex+"\t"+pop
    for genoI in range(len(mat)):
        geno = mat[genoI]
        genotype = geno[cpt]
        if sex == "9" and (genoI in iX or genoI in iY):
            genotype = 9
        if sex == "F" and genoI in iY:
            genotype = 9 
        tmpstr+="\t"+str(genotype)

    
    
    fout.write(tmpstr+"\n")

fout.close()

tmp = input("Press enter to exit")

            


