import csv

variables=['PassengerId','Survived','Pcass','Name','Sex','Age','SibSp','Parch','Ticket',
           'Fare','Cabin','Embarked']
titles=['Mr.', 'Mrs.', 'Miss.', 'Master.', 'Don.', 'Rev.', 'Dr.', 'Mme.',
         'Ms.', 'Major.', 'Lady.', 'Sir.', 'Mlle.', 'Col.', 'Capt.',
         'Jonkheer.']

embarkments=['S', 'C', 'Q']

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

def get_labels(var):
    '''Mr., Miss., ...'''
    with open('train.csv','r') as f:
        reader=csv.DictReader(f)
        var_l=[]
        for row in reader:
            if row[var] not in var_l:
                var_l.append(row[var])
        print var_l 
        
def read_train():
    '''
    read data and transform to samples as input
    '''
    data=[]
    with open('train.csv','r') as f:
        reader=csv.DictReader(f)
        for row in reader:
            print row,'\n',dict_to_feat(row)
            data.append(row) 

def dict_to_feat(sample):
    passenger_id=float(sample['PassengerId'])
    survived=float(sample['Survived'])
    pclass=float(sample['Pclass'])
    name=name_features(sample['Name'])
    sex=sex_feature(sample['Sex'])
    age=age_feature(sample['Age'])
    sibsp=float(sample['SibSp'])
    parch=float(sample['Parch'])
    #TODO: ticket number investigation
    fare=float(sample['Fare']) 
    #TODO: cabin investigation
    return passenger_id,[survived,pclass,sex,age,sibsp,parch,fare]+name

def embarked_features(embarked):
    emb_f=len(embarkments)*[0.]
    try:
        emb_f[embarkments.index(embarked)]=1.0

def name_features(name):
    length=float(len(name))
    title=(name.split(',')[1]).split()[0]
    title_f=len(titles)*[0.]
    try:
        title_f[titles.index(title)]=1. 
    except:
        pass
    n_names=float(len(name.split()))
    return [length,n_names]+title_f

def sex_feature(sex):
    return 1. if sex=='male' else -1.

def age_feature(age):
    return float(age) if age!='' else None

if __name__=='__main__':
    read_train()
    #get_titles()
    #get_labels('Ticket')
    get_labels('Embarked')
