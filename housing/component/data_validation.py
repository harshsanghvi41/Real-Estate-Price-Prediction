from housing.constant import CONFIG_FILE_PATH
from housing.logger import logging
from housing.exception import HousingException
from housing.entity.config_entity import DataValidationConfig
from housing.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact
import os,sys
import pandas  as pd
from housing.util.util import read_yaml_file
from evidently.model_profile import Profile
from evidently.model_profile.sections import DataDriftProfileSection
from evidently.dashboard import Dashboard
from evidently.dashboard.tabs import DataDriftTab
import json

class DataValidation:
    
    def __init__(self, data_validation_config:DataValidationConfig,
        data_ingestion_artifact:DataIngestionArtifact):
        try:
            logging.info(f"{'='*20}Data Valdaition log started.{'='*20} \n\n")
            self.data_validation_config = data_validation_config
            self.data_ingestion_artifact = data_ingestion_artifact
        except Exception as e:
            raise HousingException(e,sys) from e


    def is_train_test_file_exists(self) -> bool:
        try:
            logging.info("Checking if training and test file is available")
            is_train_file_exist = False
            is_test_file_exist = False

            train_file_path = self.data_ingestion_artifact.train_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path

            is_train_file_exist = os.path.exists(train_file_path)
            is_test_file_exist = os.path.exists(test_file_path)

            is_available =  is_train_file_exist and is_test_file_exist

            logging.info(f"Is train and test file exists? -> {is_available}")
            
            if not is_available:
                training_file = self.data_ingestion_artifact.train_file_path
                testing_file = self.data_ingestion_artifact.test_file_path
                message = f"Training file: {training_file} or Testing file: {testing_file} is not present"
                raise Exception(message)

            return is_available
        except Exception as e:
            raise HousingException(e,sys) from e


    def get_train_and_test_df(self):
        try:
            train_df = pd.read_csv(self.data_ingestion_artifact.train_file_path)
            test_df = pd.read_csv(self.data_ingestion_artifact.test_file_path)
            return train_df, test_df

        except Exception as e:
            raise HousingException(e,sys) from e

    
    def validate_dataset_schema(self) -> bool:
        try:
            validation_status = False
            
            train_df = pd.read_csv(self.data_ingestion_artifact.train_file_path)
            test_df = pd.read_csv(self.data_ingestion_artifact.test_file_path)

            # reading column names from schema.yaml file
            dict = read_yaml_file(file_path = r'C:\Users\harsh\Machine-Learning-Project\config\schema.yaml')['columns']
            
            schema_file_columns = []
            for key in dict.keys():
                schema_file_columns.append(key)
            
            logging.info(f"Reading column names from schema.yaml file: {schema_file_columns}")

            # comparing column names of train, test and schema.yaml file
            if train_df.columns.to_list() == test_df.columns.to_list() == schema_file_columns:

                logging.info(f"Training, Testing and schema.yaml file having same column name.")
                
                # checking values of "ocean_proximity" in schema.yaml file
                # acceptable values : <1H OCEAN, INLAND, ISLAND, NEAR BAY, NEAR OCEAN
                unique_categorical_col_value = read_yaml_file(file_path = r'C:\Users\harsh\Machine-Learning-Project\config\schema.yaml')['domain_value']['ocean_proximity']

                #checking values of "ocean_proximity" in train and test file
                ocen_proximity_val_train_df = sorted(train_df["ocean_proximity"].unique())
                ocen_proximity_val_test_df = sorted(test_df["ocean_proximity"].unique())

                # checking whethere "ocean_proximity" column having same values or not
                if ocen_proximity_val_train_df == ocen_proximity_val_test_df == unique_categorical_col_value:
                    validation_status = True
                    logging.info(f'"ocean_proximity" column hvaing same values in Training, Testing and schema.yaml file.')
                return validation_status

        except Exception as e:
            raise HousingException(e,sys) from e


    def get_and_save_data_drift_report(self):
        try:
            profile = Profile(sections=[DataDriftProfileSection()])

            train_df,test_df = self.get_train_and_test_df()

            profile.calculate(train_df,test_df)

            report = json.loads(profile.json())

            report_file_path = self.data_validation_config.report_file_path
            report_dir = os.path.dirname(report_file_path)
            os.makedirs(report_dir,exist_ok=True)

            with open(report_file_path,"w") as report_file:
                json.dump(report, report_file, indent=6)
            return report

        except Exception as e:
            raise HousingException(e,sys) from e

    def save_data_drift_report_page(self):
        try:
            dashboard = Dashboard(tabs=[DataDriftTab()])
            train_df,test_df = self.get_train_and_test_df()
            dashboard.calculate(train_df,test_df)

            report_page_file_path = self.data_validation_config.report_page_file_path
            report_page_dir = os.path.dirname(report_page_file_path)
            os.makedirs(report_page_dir,exist_ok=True)

            dashboard.save(report_page_file_path)
        except Exception as e:
            raise HousingException(e,sys) from e

    def is_data_drift_found(self)->bool:
        try:
            report = self.get_and_save_data_drift_report()
            self.save_data_drift_report_page()
            return True
        except Exception as e:
            raise HousingException(e,sys) from e

    def initiate_data_validation(self) -> DataValidationArtifact :
        try:
            self.is_train_test_file_exists()
            self.validate_dataset_schema()
            self.is_data_drift_found()

            data_validation_artifact = DataValidationArtifact(
                schema_file_path = self.data_validation_config.schema_file_path,
                report_file_path = self.data_validation_config.report_file_path,
                report_page_file_path = self.data_validation_config.report_page_file_path,
                is_validated = True,
                message = "Data Validation performed successully."
            )
            logging.info(f"Data validation artifact: {data_validation_artifact}")
            return data_validation_artifact
        except Exception as e:
            raise HousingException(e,sys) from e


    def __del__(self):
        logging.info(f"{'='*20}Data Valdaition log completed.{'='*20} \n\n")
        

