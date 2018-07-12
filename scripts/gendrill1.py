import csv

choice1 = ["1-2 Paragraphs","Half a Page","A Page","Multiple Pages"]
choice2 = ["Perfectly","Missed some minor points","Misunderstood major points","Probably didn’t read it"]
choice3 = ["Very helpful", "Somewhat helpful", "Not at all"]
choice4 = ["Very unfair","Unfair","Somewhat Fair","Fair"]
fields = ['length', 'understand', 'help', 'fair']

data = []
for length in choice1:
    for understand in choice2:
        for helpful in choice3:
            for fair in choice4:
                dataitem = {}
                dataitem['length'] = length
                dataitem['understand'] = understand
                dataitem['help'] = helpful
                dataitem['fair'] = fair
                data.append(dataitem)

with open("drilldown1.csv", mode="w", encoding="utf-8") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fields)
    writer.writeheader()
    for d in data:
        writer.writerow(d)
