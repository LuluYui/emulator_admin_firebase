# Summary 
A python script to organize messy tennis matches data into a structured match score table 

# Compilation guide 

1. Install all the necessary packages with pip
`pip install -r requirements.txt`

2. run the python script in order 
    - Reading the excel file and convert the results to json format 
    ` python read_files.py `
    - publishing the results to the localhost emulators firestore or the production server by 
    setting the destination in the script 
    ` python publish_2_firestore.py `