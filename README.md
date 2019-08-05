## Research Paper Recommendation System based on Hybrid and multi model appraches.

### Prerequisites
You must have Scikit Learn, Pandas (for Machine Leraning Model) and Flask (for API) installed.

### Project Structure
This project has four major parts :
1. model.py - This contains code fot our Machine Learning model to predict research paper recommendation on trainign data in 'papers.csv' file.
2. app.py - This contains Flask APIs that receives paper title details through GUI or API calls, computes the precited value based on our model and returns it.
3. request.py - This uses requests module to call APIs already defined in app.py and dispalys the returned value.
4. templates - This folder contains the HTML template to allow user to enter paper title or keywords and displays the recommendaded papers.

### Running the project
1. Ensure that you are in the project home directory. Create the machine learning model by running below command -
```
python3 model.py
```
This would create a serialized version of our model into a file model.pkl

2. Run app.py using below command to start Flask API
```
python3 app.py
```
By default, flask will run on port 5000.

3. Navigate to URL http://localhost:5000


4. You can also send direct POST requests to FLask API using Python's inbuilt request module
Run the beow command to send the request with some pre-popuated values -
```
python request.py
```
