#!/usr/bin/env python
# coding: utf-8

# # importing Libraries

# In[1]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')


# Content
# 
# In this Dataset, we have Historical Data of different cause of deaths for all ages around the World. The key features of this Dataset are: Meningitis, Alzheimer's Disease and Other Dementias, Parkinson's Disease, Nutritional Deficiencies, Malaria, Drowning, Interpersonal Violence, Maternal Disorders, HIV/AIDS, Drug Use Disorders, Tuberculosis, Cardiovascular Diseases, Lower Respiratory Infections, Neonatal Disorders, Alcohol Use Disorders, Self-harm, Exposure to Forces of Nature, Diarrheal Diseases, Environmental Heat and Cold Exposure, Neoplasms, Conflict and Terrorism, Diabetes Mellitus, Chronic Kidney Disease, Poisonings, Protein-Energy Malnutrition, Road Injuries, Chronic Respiratory Diseases, Cirrhosis and Other Chronic Liver Diseases, Digestive Diseases, Fire, Heat, and Hot Substances, Acute Hepatitis.

# # Basic Exploration

# In[2]:


df = pd.read_csv('cause_of_deaths dataset.csv')
df


# In[3]:


number_of_rows,no_of_columns=df.shape
print(f'Number of rows:{number_of_rows}\nNumber of columns:{no_of_columns}')


# # Data Type of Each Column

# In[4]:


column_name=list(df.columns.values)
column_dtype=pd.Series(df[column_name].dtypes)
column_dtype


# # Checking is the data have any duplicate lines

# In[5]:


Any_duplicate_rows=df.duplicated().any()
Any_duplicate_rows


# Distribution of numeric columns
# 
# #To perform statistics on numeric coumns,we need specific values as follows
# 
# #percentage(from 0 to 100) of missing values(missing ratio)
# 
# #Min Value(min)
# 
# #The value of lower quartile(25th percentile)(lower_quratile)
# 
# #Median value(50th percetile)(median)
# 
# #Value upper quratile(75th percentile)(upper_quartile)
# 
# #Max Vale(max)

# In[6]:


df.isnull().sum()


# #Hence there is no missing values in dataset

# In[7]:


df.describe()


# # Divide the causes of death into 3 main categories 

# |Communicable diseases  | Non-communicable diseases | Injures |
# |:---                   | :---                      |:---     |
# | Nutritional Deficiencies| Meningitis,Alzheimer's Disease and Other Dementias | Drowning|
# | Malaria| Parkinson's Disease | Interpersonal Violence |    
# | Maternal Disorders| Cardiovascular Diseases | Fire, Heat, and Hot Substances|    
# | HIV/AIDS| Lower Respiratory Infections | Road Injuries| 
# | Drug Use Disorders| Cirrhosis and Other Chronic Liver Diseases | Poisonings| 
# | Tuberculosis| Acute Hepatitis | Protein-Energy Malnutrition| 
# | Neonatal Disorders| Digestive Diseases | Conflict and Terrorism| 
# | Alcohol Use Disorders| Cirrhosis and Other Chronic Liver Diseases | Self-harm| 
# | Diarrheal Diseases| Chronic Respiratory Diseases | Exposure to Forces of Nature| 
# | | Diabetes Mellitus | Environmental Heat and Cold Exposure| 
# | | Chronic Kidney Disease | | 
# | | Neoplasms | | 
# 
# 

# In[8]:


communicable_diseases_df = df[["Year", "Nutritional Deficiencies", "Malaria", "Maternal Disorders", "HIV/AIDS","Drug Use Disorders","Tuberculosis","Neonatal Disorders","Alcohol Use Disorders","Diarrheal Diseases"]]

non_communicable_diseases_df = df[["Year", "Meningitis","Alzheimer's Disease and Other Dementias", "Parkinson's Disease", 
"Cardiovascular Diseases","Lower Respiratory Infections", "Acute Hepatitis", "Digestive Diseases", "Cirrhosis and Other Chronic Liver Diseases", 
"Chronic Respiratory Diseases", "Diabetes Mellitus","Chronic Kidney Disease"]]

injures_df = df[["Year","Drowning", "Interpersonal Violence", "Fire, Heat, and Hot Substances", "Road Injuries", "Poisonings" ,
"Protein-Energy Malnutrition", "Conflict and Terrorism", "Self-harm", "Exposure to Forces of Nature", 
"Environmental Heat and Cold Exposure"]]

communicable_diseases_df = df.assign(sumRow = communicable_diseases_df.sum(axis=1) - communicable_diseases_df['Year']) 
sum_by_year_communicable_diseases_df = communicable_diseases_df[['Year','sumRow']].groupby('Year').sum().reset_index(drop=False)

non_communicable_diseases_df = non_communicable_diseases_df.assign(sumRow = non_communicable_diseases_df.sum(axis=1) - non_communicable_diseases_df['Year'])
sum_by_year_non_communicable_diseases_df = non_communicable_diseases_df[['Year','sumRow']].groupby('Year').sum().reset_index(drop=False)

injures_df = injures_df.assign(sumRow = injures_df.sum(axis=1) - injures_df['Year']) 
sum_by_year_injures_df = injures_df[['Year','sumRow']].groupby('Year').sum().reset_index(drop=False)

sum_by_year_df = sum_by_year_communicable_diseases_df.merge(sum_by_year_non_communicable_diseases_df, on='Year').merge(sum_by_year_injures_df,on='Year')
sum_by_year_df.rename(columns={'sumRow_x': 'communicable_diseases', 'sumRow_y': 'non_communicable_diseases', 'sumRow': 'injures'}, inplace=True)


# In[9]:


sum_by_year_copy=sum_by_year_df.copy()
total_sum_by_year = sum_by_year_copy.sum(axis = 1) - sum_by_year_copy['Year']
sum_by_year_copy['communicable_diseases'] = (sum_by_year_copy['communicable_diseases']*100/total_sum_by_year).round(2)
sum_by_year_copy['non_communicable_diseases'] = (sum_by_year_copy['non_communicable_diseases']*100/total_sum_by_year).round(2)
sum_by_year_copy['injures'] = 100 - sum_by_year_copy['communicable_diseases'] - sum_by_year_copy['non_communicable_diseases']

plt.rcParams['figure.figsize'] = [15, 10]
 
# Stackplot

plt.plot([],[],color='m', label='Communicable Diseases', linewidth=5)
plt.plot([],[],color='c', label='Non-communicable Diseases', linewidth=5)
plt.plot([],[],color='r', label='Injures', linewidth=5)

plt.stackplot(sum_by_year_df['Year'],
                sum_by_year_df['communicable_diseases'], 
              sum_by_year_df['non_communicable_diseases'], 
              sum_by_year_df['injures'], 
             colors=['m','c','r'])
 
plt.xlabel('Year')
 
plt.ylabel('Percentage')
 
# Title of Graph
plt.title('Death By Cause From 1990 to 2019')
plt.legend(loc='center right')
# Displaying Graph
plt.show()


# # Insights

# During the 30 years from 1990 to 2019, the following trends were observed:
# 
# - The number of deaths from non-communicable diseases always accounts for the highest rate and tends to increase gradually.
# - The number of deaths from communicable diseases accounts for the lowest rate, and maintains a fairly stable number over the years.
# - The number of deaths from injures accounts for a high rate, but tends to decrease.

# # Over view of the world from 1990 to 2019

# #change in the no of deaths world wide

# In[10]:


sum_by_year_df["Total"]=sum_by_year_df["communicable_diseases"]+sum_by_year_df["non_communicable_diseases"]+sum_by_year_df["injures"]

sns.set(rc={"axes.facecolor":"#F2EAC5","figure.facecolor":"#D8D5A6"})
plt.subplots(figsize=(20,8))

p=sns.lineplot(x=sum_by_year_df["Year"] ,y=sum_by_year_df["Total"],data=sum_by_year_df,color="#11264e",marker="o",linewidth=3,markersize=10,markerfacecolor="orange",markeredgecolor="black",markeredgewidth=3)
p.axes.set_title("\n Change in the number of deaths worldwide 1990-2019\n",fontsize=25)
p.axes.set_xlabel("\nYear",fontsize=20)
p.axes.set_ylabel("Total number of deaths",fontsize=20)

sns.despine(left=True, bottom=True)
plt.show()


# # Insights

# The number of deaths in the world tends to increase each year, proportional to the population growth. Realizing that countries with a large population have a died and vice versa.
#     
# Leading in the world in the number of deaths is: China, India, United States, Russia, Indonesia (whether in 1990 or 2019, these countries are still at the top of the number of deaths).

# # Top 5 countries/territories with the lowest/highest number of deaths in 2019 

# In[11]:


death_2019=df[df['Year']==2019]
death_2019["Total"]=death_2019.iloc[:, 3:].sum(axis=1)


# In[12]:


_, axs = plt.subplots(1,2,figsize=(25,10))
plt.tight_layout(pad=4.0)

temp1=death_2019.sort_values(["Total"],ascending=True)[:5]
sns.barplot(x=temp1["Country/Territory"],y=temp1["Total"], ax=axs[0],  saturation=1,edgecolor = "#1c1c1c", linewidth = 3)
axs[0].set_xlabel("Country/Territory",fontsize=20)
axs[0].set_ylabel("Total",fontsize=20)
axs[0].set_title("\nTop 5 countries/territories with the lowest number of deaths in 2019\n",fontsize=25)
axs[0].set_xticklabels(axs[0].get_xticklabels(),rotation = 90)
for container in axs[0].containers:
    axs[0].bar_label(container,label_type="edge",padding=6,size=15,color="black",rotation=0,
    bbox={"boxstyle": "round", "pad": 0.4, "facecolor": "orange", "edgecolor": "#1c1c1c", "linewidth" : 2, "alpha": 1})

temp2=death_2019.sort_values(["Total"],ascending=False)[:5]
sns.barplot(x=temp2["Country/Territory"],y=temp2["Total"], ax=axs[1], saturation=1,edgecolor = "#1c1c1c", linewidth = 3)
axs[1].set_title("\nTop 5 countries/territories with the highest number of deaths in 2019\n",fontsize=25)
axs[1].set_xlabel("Country/Territory",fontsize=20)
axs[1].set_ylabel("Total",fontsize=20)
axs[1].set_xticklabels(axs[1].get_xticklabels(),rotation = 90)
for container in axs[1].containers:
    axs[1].bar_label(container,label_type="edge",padding=2,size=18,color="black",rotation=0,
    bbox={"boxstyle": "round", "pad": 0.6, "facecolor": "orange", "edgecolor": "#1c1c1c", "linewidth" : 3, "alpha": 1})    

sns.despine(left=True, bottom=True)    
plt.show()


# # Insight

# The countries/territories with the highest or lowest number of deaths in 2019 are directly proportional to their population. This is considered reasonable.

# Top 5 countries/territories with the highest number of deaths in 2019

# 
# | Country/Territory | Population  | Deads | 
# |:---               | :---        |:---   |
# |  China          | 1433783686 | 10442561 |
# |  India   | 1366417754 | 8812747 |
# |  United States   | 328239523 | 2834964 |
# |  Russia   | 145872256 | 1777223 |
# |  Indonesia   | 273523615 | 1713143 |

# Top 5 countries/territories with the lowest number of deaths in 2019

#     
# | Country/Territory | Population  | Deads | 
# |:---               | :---        |:---   |
# | <font color="#B40537"> Tokelau </font>  | 1340 | 9 |
# | <font color="#B40537"> Niue </font>  | 1615 | 18 |
# | <font color="#B40537"> Nauru </font>  | 10756 | 63 |
# | <font color="#B40537"> Tuvalu </font>  | 10956 | 104 |
# | <font color="#B40537"> Cook Islands </font>  | 17548 | 165 | 

# The leading causes of death in the world in 2019 

# In[13]:


temp=pd.DataFrame(df.groupby("Year")["Meningitis", "Alzheimer's Disease and Other Dementias", "Parkinson's Disease", "Nutritional Deficiencies", "Malaria", "Drowning", "Interpersonal Violence", "Maternal Disorders", "HIV/AIDS", "Drug Use Disorders", "Tuberculosis", "Cardiovascular Diseases", "Lower Respiratory Infections", "Neonatal Disorders", "Alcohol Use Disorders", "Self-harm", "Exposure to Forces of Nature", "Diarrheal Diseases", "Environmental Heat and Cold Exposure", "Neoplasms", "Conflict and Terrorism", "Diabetes Mellitus", "Chronic Kidney Disease", "Poisonings", "Protein-Energy Malnutrition", "Road Injuries", "Chronic Respiratory Diseases", "Cirrhosis and Other Chronic Liver Diseases", "Digestive Diseases", "Fire, Heat, and Hot Substances", "Acute Hepatitis"].sum()).reset_index()
cause_2019=temp[temp['Year']==2019].iloc[:, 1:]
temp1=cause_2019.T
temp1.rename(columns={29: 'Total'}, inplace=True)
temp2=temp1.reset_index().sort_values(["Total"],ascending=False)[:3]

p= sns.barplot(x=temp2["Total"],y=temp2["index"],  saturation=1,edgecolor = "#1c1c1c", linewidth = 2)
p.set_title("Top 3 causes of death in the world 2019",fontsize=25)
p.set_xlabel("\nTotal",fontsize=20)
p.set_ylabel("Cause",fontsize=20)
p.set_xticklabels(p.get_xticklabels(),rotation = 90)
for container in p.containers:
    p.bar_label(container,label_type="edge",padding=6,size=15,color="black",rotation=0,
    bbox={"boxstyle": "round", "pad": 0.4, "facecolor": "orange", "edgecolor": "#1c1c1c", "linewidth" : 2, "alpha": 1})
sns.despine(left=True, bottom=True)    
plt.show()


# Insights

# In 2019:
# 
# The number of deaths from Cardiovascular problems reached 18552218 people, accounting for the highest proportion.
# Taking the top 2 position is Neoplasms, with 10074275 deaths.
# Taking the top 3 position is Chronic Respiratory Diseases, with 3972681 deaths.

# Number of deaths from cardiovascular disease by year ¶

# In[14]:


Cardiovascular_Diseases=pd.DataFrame(df.groupby("Year")["Cardiovascular Diseases"].sum()).reset_index()
sns.set(rc={"axes.facecolor":"#F2EAC5","figure.facecolor":"#D8D5A6"})
plt.subplots(figsize=(20,8))

p=sns.lineplot(x=Cardiovascular_Diseases["Year"],
               y=Cardiovascular_Diseases["Cardiovascular Diseases"],
               data=Cardiovascular_Diseases,
               color="#2540D5",
               marker="o",linewidth=3,markersize=10,
               markerfacecolor="orange",markeredgecolor="red",markeredgewidth=3)
p.axes.set_title("\nNumber of deaths from Cardiovascular Diseases by year\n",fontsize=25)
p.axes.set_xlabel("\nYear",fontsize=20)
p.axes.set_ylabel("Total",fontsize=20)

sns.despine(left=True, bottom=True)
plt.show()


# Top 10 countries with the highest number of deaths from cardiovascular disease over the years 

# In[16]:


import plotly.express as px
temp=pd.DataFrame(df[['Country/Territory','Year','Cardiovascular Diseases']].sort_values(['Cardiovascular Diseases'],ascending=False))

fig = px.treemap(temp.head(300),
                 path = ['Country/Territory','Year','Cardiovascular Diseases'],
                 values = 'Cardiovascular Diseases')

title = 'Countries with the highest number of deaths from cardiovascular disease'
fig.update_layout(title=title,
                  titlefont={'size': 20,
                             'family': 'Proxima Nova',
                             'color': '#BB3E00',
                            },
                  template='simple_white',
                  paper_bgcolor='#F2EAC5',
                  plot_bgcolor='#FFF1D7',
                  treemapcolorway = ["#BB3E00", "#F7AD45", '#5F8D37', ],
                  height = 1000,
                  width = 800,
                  margin=dict(t=130 ,))
fig.show()


# Insight 

# Cardiovascular disease remains the leading burden of disease
# 
# The number of deaths related to cardiovascular problems increases year by year, accounting for the highest proportion of all causes. Especially in countries with large populations and developed economies.
# 
# According to WHO data, heart disease is the largest cause of death in the world. In which, ischemic heart disease accounted for 16% and stroke accounted for 11% of global deaths. Since 2000, the number of deaths from the disease has increased the most, increasing by more than 2 million to 8.9 million deaths in 2019.
# 
# Especially in the current situation of COVID-19 epidemic, the risk of death often focuses mainly on the elderly population, with underlying medical conditions such as hypertension, cardiovascular disease and other chronic diseases. Data from Wuhan (China) show that the mortality rate accounts for 10.5% in people with COVID-19 with heart disease, 7.3% in people with diabetes, 6.3% in people with diabetes. people with respiratory disease and 6% in those with hypertension. On the other hand, worries about the epidemic situation and people's travel restrictions have led to cardiovascular patients delaying their follow-up visits. This is really dangerous for general chronic illness, which often has no obvious symptoms or signs.

# # Neoplasms

# In[17]:


Neoplasms=pd.DataFrame(df.groupby("Year")["Neoplasms"].sum()).reset_index()
plt.subplots(figsize=(20,8))
sns.set(rc={"axes.facecolor":"#F2EAC5","figure.facecolor":"#D8D5A6"})

p=sns.lineplot(x=Neoplasms["Year"],
               y=Neoplasms["Neoplasms"],
               data=Neoplasms,
               color="#2540D5",
               marker="o",linewidth=3,markersize=10,
               markerfacecolor="orange",markeredgecolor="red",markeredgewidth=3)
p.axes.set_title("\nNumber of deaths from Neoplasms by year\n",fontsize=25)
p.axes.set_xlabel("\nYear",fontsize=20)
p.axes.set_ylabel("Total",fontsize=20);


# # Insight 

# Neoplasms - Cancer
# Rates of new cancer and cancer deaths continue to increase year by year. Cancer is not a disease, but a group of diseases. To date, about 200 different types of letters on the human body have been identified.
# 
# Below is a list of some of the most common types of cancer:
# 
# Lung cancer: accounts for the highest rate in men, including developed and developing countries (accounting for 12.4% of all cancers). Mortality and morbidity rates increase from age 40 and older and peak at age 75. Lung cancer mortality is estimated to be the sum of the four types of colorectal, breast, prostate, and prostate cancers. pancreas.
# 
# Stomach cancer: an estimated 934,000 new cancer patients are diagnosed each year. There are many causes of stomach cancer, but an estimated 30% of new cases in developed countries and 47% in developing countries are related to Helicobacter Pylori. Some regions such as Southeast Asia, South America, Eastern Europe... have higher rates of stomach cancer than other regions in the world.
# 
# Breast cancer: is the most common cancer in women (accounting for about 23% of all cancers), especially women in developing countries. The rate of breast cancer increases at the age of 50, 60 and peaks at the age of 70. The incidence is expected to be 111 per 100,000 population in the early years of the 21st century.
# 
# Colorectal cancer: accounts for about 9.4% of all cancers. This type of cancer is often related to diet and living standards..., the disease is more common in developed countries than in poor countries. The disease has a genetic component. The risk of colorectal cancer is increased in people with a pre-existing history of colitis.
# 
# Liver cancer: accounts for about 5.7% of all cancers and is closely related to a history of hepatitis B and C. Asian countries have high rates of liver cancer.
# 
# Prostate cancer: the disease is common in the elderly, tends to increase due to the increasing life expectancy. An estimated 679,000 people are newly diagnosed with the disease every year. The prevalence is high in developed countries and lower in developing countries.
# 
# Cervical cancer: an estimated 493,000 new cases every year. Human papilloma virus (HPV) is probably one of the risk factors for this disease in poor and developing countries.

# # HIV/AIDS

# In[18]:


HIV_AIDS=pd.DataFrame(df.groupby("Year")["HIV/AIDS"].sum()).reset_index()
sns.set(rc={"axes.facecolor":"#F2EAC5","figure.facecolor":"#D8D5A6"})
plt.subplots(figsize=(20,8))

p=sns.lineplot(x=HIV_AIDS["Year"],
               y=HIV_AIDS["HIV/AIDS"],
               data=HIV_AIDS,
               color="#2540D5",
               marker="o",linewidth=3,markersize=10,
               markerfacecolor="orange",markeredgecolor="red",markeredgewidth=3)
p.axes.set_title("\nNumber of deaths from HIV/AIDS by year\n",fontsize=25)
p.axes.set_xlabel("\nYear",fontsize=20)
p.axes.set_ylabel("Total",fontsize=20)

sns.despine(left=True, bottom=True)
plt.show()


# # Insight

# HIV/AIDS
# 
# HIV-1 originated in Central Africa in the first half of the 20th century, when a chimpanzee linked to the virus first infected humans. The global epidemic began in the late 1970s, and AIDS was recognized in 1981.
# 
# The annual decline in HIV infections, which dropped especially sharply after 2004, is largely due to efforts to increase the number of people living with HIV who know their HIV status and are virally suppressed - meaning their HIV infection is being suppressed. control through effective treatment. This is a top public health priority. Studies have shown that, in addition to improving the health of people with HIV, early treatment with antiretroviral drugs significantly reduces the risk of transmitting the virus to others.

# # Conflict and Terrorism

# Number of deaths from Conflict and Terrorism by year 

# In[19]:


Conflict_Terrorism=pd.DataFrame(df.groupby("Year")["Conflict and Terrorism"].sum()).reset_index()
sns.set(rc={"axes.facecolor":"#F2EAC5","figure.facecolor":"#D8D5A6"})
plt.subplots(figsize=(20,8))

p=sns.lineplot(x=Conflict_Terrorism["Year"],
               y=Conflict_Terrorism["Conflict and Terrorism"],
               data=Conflict_Terrorism,
               color="#2540D5",
               marker="o",linewidth=3,markersize=10,
               markerfacecolor="orange",markeredgecolor="red",markeredgewidth=3)
p.axes.set_title("\nNumber of deaths from Conflict and Terrorism by year\n",fontsize=25)
p.axes.set_xlabel("\nYear",fontsize=20)
p.axes.set_ylabel("Total",fontsize=20)

sns.despine(left=True, bottom=True)
plt.show()


# What terrible thing happened in 1994?

# In[20]:


temp=pd.DataFrame(df.groupby("Year")["Conflict and Terrorism"]).reset_index()
temp=df[df["Year"]==1994].sort_values(['Conflict and Terrorism'],ascending=False)

plt.subplots(figsize=(20,8))
p = sns.barplot(x=temp["Country/Territory"][:5],y=temp["Conflict and Terrorism"], saturation=1,edgecolor = "#1c1c1c", linewidth = 3)
p.axes.set_title("\nCountries/territories with the highest number of deaths from Conflict and Terrorism 1994\n",fontsize=25)
plt.xlabel("\nCountry/Territory",fontsize=20)
plt.ylabel("Total",fontsize=20)
plt.xticks(rotation=0)
for container in p.containers:
    p.bar_label(container,label_type="edge",padding=2,size=18,color="black",rotation=0,
    bbox={"boxstyle": "round", "pad": 0.6, "facecolor": "orange", "edgecolor": "#1c1c1c", "linewidth" : 3, "alpha": 1})

sns.despine(left=True, bottom=True)
plt.show()


# # Insight 

# In 1994, the number of deaths from Conflict and Terrorism skyrocketed in Rwanda
# 
# Cause: The Rwandan genocide occurred between 7 April and 15 July 1994 during the Rwandan Civil War. During this period of around 100 days, members of the Tutsi minority ethnic group, as well as some moderate Hutu and Twa, were killed by armed Hutu militias. The most widely accepted scholarly estimates are around 500,000 to 662,000 Tutsi deaths.

# # Tuberculosis

# In[21]:


Tuberculosis=pd.DataFrame(df.groupby("Year")["Tuberculosis"].sum()).reset_index()
sns.set(rc={"axes.facecolor":"red","figure.facecolor":"blue"})
plt.subplots(figsize=(20,8))

p=sns.lineplot(x=Tuberculosis["Year"],
               y=Tuberculosis["Tuberculosis"],
               data=Tuberculosis,
               color="#2540D5",
               marker="o",linewidth=3,markersize=10,
               markerfacecolor="orange",markeredgecolor="red",markeredgewidth=3)
p.axes.set_title("\nNumber of deaths from Tuberculosis by year\n",fontsize=25)
p.axes.set_xlabel("\nYear",fontsize=20)
p.axes.set_ylabel("Total",fontsize=20)

sns.despine(left=True, bottom=True)
plt.show()


# # Insight 

# Tuberculosis
# 
# Tuberculosis dates back to BC. In the past, due to the lack of understanding of the cause of TB, TB was considered a genetic disease. On Sunday, March 24, 1992, a German doctor named Robert Koch announced the discovery of tuberculosis bacteria. At that time TB was ravaging Europe and America with a rate of 1 out of 7 people alive and dying from TB. Thus, on the line graph we see a spike in TB deaths in 1992.
# 
# After 19992, ushered in a new era of TB understanding, advances in TB detection, diagnosis and treatment. Looking at the graph, we can see that the number of deaths from TB decreased significantly after 1992.

# In[ ]:




