from bs4 import BeautifulSoup
import requests
import pandas as pd

def convertToFrac(s):
  num,den = s.split( '/' )
  return (float(num)/float(den))



ls = []


for pg in range(1,134):
  
  res = requests.get(f"https://www.debateart.com/debates?page={pg}&order_type=&category_id=&status=finished")
  c = res.content
  
  soup = BeautifulSoup(c, 'html.parser')
  stats = soup.findAll("div", "debate-index__debate-stats-icons")

  for j in stats:
    ls.append(j.text)


splitList = [i.split("\n\n") for i in ls]

numCArgs = [int(i[1].split("/")[0]) for i in splitList]
numTArgs = [int(i[1].split("/")[1]) for i in splitList]
proportionArgs = [convertToFrac(i[1]) for i in splitList]
numComments = [int(i[2]) for i in splitList]
numVotes = [int(i[3].strip()) for i in splitList]

df = {
  "Completed Arguments": numCArgs,
  "Total Arguments": numTArgs,
  "Proportion of Arguments": proportionArgs,
  "Comments": numComments,
  "Votes": numVotes
}

df = pd.DataFrame(df)
csvData = df.to_csv('DART.csv', index=True)
