import requests
import lxml.html as lh
import pandas as pd
import matplotlib.pyplot as plt

url = 'http://rha.gtorg.gatech.edu/treats-testing'
page = requests.get(url)
doc = lh.fromstring(page.content)
tr_elements = doc.xpath('//tr')

col=[]
i=0

for t in tr_elements[0]:
    i+=1
    name=t.text_content()
    col.append((name,[]))

for j in range(1,len(tr_elements)):
    T=tr_elements[j]
    
    if len(T)!=8:
        break

    i=0

    for t in T.iterchildren():
        data=t.text_content() 
        if i>0:
            try:
                data=int(data)
            except:
                pass
        col[i][1].append(data)
        i+=1

Dict={title:column for (title,column) in col}
df=pd.DataFrame(Dict)

df.to_csv('test.csv')

df = pd.read_csv('test.csv')

for i in range(len(df)):
    df.loc[i, "Average"] = df.loc[i, "Average"][:-1]

df2 = df[["Rank*", "Residence Hall", "Average"]].copy()
df = df2
for i in range(len(df)):
    df.loc[i, "Average"] = int(df.loc[i, "Average"])

df.plot(x = 'Residence Hall', y = 'Average', kind = 'bar', title = "Average Participation by Residence Hall", legend = "False")
plt.ylabel("Average")
plt.tight_layout()
