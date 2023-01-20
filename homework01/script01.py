#hw 1 exercise 1

words = [] #can sort the list and just print the first five use method sort
with open('words', 'r') as f:
    words = f.read().splitlines()

words.sort(key=len, reverse=True)

for i in range(5):
    print(words[i])
