library(EpiNow2)
library(tidyverse)

# no-case
# no_case <- read_csv('./data/processed/no-case/no-case.csv')
# no_case$date_report <- as.Date(no_case$X1)
# reported_cases <- no_case %>% select('date_report', 'no_case')
# names(reported_cases) <- c('date', 'confirm')

# no-positive
# no_case <- read_csv('./data/processed/no-positive/no-positive.csv')
# no_case$date_report <- as.Date(no_case$date_report)
# reported_cases <- no_case %>% select('date_report', 'no_positive')
# names(reported_cases) <- c('date', 'confirm')

# no-test-pos
# no_case <- read_csv('./data/processed/no-test/no-test-pos.csv')[0:127,]
# no_case$date <- as.Date(no_case$date_report)
# reported_cases <- no_case %>% select('date', 'no_test_pos')
# names(reported_cases) <- c('date', 'confirm')

# no-death-from-treatment
no_death <- read_csv('./data/processed/no-death-from-treatment-data/no-death.csv')[0:59,0:2]
no_death$date <- as.Date(no_death$date_report)
reported_cases <- no_death %>% select('date', 'no_death')
names(reported_cases) <- c('date', 'confirm')

# no_case <- read_csv('./data/processed/no-death/no-death.csv')
# no_case <- read_csv('./data/processed/ct-from-test-data/ct.csv')

# reported_cases <- no_case %>% 
#   select('date_report', 'no_positive') %>%
#   slice(328:n())
# reported_cases <- no_case %>% select('date_report', 'no_death')

# breakpoint
reported_cases$breakpoint <- 0
# reported_cases[reported_cases$date == as.Date("2021-05-31"), 'breakpoint'] <- 1
# reported_cases[reported_cases$date == as.Date("2021-06-14"), 'breakpoint'] <- 1
# reported_cases[reported_cases$date == as.Date("2021-06-19"), 'breakpoint'] <- 1
# reported_cases[reported_cases$date == as.Date("2021-07-09"), 'breakpoint'] <- 1
# reported_cases[reported_cases$date == as.Date("2021-07-19"), 'breakpoint'] <- 1
# reported_cases[reported_cases$date == as.Date("2021-07-27"), 'breakpoint'] <- 1
# reported_cases[reported_cases$date == as.Date("2021-08-01"), 'breakpoint'] <- 1
reported_cases[reported_cases$date == as.Date("2021-08-10"), 'breakpoint'] <- 1
reported_cases[reported_cases$date == as.Date("2021-08-15"), 'breakpoint'] <- 1
reported_cases[reported_cases$date == as.Date("2021-08-23"), 'breakpoint'] <- 1

generation_time <- get_generation_time(disease = "SARS-CoV-2", source = "ganyani")
incubation_period <- get_incubation_period(disease = "SARS-CoV-2", source = "lauer")
reporting_delay <- list(
  mean = convert_to_logmean(5, 1), mean_sd = 0.1,
  sd = convert_to_logsd(5, 1), sd_sd = 0.1,
  max = 10
)

# estimate_infection <- estimate_infections(
#   reported_cases,
#   generation_time = generation_time,
#   delays = delay_opts(incubation_period, reporting_delay),
#   rt = rt_opts(prior = list(mean = 1.1, sd = 0.5)),
#   horizon = 7,
#   stan = stan_opts(cores = 4)
# )

# summary(model)
# plot(estimate_infection)

model <- epinow(reported_cases = reported_cases,
                    generation_time = generation_time,
                    delays = delay_opts(incubation_period, reporting_delay),
                    rt = rt_opts(prior = list(mean = 1.1, sd = 0.5)),
                    horizon = 7,
                    target_folder = "./data/processed/forecast-by-epinow2",
                    stan = stan_opts(cores = 4))



summarised_estimated_reported_cases <- readRDS(
  './data/processed/forecast-by-epinow2/latest/summarised_estimated_reported_cases.rds')
write_csv(
  summarised_estimated_reported_cases,
  './data/processed/forecast-by-epinow2/latest/summarised_estimated_reported_cases.csv'
)

summarised_estimates <- readRDS(
  './data/processed/forecast-by-epinow2/latest/summarised_estimates.rds')
write_csv(
  summarised_estimates,
  './data/processed/forecast-by-epinow2/latest/summarised_estimates.csv'
)

reported_cases <- readRDS(
  './data/processed/forecast-by-epinow2/latest/reported_cases.rds')
write_csv(
  reported_cases,
  './data/processed/forecast-by-epinow2/latest/reported_cases.csv'
)

# model_args <- readRDS(
#   './data/processed/forecast-by-epinow2/latest/model_args.rds')
# write_csv(
#   model_args,
#   './data/processed/forecast-by-epinow2/latest/model_args.csv'
# )

summary <- readRDS(
  './data/processed/forecast-by-epinow2/latest/summary.rds')
# write_csv(
#   summary,
#   './data/processed/forecast-by-epinow2/latest/summary.csv'
# )

