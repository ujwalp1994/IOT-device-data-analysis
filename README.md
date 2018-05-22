# IOT-device-data-analysis

Project Structure:

![fullworkflow](https://user-images.githubusercontent.com/20211851/40383318-9b93f2cc-5dce-11e8-99f7-0cc2ecaf522c.png)

Technology Usage:

Selenium, TestNG [Maven], Jenkins:
  - The primary goal of using Selenium is to automate the process of data gathering. 
  - The TestNG scripts are written to go to the hexoskin dashboard and download only the latest record uploaded on the             hexoskin device servers.
  - The script looks up into a text file [record_data.txt] to check if a records exists on the local machine or not.
  - Jenkins CI server is configured to fire up the scipts after every 10 minutes. 
  
Hadoop [HDFS]:
  - Configured a data warehouse i.e. a Hadoop one-node cluster to store the data file retrieved from the hexoskin device.
  - Jenkins CI server fires a shell script after every 12 minutes to move the data from local machine into HDFS.

Python [Pandas]: 
  - Connect HDFS with python via HDFSSecureClient library and store the .csv data into a pandas dataframe
  - Perform data cleaning, exploration and transformation.
  - Apply appropriate logic to derive valuable insights from the data. 
 
Dash by Plotly:
  - Provide a intuitive UI for the end-user so that, the user can view the insights and interact with the graphs. 
