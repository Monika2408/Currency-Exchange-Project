# -*- coding: utf-8 -*-
"""
Created on Sat Feb 18 15:02:18 2023


"""

import streamlit as st
import pandas as pd
import numpy as np

import datetime as dt
from datetime import timedelta
from fbprophet import Prophet
import matplotlib.pyplot as plt
from datetime import datetime

st.markdown("""
            <style>
            .css-9s5bis.edgvbvh3
            {
                visibility:hidden;
                }
            .css-h5rgaw.egzxvld1
            {
                visibility:hidden;
                }
            """,unsafe_allow_html=True)
            

ind,tit,usa=st.columns(3)
ind.image("India_flag.jpg")
tit.title("USD$ - INR Curency Ex")
usa.image("flag.jpg")



def data_collection():
    data=pd.read_csv("usd_data_2010_inr.csv")
    data=data.drop(columns=['Unnamed: 0', 'Unnamed: 0.1', 'Currency', 'Name', 'USD per unit'])
    def dateRange(StartDate,EndDate):
        for n in range(int((EndDate-StartDate).days)):
            yield StartDate + timedelta(n)
    def string_to_date(date_str):
        return datetime.strptime(date_str, '%Y-%m-%d').date()
    
    StartDate=string_to_date(data['Date'][len(data)-1])+timedelta(days=1)
    EndDate=dt.date.today()
    curr_data=pd.DataFrame()
    for Single_date in dateRange(StartDate, EndDate):
        dfs=pd.read_html(f'https://www.xe.com/currencytables/?from=USD&date={Single_date.strftime("%Y-%m-%d")}')[0]
        dfs['Date']=Single_date.strftime("%Y-%m-%d")
        curr_data=curr_data.append(dfs)

    inr_data=curr_data[curr_data['Currency']=='INR']
    inr_data=inr_data.drop(columns=['Currency','Name','USD per unit'])
    inr_data=pd.concat([data,inr_data], ignore_index=True)
    inr_data['org_Units per USD']=inr_data['Units per USD']
    inr_data['Units per USD']=np.log(inr_data['Units per USD'])
    inr_data=inr_data.rename(columns={'Units per USD':'y','Date':'ds'})
    return inr_data


def ForecastPredection(x,y,data):
    model=Prophet()
    model.fit(data)
    future_data=model.make_future_dataframe(periods=x,freq=y)
    forecast_data=model.predict(future_data)
    forecast_data['yhat']=np.exp(forecast_data['yhat'])
    forecast_data['yhat_lower']=np.exp(forecast_data['yhat_lower'])
    forecast_data['yhat_upper']=np.exp(forecast_data['yhat_upper'])
    raw_yprd_data=pd.DataFrame(forecast_data)
    mod_ypred_data=raw_yprd_data.drop(columns=['trend','trend_lower','trend_upper','additive_terms','additive_terms_lower',
                                               'additive_terms_upper','weekly','weekly_lower','weekly_upper','yearly',
                                               'yearly_lower','yearly_upper','multiplicative_terms',
                                               'multiplicative_terms_lower','multiplicative_terms_upper'])
    
    return mod_ypred_data



def main():
    sel_box=st.selectbox("***Select Time Parameter for Forecasting***", options=("--Select Cetegory-- ","Day","Week","Fortnight","Month","Year"))

    cate=""     #Category "None","Day","Week","Fortnight","Month","Year"

    min_val=0
    max_val=365
    if sel_box=="--Select Cetegory--":
        pass
    elif sel_box=="Day":
        cate="D"
        min_val=0
        max_val=365
    elif sel_box=="Week":
        cate="W"
        min_val=0
        max_val=104
    elif sel_box=="Fortnight":
        cate="F"
        min_val=0
        max_val=120
    elif sel_box=="Month":
        cate="M"
        min_val=0
        max_val=120
    elif sel_box=="Year":
        cate="Y"
        min_val=0
        max_val=12
    #st.write(cate)
    prd=st.number_input("Enter the time period for Forecasting",min_value=min_val, max_value=max_val)
        
    if st.button('Forecast'):
        data=data_collection()
        #st.write(data)
        final_data=ForecastPredection(prd,cate,data)
        st.write(final_data)
        data['idx'] = data.index
        final_data['idx'] = final_data.index
        merged_df = pd.merge(data, final_data, on='idx', how='outer')
        #st.write(merged_df)
        Actual=merged_df['org_Units per USD']
        ds = merged_df['ds_y']
        Predicted = merged_df['yhat']
        yhat_upper = merged_df['yhat_upper']
        yhat_lower = merged_df['yhat_lower']
        fig=plt.figure()
        ax=fig.add_subplot(111)
        ax.plot(ds,Predicted,label='Predicted')
        ax.plot(ds,Actual,label='Actual')
        ax.plot(ds,yhat_lower,label='Yhat_Lower')
        ax.plot(ds,yhat_upper,label='Yhat_Upper')
        ax.set_ylabel('Exchange Rates')
        ax.set_xlabel('Timeline')
        ax.set_title('Graphical Representation')
        plt.show()
        st.plotly_chart(fig, use_container_width=True)
        
        
        
           
        
if __name__=='__main__':
    main()
