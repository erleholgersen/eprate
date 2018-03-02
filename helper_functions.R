
### capitalize ####################################################################################
# Description:
#	Capitalize first letter of a string
capitalize <- function(phrase) {

	capitalized.phrase <- paste0(
		toupper(
			substr(
				phrase, 
				1,
				1
				)
			),
		substr(
			phrase, 
			2,
			nchar(phrase)
			)
		);

	return(capitalized.phrase);
}


### dotboxplot ####################################################################################
# Description:
#	Make boxplot with dots for episode ratings
# Input variables:
#	plot.data
#	ylab.labels
#	colours
dotboxplot <- function(plot.data, ylab.labels, colours, xaxt = 's', rating.lim = NULL) {

	if(is.null(rating.lim)) {
		rating.lim <- range(plot.data$rating);
	}

	# capitalize
	plot.data$word <- sapply(
		plot.data$word, 
		capitalize
		)

	ylab.labels <- sapply(
		ylab.labels,
		capitalize
		);

	# fix order
	plot.data$word <- factor(
	    plot.data$word,
	    levels = ylab.labels
	    );

	# make background plot
	boxplot.rows <- match(plot.data$word, ylab.labels);
	row.jitter <- runif(
	    length(boxplot.rows), 
	    -0.25,
	    0.25
	    );

	plot(
	    plot.data$rating, 
	    boxplot.rows + row.jitter, 
	    col = colours,
	    xaxt = 'n',
	    yaxt = 'n',
	    xlim = rating.lim,
	    ylim = c(0.4, length(unique(ylab.labels)) + 0.6),
	    ylab = '',
	    xlab = '',
	    pch = 16,
	    cex = 0.7,
	    yaxs = 'i'
	    );



	boxplot(
	    rating ~ word,
	    plot.data,
	    xaxt = xaxt,
	   	yaxs = 'i',
	    horizontal = TRUE,
	    outline = FALSE,
	    add = TRUE,
	    col = 'transparent',
	    las = 1
	    );

	abline(v = median(episode.data$rating), lty = 3);


}