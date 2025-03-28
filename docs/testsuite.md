| Test Target | input data | Expected output | pass/fail criteria | Testing method | in scope modules | Test type
| ----------- | --------------- | ----------- | ----------- | ----------- | ----------- | ----------- |
Log-in rejction | Username: Jonday Password: PasswordQassword | log in details gety flagged as invalid and you remain on the log-in page | if the log in isnt flagged  as invalid or log in is accpepted this is considered a faliure | Simply attempting to log into the website with an invalid log in. | Sign-up/Log in functionality | Manual
| Sign up | Username: Johndoe Password: PasswordPassword | Be taken directly to the logged in page or told sign up info is invalid | not taken to logged in page or flagged for invalid credentials | Attempt to sign up with a dummy accout username and password from the sign up page. | Sign-up/Log in functionality | Manual
| Log in | Same as above | same as above | same as above | Atteempt to Log in with previously used sign up credentials from the log in page. | Sign-up/Log  in functionality | Manual
| page accessability | N/A | A light house score of 90 or above | a score of 90 or above will be considered a pass anything below 90 will be considered a faliure | using the lighthouse accessability extension to test each of the webpages accessability of both mobile and regular webpage displays. | Display Functionality | Automated
River Map gradient display | To be decided | The river color gradient between two sensor point will change colour gradually between two points | A successful gradient displaying the temperature change between two points will constitute a success | using test data streamed to two sensor nodes on the river map, we should see the gradient display between the two of them function properly.| Display Functionality | Manual
 | Performance rating  | N/A  |  A lighthouse performance score of 90+  | anything below 90 on lighthouse is considered a faliure  | Using lightouse metrics we will run a test on the website to check its performance score as an overall metric.  |  Performance functionality | Manual
 |Map style change | N/A | when selecting a different map style the map display changes accordingly | if the map style doesnt change this will be considered a faliure | Selecting between the different style options for the river map display manually | Display/accesibility Functionality | Manual 
 Sensor end point testing | N/A | recieveing a response status code 200 from the unit test to affirm the end points are connected | if the response code returns anything other than 200 | ![alt text](image-2.png) | Sensor data | Automated testing




