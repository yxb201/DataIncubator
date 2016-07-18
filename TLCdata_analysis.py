%matplotlib inline 
import matplotlib
import matplotlib.pylab as plt
import pandas as pd
import numpy as np
matplotlib.style.use('ggplot')


def nyctaxi_data(LAT, LONG, RADIUS, df_trip):

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
        # compute pickup hour and trip duration
        pickup_hour[i]=t_pickup.hour
        trip_dur[i]= (t_dropoff - t_pickup).seconds / SEC2MIN

	# add pickup_hour and trip duration as columns 
    df_new["pickup_hour"] = pd.DataFrame(pickup_hour)
    df_new["trip_duration_mins"] = pd.DataFrame(trip_dur)

    fare =     df_new[(df_new['trip_duration_mins']>1.0) & (df_new['trip_distance']>0.0)]['fare_amount']
    duration = df_new[(df_new['trip_duration_mins']>1.0) & (df_new['trip_distance']>0.0)]['trip_duration_mins']
    mileage =  df_new[(df_new['trip_duration_mins']>1.0) & (df_new['trip_distance']>0.0)]['trip_distance']
    
    # compute useful ratios
    df_new["payout_per_min"]  = pd.DataFrame(fare/duration)
    df_new["payout_per_mile"] = pd.DataFrame(fare/mileage)
    df_new["speed_mile_per_hour"] = pd.DataFrame(mileage/duration*SEC2MIN)

    return df_new
    
    
# change your dataset location
yellow_data = "~/Desktop/yellow_tripdata_2015-12.csv"
yfields = ["tpep_pickup_datetime",
           "tpep_dropoff_datetime",
           "pickup_latitude",
           "pickup_longitude",
           "trip_distance",
           "fare_amount"]
df_ytrip = pd.read_csv(yellow_data, usecols = yfields)


# constant for converting time units
SEC2MIN = 60.0

# JFK coordinates and data
JFK_LAT = 40.645391
JFK_LONG = -73.784772
radius = 0.01
df_JFK = nyctaxi_data(JFK_LAT, JFK_LONG, radius, df_ytrip)

# Upper East coordinates and data
UPPER_EAST_LAT =  40.769685
UPPER_EAST_LONG = -73.960588
radius = 0.006
df_UPPER_EAST = nyctaxi_data(UPPER_EAST_LAT, UPPER_EAST_LONG, radius, df_ytrip)

# City Hall coordinates and data
CITY_HALL_LAT =   40.712980
CITY_HALL_LONG = -74.007432
radius = 0.006
df_CITY_HALL = nyctaxi_data(CITY_HALL_LAT, CITY_HALL_LONG, radius, df_ytrip)

# Times Square coordinates and data
TIMES_SQ_LAT = 40.754790
TIMES_SQ_LONG = -73.987958
radius = 0.006
df_TIMES_SQ = nyctaxi_data(TIMES_SQ_LAT, TIMES_SQ_LONG, radius, df_ytrip)

# East Village coordinates and data
EAST_VILLAGE_LAT =  40.727811
EAST_VILLAGE_LONG = -73.982154
radius = 0.006
df_EAST_VILLAGE = nyctaxi_data(EAST_VILLAGE_LAT, EAST_VILLAGE_LONG, radius, df_ytrip)

# Williamsburg coordinates and data
WILLIAMSBURG_LAT =  40.712240
WILLIAMSBURG_LONG = -73.957184
radius = 0.006
df_WILLIAMSBURG = nyctaxi_data(WILLIAMSBURG_LAT, WILLIAMSBURG_LONG, radius, df_ytrip)


# ------ PLOT ---------
# histogram of number of pickups
plt.figure(1,figsize = [16,20])
plt.subplot(2,2,1)
df_TIMES_SQ["pickup_hour"].hist(bins=24,range=(0,23), stacked = True, alpha=0.7)
df_UPPER_EAST["pickup_hour"].hist(bins=24,range=(0,23), stacked = True, alpha=0.7)
df_CITY_HALL["pickup_hour"].hist(bins=24,range=(0,23), stacked = True, alpha=0.7)
plt.legend(['Times Square', 'Upper East', 'City Hall'], loc = 2)
plt.xlabel('Hour of pick up')
plt.ylabel('Number of pickups in Dec 2015')
plt.xlim([0,23])


plt.subplot(2,2,2)
df_EAST_VILLAGE["pickup_hour"].hist(bins=24,range=(0,23), stacked = True,alpha=0.7)
df_JFK["pickup_hour"].hist(bins=24,range=(0,23), stacked = True,alpha=0.7)
df_WILLIAMSBURG["pickup_hour"].hist(bins=24,range=(0,23), stacked = True, alpha=0.7)
plt.ylim([0,60000])
plt.legend(['East Village', 'JFK', 'Williamsburg'])
plt.xlabel('Hour of pick up')
plt.ylabel('Number of pickups in Dec 2015')
plt.xlim([0,23])
plt.savefig('DataIncubator/hist_pickups.png',bbox_inches='tight',format='png', dpi = 300)


# avg payout per min 
plt.figure(2,figsize = [16,20])
plt.subplot(2,2,1)
df_TIMES_SQ.groupby(["pickup_hour"])["payout_per_min"].mean().plot()
df_UPPER_EAST.groupby(["pickup_hour"])["payout_per_min"].mean().plot()
df_CITY_HALL.groupby(["pickup_hour"])["payout_per_min"].mean().plot()
plt.ylim([0.8,2.0])
plt.legend(['Times Square', 'Upper East', 'City Hall'])
plt.xlabel('Hour of pick up')
plt.ylabel('Avg payout per min (dollar/min)')

plt.subplot(2,2,2)
df_EAST_VILLAGE.groupby(["pickup_hour"])["payout_per_min"].mean().plot()
df_JFK.groupby(["pickup_hour"])["payout_per_min"].mean().plot()
df_WILLIAMSBURG.groupby(["pickup_hour"])["payout_per_min"].mean().plot()
plt.legend(['East Village', 'JFK', 'Williamsburg'])
plt.xlabel('Hour of pick up')
plt.ylabel('Avg payout per min (dollar/min)')
plt.savefig('DataIncubator/payout_per_min.png',bbox_inches='tight',format='png', dpi = 300)

# avg payout per mile
plt.figure(3,figsize = [16,20])
plt.subplot(2,2,1)
df_TIMES_SQ.groupby(["pickup_hour"])["payout_per_mile"].mean().plot()
df_UPPER_EAST.groupby(["pickup_hour"])["payout_per_mile"].mean().plot()
df_CITY_HALL.groupby(["pickup_hour"])["payout_per_mile"].mean().plot()
plt.legend(['Times Square', 'Upper East', 'City Hall'], loc = 3)
plt.ylim([0,9])
plt.xlabel('Hour of pick up')
plt.ylabel('Avg payout per mile (dollar/mile)')


plt.subplot(2,2,2)
df_EAST_VILLAGE.groupby(["pickup_hour"])["payout_per_mile"].mean().plot()
df_JFK.groupby(["pickup_hour"])["payout_per_min"].mean().plot()
df_WILLIAMSBURG[df_WILLIAMSBURG["payout_per_mile"]<1000].groupby(["pickup_hour"])["payout_per_mile"].mean().plot()
plt.legend(['East Village', 'JFK', 'Williamsburg'], loc = 3)
plt.xlabel('Hour of pick up')
plt.ylabel('Avg payout per mile (dollar/mile)')
plt.savefig('DataIncubator/payout_per_mile.png',bbox_inches='tight',format='png', dpi = 300)

# avg fare amount 
plt.figure(4,figsize = [16,20])
plt.subplot(2,2,1)
df_TIMES_SQ.groupby(["pickup_hour"])["fare_amount"].mean().plot()
df_UPPER_EAST.groupby(["pickup_hour"])["fare_amount"].mean().plot()
df_CITY_HALL.groupby(["pickup_hour"])["fare_amount"].mean().plot()
plt.legend(['Times Square', 'Upper East', 'City Hall'])
plt.xlabel('Hour of pick up')
plt.ylabel('Avg fare amount in dollars')

plt.subplot(2,2,2)
df_EAST_VILLAGE.groupby(["pickup_hour"])["fare_amount"].mean().plot()
df_JFK.groupby(["pickup_hour"])["fare_amount"].mean().plot()
df_WILLIAMSBURG.groupby(["pickup_hour"])["fare_amount"].mean().plot()
plt.legend(['East Village', 'JFK', 'Williamsburg'])
plt.xlabel('Hour of pick up')
plt.ylabel('Avg fare amount in dollars')
plt.savefig('DataIncubator/avg_fare.png',bbox_inches='tight',format='png', dpi = 300)