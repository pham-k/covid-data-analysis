# package
library(tidyverse)
library(readxl)
library(car)
library(zoo)
library(lubridate)
# library(janitor)


# declare variable
col_names <- c("date_report", "name", "loc_firstid", "yob", "res_loc_dis", "test_date", "where","id")
# col_names <- c("idx", "loc_firstid", "f_to0",
#                 "case0", "case_direct", "contact_loc", "contact_loc_dis",
#                 "contact_loc_com", "contact_lastdate", "contact_type", "rel_to_case_direct",
#                 "date_report", "date_public",
#                 "id", "name", "id_name", "yob", "sex",
#                 "national", "passport", "tel", "email",
#                 "job", "job_loc", "job_loc_block", "job_loc_floor", "job_loc_room",
#                 "job_loc_pro", "job_loc_dis", "job_loc_com",
#                 "trans_seatnum",
#                 "res_loc", "res_loc_block", "res_loc_floor", "res_loc_room",
#                 "res_loc_pro", "res_loc_dis", "res_loc_com",
#                 "qrt_type", "qrt_pro", "qrt_dis", "qrt_name", "qrt_date",
#                 "test_01_taken", "test_01_who_taken", "test_01_who_proc", "test_01_date_taken",
#                 "test_01_result", "test_01_date_result",
#                 "test_02_taken", "test_02_who_taken", "test_02_who_proc", "test_02_date_taken",
#                 "test_02_result", "test_02_date_result",
#                 "test_03_taken", "test_03_who_taken", "test_03_who_proc", "test_03_date_taken",
#                 "test_03_result", "test_03_date_result",
#                 "test_04_taken", "test_04_who_taken", "test_04_who_proc", "test_04_date_taken",
#                 "test_04_result", "test_04_date_result",
#                 "test_05_taken", "test_05_who_taken", "test_05_who_proc", "test_05_date_taken",
#                 "test_05_result", "test_05_date_result",
#                 "local_confirmed", "note", "test_ab_date", "test_ab_result", "student",
#                 "clin_symptoms", "clin_date_onset", "clin_prog", "clin_fever",
#                 "clin_cough", "clin_sneeze", "clin_sore", "clin_chest", "clin_breath",
#                 "clin_tastelost", "clin_smelllost", "clin_chills", "clin_tired", "clin_other",
#                 "CT_test_pos", "contact_loc2", "invest_form", "test_date", "qrt_date_in", "f0_loc", "loc")

# import raw data

raw <- read_csv('./dataset/covid-2021-06-24.csv')
names(raw) <- col_names
df <- raw %>% 
  select(id, loc_firstid, yob, res_loc_dis, test_date) %>% 
  mutate(
    test_date = as.Date(test_date),
    # sex = factor(sex),
    res_loc_dis = factor(res_loc_dis),
    loc_firstid = factor(loc_firstid),
    age = as.integer(format(Sys.Date(), "%Y")) - as.integer(yob),
    age_group = cut(
      age,
      breaks=c(-Inf, 6, 11, 15, 18, 30, 40, 50, 60, 70, Inf),
      right=FALSE,
      ordered_result=TRUE
    ),
    adult = age >= 18
  )

# filter(df, test_date==as.Date('2021-05-26'))

# roll mean
roll_mean <- function (x) {
  if (length(x) < 7) {
    rep(NA,length(x)) 
  } else {
    rollmean(x,7,align="right",na.pad=TRUE)
  }
}

# create complete date seq
begin <- as.Date(min(df$test_date, na.rm=TRUE))
end <- as.Date(max(df$test_date, na.rm=TRUE))
complete_date <- data.frame(test_date = seq(begin, end, by=1))

# incidence
inc <- df %>%
  select(test_date, id) %>%
  dplyr::filter(
    !is.na(test_date) &
    !is.na(id)) %>%
  distinct(test_date, id, .keep_all = TRUE) %>%
  group_by(test_date) %>%
  count()

# complete_date left join inc
inc <- merge(complete_date, inc, all.x = TRUE)

# replace NA, calculate roll mean
inc <- inc %>% 
  replace_na(replace=list(n=0)) %>% 
  mutate(
    rm = roll_mean(n),
    # diff = c(NA, diff(n)),
    diff = n - lag(n),
    reldiff = diff / lag(n)
    )


inc_dis <- df %>%
  select(test_date, res_loc_dis, id) %>% 
  filter(!is.na(test_date) & !is.na(id) & !is.na(res_loc_dis)) %>% 
  distinct(test_date, res_loc_dis, id, .keep_all = TRUE) %>% 
  group_by(test_date, res_loc_dis) %>% 
  count() %>% 
  ungroup() %>% 
  complete(
    res_loc_dis,
    test_date = seq.Date(
      begin,
      end,
      by = "day")
  ) %>%
  replace_na(replace=list(n=0)) %>%
  group_by(res_loc_dis) %>% 
  mutate(
    rm = roll_mean(n),
    diff = n - lag(n),
    reldiff = diff / lag(n)
  )

inc_series <- df %>%
  select(test_date, loc_firstid, id) %>% 
  filter(!is.na(test_date) & !is.na(id) & !is.na(loc_firstid)) %>% 
  distinct(test_date, loc_firstid, id, .keep_all = TRUE) %>% 
  group_by(test_date, loc_firstid) %>% 
  count() %>% 
  ungroup() %>% 
  complete(
    loc_firstid,
    test_date = seq.Date(
      begin,
      end,
      by = "day")
  ) %>%
  replace_na(replace=list(n=0)) %>% 
  mutate(
    rm = roll_mean(n)
  )


saveRDS(inc, './output/inc.rds')
saveRDS(inc_dis, './output/inc_dis.rds')
saveRDS(inc_series, './output/inc_series.rds')

# write_csv(inc, './output/inc.csv')
# write_csv(inc_dis, './output/inc_dis.csv')
# write_csv(inc_series, './output/inc_series.csv')


