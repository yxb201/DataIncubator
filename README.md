# Data Incubator Project Proposal

## Motivation
On each day, it is estimated that more than 400,000 thousand taxi-rides are taken by New Yorkers, creating an enormous amount of trip data that symbolize the heartbeat of the Big Apple. Since the public release of the TLC trip record data, there have been many analyses from the policy-making perspective, primarily focusing on understanding and improving the traffic congestion in the Greater New York Area. Others are interested in how the data can benefit the daily riders, providing services such as tips for cab hailing in Manhattan. For my Data Incubator project, I would like to focus on the standpoint of a yellow cab driver and to answer the general question “What passenger-seeking strategy should I adopt to maximize my daily earning?” in a more quantitative way. This idea is motivated by the observation that, Uber drivers are aided by a mobile app that helps them to identify the next trip, while the vast majority of cab drivers rely on their own experience which can take a long time to build up.  With the tens of millions of TLC trip data available, I am able to dig in deep and quantitatively answer questions such as which neighborhoods have the highest probability of picking up a passenger between 10am-11am, what is the average trip time from Midtown to lower Manhattan between 2pm-3pm, what is the likelihood of getting a high-fare trip at the JFK airport in the evening. With answers to questions like these in mind, I expect to extract the main features that contribute positively toward a daily revenue an the final goal of my project is to build a web recommendation system that provides yellow cab drivers with guides for seeking their next passengers. 

## Exploratory data analysis
The goal of this preliminary exploratory analysis is to convince myself that there is enough spatial-temporal heterogeneity in the data so that my recommendation engine will provide a better strategy to pick the next passenger ride based on the current time and location of the driver. The New York City taxi & limo trip record data from 2009-2015 is publically accessible at [here](http://www.nyc.gov/html/tlc/html/about/trip_record_data.shtml) with an estimated total size of 200GB. For the purpose of exploratory analysis, I will focus on the data of one month (Dec 2015) of yellow cab rides, which consists of a total of more than 10 million rows.  The attributes that I am interested in are pickup/drop-off time and location of a trip, trip distance and fare amount. The pickup/drop-off location of a trip is represented by the latitude and longitude of the GPS coordinate of the location. Ideally, I would like to map these coordinates to a real neighborhood map of NYC and use street blocks to cluster trips that originate from similar locations.  For now, I write a simple route that selects trips within in a prescribed radius of a center coordinate.

```python
def nyctaxi_data(LAT, LONG, RADIUS,df_trip):

    # select pickup locations near (LAT,LONG)
    df = df_trip[(df_ytrip['pickup_longitude']< LONG + RADIUS) 
    & (df_trip['pickup_longitude']> LONG - RADIUS) 
    & (df_trip['pickup_latitude'] < LAT + RADIUS) 
    & (df_trip['pickup_latitude'] > LAT - RADIUS)]

    # extract Hour of pickup and compute statistics of trips
    pickup_hour = np.zeros(len(df))
    trip_dur = np.zeros(len(df))
    trip_dist = np.zeros(len(df))
    speed = np.zeros(len(df))
    
    df_new =df.reset_index()
    for i in range(0, len(df)):
        t_pickup = pd.Timestamp(df_new['tpep_pickup_datetime'][i])
        t_dropoff = pd.Timestamp(df_new['tpep_dropoff_datetime'][i])
        pickup_hour[i]=t_pickup.hour
        # payout per minute
        trip_dur[i]= (t_dropoff - t_pickup).seconds / SEC2MIN

    df_new["pickup_hour"] = pd.DataFrame(pickup_hour)
    df_new["trip_duration_mins"] = pd.DataFrame(trip_dur)

    fare =     df_new[(df_new['trip_duration_mins']>1.0) & (df_new['trip_distance']>0.0)]['fare_amount']
    duration = df_new[(df_new['trip_duration_mins']>1.0) & (df_new['trip_distance']>0.0)]['trip_duration_mins']
    mileage =  df_new[(df_new['trip_duration_mins']>1.0) & (df_new['trip_distance']>0.0)]['trip_distance']
    
    df_new["payout_per_min"]  = pd.DataFrame(fare/duration)
    df_new["payout_per_mile"] = pd.DataFrame(fare/mileage)
    df_new["speed_mile_per_hour"] = pd.DataFrame(mileage/duration*SEC2MIN)

    return df_new
```

In the above routine, I also calculate a few attributes that are not available in the data to aid my analysis. For example, “payout_per_min” measures the revenue per minute of a trip.  My analysis focuses on six representative locations of the city: Times Square, Upper East, City Hall, East Village, JFK and Williamsburg. In the following figure, I plot a histogram of the number of cab pickups in Dec 2015 near these six locations vs. the hours of a day. We observe that the number of pickups near Times Square tops the six locations followed by the Upper East. In particular, Williamsburg seems to have a surprisingly low number of pickups given its popular bars and restaurants. One possible explanation is that taxi service in Williamsburg is mainly covered by the green cabs since its introduction in 2013.  It is also interesting that how the number of pickups vary over the course of a day in each location. For example, it is obvious that Time Square is busy all day as a popular tourist attraction. The number of pickups remains flat for the Upper East in daytime and it quickly dies off in the evening. On the other hand, the number of pickups in East village trends up in the evening mainly because of its bars and restaurants. But does it infer that a driver will be better-off by always picking up passengers near Times Square?

<br>
<img  src = "https://github.com/yxb201/DataIncubator/blob/master/hist_pickups.png" />
<br>

In the next figure, let’s look at the average trip fare amount vs. hours of a day for a trip originating from each location. Interestingly, trips from the City Hall seems to have a higher fare amount compared to the other parts of the city compared here. Not surprisingly, trip fares from JFK tops among the six locations, as it is located far away from the city center. Does it suggest that the JFK airport is ideal place for high-fare ride?

<br>
<img  src = "https://github.com/yxb201/DataIncubator/blob/master/avg_fare.png" />
<br>


In the following figure, we will take a look at the average payout per mile vs. hours of day for trips from these six locations. Again trips from Times Square have the highest ratio of revenue vs. mileage with $8 per mile during rush hour. On the other hand, JFK has lowest overall payout per mile ratio. This can be explained by that yellow cabs charge a flat for trips to Manhattan. But this doesn’t show the whole picture either, as the high payout per mile ratio near Times Square can be caused by heavy traffic in the Midtown. 

<br>
<img  src = "https://github.com/yxb201/DataIncubator/blob/master/payout_per_mile.png" />
<br>

Lastly, we take a look at the average payout per min ratio. This shows a completely opposite story of trips from Times Square with the lowest average payout per min.  On the other hand, low fare rides in the Upper East gives an overall higher ratio. In particular, this ratio increases dramatically in the late night. Maybe it’s a good to pick a passenger from JFK in those times. 

<br>
<img  src = "https://github.com/yxb201/DataIncubator/blob/master/payout_per_min.png" />
<br>

## In Closing
From the preliminary data exploration above, I am convinced that there is enough spatial-temporal heterogeneity in the data that a driver can take advantage of when seeking the next passenger. Yet, there is still other factors such as traffic congestion, trip speed that I have not got the time to touch on. 


