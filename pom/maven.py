#!/usr/local/bin/python3
import json
from urllib.request import urlopen


f = open('./jar-sha1sums.txt','r')
pom = open('./pom.xml','a')
pom.write('<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/maven-v4_0_0.xsd">\n')
pom.write('<modelVersion>4.0.0</modelVersion>\n')
pom.write('<groupId>samples</groupId>\n')
pom.write('<artifactId>sample</artifactId>\n')
pom.write('<version>1.0</version>\n')
pom.write('<packaging>war</packaging>\n')
pom.write('<dependencies>\n')
for line in f.readlines():
    sha = line.split("  ")[0]
    jar = line.split("  ")[1]
    print("Looking up "+jar)
    searchurl = 'http://search.maven.org/solrsearch/select?q=1:%22'+sha+'%22&rows=20&wt=json'
    page = urlopen(searchurl)
    data = json.loads(b" ".join(page.readlines()))
    if data["response"] and data["response"]["numFound"] == 1:
        print("Found info for "+jar)
        jarinfo = data["response"]["docs"][0]
        pom.write('<dependency>\n')
        pom.write('\t<groupId>'+jarinfo["g"]+'</groupId>\n')
        pom.write('\t<artifactId>'+jarinfo["a"]+'</artifactId>\n')
        pom.write('\t<version>'+jarinfo["v"]+'</version>\n')
        pom.write('</dependency>\n')
    else:
        print("No info found for "+jar)
pom.write('</dependencies>\n')
pom.write('<build>\n')
pom.write('<plugins>\n')
pom.write('<plugin>\n')
pom.write('<groupId>org.codehaus.mojo</groupId>\n')
pom.write('<artifactId>versions-maven-plugin</artifactId>\n')
pom.write('<version>2.7</version>\n')
pom.write('<configuration>\n')
pom.write('<excludes>\n')
pom.write('<exclude>org.apache.commons:commons-collections4</exclude>\n')
pom.write('</excludes>\n')
pom.write('</configuration>\n')
pom.write('</plugin>\n')
pom.write('</plugins>\n')
pom.write('</build>\n')
pom.write('</project>\n')

pom.close()
f.close()
