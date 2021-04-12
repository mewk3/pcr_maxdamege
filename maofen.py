# -*- coding: utf-8 -*-
"""
Created on Thu Mar 25 15:36:05 2021

@author: mewk
"""

import pandas as pd
import numpy as np





score_rank = {'A1':1,'A2':1,'A3':1.1,'A4':1.1,'A5':1.2,
              'B1':1.2,'B2':1.2,'B3':1.8,'B4':1.8,'B5':2,
              'C1':2.2,'C2':2.2,'C3':2.5,'C4':2.5,'C5':3
              }

#df_m = pd.read_excel('./猫猫连接box收集表.xlsx')
#df_m1 = df_m.iloc[3:]
#df_char = df_m1.iloc[:,7:]     
#res_char = pd.DataFrame()
#for i in range(int(df_char.shape[1]/3)):
#    df_char1 = df_char.iloc[:,i*3:i*3+3]
#    df_char1['char'] = df_char1.columns[0]
#    df_char1 = pd.concat([df_m1.iloc[:,:2],df_char1],axis=1)
#    df_char1.columns = ['player','time','star','rank','zhuan','char']
#    res_char = pd.concat([res_char,df_char1])
#res_char_drop = res_char.dropna(subset=['star'])
#res_char_drop = res_char_drop[res_char_drop['star']!='无']
#res_char_player = res_char_drop[res_char_drop['player']=='全网在逃']
#
#player_pool = res_char_player['char'].unique().tolist()  

df_player = pd.read_excel('box.xlsx')
player_pool = df_player['wkq'].dropna().astype(str).values.tolist()
#df = pd.read_excel('rk.xlsx')
df = pd.read_excel('homework.xlsx',sheet_name='Sheet3')
test = pd.read_excel('./name_mapping.xlsx')

def scan_team(str1):
#str1 = '真琴克总狗环忍'
#test = test.set_index('after')
    res =[]
    for j in range(1,test.shape[1]):
        for i in range(test.shape[0]):    
            bf_str =  str(test[test.columns[j]].values[i])
            af_str =  str(test['after'].values[i])
            if bf_str==bf_str and  bf_str in str1:
                str1 = str1.replace(bf_str,'')
                res.append(af_str)
    return res
if 'team' in df.columns: 
    df['team_l'] = df['team'].map(scan_team)
    df2 = df['team_l'].apply(pd.Series)
    df2.columns = ['p1','p2','p3','p4','p5']
    df = pd.concat([df,df2],axis=1)

df['score_rank'] = df['boss'].replace(score_rank)
df['score'] = df['dmg']*df['score_rank']
df['p1'] = df['p1'].astype(str)
df['p2'] = df['p2'].astype(str)
df['p3'] = df['p3'].astype(str)
df['p4'] = df['p4'].astype(str)
df['p5'] = df['p5'].astype(str)
res_df = pd.DataFrame({'刀1':[],'刀1练度':[],'刀2':[],'刀2练度':[],'刀3':[],'刀3练度':[],'总伤':[],'总分':[],'作业号':[]})
for i in range(0,len(df.index)):
    for j in range(i,len(df.index)):
        for k in range(j,len(df.index)):
            team1 = df.loc[i,['p1','p2','p3','p4','p5']].values
            team2 = df.loc[j,['p1','p2','p3','p4','p5']].values
            team3 = df.loc[k,['p1','p2','p3','p4','p5']].values
            t12 = pd.Series(np.concatenate([team1,team2])).value_counts()
            t13 = pd.Series(np.concatenate([team1,team3])).value_counts()
            t23 = pd.Series(np.concatenate([team2,team3])).value_counts()
#            need_character = t12[t12>=2].index.tolist()+t13[t13>=2].index.tolist()+t23[t23>=2].index.tolist()
            need_character = set(t12.index.tolist()+t13.index.tolist()+t23.index.tolist())
            if [x for x in need_character if x not in player_pool]:
                continue
            elif len(t12[t12>=2])<2 and len(t13[t13>=2])<2 and len(t23[t23>=2])<2:
                res = {}
                res['刀1'] = df.loc[i,'boss'] +':'+','.join(team1.tolist())+':'+str(df.loc[i,'dmg'])
                res['刀2'] = df.loc[j,'boss'] +':'+','.join(team2.tolist())+':'+str(df.loc[j,'dmg'])
                res['刀3'] = df.loc[k,'boss'] +':'+','.join(team3.tolist())+':'+str(df.loc[k,'dmg'])
                res['刀1练度'] = df.loc[i,'note']
                res['刀2练度'] = df.loc[j,'note']
                res['刀3练度'] = df.loc[k,'note']
                res['总伤'] = int(df.loc[i,'dmg'])+int(df.loc[j,'dmg'])+int(df.loc[k,'dmg'])
                res['总分'] = int(df.loc[i,'score'])+int(df.loc[j,'score'])+int(df.loc[k,'score'])
                res['作业号'] = df.loc[i,'pid']+' '+ df.loc[j,'pid']+' '+ df.loc[k,'pid']
                res_df = res_df.append(res,ignore_index=True)
            else:
                continue
res_df = res_df.sort_values(by=['总分','总伤'],ascending=False)
res_df['dr'] = res_df['刀1'] +'!!'+ res_df['刀2'] +'!!'+ res_df['刀3']
res_df['dr'] = res_df['dr'].str.split('!!')
res_df['dr'] = res_df['dr'].map(lambda x:sorted(x))
res_df['dr'] = res_df['dr'].astype(str)
res_df = res_df.drop_duplicates(subset='dr')


#1

#import pandas as pd
#test = pd.read_excel('./角色匹配表.xlsx')
#
#str1 = '真琴克总狗环忍'
##test = test.set_index('after')
#res =[]
#for j in range(1,test.shape[1]):
#    for i in range(test.shape[0]):    
#        bf_str =  str(test[test.columns[j]].values[i])
#        af_str =  str(test['after'].values[i])
#        print(bf_str,af_str)
#        if bf_str==bf_str and  bf_str in str1:
#            str1 = str1.replace(bf_str,'')
#            res.append(af_str)
