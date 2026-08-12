marks = {
    "Harsh": [80, 90, 85],
    "Rahul": [60, 70, 65],
    "Aman": [95, 92, 98]
}

avg = {}

for name, scores in marks.items(): 
    average = sum(scores)/len(scores)
    avg[name] = average
print (avg)
