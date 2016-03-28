Currency-XChange
================

Introduction
------------
A lot of folks talk about how they use Algorithmic Trading in Foreign Exchange. I like reading about finance and messing with code, so I figure I'd try my hand at maximizing the exchange rates between two currencies and, in addition, whether you can actually get more money by converting from one currency back to the original currency. So, I build a little algorithm using the Fixer.io API and a bit of python code. 

How It Works
------------
The essence of this algorihm is to find the largest exchange rate. In other words, if you have exchange rates r_1, r_2, r_3, ..., r_n in order to get from an original currency through intermediate currencies, to a final currency, you would just maximize their product with the equation max(r_1*r_2*...*r_n). 

The algorithm that I wanted to use is called Floyd-Warshall's Algorithm. This algorithm gets you the shortest path between all pairs of nodes in the graph. In other words, it minimizes the sum of the weights in a path between two nodes to get you all of the shortest path. The problem is that this isn't exactly what we want. We have to modify the algorithm slightly. 

Right now, we are maximizing the product with the equation max(r_1*r_2*...*r_n). Our algorithm can't handle products. What we can do is take the log of this to get max(log(r_1*r_2*...*r_n)) = max(log(r_1) + log(r_2) + ... + log(r_n)). Still, this isn't exactly what we want. So, we can negate the summation to get the same answer min(-log(r_1) - log(r_2) - ... - log(r_n)). Thus, between each node, which represents a currency, each directed edge will not be the exchange rate r_i but rather will me a modification -log(r_i). 

We can get the original exchange rate by doing 10^(-(-log(r_1) - log(r_2) - ... - log(r_n))) = 10^(log(r_1) + log(r_2) + ... + log(r_n)) = 10^(log(r_1*r_2*...*r_n)) = r_1*r_2*...*r_n, which is what we want. 

How to use
------------
Want to use this file? Simply download it and then run 
'''
python -i max_exchange.py
'''
to get started. When you're there, you can get the maximum conversion between, say, the Euro and the U.S. Dollar by running: 
'''
>>> max_exchange('EUR', 'USD')
'''
You can also get the path that corresponds to the maximum exchange rate between two currencies by running
'''
>>> get_order('EUR', 'USD')
'''
which will output an array corresponding to the order you should take. 

Problems
---------
The Fixer API records somewhat inaccurate measures. For intance, if you go from one Bulgarian Lev to Brazillian Peso, you get 2.1125 Brazillian Pesos. When you convert back, you get 1.00001525 Levs. So, the algorithm just returns infinity for many exchange rates, because with any exchange rate, you can just find one of these cycles for the intermediate nodes and just cycle between them as many times as you want before hitting infinity. I'll probably rewrite the algorithm using Bellman-Ford, which avoids negative cycles. 

To-Do
-----
- Write Algorithm using Bellman Ford
- Make a UI using Flask
