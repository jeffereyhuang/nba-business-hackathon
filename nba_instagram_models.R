require(caTools)

df <- read.csv("~/Desktop/nba_hack_19/data/training_set_extended.csv")
head(df)

# Model 1: Linear Regression
# For videos, not using description data
df_vid = df[df$Type == 'Video',]
set.seed(123) 
sample = sample.split(df_vid, SplitRatio = 0.75)
train_vid = subset(df_vid, sample == TRUE)
test_vid = subset(df_vid, sample == FALSE) 
fit = lm(Engagements ~ Followers + year + month + weekday + day_time + is_playoffs, data = train_vid)
summary(fit) # remove is_playoffs
fit.2 = lm(Engagements ~ Followers + year + month + weekday + day_time, data = train_vid)
summary(fit.2)

actual = test_vid$Engagements
predicted = predict(fit.2, test_vid)
mape = mean(abs((actual - predicted)/actual) * 100)
mape # = 9.72, decent number to baseline against
