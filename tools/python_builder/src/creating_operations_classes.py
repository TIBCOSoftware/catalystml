import json
import os
import sys

v=sys.argv[1]
print("spec version = ",v)

opdir=f"../../../versions/{v}/operations/"
filenameoutput="opsclasses.py"

def create_class(m,fout):
    op=m['title']
    opdesc=m['desc']
    inplist=[inp['name'] for inp in m['input']] if 'input'  in m else []
    parlist=[par['name'] for par in m['params']] if 'params' in m else []
    eqls=lambda x:x+'=None'
    
    fout.write(f"class {op}(operation):\n")
    fout.write('\t"""\n')
    fout.write(f'\t{opdesc}\n')
    fout.write('\t"""\n')
    def create_innerclass(name,m,mapkey):
        l=m[mapkey]
        fout.write(f'\tclass {name}:\n')
        fout.write('\t\t"""\n')
        #print(l)
        fout.write(f"\t\t{name}'s possible keys:\n")
        for  p in m[mapkey]:
            reqstr='required'
            if 'optional' in p and p['optional']==True: reqstr='optional'
            s=f"\t\t\t{p['name']} ({reqstr})- {p['description']}\n"
            fout.write(s)
        fout.write('\t\t"""\n')
        fout.write(f'\t\tdef __init__(self,{",".join(eqls(x["name"]) for x in l)}):\n')
        fout.write('\t\t\t"""\n')
        fout.write(f'\t\t\tinitializing {name}\n')
        fout.write('\t\t\t"""\n')
        for  p in m[mapkey]:
            s=f"\t\t\tself.{p['name']}={p['name']}\n"
            fout.write(s)
        fout.write(f'\t\tdef make_map(self):\n')
        fout.write('\t\t\t"""\n')
        fout.write('\t\t\tmethod to convert data into a map for later printing\n')
        fout.write('\t\t\t"""\n')
        fout.write('\t\t\tm={}\n')
        for p in m[mapkey]:
            if p['optional']==True:
                s=f"\t\t\tif self.{p['name']}!=None:m['{p['name']}']=self.{p['name']}\n"
            else:
                s=f"\t\t\tm['{p['name']}']=self.{p['name']}\n"
            fout.write(s)
        fout.write("\t\t\treturn m\n")
    if 'input' in m and len(m['input'])>=1:create_innerclass("inputs",m,"input")
    if 'params' in m and len(m['params'])>=1: create_innerclass("params",m,"params")

    fout.write("\tdef __init__(self,inputs=None,params=None,output=None):\n")
    fout.write(f'\t\t""" Initialize {op} operation and define inputs, parameters, and outputs"""\n')
    fout.write(f'\t\tself.operation="{op}"\n')
    fout.write('\t\toperation.__init__(self,inputs=inputs,params=params,output=output,operation=self.operation)\n\n\n')

def make_ops_class(opdir,fout):
    fout.write("class ops:\n")
    for d in os.listdir(opdir):
        fout.write(f"\tclass {d}:\n")
        fout.write('\t\t"""\n')
        fout.write(f'\t\t{catdescs[d]}\n')
        fout.write('\t\t"""\n')
        for f in os.listdir(opdir+d):
            o=f.split(".")[0]
            s=f"\t\tclass {o}({o}):\n"
            fout.write(s)
            fout.write("\t\t\tdef __init__(self,inputs=None,params=None,output=None):\n")
            fout.write(f"\t\t\t\t{o}.__init__(self,inputs=inputs,params=params,output=output)\n")

#creating map with labels for operation catagories
catdescs={}
catdescs["math"]="Math based operations"
catdescs["cleaning"]='Operations that fall best under data cleaning'
catdescs["restructuring"]='Operations that restructure data (pivot, join, etc.)'
catdescs["string_processing"]='Operations that act on strings'
catdescs["nlp"]='Natural Language Processing(NLP) related operations'
catdescs["image_processing"]='Image processing related operations'
catdescs["utils"]='Misc. Operations'

ops=[]
for d in os.listdir(opdir):
    for f in os.listdir(opdir+d):
        path=f"{opdir}/{d}/{f}"
        ops.append(path)

fout = open(filenameoutput, "w")
        
for fname in ops:
    fn=fname
    if fn:
        with open(fn,"r") as f:
            #print(fn.split("/")[-1])
            m=json.load(f)
            create_class(m,fout)
fout.close()

fout = open(filenameoutput, "a")
make_ops_class(opdir,fout)

s="\tdef listAllOps():"
s+="\n\t\tprint('{:18s} {:20s}  {:s}')".format('Category:','Op name:','Description:')
for op in ops:
    cat=op.split("/")[-2]
    with open(op) as f:
        m=json.load(f)
    s+="\n\t\tprint('{:18s} {:21s}  {:s}')".format(cat,m['title'],m['desc'][:65])
fout.write(s)
fout.close()

