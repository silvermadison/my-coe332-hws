#hw 1 exercise 2

import names

for n in range(5):
    name = names.get_full_name()
    name=name.strip()
    while(len(name)!= 9):
        name=names.get_full_name()
        name=name.strip()
    print(name)
