Monty <- function(n, switch){
  wins <- 0
  for (i in 1:n) {
    doors <- c(1:3)
    prize_door <- sample(doors, 1)
    choosen_door <- sample(doors, 1)
    if (prize_door == choosen_door) {
      if (switch == FALSE) {
        wins = wins + 1
      }
    } else {
      if (switch == TRUE) {
        wins = wins + 1
      }
    }
  }
  return(wins/n)
}

#tip for exercises
switch <- c(TRUE, FALSE)
n<- c(100,1000,10000)
conditions <- expand.grid(switch, n)
results <- rep(NA, 6)
for(i in 1:nrow(conditions)) {
  results[i] <- Monty(n = conditions[i, 2], switch = conditions[i, 1])
}
cbind(conditions, results)
