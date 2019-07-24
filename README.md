# NBA Business Hackathon

Project Participants: Ramtin Talebi, Jefferey Huang, Daniel Alpert, Nate Hollenberg\\ 
Hackathon Info: https://hackathon.nba.com/

This project, part of the NBA Hackathon challenge, predicts the number of engagements (as defined by the NBA) using random forest algorithms based upon three provided variables: the post type (photo, video, album), post date-time, and full description. A training set of 7500+ posts and hold-out set of 1000 posts were provided, and submissions are graded on Mean Absolute Prediction Error (MAPE) on the holdout set.

In this project, we trained a random forest algorithm on our data, after extending our dataset. We used each of the three variables to create more descriptive ones (i.e. whether or not post was made during the playoffs, whether it mentioned an all-NBA player, etc.). Descriptions of our data wrangling process can be found in the PDF writeup and in the RMD file above. 
