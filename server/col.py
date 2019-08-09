import csv

def recommend_collaborative_filtering(target_paper_id):

    target_references = []
    count = 0
    with open('papers.csv') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')

        for row in readCSV:
            if count > 0:
                if row[2] == target_paper_id:
                    ref = row[6].split(',')
                    for r in ref:
                        target_references.append(r)
                    break
            count+=1

    id_title_dict = {}

    count = 0
    candidate_papers = []
    with open('papers.csv') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            if count > 0:

                id_title_dict[row[2]] = row[3]

                refs = row[6].split(',')
                for r in refs:
                    if r == target_paper_id:
                        candidate_papers.append(row[2])
                    if r in target_references:
                        candidate_papers.append(row[2])
                        break
            count+=1

    if target_paper_id in candidate_papers:
        candidate_papers.remove(target_paper_id)

    candidate_papers_titles = []
    for id_ in candidate_papers:
        candidate_papers_titles.append(id_title_dict.get(id_))

    return candidate_papers_titles

print(recommend_collaborative_filtering('4ab3a98c-3620-47ec-b578-884ecf4a6206'))
