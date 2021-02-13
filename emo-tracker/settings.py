TRACK_WORDS = ['music', 'reading', 'movies', 'books', 'workout', 'yoga', 'netflix', 'Netflix',
				'instagram', 'twitter', 'tiktok', 'cooking']
TABLE_NAME = "nairobitweets"
TABLE_ATTRIBUTES = "id_str VARCHAR(255), created_at Timestamp, text VARCHAR(255), \
            polarity INT, subjectivity INT, user_created_at VARCHAR(255), user_location VARCHAR(255), \
            user_description VARCHAR(255), user_followers_count INT, longitude double precision, latitude double precision, \
            retweet_count INT, favorite_count INT"
REGION = [-1.2921, 36.8219, -1.2921, 36.8219]
'''bounding_box = [-1.1597918307560573,37.106463945682584,-1.1597918307560573, 36.665974517587834, -1.3891756881977984,36.665974517587834, -1.3891756881977984, 37.106463945682584]


location =  {
					'type': 'Polygon',
					'coordinates': [
							[
								[-1.1597918307560573, 37.106463945682584],
								[-1.1597918307560573, 36.665974517587834],
								[-1.3891756881977984, 36.665974517587834],
								[-1.3891756881977984, 37.106463945682584]
							]
					]
		}

print(location)
print(type(location))'''