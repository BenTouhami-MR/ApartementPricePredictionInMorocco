from flask import Flask, render_template, request
import pandas as pd
import pickle
from sklearn.metrics.pairwise import cosine_similarity
import re,os 

root_path=os.getcwd().replace('\webApplication','')
print(root_path)
app = Flask(__name__,template_folder='template')
Model_path = root_path+"\\Models\\Stacking.pkl"
df_and_vec_path=root_path+"\\transformers"


# Load the pre-trained model
with open(Model_path, 'rb') as file:
    stacking_model = pickle.load(file)

# Load the dataFrame
df =pd.read_csv(root_path+'\\data\\preprocessed_data.csv')
df.set_index('Unnamed: 0',inplace=True)
df*=1000
# Load the pre-trained model
file =open(df_and_vec_path+r'\vectorizer.pkl', 'rb')
vectorize = pickle.load(file)


# Load the apartment data
data1 = pd.read_csv(root_path+'\\data\\appartements1.csv')
data2 = pd.read_csv(root_path+'\\data\\appartements2.csv')
appartements = pd.concat([data1, data2], axis=0, ignore_index=True)





# Function to prepare data for prediction
def prepare_data_for_prediction(df):
    prediction=df

    df['etat'] =df['etat'].str.lower().str.replace(' ','')


    ## handle cities
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



  ## handle the age
    df['ans'] = df['ans'].str.replace('Over 100 years','morethan100').str.replace('years','').str.replace('-','to').str.strip()



    numerica_cols = ['surface(m²)', 'pieces', 'chambres', 'salles de bains']

    df['Description'] = (df['etat'].fillna('') +" " +df['etage'].fillna('') +" "+
                    " "+ df['ans'].fillna('') +" "+ df['ville'].fillna('') +" "+
                        df['autre'].fillna('')).str.replace('  ',' ').str.replace('nan','').str.lower().str.strip()

    v=df['Description']
    pd.set_option('display.max_columns', None)

    ##--apply TF-IDF on the appartment we want to predict the price
    X =vectorize.transform(v)
    X_tfidf_pred =pd.DataFrame(X.toarray(),columns=vectorize.get_feature_names_out())
    numeric_cols_pred =prediction[list(numerica_cols)]
    to_predict =pd.concat([numeric_cols_pred,X_tfidf_pred],axis=1)

    return to_predict



#--Function to calculate similarity
def calculate_similarity(df,to_predict):
    df_test=df.copy()
    similarities = cosine_similarity(df_test, to_predict)
    df_test['similarity'] = similarities
    index = df_test['similarity'].idxmax()
    similar_apartment = appartements.loc[index]

    return similar_apartment['lienImage'],similar_apartment['lienArticle'],similar_apartment['prix(DHs)']


#--Flask route for the home page
@app.route('/')
def home():
    return render_template('index.html')



#--Flask route for prediction
@app.route('/predict', methods=['POST'])
def predict():

    # --handle numerical varaibles
    data_dict = request.form.to_dict()
    print(data_dict)

    data_dict['surface(m²)']=int(data_dict['surface(m²)'])
    data_dict['chambres']=int(data_dict['chambres'])
    data_dict['pieces']=int(data_dict['pieces'])
    data_dict['salles de bains']=int(data_dict['salles de bains'])
    data_dict['etage']=data_dict['etage']+"etage"

    to_predict=pd.DataFrame.from_dict(data_dict, orient='index').T

    to_predict = prepare_data_for_prediction(to_predict)

    predicted_price = stacking_model.predict(to_predict)

    to_predict['prix(DHs)']=predicted_price

    # Print the result
    similar_apartment_link,sim_artc,price = calculate_similarity(df, to_predict)

    return render_template('index.html', Article_link=sim_artc, prediction=int(predicted_price[0]) ,price=price, similar_apartment_link=similar_apartment_link)

if __name__ == '__main__':
    app.run(debug=True)