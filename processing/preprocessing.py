import re
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
from sklearn.impute import SimpleImputer


class Preprocessing:
    
    ## this method clean the data 
    def data_cleaning(self,df):
        
        ## drop apartments where the price is not mentioned
        df['prix(DHs)'].isna().sum()
        df  = df[df['prix(DHs)'].notna()]

        df['etat'] =df['etat'].str.lower().str.replace(' ','')
        df['autre'] =df['autre'].str.lower()

        ##----extract cities---

        def extractcity(text):
                    pattern =r'à\s\w+\s?(\w*)'
                    match = re.search(pattern, text)
                    if match:
                            value =match.group(0).replace('à','').strip().split(' ')
                            return ''.join(value)
                    else:
                            value =text.split(' ')
                            return ''.join(value)


        df['ville'] =df['ville'].apply(extractcity)

        # ----extract numerical data
        numeric_cols =['surface(m²)','pieces','chambres','salles de bains']

        for col in numeric_cols:
                    df[col]=df[col].replace({'Pièces':'','Chambres':'','Salles de bains':'','m²':''},regex=True)
                    df[col] = pd.to_numeric(df[col], errors='coerce')


        ##----extract prices---
        def extractPrix(value):

                    value,type= str(value).split(' ')
                    if type=='DH':
                            return float(value)
                    elif type=='EUR':
                            return float(value)*11
                    
        ##----extract floors---
        def extractfloor(value):
                    return str(value).replace('ème\n\t\t\t\t\tétage','etage').replace('er\n\t\t\t\t\tétage','etage')
        df.loc[df['etage'].notna(),'etage'] = df[df['etage'].notna()]['etage'].apply(extractfloor)
        df['prix(DHs)'] = df['prix(DHs)'].apply(extractPrix)

        ##----cleaning text---
        def text_cleaning(value):
                    return str(value).replace('orientation:  ','').replace('type du sol:  ','').replace('  ',' ').strip() if value else ''
        df['autre'] = df['autre'].apply(text_cleaning)

        df['ans'] = df['ans'].str.replace('Plus de 100','morethan100').str.replace('ans','').str.replace('-','to').str.strip()



        #--remove some inconsistents and outiers data

        df=df[df['prix(DHs)']>160000]

        df =df[df['prix(DHs)']<=3200000.0]
        df =df[df ['surface(m²)']<800]


        ##--remove useless data
        df = df.drop(['lienImage','lienArticle'],axis=1)

        # Remove duplicates
        df = df.drop_duplicates()

        # Remove records where the 'autre' column is missing
        df = df.dropna(subset=['autre'])


        return df

    ## we gonna collect all categorical data in one variable called description to apply text_mining on this feature  

    def Feature_Engineering(self,df):
        numerica_cols =df.select_dtypes('float')

        df['Description'] = (df['etat'].fillna('') +" " +df['etage'].fillna('') +" "+
                        " "+ df['ans'].fillna('') +" "+ df['ville'].fillna('') +" "+
                            df['autre'].fillna('')).str.replace('  ',' ').str.replace('nan','').str.lower().str.strip()
        df= df[list(numerica_cols)+['Description']]
        return df


    def textMining(self,df,numeric_cols):
        vectorize =TfidfVectorizer(encoding='utf-8')

        X =vectorize.fit_transform(df['Description']).toarray()
        X_tfidf =pd.DataFrame(X,columns=vectorize.get_feature_names_out())
        X_tfidf.index=df.index
        df =pd.concat([df[list(numeric_cols)],X_tfidf],axis=1)
        return  df,vectorize


    def data_imputer(self,df):
        
        #--Separate categorical and numerical columns
        categorical_cols = df.select_dtypes(include='object').columns
        numerical_cols = df.select_dtypes(include=['int64', 'float64']).columns

        #--Impute missing values in categorical columns with the mode
        categorical_imputer = SimpleImputer(strategy='most_frequent')
        df[categorical_cols] = categorical_imputer.fit_transform(df[categorical_cols])

        #--Impute missing values in numerical columns with the mean
        numerical_imputer = SimpleImputer(strategy='mean')
        df[numerical_cols] = numerical_imputer.fit_transform(df[numerical_cols])

        return df

    def processing(self,df):
        df = self.data_cleaning(df)
        
        numerica_cols =df.select_dtypes('float')

        df = self.data_imputer(df)
        df =self.Feature_Engineering(df)
        df,vectorize= self.textMining(df,numerica_cols)
        X=df.drop('prix(DHs)',axis=1)
        y=df['prix(DHs)']
        return X,y,vectorize
