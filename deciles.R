library(rjson)
library(plyr)
allfiles <- Sys.glob("jsoncache/*.json")

j  <- lapply(allfiles, function (fn) { fromJSON(file = fn) })
idx <- ldply(j, function (json) {
  data.frame(json$dataset, gini = json$dist$Gini)
})

A <- which(idx$cc3=="AZE" & idx$year==2004)
B <- which(idx$cc3=="MWI" & idx$year==1997)
C <- which(idx$cc3=="GBR" & idx$year==2012)

barplot(j[[A]]$deciles, ylim=c(0,50), main=paste(j[[A]]$dataset$country, j[[A]]$dataset$year))
barplot(j[[B]]$deciles, ylim=c(0,50), main=paste(j[[B]]$dataset$country, j[[B]]$dataset$year))
barplot(j[[C]]$deciles, ylim=c(0,50), main=paste(j[[C]]$dataset$country, j[[C]]$dataset$year))
