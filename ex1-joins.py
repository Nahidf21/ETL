import io
import pandas as pd
import requests as r

#variables needed for ease of file access
url = 'http://drd.ba.ttu.edu/isqs6339/ex/L2.1/'
file_1 = 'employment.csv'
file_2 = 'job_title.csv'
file_3 = 'job_title_year.csv'

#pull employment
res = r.get(url + file_1)
res.status_code
df_emp = pd.read_csv(io.StringIO(res.text)) 

#pull job
res = r.get(url + file_2)
res.status_code
df_job = pd.read_csv(io.StringIO(res.text)) 

df_emp.head()
df_job.head()

###############################################################################
#                Basic joins                                                  #
###############################################################################

#Note, could just use "on" rather than left/right on as the field is the same name
df_emp_merge = df_emp.merge(df_job, how="inner", left_on="jobtitleid", right_on="jobtitleid")
df_emp_merge.head()

#Did we lose any data?  i.e.  what is the meaning of an inner join
df_emp_merge['jobtitle'].value_counts()
df_job['jobtitle']

#Let's do a left join
df_emp_merge_left = df_emp.merge(df_job, how='left', on='jobtitleid')
df_emp_merge_left['jobtitle'].value_counts() #wait!  we left join, where's the mungers!

#Time to demo the right join
df_emp_merge_right = df_emp.merge(df_job, how='right', on='jobtitleid')
df_emp_merge_right['jobtitle'].value_counts() #Ahh, so outside is left side of 
#operator and inside is the right side of the operator.

#Wait, why is Munger a "1" on value_counts????
#Answer, we only asked it to count that column
#More on how this can help us later.

###############################################################################
#                               Multikey join                                 #
###############################################################################

#Let's say our employees were only for 2018 and our job title file was
#also keyed to year.  

#Let's get our new job title file
#pull job
res = r.get(url + file_3)
res.status_code
df_job_year = pd.read_csv(io.StringIO(res.text)) 

#Notice the yr and salary increases of 2K
df_job_year

#Let's add a yr field to our emps and make it 2019
df_emp['yr'] = 2019
df_emp.head()

#Now, let's join.  Note, we can't do it on a single field
df_emp_merge_yr = df_emp.merge(df_job_year, how='inner', on=['jobtitleid', 'yr'])
df_emp_merge_yr

#similar logic using left_on, right_on.  
df_emp_merge_yr_lr = df_emp.merge(df_job_year, how='inner', left_on=['jobtitleid', 'yr'], right_on=['jobtitleid', 'yr'])
df_emp_merge_yr_lr

#Note, the order of the fields matters
df_emp_merge_yr_lr2 = df_emp.merge(df_job_year, how='inner', left_on=['yr', 'jobtitleid'], right_on=['jobtitleid', 'yr'])
df_emp_merge_yr_lr2


###############################################################################
#                            Join Issues - Missing Keys                       #
###############################################################################

#pull employment
res = r.get(url + file_1)
res.status_code
df_emp = pd.read_csv(io.StringIO(res.text)) 

#pull job
res = r.get(url + file_2)
res.status_code
df_job = pd.read_csv(io.StringIO(res.text)) 

#Let's join our files
dfmerged = df_emp.merge(df_job, how='inner', on='jobtitleid')
dfmerged.head()

#let's look at count
dfmerged.count()
#where are our rows????.  note our join type
dfmerged = df_emp.merge(df_job, how='left', on='jobtitleid')
dfmerged.count()

#so what happened?
#Let's update with an "other" option.  0 for average age and salary
dfmergedcln = dfmerged.fillna({'jobtitleid' : -1, 'jobtitle':'other', 'avg_salary':0, 'avg_age':0})
dfmergedcln.count()

#Note, the prior example has us update values "hardcoded"
#in practice, it may be better to add that row to the job file,
#add our 'dummy' job titleid to our file
#then remerge.  It may save potential errors in keying in data.


###############################################################################
#                           Update on groupings                               #
###############################################################################


res = r.get(url + 'emplist_salary.csv')
res.status_code
dfemplist = pd.read_csv(io.StringIO(res.text)) 

#Recall our missing salaries.  
dfemplist[dfemplist['salary'].isna()]

#Let's do a grouping based on jobtitle
dfavgsal = dfemplist[['jobtitle', 'salary']].groupby('jobtitle').mean()
dfavgsal
#notice that computing averages does not take into account "null" rows.  no need to
#run the next line.  uncomment to see point.
#dfavgsal2 = dfemplist[['jobtitle', 'salary']][dfemplist['salary'].notnull()].groupby('jobtitle').mean()

#Now, let's merge this onto our emplist file.  
dfempfinal = dfemplist.merge(dfavgsal, how='inner', on='jobtitle')
dfempfinal
#Note, it is in the index (jobtitle on dfavgsal), this is also valid.  

#dfempfinal2 = dfemplist.merge(dfavgsal, how='inner', left_on='jobtitle', right_index=True)

#Wait, what happen??????  Look at the column names.
#where did the _x and _y come from?

#better solution.  rename the columns from the average dataframe first.
dfavgsal.rename(columns={'salary' : 'avg_salary'}, inplace=True)

#Now merge.  see the difference
dfempfinal2 = dfemplist.merge(dfavgsal, how='inner', on='jobtitle')
dfempfinal2

#Finally, let's update the missing salaries.
dfempfinal2['salary'][dfempfinal2['salary'].isna()] = dfempfinal2['avg_salary']

#Note, if you don't want to change the copy with settings, you can alternatively
#do the following without the merge

#update post merge no copywithsettings
for index, row in dfempfinal2[dfempfinal2['salary'].isna()].iterrows():
    dfempfinal2.at[index, 'salary'] = row['avg_salary']
dfempfinal2

#update pre-merge, no rename, no copy with settings.  
for index, row in dfemplist[dfemplist['salary'].isna()].iterrows():
    dfemplist.at[index, 'salary'] = dfavgsal.at[row['jobtitle'], 'avg_salary']    
dfemplist









