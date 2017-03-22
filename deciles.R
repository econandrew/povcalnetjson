library(rjson)
library(plyr)
allfiles <- Sys.glob("jsoncache/*.json")

j  <- lapply(allfiles, function (fn) { fromJSON(file = fn) })
idx <- ldply(j, function (json) {
  data.frame(
    json$dataset,
    gini = json$dist$Gini,
    modelled = "beta" %in% names(json))
})

A <- which(idx$cc3=="AZE" & idx$year==2004)
B <- which(idx$cc3=="MWI" & idx$year==1997)
C <- which(idx$cc3=="USA" & idx$year==2010) # Pikkety has top decile = 45%+ - net/gross?

barplot(j[[A]]$deciles, ylim=c(0,50), main=paste(j[[A]]$dataset$country, j[[A]]$dataset$year))
barplot(j[[B]]$deciles, ylim=c(0,50), main=paste(j[[B]]$dataset$country, j[[B]]$dataset$year))
barplot(j[[C]]$deciles, ylim=c(0,50), main=paste(j[[C]]$dataset$country, j[[C]]$dataset$year))

plot(j[[B]]$distribution$p, j[[B]]$distribution$L,type="l",col="red")
lines(j[[A]]$distribution$p, j[[A]]$distribution$L,col="blue")
lines(c(0,1),c(0,1),col="black")

library(splines)
L.B <- splinefun(c(0.0, j[[B]]$distribution$p), c(0.0,j[[B]]$distribution$L), method="monoH.FC")
plot(L.B)
L.B <- smooth.spline(c(0.0, j[[B]]$distribution$p), c(0.0,j[[B]]$distribution$L))
points(L.B)

mean <- 100
L <- data.frame(p=j[[C]]$distribution$p, L=j[[C]]$distribution$L)

L$Finv <- c(L$L[1:nrow(L)] - c(0,L$L[1:nrow(L)-1])) / (L$p[1:nrow(L)] - c(0,L$p[1:nrow(L)-1]))


thecdf <- splinefun(L$Finv, L$p)
plot(thecdf)
points(L$Finv, L$p)
