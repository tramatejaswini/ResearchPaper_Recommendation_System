## Research Paper Recommendation System

## Objective:

Researchers find it difficult to access and keep track of the most relevant and promising research papers of their interest. The known approach to get research papers is to follow the list of references from the documents they already possessed Even though this approach might be quite effective in some instances, it does not guarantee full coverage of recommending research papers and cannot trace papers published after the possessed paper.In this project, a pipelined hybrid based approach for research paper recommender system is developed where users will be provided with top most recommendation with high accuracy. 

### Prerequisites
You must have Scikit Learn, Pandas (for Machine Leraning Model) and Flask (for API) installed.

## Dataset:
 
We have scraped the research papers a dataset from ww.ieee.org, where we have titles, abstract, authors, url’s of the papers, references, citations and keywords of the paper. This web scraping is done using the beautiful soup and html parser framework. Firstly , we have downloaded all the html pages with the required information, and from those html pages we have inspected the class and id of the tables containing the required information. This information is retrieved using find_all API and saved into CSV files.

## Data Preprocessing:

The fields ‘paper authors’ , ‘citation number’, ‘paper venue’ ,’published year’ are dropped from the csv file.
Removing the records, which do not have title
Replacing the records’ null abstract with title where there is no abstract
The extracted text is cleaned such that only english words are contained in the csv file.
In order to maintain 3 characteristics volume, velocity and variety of the data, we have done these data processing steps. After preprocessing the data looks like.

## Analysis and Methodology of project:
	
This project is implemenpelined hybrid approach where the output of content based implementation is provided to collaborative filtering implementation as input.
To overcome all the limitations of the above mentioned approaches and as we have a large set of data, we are using the below mentioned models with features like title and abstract, References, Citations and Author.

Content Based
      TF-IDF & cosine similarity 
       K Nearest Neighbour using Bag of words model and Euclidean Distance.
              Word2Vec model, Cosine Similarity
Collaborative Filtering
Pipelined Hybrid System(Sending the result of the Content based Filtering to Collaborative Filtering)
Page Rank Algorithm using Neo4j

### Project Structure
This project has four major parts :
1. model.py - This contains code fot our Machine Learning model to recommend research papers absed on trainign data in 'papers.csv' file.
2. app.py - This contains Flask APIs that receives research paper details through GUI or API calls, computes the precited value based on our model and returns it.
3. request.py - This uses requests module to call APIs already defined in app.py and dispalys the returned value.
4. templates - This folder contains the HTML template to allow user to enter user search query details and displays the recommended research papers to users.

### Running the project
1. Ensure that you are in the project home directory. Create the machine learning model by running below command -
```
cd server
python model.py
```
This would create a serialized version of our model into a file model.pkl

2. Run app.py using below command to start Flask API
```
python app.py
```
By default, flask will run on port 5000.

3. Navigate to URL http://localhost:5000

You should be able to view the homepage as below :
![alt text](http://www.thepythonblog.com/wp-content/uploads/2019/02/Homepage.png)

Enter valid numerical values in all 3 input boxes and hit Predict.

If everything goes well, you should  be able to see the predcited salary vaule on the HTML page!
![alt text](http://www.thepythonblog.com/wp-content/uploads/2019/02/Result.png)

4. You can also send direct POST requests to FLask API using Python's inbuilt request module
Run the beow command to send the request with some pre-popuated values -
```
python request.py
```
