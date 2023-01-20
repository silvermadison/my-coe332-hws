#hw 1 exercise 3

import names

def name_length(name):
    name = name.replace(' ','')
    return ( len(name) )    

full_name = []
for i in range(5): #get five names
    full_name.append ( names.get_full_name() ) 

for n in full_name :
    print( n + " " +  str(name_length(n)) )
