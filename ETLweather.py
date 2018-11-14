# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import requests
import json
import calendar
    
    
def get_data(api_key,q,f,tp,startdate,enddate):
    parameters={"key":api_key,
           "q":q,
           "format":f,
           "date":startdate,
           "enddate":enddate,
           "tp":tp
           }

    basic_url= "http://api.worldweatheronline.com/premium/v1/past-weather.ashx" 
    response=requests.get(basic_url,params=parameters)
   
    result=json.loads(response.text)
    result=result["data"]["weather"]
    
    weather_dict=[]
   
    for i in result:
        date=i["date"]
        hour=i["hourly"]
        for j in hour:
            if tp==24:
                weather_dict+=[(date,j["tempF"])]
            else:
                if j["time"]=='2300':
                    weather_dict+=[(date,str(int(int(j["time"])/100))+":"+"00","23:59",j["tempF"])]
                else:
                    weather_dict+=[(date,str(int(int(j["time"])/100))+":"+"00",str(int(int(j["time"])/100)+1)+":"+"00",j["tempF"])]
    return weather_dict

def get_start_end_date_month(year,month):
    days=calendar.monthrange(year,month)[1]
    start_date=str(year)+"-"+str(month)+"-"+"1"
    end_date=str(year)+"-"+str(month)+"-"+str(days)
    return start_date,end_date
    


    
def main():
    api_key='6cb8976bd5b24c40b98200937180911'
    f="json" #alternative xml
    q="37.831106,-122.254110" #lat/lon
    tp=1 #by hourly default by 3
    tp_daily=24 #daily average 
    
    weather_dict=[]
    dailyweather_dict=[]
    for i in range(1,13):
        s,e=get_start_end_date_month(2016,i)
        next_month=get_data(api_key,q,f,tp,s,e)
        next_month_daily=get_data(api_key,q,f,tp_daily,s,e)
        weather_dict+=next_month
        dailyweather_dict+=next_month_daily
    

    with open('hourlyweather.csv','w') as hourlyweather_file:
        hourlyweather_file.write("recorddate"+","+"starttime"+","+"endtime"+","+"hourlytemp" + "\n")
        for i in weather_dict:
            hourlyweather_file.write(i[0]+ "," +i[1]+"," +i[2]+","+i[3])
            hourlyweather_file.write("\n")
    with open('dailyweather.csv','w') as dailyweather_file:
        dailyweather_file.write("recordtime"+"," +"dailytemp" + "\n")
        for i in dailyweather_dict:
            dailyweather_file.write(i[0]+ "," +i[1])
            dailyweather_file.write("\n")

if __name__== "__main__":
    main()