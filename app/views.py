#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 20 11:54:27 2017

@author: cricket
"""

from flask import Flask, render_template, request
from app import app
from delayengine import delaypredict
import datetime
now = datetime.datetime.now()

predictioneng = delaypredict.Predictioneng()

@app.route('/')
#@app.route('/index')
def index():
    return render_template('index.html',
                           codes=sorted(predictioneng.airportsavail().keys()),
                            airports = predictioneng.airportsavail(),
                            currentdate = now.strftime('%Y-%m-%d'),
                            currenthour = int(now.strftime('%H')))




@app.route('/result',methods = ['POST', 'GET'])
def result():
   if request.method == 'POST':
      result = request.form
      print(result)
      table = predictioneng.predicttable((result['ORIGIN'], result['DEST']))
      return render_template("result.html",table = table, result = result,
                             airportsdict = predictioneng.airportsavail())
   else:
       return 'go to the main page'