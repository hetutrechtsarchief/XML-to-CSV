#!/usr/bin/env python3
import json,argparse,csv,sys,codecs
import xml.etree.ElementTree as ET 

argparser = argparse.ArgumentParser(description='XML to CSV') 
argparser.add_argument('infile', default=sys.stdin, type=argparse.FileType('r', encoding="utf-8"), nargs='?')
argparser.add_argument('outfile', default=sys.stdout, type=argparse.FileType('w', encoding="utf-8"), nargs='?')
argparser.add_argument('--itemObject',help='for example ./channel/item', required=True)


args = argparser.parse_args()

def parseXML(xmlfile): 
  tree = ET.parse(xmlfile) 
  root = tree.getroot() 
  items = [] 
  for item in root.findall(args.itemObject):
    news = {} 

    for child in item: 

      if child.tag and child.text: 
        news[child.tag] = child.text.strip()

    items.append(news) 

  return items 

    

def main(): 
  data = parseXML(args.infile) 

  #collect all fieldnames found in file to use as header of the csv
  headers = {}
  for obj in data:
    for key in obj:
      headers[key] = 1

  writer = csv.DictWriter(sys.stdout, fieldnames=headers.keys(), delimiter=',', quoting=csv.QUOTE_ALL, dialect='excel')
  writer.writeheader()
  writer.writerows(data)


if __name__ == "__main__": 
  main() 
