### make_plots.R ##################################################################################

### PREAMBLE ######################################################################################
library(tidytext);
library(dplyr);

# clear workspace in an effort to combat bugs
rm(list = ls(all = TRUE));

options(stringsAsFactors = FALSE);


source('~/eprate/helper_functions.R');

### PARAMETERS ####################################################################################

min.recurrence <- 5;
n <- 10;

season.colours <- c(
    '#a6cee3','#1f78b4','#b2df8a','#33a02c',
    '#fb9a99','#e31a1c','#fdbf6f','#ff7f00',
    '#cab2d6','#6a3d9a'
    );

### PREPARE DATA ##################################################################################

episode.data <- read.table(
    "friends_episodes.tsv", 
    sep = '\t', 
    header = TRUE
    );


tidy.data <- unnest_tokens(
    episode.data, 
    word, 
    plot
    );

# remove stop words
data('stop_words');
tidy.data <- anti_join(tidy.data, stop_words);

### ANALYSIS ######################################################################################

if(max(episode.data$season) > 10) {
    season.colours <- rep('black', max(episode.data$season));
}

common.words <- count(
    tidy.data, 
    word,
    sort = TRUE
    );

# get rating info by word
ratings <- tidy.data %>% 
    group_by(word) %>%
    summarize(
        n = n(),
        n.episodes = length(unique(title)),
        mean.rating = mean(rating), 
        median.rating = median(rating),
        sd.rating = sd(rating),
        min.rating = min(rating), 
        max.rating = max(rating)
        );

# restrict to recurrent ones
ratings <- ratings[ratings$n.episodes >= min.recurrence, ];

ratings <- ratings[order(ratings$median.rating, decreasing = TRUE), ];


### MAKE PLOT #####################################################################################

best.words <- rev(ratings$word[1:n]);
worst.words <- rev(ratings$word[(nrow(ratings) - n + 1):nrow(ratings)]);

par(
    mfrow = c(2, 1),
    oma = c(4,6.2,0,0) + 0.1,
    mar = c(0,0,0.5,0.5) + 0.1
    );


best.words.data <- tidy.data[tidy.data$word %in% best.words, ];
dotboxplot(
    plot.data = best.words.data,
    ylab.labels = best.words,
    colours = season.colours[best.words.data$season],
    xaxt = 'n',
    rating.lim = range(episode.data$rating)
    );


worst.words.data <- tidy.data[tidy.data$word %in% worst.words, ];
dotboxplot(
    plot.data = worst.words.data,
    ylab.labels = worst.words,
    colours = season.colours[worst.words.data$season],
    rating.lim = range(episode.data$rating)
    );


title(
    xlab = 'Rating',
    outer = TRUE, 
    line = 2
    );




