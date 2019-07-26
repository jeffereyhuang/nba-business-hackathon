NBA Hackathon (Business Analytics) - Tuned Random Forest Model for Predicting Instagram Engagments
================

### Introduction

Presented with the task of predicting the number of engagements with Instagram posts of the account from the past two years, our team elected to create a partitioned Random Forest Model from the package in . Our models were partitioned based on post medium (The prompt seemed to allude to this as well, so we explored accordingly and confirmed the suggestion). Here we present our process for cleaning and modifying the data, visualizing trends, training the Random Forest, evaluating and tuning it, and finally applying it to predict in our holdout set.

First, we defined functions to calculate predicted values, absolute percent error of each prediction, and mean absolute percent error as follows (this will be useful for training later):

``` r
## Create useful functions for calculating mape
Calc_Mape <- function(labels, dataset, model)
  {
    actual = labels
    predicted = predict(model, dataset)
    APE = abs((actual - predicted)/actual) * 100
    mape = mean(APE)
    return(mape)
  }
Calc_Predicted <- function(model, dataset)
  {
    predicted = predict(model, dataset)
    return(predicted)
  }
Calc_PE <- function(labels, dataset, model)
  {
    actual = labels
    predicted = predict(model, dataset)
    PE = ((actual - predicted)/actual) * 100
    return (PE)
  }
```

Next we loaded in the necessary packages and read in the training set:

Predictors Preparation and Data Parsing
---------------------------------------

After sorting and examining the dataset across a number of predictors, we noticed that some of the posts did not contain descriptions and others only contained an emoji or symbol. To avoid any unnecessary influence from these observations, we deleted these entries entirely (while we recognize that imputing the mean for the predictors of these observations is likely a better approach, we felt that this wouldn't entirely be accurate given that they were text descriptions).

In addition, we created variables for the number of instagram accounts mentioned (num\_ats) and the number of hashtags (num\_hash) in each post. We also converted some of our categorical predictors into numerical predictors (useful for creating a Correlation Plot later).

Note: In an attached Python file, you will find some code with our initial modifications to the dataset, including using datetime functions, parsing out important information from the column and Instagram descriptions.

``` r
## Deleting missing data

# Order data by post description
df <- df[order(df$Description),]

# Delete descriptions with NAs, just symbols, or just emojis
# and remove season_yr and is_finals column

nba <- df[-c(1:14,20:35),-c(15,17)]
```

By the end, both our training and holdout sets contained the following predictors:

 - Index variable

 - \# of Followers at time of posting

 - Timestamp of posting

 - Type of Post; three factors:

 - Post caption

 - Datetime variable parsed from

 - Year it was posted

 - Month posted (parsed )

 - Numeric variable for months ( = January). Useful for correlation plot

 - Day of week posted

 - Time of day posted

 - Boolean: whether the post was made in the playoffs (True) or not (False)

 - Boolean: whether the post was made during the season/playoffs (True) or off-season (False)

 - Number of followers of nba team accounts mentioned in post

 - Three factor variable: if no all-nba or all-star players are mentioned in . if an all-nba is mentioned in the , not including those to follow. if Lebron James, Stephen Curry, Kyrie Irving, or Kobe Bryant (NBA players with highest number of instagram followers) are mentioned. Although Kobe is retired, posts with his mention appeared to garner more engagements.

 - if mentioned the WNBA or G-League, otherwise.

 - if post was created within the same on the same day. otherwise. Parsed from .

 - Number of hashtags in the .

 - Number of @ symbols in the .

 - Numerical variable for ( = Video, = Album, = Photo). Useful for correlation plot.

 - Only in training. Numerical variable for ( = Monday, = Sunday)

 - Only in training. Numerical variable for ( = deazone, = postgame)

### Data Visualizations

Here we provide some visualizations of our training data to understand the relationships between some of our predictors and Engagements. First some boxplots of predictors effects on .

![](Predicting_IG_Engagements_files/figure-markdown_github/plots-1.png)![](Predicting_IG_Engagements_files/figure-markdown_github/plots-2.png)![](Predicting_IG_Engagements_files/figure-markdown_github/plots-3.png)![](Predicting_IG_Engagements_files/figure-markdown_github/plots-4.png)![](Predicting_IG_Engagements_files/figure-markdown_github/plots-5.png)![](Predicting_IG_Engagements_files/figure-markdown_github/plots-6.png)![](Predicting_IG_Engagements_files/figure-markdown_github/plots-7.png)

Now let's see how our data looks across post types.

![](Predicting_IG_Engagements_files/figure-markdown_github/post%20type%20plots-1.png)![](Predicting_IG_Engagements_files/figure-markdown_github/post%20type%20plots-2.png)![](Predicting_IG_Engagements_files/figure-markdown_github/post%20type%20plots-3.png)![](Predicting_IG_Engagements_files/figure-markdown_github/post%20type%20plots-4.png)![](Predicting_IG_Engagements_files/figure-markdown_github/post%20type%20plots-5.png)![](Predicting_IG_Engagements_files/figure-markdown_github/post%20type%20plots-6.png)![](Predicting_IG_Engagements_files/figure-markdown_github/post%20type%20plots-7.png)

From our visualizations, one notable result sticks out: The effect of mentioning a superstar player (LBJ, Curry, Kobe, or Kyrie), is quite significant. Other trends seem to be relatively straightforward with some minor exceptions.

In order to assess multicollinearity in our predictors, we created a plot to visualize correlations between each variable The first plot displays the pearson correlation coefficient (R) between predictors, shown by the size and color of the circles at each point in the matrix. The second plot shows the same matrix, but this time with insignificant predictors (p-value &lt; 0.01) crossed-out. With the remaining predictors, nothing in particular seems striking, except for two points:

1.  The correlation between and . Intuitively this makes sense, a post must mention another team's IG account in order for the to be a non-zero number. It may be worth looking into removing this variable after some cross validation.

2.  The correlation between and . Intuitively this makes sense, a post must be, by our definition, during the same time period as another for to return a 1. It may be worth looking into removing one of these variables after some cross validation.

![](Predicting_IG_Engagements_files/figure-markdown_github/corr%20plots-1.png)![](Predicting_IG_Engagements_files/figure-markdown_github/corr%20plots-2.png)

Lastly, as hinted by the prompt, we viewed the distributions of our training data by post type (either Video, Album, or Photo) to determine whether they differed significantly.

While the distribution of Video and Photo distribution seems to be fairly normal, Album appears bimodal, and all three fall under different mean values for Engagements. Based on the plots, it does seem like each distribution is different enough to warrant each having their own model. In addition, the data set contains many more videos than it does photos or albums, so if we chose to simply include post type as a predictor in one model, we'd have to weight each level accordingly. Instead we chose to create three seperate models.

![](Predicting_IG_Engagements_files/figure-markdown_github/density%20plots-1.png)

### Model Training and Validation

First we scramble our training set in preparation for building our model.

``` r
## Subset data for just videos and scramble data
set.seed(92123)
nba <- nba[sample(1:nrow(nba)), ]
```

Although the code is not included here, we tried to create a number of different models, inlcuding a least squares regression model, a gradient boosted model, a model using NLP that vectorized the descriptions column, and even using predicted values from these models into other models. Ultimately, after testing the accuracy of each, we settled on a Random Forest, as it appeared to perform best and was the least overfitted.

In order to train and validate our Random Forest model, we first divide our training set by post type, and then within each division, we subset a small testing data set from our full training set and use it to calculate the MAPE.

More extensive cross-validation methods were used as well, but for brevity's sake, we don't include them here. Our cross-validation was useful in selecting the correct , as well as eliminating two predictors that appeared to aid the model little: , and . After eliminating these variables and tuning, our model's improved by over 1%.

``` r
# Deleting unneeded variables
nbanew <- nba[,c(2,3,4,5,6,9,11,12,15,16,17,18,20,21)]

# Creating Video/Photo/Album subsets from nba data
nba_Video = nbanew[nbanew$Type == "Video",]
nba_Photo = nbanew[nbanew$Type == "Photo",]
nba_Album = nbanew[nbanew$Type == "Album",]

# Splitting Video/Album/Photo subsets into training and test sets
numberOfTrainingSamples_Video <- round(length(nba_Video$Engagements) * .80)
numberOfTrainingSamples_Photo <- round(length(nba_Photo$Engagements) * .80)
numberOfTrainingSamples_Album <- round(length(nba_Album$Engagements) * .80)

train_dataRF_Video <- nba_Video[1:numberOfTrainingSamples_Video,]
test_dataRF_Video <- nba_Video[-(1:numberOfTrainingSamples_Video),]

train_dataRF_Album <- nba_Album[1:numberOfTrainingSamples_Album,]
test_dataRF_Album <- nba_Album[-(1:numberOfTrainingSamples_Album),]

train_dataRF_Photo <- nba_Photo[1:numberOfTrainingSamples_Photo,]
test_dataRF_Photo <- nba_Photo[-(1:numberOfTrainingSamples_Photo),]
```

We then train the Random Forest model to predict on the test set and then calculate and append columns for predicted Engagements, percent error, and absolute percent error.

    ## 
    ## Call:
    ##  randomForest(formula = Engagements ~ Followers + month + day_time +      weekday + Followers_Mentioned + is_season + all_nba + league_type +      num_ats + num_hash, data = train_dataRF_Video, ntree = 1000,      mtry = 7, importance = TRUE) 
    ##                Type of random forest: regression
    ##                      Number of trees: 1000
    ## No. of variables tried at each split: 7
    ## 
    ##           Mean of squared residuals: 2269818337
    ##                     % Var explained: 77.14

    ## 
    ## Call:
    ##  randomForest(formula = Engagements ~ Followers + month + day_time +      weekday + Followers_Mentioned + is_season + all_nba + league_type +      num_ats + num_hash, data = train_dataRF_Album, ntree = 1000,      mtry = 8, importance = TRUE) 
    ##                Type of random forest: regression
    ##                      Number of trees: 1000
    ## No. of variables tried at each split: 8
    ## 
    ##           Mean of squared residuals: 850017793
    ##                     % Var explained: 78.54

    ## 
    ## Call:
    ##  randomForest(formula = Engagements ~ Followers + month + day_time +      weekday + Followers_Mentioned + is_season + all_nba + league_type +      num_ats + num_hash, data = train_dataRF_Photo, ntree = 1000,      mtry = 7, importance = TRUE) 
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

Let's take a look at how our percent error is distributed across the testing set.

![](Predicting_IG_Engagements_files/figure-markdown_github/PE%20distribution-1.png) It appears that there are a few extreme outliers in our dataset that the model performs particularly poorly on. One in particular our model overshoots the most appears to be a post about Lebron James at a WNBA game. Intuitively, it makes sense that our model would perform poorly here. Mentioning Lebron would push the model to predict a higher engagement than would be normal for a WNBA game. Given how few outliers are, that the Random Forest is typically robust to outliers, and how rare a post like Lebron at a WNBA game is, we conclude that our model performs quite well.

Here we plot some of our variables to examine which are most critical to our model's accuracy. Notably, it appears that our variables vary in importance between the subsets for Videos, Albums, and Photos. This gives some credibility to our initial assumption that Video, Albums, and Photos should each have their own model.

``` r
varImpPlot(RF_Video)
```

![](Predicting_IG_Engagements_files/figure-markdown_github/varplot-1.png)

``` r
varImpPlot(RF_Album)
```

![](Predicting_IG_Engagements_files/figure-markdown_github/varplot-2.png)

``` r
varImpPlot(RF_Photo)
```

![](Predicting_IG_Engagements_files/figure-markdown_github/varplot-3.png)

### Final Predictions

Finally, statisfied with our validation results, we train our Random Forest on the whole of the training set and apply it to the 1000-post holdout set.

``` r
# Read in holdout set and make same modifications as training set


holdout_pre <-
  read.csv("data/holdout_final.csv")

holdout <- holdout_pre[,c(3,4,5,6,7,11,13,14,16,19,20,21,23,24)]
holdout$Engagements <- as.integer(holdout$Engagements)
for (i in 1:length(holdout[,1])){
  if(holdout$is_season[i]==TRUE)(holdout$is_season[i]='True')
  if(holdout$is_season[i]==FALSE)(holdout$is_season[i]='False')
}
holdout$is_season <- as.factor(holdout$is_season)
```

``` r
## Final models for training and prediction

RF_Video_Final <- randomForest(Engagements ~ Followers+month+day_time
                               +weekday+Followers_Mentioned
                               +is_season+all_nba+league_type+num_ats+num_hash,
                               ntree=1000, mtry=7,importance=TRUE, data=nba_Video)

RF_Photo_Final <- randomForest(Engagements ~ Followers+month+day_time
                               +weekday+Followers_Mentioned
                               +is_season+all_nba+league_type+num_ats+num_hash,
                               ntree=1000, mtry=8,importance=TRUE, data=nba_Photo)

RF_Album_Final <- randomForest(Engagements ~ Followers+month+day_time
                               +weekday+Followers_Mentioned
                               +is_season+all_nba+league_type+num_ats+num_hash,
                               ntree=1000,mtry=7,importance=TRUE, data=nba_Album)
```

``` r
#Calculate predicted values and append to holdout dataframe


holdout_Video = holdout %>% filter(Type == "Video")
holdout_Photo = holdout %>% filter(Type == "Photo")
holdout_Album = holdout %>% filter(Type == "Album")
holdout_Video$Engagements = round(predict(RF_Video_Final, newdata=holdout_Video))
holdout_Photo$Engagements = round(predict(RF_Photo_Final, newdata=holdout_Photo))
holdout_Album$Engagements = round(predict(RF_Album_Final, newdata=holdout_Album))

holdout <- rbind(holdout_Album, holdout_Photo, holdout_Video)

write_csv(holdout, "holdout_final.csv")
```

The predictions are contained in the attached "holdout.csv" file.
