from housing.entity.config_entity import DataIngestionConfig
import sys,os
from housing.exception import HousingException
from housing.logger import logging
from housing.entity.artifact_entity import DataIngestionArtifact
import numpy as np
import pandas as pd
import pymongo
from sklearn.model_selection import StratifiedShuffleSplit

class DataIngestion:

    def __init__(self,data_ingestion_config:DataIngestionConfig ):
        try:
            logging.info(f"{'=='*20}Data Ingestion log started.{'=='*20} ")
            self.data_ingestion_config = data_ingestion_config

        except Exception as e:
            raise HousingException(e,sys)
    
    """"
    def get_data_from_sql(self):
        try:
            self.db = conn.connect(host = 'localhost', user = 'root', passwd = 'root', database = 'housing')
            logging.info("Database Authenticated!")

            cursor = self.db.cursor()
            query = "select * from housing"
            logging.info("Query running!")
            
            cursor.execute(query)
            myallData = cursor.fetchall()

            all_longitude = []
            all_latitude = []
            all_housing_median_age = []
            all_total_rooms =[]
            all_total_bedrooms = []
            all_population = []
            all_households = []
            all_median_income = []
            all_median_house_value = []
            all_ocean_proximity = []
            logging.info("All List has been created sucessfully for storing the data")

            for i in myallData:
                all_longitude.append(i[0])
                all_latitude.append(i[1])
                all_housing_median_age.append(i[2])
                all_total_rooms.append(i[3])
                all_total_bedrooms.append(i[4])
                all_population.append(i[5])
                all_households.append(i[6])
                all_median_income.append(i[7])
                all_median_house_value.append(i[8])
                all_ocean_proximity.append(i[9])
            logging.info("Data appened to the list")

            # We need to store this data to CSV
            dict = {'longitude' : all_longitude , 
                    'latitude': all_latitude, 
                    'housing_median_age':all_housing_median_age,
                    'total_rooms' : all_total_rooms,
                    'total_bedrooms' : all_total_bedrooms,
                    'population' : all_population,
                    'households' : all_households,
                    'median_income' : all_median_income,
                    'median_house_value' : all_median_house_value,
                    'ocean_proximity' : all_ocean_proximity
                    }

            logging.info("Dict created!")
            raw_data_dir = self.data_ingestion_config.raw_data_dir

            if os.path.exists(raw_data_dir):
                os.remove(raw_data_dir)

            os.makedirs(raw_data_dir,exist_ok=True)
            logging.info("raw_data folder has created")

            df_sql = pd.DataFrame(dict)
            logging.info("Storing data from dict to df_sql dataframe")

            housing_file_name = 'Housing_Data.csv'
            raw_file_path = os.path.join(raw_data_dir, housing_file_name)

            df_csv = df_sql.to_csv(raw_file_path, index=False)
            logging.info("Stored data into csv file")
            return df_csv

        except Exception as e:
            raise HousingException(e)
        """
    
    def get_data_from_mongodb(self):
        try:
            self.client = pymongo.MongoClient("mongodb+srv://mongodb:mongodb@cluster0.akfky.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
            db = self.client['harsh']
            logging.info("Database Authenticated!")

            col = db['HousingData']
            logging.info("Collection Created/Found!")

            cursor = col.find()
            mongo_docs = list(cursor)

            df_csv = pd.DataFrame(mongo_docs, columns=["longitude", "latitude", "housing_median_age", "total_rooms", "total_bedrooms", "population", "households", "median_income", "median_house_value", "ocean_proximity"])
            logging.info("Storing data into dataframe : df_csv")

            raw_data_dir = self.data_ingestion_config.raw_data_dir

            if os.path.exists(raw_data_dir):
                os.remove(raw_data_dir)

            os.makedirs(raw_data_dir,exist_ok=True)
            logging.info("raw_data folder has created")

            housing_file_name = 'Housing_Data.csv'
            raw_file_path = os.path.join(raw_data_dir, housing_file_name)
            
            df_csv.to_csv(raw_file_path, index=False)
            logging.info("Stored data into csv file")
            return df_csv

        except Exception as e:
            raise HousingException(e)
    

    def split_data_as_train_test(self) -> DataIngestionArtifact:
        try:
            raw_data_dir = self.data_ingestion_config.raw_data_dir

            file_name = os.listdir(raw_data_dir)[0]

            housing_file_path = os.path.join(raw_data_dir,file_name)


            logging.info(f"Reading csv file: [{housing_file_path}]")
            housing_data_frame = pd.read_csv(housing_file_path)

            housing_data_frame["income_cat"] = pd.cut(
                housing_data_frame["median_income"],
                bins=[0.0, 1.5, 3.0, 4.5, 6.0, np.inf],
                labels=[1,2,3,4,5]
            )
            

            logging.info(f"Splitting data into train and test")
            strat_train_set = None
            strat_test_set = None

            split = StratifiedShuffleSplit(n_splits=1, test_size=0.3, random_state=42)

            for train_index,test_index in split.split(housing_data_frame, housing_data_frame["income_cat"]):
                strat_train_set = housing_data_frame.loc[train_index].drop(["income_cat"],axis=1)
                strat_test_set = housing_data_frame.loc[test_index].drop(["income_cat"],axis=1)

            train_file_path = os.path.join(self.data_ingestion_config.ingested_train_dir,
                                            file_name)

            test_file_path = os.path.join(self.data_ingestion_config.ingested_test_dir,
                                        file_name)
            
            if strat_train_set is not None:
                os.makedirs(self.data_ingestion_config.ingested_train_dir,exist_ok=True)
                logging.info(f"Exporting training datset to file: [{train_file_path}]")
                strat_train_set.to_csv(train_file_path,index=False)

            if strat_test_set is not None:
                os.makedirs(self.data_ingestion_config.ingested_test_dir, exist_ok= True)
                logging.info(f"Exporting test dataset to file: [{test_file_path}]")
                strat_test_set.to_csv(test_file_path,index=False)
            

            data_ingestion_artifact = DataIngestionArtifact(train_file_path=train_file_path,
                                test_file_path=test_file_path,
                                is_ingested=True,
                                message=f"Data ingestion completed successfully."
                                )
            logging.info(f"Data Ingestion artifact:[{data_ingestion_artifact}]")
            return data_ingestion_artifact

        except Exception as e:
            raise HousingException(e,sys) from e


    def initiate_data_ingestion(self)-> DataIngestionArtifact:
        try:
            self.get_data_from_mongodb()
            return self.split_data_as_train_test()

        except Exception as e:
            raise HousingException(e,sys) from e
    

    def __del__(self):
        logging.info(f"{'=='*20}Data Ingestion log completed.{'=='*20} \n\n")
