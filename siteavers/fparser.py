# -*- coding:utf-8 -*-
import sys,re


def parsefile(filename,allowed_linestarts):
    stack = []
    with open(filename) as f:
        for line in f:
            line_split = re.split(r'\s{2,}|:\s+',line,flags=re.I+re.U)
            if line_split[0]!='' and line_split[0].startswith(allowed_linestarts):
                #line_split = [item for item in line_split]
                stack.append(line_split)
    f.close()
    return stack


def groupres(stack,allowed_linestarts):
    inserts=[]
    deletes=[]
    updates=[]
    for elem in stack:
        if elem[0] == allowed_linestarts[0]:
            inserts.append(elem)
            del elem
        elif elem[0] == allowed_linestarts[1]:
            deletes.append(elem)
            del elem
        elif elem[0] == allowed_linestarts[2]:
            updates.append(elem)
            del elem
    return {'inserts':inserts,'deletes':deletes,'updates':updates}


def prepare_lines(stack,allowed_linestarts):
    prepared=[]
    for line in stack:
        # insert & update
        if line[0] == allowed_linestarts[0] or line[0] == allowed_linestarts[2]:
            split_line5=re.split(r'\s',line[5],flags=re.U+re.I)
            split_line7=line[7].split(';')
            try:
                lined = dict(
                    code=line[1],
                    city=line[2],
                    provider=line[3],
                    address=line[4],
                    country_mnemo=split_line5[0].strip(),
                    works=line[6] + ' '+split_line7[0].strip(),
                    currencies=split_line7[1].strip(),
                    telns=split_line7[2].strip()
                )
            except:
                continue
        # delete
        elif line[0] == allowed_linestarts[1]:
            try:
                lined = dict(
                    code=line[1],
                    city='',
                    provider='',
                    address='',
                    country_mnemo='',
                    works='',
                    currencies='',
                    telns=''
                )
            except:
                continue
        prepared.append(lined)
    return prepared

def printres(stack):
    for elem in stack:
        print elem['code']+' | '+elem['city']+' | '+elem['provider']+' | '+elem['address']+' | '+elem['country_mnemo']+' | '+elem['works']+' | '+elem['currencies']+' | '+elem['telns']+' | '

def main(filename):
    allowed_linestarts=('Добавлен','Удален','Изменен')
    stack = parsefile(filename,allowed_linestarts)
    groups = groupres(stack,allowed_linestarts)
    forupdate=prepare_lines(groups['updates'],allowed_linestarts)
    forinsert=prepare_lines(groups['inserts'],allowed_linestarts)
    fordelete=prepare_lines(groups['deletes'],allowed_linestarts)
    printres(forinsert)

if __name__ == '__main__':
    main(sys.argv[1])
