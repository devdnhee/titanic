import csv
import pandas as pd

variables=['PassengerId','Survived','Pcass','Name','Sex','Age','SibSp','Parch','Ticket',
           'Fare','Cabin','Embarked']
TITLES_ARRAY = ['Mr', 'Mrs', 'Miss', 'Master', 'Don', 'Rev', 'Dr', 'Mme', 'Ms', 'Major', 'Lady', 'Sir', 'Mlle', 'Col',
                'Capt', 'the Countess', 'Jonkheer']
EMBARKMENT_ARRAY = ['S', 'C', 'Q']

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
        print(title_l)

def get_labels(var):
    '''Mr., Miss., ...'''
    with open('train.csv','r') as f:
        reader=csv.DictReader(f)
        var_l=[]
        for row in reader:
            if row[var] not in var_l:
                var_l.append(row[var])
        print(var_l)
        
def read_train():
    '''
    read data and transform to samples as input
    '''
    data=[]
    with open('train.csv','r') as f:
        reader=csv.DictReader(f)
        for row in reader:
            print(row,'\n',dict_to_feat(row))
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
    emb_f=len(EMBARKMENT_ARRAY)*[0.]
    try:
        emb_f[EMBARKMENT_ARRAY.index(embarked)]=1.0
    except:
        raise

def name_features(name):
    length=float(len(name))
    title=(name.split(',')[1]).split()[0]
    title_f=len(TITLES_ARRAY)*[0.]
    try:
        title_f[TITLES_ARRAY.index(title)]=1.
    except:
        pass
    n_names=float(len(name.split()))
    return [length,n_names]+title_f

def sex_feature(sex):
    return 1. if sex=='male' else -1.

def age_feature(age):
    return float(age) if age!='' else None

def transform_df(df):
    """
    transform the raw titanic dataset to be processable
    :param df: dataframe containing the titanic data
    :return: processed dataframe
    """
    df['length'] = df['Name'].apply(len)
    df['Title'] = df['Name'].str.extract(', ?([^\.]*)\.', expand=True)
    onehot_title_df = pd.get_dummies(df['Title'], columns=TITLES_ARRAY)
    df = pd.concat([df, onehot_title_df], axis=1, join='inner')
    df['Sex'] = df['Sex'].apply(lambda x: 1. if x == 'male' else -1.)
    onehot_embarked_df = pd.get_dummies(df['Embarked'], columns=EMBARKMENT_ARRAY)
    df = pd.concat([df, onehot_embarked_df], axis=1, join='inner')
    df = df.drop(['Name', 'Ticket', 'Cabin', 'Embarked', 'Title'], axis=1)
    for column in ['Age', 'Fare']:
        avg_value = df[column].mean()
        df[column] = df['Age'].fillna(avg_value)

    # fix missing columns
    c1 = set(EMBARKMENT_ARRAY) | set(TITLES_ARRAY)
    c2 = set(list(onehot_embarked_df)) | set(list(onehot_title_df))
    missing_cols = c1 - c2
    for c in missing_cols:
        df[c] = 0

    # drop additional columns
    add_cols = c2 - (c1 & c2)
    df = df.drop(add_cols, axis=1)

    return df

def transform_csv(input_filepath, output_filepath):
    df = pd.read_csv(input_filepath)
    df = transform_df(df)
    df.to_csv(path_or_buf=output_filepath, index=False)

if __name__=='__main__':
    #read_train()
    #get_titles()
    #get_labels('Ticket')
    transform_csv('test.csv', 'test_processed.csv')
