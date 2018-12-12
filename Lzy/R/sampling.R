# sampling 50 customers from the original data.

# loading data
library(readxl)
input_all <- read_excel("input_node.xlsx", sheet = "Customer_data")

# slicing
distribution_center <- input_all[1, c(1,3,4,5,6)]
distribution_center[1, c(4, 5)] <- 0
customer_data <- input_all[ -1, c(1,3,4,5,6)]

# sampling
set.seed(3)    # using seed 3
sample_ind <- sample(x = seq(length(customer_data$ID)), size = 50, replace = FALSE)
customer_sample <- customer_data[sample_ind, ]

# integration
customer_sample <- rbind(distribution_center, customer_sample)

customer_sample$pack_total_weight <- as.numeric(customer_sample$pack_total_weight)
customer_sample$pack_total_volume <- as.numeric(customer_sample$pack_total_volume)

# writing data to .xlsx file
library(xlsx)
write.xlsx2(customer_sample, "customer_sample.xlsx", sheetName = "customer_sample", append=FALSE)

# write .csv
write.csv(customer_sample, "customer_sample.csv", row.names=FALSE)

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

# changing unit to Kilometer and Hour
dist_time_sample$distance <- dist_time_sample$distance / 1000
dist_time_sample$travel_time <- dist_time_sample$travel_time / 60

# write to file
write.csv(dist_time_sample, "dist_time_sample.csv", row.names=FALSE)
test_data <- read.csv("dist_time_sample.csv")

library(xlsx)
write.xlsx2(dist_time_sample, "dist_time_sample.xlsx", sheetName = "dist_time_sample", append=FALSE)

# construct solution file

# route 1
route <- data.frame(id = 1, node_1 = 0, node_2 = 616,
                    node_3 = 645, node_4 = 423, node_5 = 689,
                    node_6 = 400, node_7 = 947, node_8 = 763,
                    node_9 = 810, node_10 = 0, node_11 = 0,
                    node_12 = 0)

route_2 <- c(2, 0, 276, 550, 255, 484, 582, 660, 662, 0, 0, 0, 0)

route_3 <- c(3, 0, 247, 221, 182, 604, 283, 101, 606, 360, 977, 842, 0)

route_4 <- c(4, 0, 406, 184, 299, 901, 303, 0, 0, 0, 0, 0, 0)

route_5 <- c(5, 0, 443, 631, 215, 888, 185, 121, 833, 0, 0, 0, 0)

route_6 <- c(6, 0, 851, 972, 109, 331, 137, 322, 559, 140, 601, 0, 0)

route_7 <- c(7, 0, 17, 943, 359, 51, 0, 0, 0, 0, 0, 0, 0)

route <- rbind(route, route_2, route_3, route_4, route_5, route_6, route_7)

write.csv(route, "route.csv", row.names=FALSE)
library(xlsx)
write.xlsx2(route, "route.xlsx", row.names=FALSE, sheetName = "route", append=FALSE)










