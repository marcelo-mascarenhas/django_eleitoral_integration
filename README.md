# django_eleitoral_integration


## Execution Instructions

### User Session
After this step, install the requirements.txt ( preferebly on a virtual enviroment ), and run the command in the base directory:

python3 manage.py runserver

Enter in the link.

### System's Administrator Session

To enter in the system's administrator session, you need to run the following command on the base directory:

                  python3 manage.py createsuperuser 

And register a user. After this, you can access the django admin page on:

                  http://127.0.0.1:8000/admin/

After logging in, click on the 'View Site' option and the Configuration and Execution pages should appear.


### Execute Collector and Classifier

To execute the tool, first you need download the Trained model (RNN) in the following link:
https://drive.google.com/drive/folders/1Li9zMkeLExxt37GCkaaFLONajALgf2pF?usp=sharing ( We can't put in github because of the size )

After the download, insert the folders in the following directory: ../main/monitor/model_files/

Open another terminal, and execute the following command:

python3 manage.py rqworker

Also, insert your Twitter Keys on the Configuration Page to enable the collector.

Click in the 'Start Collector' button.



