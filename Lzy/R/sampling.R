# sampling 50 customers from the original data.

# loading data
library(readxl)
input_all <- read_excel("input_node.xlsx", sheet = "Customer_data")

# slicing
customer_data <- input_all[ -1, c(1,3,4,5,6)]

# sampling
set.seed(3)    # using seed 3
sample_ind <- sample(x = seq(length(customer_data$ID)), size = 50, replace = FALSE)
customer_sample <- customer_data[sample_ind, ]
customer_sample$pack_total_weight <- as.double(customer_sample$pack_total_weight)
customer_sample$pack_total_volume <- as.double(customer_sample$pack_total_volume)

# writing data to .xlsx file
library(xlsx)
write.xlsx2(customer_sample, "customer_sample.xlsx", sheetName = "customer_sample", append=FALSE)
# write .csv
write.csv2(customer_sample, "customer_sample.csv", row.names=FALSE)
test_data <- read.csv2("customer_sample.csv")

# read distance and time
dist_time <- read.delim2("input_distance-time.txt", sep = ",")
dist_time_sample <- dist_time[FALSE, -1]
for (from in customer_sample$ID){
  for (to in customer_sample$ID){
    if(from == to){
      next
    }
    ind <- which(dist_time$from_node == from & dist_time$to_node == to)
    dist <- dist_time[ind, which(names(dist_time)=="distance")]
    travel_time <- dist_time[ind, which(names(dist_time)=="spend_tm")]
    dist_time_sample <- rbind(dist_time_sample, c(from, to, dist, travel_time))
  }
}
names(dist_time_sample) <- c("from_node", "to_node", "distance", "travel_time")
rm(from, to, ind, dist, travel_time)













