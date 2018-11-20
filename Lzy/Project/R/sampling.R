# sampling 50 customers from the original data.

# loading data
library(readxl)
input_all <- read_excel("input_node.xlsx", sheet = "Customer_data")

# slicing
customer_data <- input_all[ -1, c(1,3,4,5,6)]

# sampling
set.seed(3)    # using seed 8
sample_ind <- sample(x = seq(length(customer_data$ID)), size = 50, replace = FALSE)
customer_sample <- customer_data[sample_ind, ]
customer_sample <- lapply(customer_sample, as.double)
customer_sample$pack_total_weight <- format(customer_sample$pack_total_weight , digits = 2, scientific = FALSE)
customer_sample$pack_total_volume <- format(customer_sample$pack_total_volume , digits = 2, scientific = FALSE)


# writing data to .xlsx file
library(xlsx)
write.xlsx2(customer_sample, "customer_sample.xlsx", sheetName = "customer_sample", append=FALSE)



