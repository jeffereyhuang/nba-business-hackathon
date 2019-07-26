# NBA Business Hackathon - Predicting Instagram Engagments using Tuned Random Forest model

Project Participants: Ramtin Talebi, Jefferey Huang, Daniel Alpert, Nate Hollenberg

### Introduction
This project, part of the NBA Hackathon challenge (https://hackathon.nba.com/), predicts the number of engagements (as defined by the NBA) using random forest algorithms. The dataset provided gives three variables: the post type (photo, video, album), post date-time, and full post description. A training set of 7500+ posts and hold-out set of 1000 posts were provided, and submissions are graded on Mean Absolute Prediction Error (MAPE) on the holdout set. The report is in PDF and MD form above, and additional code is found in the Business Analytics directory. Predictions are found in the holdout_set above.

### Approach

In this project, we trained a random forest algorithm on our data, after extending our dataset. We used each of the three variables to create more descriptive ones (i.e. whether or not post was made during the playoffs, whether it mentioned an all-NBA player, etc.). Then, after conducting EDA, we determined more meaningful splits, and training random forest algorithms on each post type (photos, videos and albums), ultimately arriving at a MAPE of 5%. See below for our calculations.

![](Predicting_IG_Engagements_files/figure-markdown_strict/unnamed-chunk-7-1.png)

### Code Snippets & Primary Results

Although the code is not included here, we tried to create a number of different models, inlcuding a least squares regression model, a gradient boosted model, a model using NLP that vectorized the descriptions column, and even using predicted values from these models into other models. Ultimately, after testing the accuracy of each, we settled on a Random Forest, as it appeared to perform best and was the least overfitted.

In order to train and validate our Random Forest model, we first divide our training set by post type, and then within each division, we subset a small testing data set from our full training set and use it to calculate the MAPE.
 
``` r
RF_Video <- randomForest(Engagements ~ Followers+month+day_time+weekday+Followers_Mentioned
                         +is_season+all_nba+league_type+num_ats+num_hash,
                         ntree=1000, mtry=7,importance=TRUE,
                         data=train_dataRF_Video)

RF_Album <- randomForest(Engagements ~ Followers+month+day_time+weekday+Followers_Mentioned
                         +is_season+all_nba+league_type+num_ats+num_hash,
                         ntree=1000, mtry=8,importance=TRUE,
                         data=train_dataRF_Album)

RF_Photo <- randomForest(Engagements ~ Followers+month+day_time+weekday+Followers_Mentioned
                         +is_season+all_nba+league_type+num_ats+num_hash,
                         ntree=1000, mtry=7,importance=TRUE,
                         data=train_dataRF_Photo)
```

    ## Video
    ##                Type of random forest: regression
    ##                      Number of trees: 1000
    ## No. of variables tried at each split: 7
    ## 
    ##           Mean of squared residuals: 2269818337
    ##                     % Var explained: 77.14

    ## Album
    ##                Type of random forest: regression
    ##                      Number of trees: 1000
    ## No. of variables tried at each split: 8
    ## 
    ##           Mean of squared residuals: 850017793
    ##                     % Var explained: 78.54

    ## Photo
    ##                Type of random forest: regression
    ##                      Number of trees: 1000
    ## No. of variables tried at each split: 7
    ## 
    ##           Mean of squared residuals: 727415628
    ##                     % Var explained: 81.61

``` r
mape_Rf
```

    ## [1] 4.93106

Our validation MAPE came out to about 5%. Not bad!

### Insights & Tuning the Model
Let's take a look at how our percent error is distributed across the testing set.

![](Predicting_IG_Engagements_files/figure-markdown_strict/unnamed-chunk-12-1.png) 

It appears that there are a few extreme outliers in our dataset that the model performs particularly poorly on. One in particular our model overshoots the most appears to be a post about Lebron James at a WNBA game. Intuitively, it makes sense that our model would perform poorly here. Mentioning Lebron would push the model to predict a higher engagement than would be normal for a WNBA game. Given how few outliers are, that the Random Forest is typically robust to outliers, and how rare a post like Lebron at a WNBA game is, we conclude that our model performs quite well.

Here we plot some of our variables to examine which are most critical to our model's accuracy. Notably, it appears that our variables vary in importance between the subsets for Videos, Albums, and Photos. This gives some credibility to our initial assumption that Video, Albums, and Photos should each have their own model.


![](Predicting_IG_Engagements_files/figure-markdown_strict/unnamed-chunk-13-1.png)

``` r
varImpPlot(RF_Album)
```

![](Predicting_IG_Engagements_files/figure-markdown_strict/unnamed-chunk-13-2.png)

``` r
varImpPlot(RF_Photo)
```

![](Predicting_IG_Engagements_files/figure-markdown_strict/unnamed-chunk-13-3.png)

### Results
The predictions are contained in the attached "holdout.csv" file.

