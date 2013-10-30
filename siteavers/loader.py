# -*- coding:utf-8 -*-
import sys, re

def parsefile(filename,stack):
    with open(filename) as f:
        for line in f:
            line_splitted = re.split(r'\s{2,}', line, flags=re.U+re.I)
            if line_splitted[0] != '' and re.match(r'^[0-9]{2}',line, flags=re.U+re.I):
                stack.append(line_splitted)
    f.close()

def prepare_lines(stack,prepared):
    for line in stack:
        #
        split_line0=re.split(r'\s',line[0],flags=re.U+re.I)

        split_line4 = re.split(r'\s',line[4],flags=re.U+re.I)

        split_line5=line[5].split(';')

        #line[0] = split_line0[1]
        #line[4] = split_line4[0]
        #line[5] = split_line5[0]
        #line[6] = split_line5[1]
        #line.append(split_line5[2])
        try:
            lined = dict(
                code=split_line0[1],
                city=line[1],
                provider=line[2],
                address=line[3],
                coutry_mnemo=split_line4[0],
                works=split_line5[0],
                currencies=split_line5[1].strip(),
                telns=split_line5[2].strip()
            )
            prepared.append(lined)
        except:
            continue
        #

def printres(prepared):
    e=0
    for elem in prepared:
        e = e + 1
        print str(elem) + ' - '+ str(e)


def main(filename):
    stack=[]
    prepared=[]
    parsefile(filename,stack)
    prepare_lines(stack,prepared)
    printres(prepared)

if __name__ == '__main__':
    main(sys.argv[1])
