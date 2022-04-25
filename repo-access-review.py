#!/user/bin/python3

import requests
import time
import datetime
import sys
import getpass

# Edit baseUri value to reflect company bitbucket rest api URI
# Example:
#   https://bitbucket.'companyX'.com/rest/api/1.0/
#   https://api.github.com/orgs/'companyX'/repos
baseUri = ''

def access_api(url, user, passwd):
    start  = 0
    isLastPage = 0
    data = []
    while isLastPage == 0:
        time.sleep(1/100)
        getURI = url + "start=" + str(start)
        print(getURI)
        requestData = requests.get(getURI, auth=(user,passwd))
        if requestedData.status_code != 200:
            print("Error connecting to " + getURI + " status: " + str(requestedData.status_code))
            isLastPage = 1
        else:
            jsonData = requestedData.json()
            try:
                    isLastPage = jsonData['isLastPage']
                    if isLastPage == 0:
                        start = jsonData['nextPageStart']
            except:
                    isLastPage = 1
                    print("An error occured getting " + getURI + " (Check permissions)")
            if jsonData['size'] > 0:
                jsonValues = jsonData['values']
                for x in jsonValues:
                    data.append(x)
    return data

def main():
    filename = ""
    try:
        filename = sys.argv[1]
    except:
        while filename == "":
            filename = input("Enter File name: ")
    outFile = open(filename, "w", encoding='utf-8')
    print("REPOSITORY ACCESS REVIEW TOOL")

    username = input("Repository Username: ")
    password = input("Password: ")

    # Get all Projects from Code Repository
    projectKeys = []
    projectData = access_api(baseUri + 'projects?', username, password)
    for x in projectData:
        projectKeys.append(x['key'])
        
    # Get all Repos for each Project
    repoKeys = []
    for proKey in projectKeys:
        repoData = access_api(baseUri + 'projects/' + projkey + '/repos/?', username, password)
        for repo in repoData:
            repoKeys.append((projKey, repo['slug']))

    # Get all closed PRs for each Repo
    print("***************** Merged Pull Requests REPOSITORY PERMISSIONS *****************")
    outFile.write("Project,Repo,ToBranch,FromBranch,ID,Title,Description,State,Created,Updated,Closed,Author,Reviewer,Participants,Link\n")
    for repo in repoKeys:
        pullRequests = access_api(baseUri + 'projects/' + repo[0] + '/repos/' + repo[1] + '/pull-requests?state=merged&', username, password)
        for x in pullRequests:
            try:
                outFile.write('"%s",' % x['toRef']['repository']['project']['name'])
                outFile.write('"%s",' % x['toRef']['repository']['name'])
                outFile.write('"%s",' % x['toRef']['displayId'])
                outFile.write('"%s",' % x['fromRef']['displayId'])
                outFile.write('"%s",' % x['id'])
                outFile.write('"%s",' % x['title'].replace('"', '"'))
                outFile.write('"%s",' % x['description'].replace('"', '"')) if 'description' in x else outFile.write(',')
                outFile.write('"%s",' % x['state'])
                outFile.write('"%s",' % datetime.datetime.fromtimestamp(x['createdDate']/1000).strftime('%Y-%m-%d %H:%M:%S'))
                outFile.write('"%s",' % datetime.datetime.fromtimestamp(x['updatedDate']/1000).strftime('%Y-%m-%d %H:%M:%S'))
                outFile.write('"%s",' % datetime.datetime.fromtimestamp(x['closedDate']/1000).strftime('%Y-%m-%d %H:%M:%S'))
                outFile.write('"%s",' % x['author']['user']['displayName'])
                for user in x['reviewers']:
                    outFile.write('%s\n' % user['user']['displayName'])
                outFile.write('","')
                for user in x['participants']:
                    outFile.write('%s\n' % user['user']['displayName'])
                outFile.write('","')
                for url in x ['links']['self']:
                    outFile.write('%s\n' % url['href'])
                outFile.write('"\n"')

            except:
                outFile.write("ERROR\n")
    exit()
if __name__ == "__main__":
        main()