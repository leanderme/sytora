# Sytora
Sytora is a multilingual symptom-disease classification app. Translation is managed through the UMLS coding standard. A multinomial Naive Bayes classifier is trained on a handpicked dataset, which is freely available under CC4.0. 

To get started:
- Clone this repo
- Install requirements
- Run the scripts (see below) and npm dependencies
- Get a UMLS license to download UMLS lexica & generate DB (umls.sh)
- Run and check [ http://localhost:5001]( http://localhost:5001)
- Done! :tada:

![search](https://raw.githubusercontent.com/leanderme/sytora/master/screenshots/search.png)

Check out [sytora.com](sytora.com) for a demo.


### Motivation
Finding the right diagnosis cannot be achieved by extracting symptoms and running a classification algorithm. The hardest part is asking the right questions, focusing what is important in the situation, connecting other events, and much more. Despite all this, I have long been exited about writing a symptom-disease lookup system to quickly gather related symptoms to symptoms etc. Not everything the model outputs is nonsense. Actually it helps a lot to quickly get a list of diseases given to a set of symptoms.

### Data
The data is formatted as CSV files. Example entry:
```csv
Disease,Symptom
C0162565,C0039239
```

Data sources:
- `DiseaseSymptomKB.csv`: extracted from [Disease-Symptom Knowledge Database](http://people.dbmi.columbia.edu/~friedma/Projects/DiseaseSymptomKB/index.html). This data solely belongs to the respective authors. The authors are not not affiliated with this project.
- `disease-symptom.csv`: Manually created by hand. Freely available under CC 4.0.

### Install
**Training models & generating files from data:**
1. Run `cui2vec-converter.py` to convert to GloVe-format. You need to get the pretrained embeddings first, available here: https://figshare.com/s/00d69861786cd0156d81. Place them in the data folder.
2. Run `generateLabels.py` to create the option labels for the select fields. Languages are currently hardcoded as list and can be extended if needed.
3. Run `train.py` to train a MNB classifier (for the disease prediction). Other necessary files are generated, too. 
4. Run `relatedSymptoms.py` to train the model for the autosuggestion feature. This uses cui2vec. Please note that the authors of cui2vec are not affiliated with this code. 

**React client:**
cd into `flaskapp` and `npm install`. For development `npm run watch`, for production `npm run build`.

### Flask Service
A small flask app is avaiable to showcase the trained models. cd into the `flaskapp` folder and start the app
```bash
python app.py
```

### Deployment
Make sure to export `REACT_APP_ENDPOINT` with the correct address (e.g. http://yoursite.com)

Get going in ~10 min:
```
sudo apt update
sudo apt install python3-pip python3-dev build-essential libssl-dev libffi-dev python3-setuptools
sudo apt install python-pip python-dev
sudo apt install nodejs npm
pip install flask pandas sklearn numpy
pip install Flask-Limiter flask-expects-json
pip install more-itertools requests configparser
sudo apt-get install nginx supervisor

git clone https://github.com/leanderme/sytora
cd sytora/flaskapp && npm i

vi /etc/supervisor/conf.d/sytora.conf
sudo supervisorctl reread
sudo service supervisor restart
sudo supervisorctl status

sudo vim /etc/nginx/conf.d/virtual.conf
sudo nginx -t
sudo service nginx restart
```

sytora.conf:
```
[program:sytora]
directory=/root/sytora/flaskapp
command=gunicorn app:app -b 0.0.0.0:5001
autostart=true
autorestart=true
stderr_logfile=/var/log/sytora/sytora.err.log
stdout_logfile=/var/log/sytora/sytora.out.log
```

virtual.conf
```
server {
    listen       80;
    server_name  site.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
    }
}
```

don't forget to transfer the umls.db, e.g. 
`scp ./umls.db root@address:/root/sytora/flaskapp/umls/database`



### Coding quality, security & stability
This project was written *very* quickly with no performance or stability features in mind; the code base suffered accordingly. Expect things to be cleaned up soon though.

Please note that I'm a machine learning hobbyist and a medical student. The code may not in accordance with common conventions. 

### Acknowledgements
This project is **heavily** inspired by:
- https://github.com/Aniruddha-Tapas/Predicting-Diseases-From-Symptoms
- https://github.com/sekharvth/symptom-disease