import csv
from django.shortcuts import render
import numpy as np
import matplotlib.pyplot as plt
from apyori import apriori
import re

def index(request):
    return render(request,'index.html',{})
def results(request):
    inp=re.split(r'\s*[;,+|]\s*', request.POST.get('param'))
    groc = [x.title() for x in inp]
    try:
        support=float(request.POST.get('support'))
        if support <= 0:
            raise ValueError
    except ValueError:
        support=0.0053
    try:
        confidence=float(request.POST.get('confidence'))
    except ValueError:
        confidence=0.20
    try:
        lift=float(request.POST.get('lift'))
    except ValueError:
        lift=0
    try:
        length=float(request.POST.get('length'))
    except ValueError:
        length=0
    with open("groceries.csv","r") as csvfile:
        data=csv.reader(csvfile)
        rows=[]
        for row in data:
            rows.append(list(row))
        association_rules = apriori(
                                    rows,min_support=support,
                                    min_confidence=confidence,
                                    min_lift=lift,
                                    min_length=length
                                    )
        association_results = list(association_rules)
        res=[]
        for item in association_results:
            pair=item[0]
            items=[str(x).title() for x in pair]
            for i in groc:
                if i in items:
                    res.append(', '.join(items))
        return render(request,'results.html',{'data':res})