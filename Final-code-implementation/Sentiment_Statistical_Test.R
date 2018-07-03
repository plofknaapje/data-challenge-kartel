# Sentiment_Delta.csv is achieved by running this in conversations.py:
# Airline('AmericanAir', '22536055').airlineSentimentDeltas()['delta'].to_csv('Sentiment_Delta.csv')

data <- read.csv('Sentiment_Delta.csv', header=FALSE)
plot(density(data[,2]))
print(t.test(data[,2], alternative='greater', mu=0)) # one-sided one-sample t-test

# Optional to test hypotheses when sentiment intially is lower / higher than 0:

#data2 <- read.csv('hi3.csv', header=TRUE)
#data2 <- data2[,c('delta', 'start')]
#data2 <- data2[data2$start < 0,]
#plot(density(data2$delta))
#t.test(data2$delta, alternative='greater', mu=0)

#data3 <- read.csv('hi3.csv', header=TRUE)
#data3 <- data3[,c('delta', 'start')]
#data3 <- data3[data3$start > 0,]
#plot(density(data3$delta))
#t.test(data3$delta, alternative='greater', mu=0)
