# API Issues

1) authentication in query url
2) csv is only semi-structured and requires a custom parser
3) if a sensor goes down for a full day and you request that days data, it just serves you all the data that sensor ever recorded. (~1.2mb so far)
4) datetime formats are not following any ISO standard
5) invalid dates do not return an error and instead return all data ever recorded

Note: Having dissolved oxygen percentage and amount opens up the possibility of having inconsistent data. There is an example of this in the data if you request for `start_date=2025-02-14&end_date=2025-02-14`, where all values are 0 except for dissolved oxygen percentage which is NaN.

