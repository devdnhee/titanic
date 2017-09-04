import csv

variables=['PassengerId','Survived','Pcass','Name','Sex','Age','SibSp','Parch','Ticket',
           'Fare','Cabin','Embarked']
titles=['Mr.', 'Mrs.', 'Miss.', 'Master.', 'Don.', 'Rev.', 'Dr.', 'Mme.',
         'Ms.', 'Major.', 'Lady.', 'Sir.', 'Mlle.', 'Col.', 'Capt.',
         'Jonkheer.']

def get_titles():
    '''Mr., Miss., ...'''
    with open('train.csv','r') as f:
        reader=csv.DictReader(f)
        title_l=[]
        for row in reader:
            first=row['Name'].split(',')[1] 
            title=first.split()[0]
            if title not in title_l:
                title_l.append(title)
        print title_l

def read_train():
    '''
    read data and transform to samples as input
    '''
    data=[]
    with open('train.csv','r') as f:
        reader=csv.DictReader(f)
        for row in reader:
            data.append(row) 

def dict_to_feat(sample):
    passenger_id=[int(sample['PassengerId'])]
    survived=[int(sample['Survived'])]

def name_features(name):
    length=len(name)
    title=(name.split(',')[1]).split()[0]
    title_f=len(titles)*[]
    #n_names=len(

if __name__=='__main__':
    #read_train()
    get_titles()
