
library(ggplot2)

###############################################################################
###############################################################################

plot_model_fit <- function(time_input, y_obs, y_mod, mod_metrics = NULL, title = "") {

  # Generate model fit plot.
  ggplot_pmf <- ggplot(data.frame("y_obs" = y_obs, "y_mod" = y_mod),
                  aes(x = y_obs, y = y_mod)) +
    geom_point(shape = 16, color = "#4c72b0") +   # medium size, filled round point.
    geom_abline(slope = 1, color = "red", linetype = "dashed") +
    ggtitle(title) +
    xlab("Observed") +
    ylab("Modelled") +
    theme_dare()

  print(ggplot_pmf)


  # Generate time series plot.
  df1 <- data.frame("date" = time_input, "value" = y_obs, "variable" = "Observed")
  df2 <- data.frame("date" = time_input, "value" = y_mod, "variable" = "Modelled")
  df_new <- rbind(df1, df2)

  ggplot_tsp <- ggplot(df_new, aes(x = date, y = value)) +
    geom_line(aes(color = variable), size = 1) +
    scale_color_manual(values = c("orange", "blue")) +
    ggtitle(paste0("Time series - ", tolower(title))) +
    xlab("Date") +
    ylab("Value") +
    theme_dare()

  print(ggplot_tsp)
}

###############################################################################
###############################################################################

theme_dare <- function() {

  # Ensure required fonts are available.S
  #stopifnot(validate_ghostscript_paths())
  extrafont::loadfonts(quiet = TRUE)

  theme(axis.line = element_line(linewidth = 0.4),
        axis.text = element_text(colour = "black"),
        axis.ticks = element_line(colour = "black"),
        legend.position = "none",
        panel.background = element_rect(fill = "white"),
        panel.border = element_rect(
           colour = "black",
           fill = "transparent"
        ),
        panel.grid.major = element_line(
           size = 0.25,
           linetype = "dashed",
           colour = "grey"
        ),
        panel.grid.minor = element_line(
           size = 0.25,
           linetype = "dashed",
           colour = "grey"
        ),
        text = element_text(family = "CM Roman", size = 10))
}

###############################################################################
###############################################################################
