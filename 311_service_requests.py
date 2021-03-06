# -*- coding: utf-8 -*
"""
Automatically generated by Colaboratory.
"""
from google.colab import drive
drive.mount('/content/drive')

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

"""**Inspect Data**"""

data = pd.read_csv("/content/drive/My Drive/31-M29/311_Service_Requests_H2_subset.csv",index_col=0)
print("Number of rows: {0:,}".format(len(data)))
print("Number of columns: {0:,}".format(len(data.columns)))

display(data.head())
print('\n Data Types:')
print(data.dtypes)

#checking for missing values in each column
data.isna().sum()

data.shape

data.columns

"""**changeing datetype**"""

data["Created Date"] = pd.to_datetime(data["Created Date"])
data["Closed Date"] = pd.to_datetime(data["Closed Date"])

"""**creating new coloumn with the weekday when complain was created and closed**"""

data["Created Date weekday"] = data["Created Date"].dt.weekday_name
data["Closed Date weekday"] = data["Closed Date"].dt.weekday_name

"""**Adding new columns *Duration Ticket,Duration Ticket in minutes* ,which saves the time differnce between Closed Date and Created Date**
Before working with Duration Ticket though,we need to check if the values make sense.
"""

data["Duration Ticket True"] = data["Closed Date"] < data["Created Date"]

wrong_date = data["Duration Ticket True"]
wrong_date.sum()

data[wrong_date]

"""3356 reports are closed before they are created.For further visualizations i delete theses entries."""

data.drop(data.loc[data["Duration Ticket True"]==True].index,inplace = True)

checking_date = data["Duration Ticket True"]
checking_date.sum()

"""**Now we can add the Duration Ticket,Duration Ticket in minutes columns**"""

data["Duration Ticket"] = data["Closed Date"] - data["Created Date"]

data["Duration Ticket in minutes"] = (data["Duration Ticket"].dt.seconds / 60).round(2)

data.head()

data.shape

"""# **non-graphical**
1 First look about the twenty largest complains overall
"""

data['Complaint Type'].value_counts().nlargest(20)

"""and the twenty smallest complains"""

data['Complaint Type'].value_counts().nsmallest(20)

"""*51448 of the 495944 reported complains are about Illegal Parking*
*only 1 of the whole complains is about Building Conditions*
2 which agency is called the most in terms of percentage in each borough,only consider agencys with atleast 0.8% of received calls
"""

freq_borough = data.groupby("Borough")["Agency Name"].value_counts(normalize = True)
(freq_borough[(freq_borough >= 0.008)]*100).round(2)

"""*42.20% of the complaints in bronx are headed to the NYPD, 30.07% to the Department of Housing and Development,9.32% to the Department of Transportation and so on*
0.8% was the lowest value to display most of the data on the screen
3 checking for top complaints in each borough
"""

data.groupby('Borough').get_group('BRONX')['Complaint Type'].value_counts()[:10]

"""*In Bronx the top complaint is about Heat/Hot Water missing*"""

data.groupby('Borough').get_group('BROOKLYN')['Complaint Type'].value_counts()[:10]

"""*In Brooklyn the top complaint is about Illegal Parking*"""

data.groupby('Borough').get_group('MANHATTAN')['Complaint Type'].value_counts()[:10]

"""*In Manhattan the top complaint is about Noise - Residential*"""

data.groupby('Borough').get_group('QUEENS')['Complaint Type'].value_counts()[:10]

"""*In Queens the top complaint is about Illegal Parking*"""

data.groupby('Borough').get_group('STATEN ISLAND')['Complaint Type'].value_counts()[:10]

"""*In Staten Island the top complaint is about Illegal Parking*
4 Top 20 descriptions about complains and which agency was contacted
"""

description_of_complaint = data.groupby(['Complaint Type',"Descriptor","Agency"]).size().to_frame("Count").reset_index()

description_of_complaint = description_of_complaint.sort_values(by = "Count",ascending=False)[:20]
description_of_complaint

"""*35625 complaints received the NYPD about Noise - Residentials,where the cause was Loud Music/Party.*
*32737 complaints received the HPD about Heat/Hot Water missing in the entire Building.*
5 How many complaints are created on which weekday
"""

complains_weekday = data.groupby("Created Date weekday").size().to_frame("Count").reset_index()
cats = [ 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
complains_weekday = complains_weekday.set_index("Created Date weekday").reindex(cats)
complains_weekday

"""*73523 of the 495944??? created complaints where on a Friday and only 66851 are created on a Sunday .
# **Graphical**
1 Overall view off calls per agency
"""

plt.figure(figsize=(12, 5))
overall_calls_agency = sns.countplot("Agency",data=data)
overall_calls_agency.set_xticklabels(overall_calls_agency.get_xticklabels(), rotation=30, ha="right")
overall_calls_agency.set_title("Calls per agency")
# set individual bar lables using above list https://robertmitchellv.com/blog-bar-chart-annotations-pandas-mpl.html
for i in overall_calls_agency.patches:
    # get_x pulls left or right; get_height pushes up or down
    overall_calls_agency.text(i.get_x(), i.get_height(), \
            str(round((i.get_height()))), fontsize=12,
                color='black')
plt.tight_layout()
plt.show()

"""*211130 of the 495944 complaints received the NYPD*
*only 101 calls got the DOITT**
2 How is the status of the complaints
"""

plt.figure(figsize=(12, 5))
status_progress = sns.countplot(data.Status)
status_progress.set_xticklabels(status_progress.get_xticklabels(), fontsize=12)
status_progress.set_title("Status of reported complaints")
for i in status_progress.patches:
    # get_x pulls left or right; get_height pushes up or down
    status_progress.text(i.get_x()+.2, i.get_height(), \
            str((i.get_height())), fontsize=12,
                color='black')
plt.tight_layout()
plt.show()

"""*428005 of the 495944 reported complaints are already closed,which is 86.30%.*
*43805 or 8.83% of the reported complaints are still in progress*
For a large city like NYC i was surprised how many complaints already got handled.
3 Which complaints gets fastes closed,which slowest(average)?
"""

complain_duration_fast = data.groupby("Complaint Type")["Duration Ticket in minutes"].mean().round(2).reset_index()
complain_duration_fast = complain_duration_fast.sort_values(by = "Duration Ticket in minutes")[:10]
pal = sns.color_palette("colorblind")
plt.figure(figsize=(12, 5))
complain_duration_fast_plot = sns.barplot(y = "Complaint Type",x = "Duration Ticket in minutes",data = complain_duration_fast,palette = pal)
complain_duration_fast_plot.set_title("Duration of reported complaints untill closed(fastes)")
complain_duration_fast_plot.set_xlabel("Average duration in minutes")
# set individual bar lables using above list https://robertmitchellv.com/blog-bar-chart-annotations-pandas-mpl.html
for i in complain_duration_fast_plot.patches:
    # get_width pulls left or right; get_y pushes up or down
    complain_duration_fast_plot.text(i.get_width()+.3, i.get_y()+.38, \
            str(round((i.get_width()), 2)), fontsize=10,
color='black')

"""*The average waiting time if u reported Helicopter Noise is 0.07 minutes*
*If u create a complaint regards Violation of Park Rules,the average time untill the ticket gets closed is 143.94 minutes*
"""

complain_duration_slow = data.groupby("Complaint Type")["Duration Ticket in minutes"].mean().round(2).reset_index()
complain_duration_slow = complain_duration_slow.sort_values(by = "Duration Ticket in minutes",ascending=False)[:10]
pal = sns.color_palette("colorblind")
plt.figure(figsize=(15, 5))
complain_duration_slow_plot = sns.barplot(y = "Complaint Type",x = "Duration Ticket in minutes",data = complain_duration_slow,palette = pal)
complain_duration_slow_plot.set_title("Duration of reported complaints untill closed(slowest)")
complain_duration_slow_plot.set_xlabel("Average duration in minutes")
# set individual bar lables using above list https://robertmitchellv.com/blog-bar-chart-annotations-pandas-mpl.html
for i in complain_duration_slow_plot.patches:
    # get_width pulls left or right; get_y pushes up or down
    complain_duration_slow_plot.text(i.get_width()+.3, i.get_y()+.38, \
            str(round((i.get_width()), 2)), fontsize=10,
color='black')

"""*If u reported a complaint about Building Condition,the average waiting time until the report gets closed is 1385.5 minutes*
4 Overall complaints per borough(sum)
"""

borough_complaints = data.groupby(['Borough', 'Complaint Type']).size().to_frame("Count").reset_index()
borough_complaints.info

plt.figure(figsize=(18, 5))
pal = sns.color_palette("colorblind")
borough_complaints_sum = borough_complaints.groupby("Borough").sum()
borough_complaints_sum = borough_complaints_sum.reset_index()
borough_complaints_sum_barplot = sns.barplot(x = "Count",y = "Borough",data = borough_complaints_sum,palette=pal)
borough_complaints_sum_barplot.set_title("Complaints per Borough")
for i in borough_complaints_sum_barplot.patches:
    # get_width pulls left or right; get_y pushes up or down
    borough_complaints_sum_barplot.text(i.get_width()+.3, i.get_y()+.38, \
            str((i.get_width())), fontsize=10,
color='black')

"""*The most complaints are from Brooklyn.Staten Island only has 23061 reported complaints overall,which depends on the population density in the district.*
*Staten Island has 479.458 citiziens*,
*Manhattan has 1.63M citiziens*,
*Bronx has 1.47M citiziens*,
*Queens has 2.36M citiziens*,
*Brooklyn has 2.53M citiziens*
* We can see that the reported complaints depends on the populatin density*
5 Complaints for Central Park
"""

park_complaints = data.groupby("Park Facility Name")
central_park_complaints = park_complaints.get_group("Central Park")["Complaint Type"].value_counts().reset_index()
central_park_complaints.rename(columns={"index":"Park Name"},inplace= True)

pal = sns.color_palette("colorblind")
central_park_complaints_plot = sns.barplot(x="Complaint Type", y="Park Name", data=central_park_complaints,palette=pal)
central_park_complaints_plot.set_title("Complaints for Central Park")
central_park_complaints_plot.set_xlabel("Amount of complaints")
central_park_complaints_plot.set_ylabel("Complaint Type")

"""Central Park is the most well known park in NYC,thats why i focus on it.
*The most complaints for the Central Park is Noise, followed by Violation of Park Rules, Maintenance problems, Animals in Park and last Homless Persons Assistance*
*
6 Top 10 complaints on weekdays
"""

weekday = data.groupby("Created Date weekday")
monday_complaints = weekday.get_group("Monday")["Complaint Type"].value_counts().reset_index()
monday_complaints.rename(columns={"index":"Complaint Type","Complaint Type":"Count"},inplace= True)
monday_complaints = monday_complaints.set_index("Complaint Type").reset_index()[:10]

monday_complaints_plot = sns.catplot(y = "Complaint Type",x = "Count",data = monday_complaints,kind="bar")

weekday = data.groupby("Created Date weekday")
tuesday_complaints = weekday.get_group("Tuesday")["Complaint Type"].value_counts().reset_index()
tuesday_complaints.rename(columns={"index":"Complaint Type","Complaint Type":"Count"},inplace= True)
tuesday_complaints = tuesday_complaints.set_index("Complaint Type").reset_index()[:10]

tuesday_complaints_plot = sns.catplot(y = "Complaint Type",x = "Count",data = tuesday_complaints,kind="bar")

weekday = data.groupby("Created Date weekday")
wednesday_complaints = weekday.get_group("Wednesday")["Complaint Type"].value_counts().reset_index()
wednesday_complaints.rename(columns={"index":"Complaint Type","Complaint Type":"Count"},inplace= True)
wednesday_complaints = wednesday_complaints.set_index("Complaint Type").reset_index()[:10]

wednesday_complaints_plot = sns.catplot(y = "Complaint Type",x = "Count",data = wednesday_complaints,kind="bar")

weekday = data.groupby("Created Date weekday")
thursday_complaints = weekday.get_group("Thursday")["Complaint Type"].value_counts().reset_index()
thursday_complaints.rename(columns={"index":"Complaint Type","Complaint Type":"Count"},inplace= True)
thursday_complaints = thursday_complaints.set_index("Complaint Type").reset_index()[:10]

thursday_complaints_plot = sns.catplot(y = "Complaint Type",x = "Count",data = thursday_complaints,kind="bar")

weekday = data.groupby("Created Date weekday")
friday_complaints = weekday.get_group("Friday")["Complaint Type"].value_counts().reset_index()
friday_complaints.rename(columns={"index":"Complaint Type","Complaint Type":"Count"},inplace= True)
friday_complaints = friday_complaints.set_index("Complaint Type").reset_index()[:10]

friday_complaints_plot = sns.catplot(y = "Complaint Type",x = "Count",data = friday_complaints,kind="bar")

weekday = data.groupby("Created Date weekday")
saturday_complaints = weekday.get_group("Saturday")["Complaint Type"].value_counts().reset_index()
saturday_complaints.rename(columns={"index":"Complaint Type","Complaint Type":"Count"},inplace= True)
saturday_complaints = saturday_complaints.set_index("Complaint Type").reset_index()[:10]

saturday_complaints_plot = sns.catplot(y = "Complaint Type",x = "Count",data = saturday_complaints,kind="bar")

weekday = data.groupby("Created Date weekday")
sunday_complaints = weekday.get_group("Sunday")["Complaint Type"].value_counts().reset_index()
sunday_complaints.rename(columns={"index":"Complaint Type","Complaint Type":"Count"},inplace= True)
sunday_complaints = sunday_complaints.set_index("Complaint Type").reset_index()[:10]

sunday_complaints_plot = sns.catplot(y = "Complaint Type",x = "Count",data = sunday_complaints,kind="bar")

"""* We can see during the workdays (Mo-Fr) the highest complaints are about Illegal Parking, which makes sense because more people drive to work in the city, for shopping and so on.*
*The day with the most complaints is Friday. Heat/Hot water problems are the top complaints.Which can be correlated with the citiziens coming home for the weekend.We also have an increase in Noise - Residential,which is the top complain on Saturday and Sunday. Which makes sense,because on weekends,most citiziens are home and are more sensitive to noise(want to relax),also on weekends parties and loud music are more likely.*
7 checking what the main complaint(description) is on Sunday
"""

weekday = data.groupby("Created Date weekday")
sunday_complaints_deep = weekday.get_group("Sunday")[["Complaint Type","Descriptor"]].sum()
#sunday_complaints.rename(columns={"index":"Complaint Type","Complaint Type":"Count"},inplace= True)
#sunday_complaints = sunday_complaints.set_index("Complaint Type").reset_index()[:10]

sunday_complaints_deep

weekday_complaint_descr = data.groupby(['Complaint Type',"Descriptor","Created Date weekday"]).size().to_frame("Count")
sunday_complain = weekday_complaint_descr.reset_index()

sunday = sunday_complain["Created Date weekday"] =="Sunday"
sunday_complaints_deepdive = sunday_complain[sunday].sort_values(by ="Count",ascending = False)[:10]

sunday_complaints_deepdive

sunday_complaints_deepdive_plot = sns.catplot(y = "Descriptor",x = "Count",data = sunday_complaints_deepdive,kind="bar")

"""*Loud Music/Party is the reason for the complaints about noise*"""
