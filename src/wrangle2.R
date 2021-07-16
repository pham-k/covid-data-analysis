# package
library(tidyverse)
library(readxl)
library(car)
library(zoo)
library(lubridate)

# import
raw <- read_csv2('./dataset/shift-2021-06-24.csv')

# select col
df <- raw %>% 
  select(1, 3, 8, 11:20, 29)

names(df) <- c('submit_date', 'full_name', 'res_loc_dis', paste(c('td', 'r'), rep(1:5, each=2), sep=""), 'loc_firstid' )

df <- df %>% 
  mutate(
    td1 = substr(td1, 1, 10),
    td2 = substr(td2, 1, 10),
    td3 = substr(td3, 1, 10),
    td4 = substr(td4, 1, 10),
    td5 = substr(td5, 1, 10),
    test_date = case_when(
      r1 == 'Dương tính' ~ td1,
      r2 == 'Dương tính' ~ td2,
      r3 == 'Dương tính' ~ td3,
      r4 == 'Dương tính' ~ td4,
      r5 == 'Dương tính' ~ td5,
      TRUE ~ ''
    ),
    test_date = as.Date(test_date, format='%d/%m/%Y'),
    res_loc_dis = factor(res_loc_dis)
    # submit_date = as.Date(
    #   stringi::stri_c(stringi::stri_sub(df$submit_date, -4, -1), '/2021', sep=''),
    #   format='%d/%m/%Y'
    # )
  ) %>% 
  separate(submit_date, into = c('a', 'b'), extra = 'merge') %>%
  select(1:3, 14, 15)
  

