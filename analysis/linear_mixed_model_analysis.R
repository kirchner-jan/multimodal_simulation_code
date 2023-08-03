# Load packages
library(lmerTest)
library(ggplot2)
library(plyr)
library(fitdistrplus)
library(texreg)

# Working directory has to contain BolusLoad_nov.csv
# setwd("~/LinearMixedModelAnalysis/")
mydata <- read.table("~/LinearMixedModelAnalysis/BolusLoad_nov.csv", header=TRUE, 
                     sep=",",colClasses=c(rep('numeric', 7), 'factor','numeric', rep('factor', 2),'numeric'))

## create new feature for nested ids
mydata <- na.omit(within(mydata, sample <- factor(id:id2)))
## only keep events with > 8 % participation rate
mydata <- within(mydata, H <- factor(mydata$rates >= 0.8))
## rename column and remove extreme samples
colnames(mydata)[8] <- "region"
mydata$region <-revalue(mydata$region, c("1"="V1", "2"="S1" , "3"="AL" , "4"="RL"))
mydata$rates[mydata$rates >= 1] = 0.99
mydata <- mydata[which(mydata$rates >= 0.08) , ]

## Fit amplitude as function of age*region and with animal and sample ID as hidden factors
mixed.lmer1 <- lmer(amps ~ age*region +  (1 |id) +  (1 |sample) , data = mydata )
## check normality of sample
qqnorm(residuals(mixed.lmer1))
qqline(residuals(mixed.lmer1) , col = 2,lwd=2,lty=2)
s1 <- summary(mixed.lmer1)
print(s1)

## Generalized linear mixed model with logit link function -> map [0 , 1] to [-inf , inf]
mixed.lmer2 <- glmer(rates ~ age*region +  (1 |id) +  (1 |sample) , family = binomial() , data = mydata )
qqnorm(residuals(mixed.lmer2))
s2 <- summary(mixed.lmer2)
qqline(residuals(mixed.lmer2) , col = 2,lwd=2,lty=2)
print(s2)

mixed.lmer3 <- lmer(jitter ~ age*region +  (1 |id) +  (1 |sample) , data = mydata )
qqnorm(residuals(mixed.lmer3))
qqline(residuals(mixed.lmer3) , col = 2,lwd=2,lty=2)
s3 <- summary(mixed.lmer3)
print(s3)

mixed.lmer4 <- lmer(IEI ~ age*region +  (1 |id) +  (1 |sample) , data = mydata )
qqnorm(residuals(mixed.lmer4))
qqline(residuals(mixed.lmer4) , col = 2,lwd=2,lty=2)
s4 <- summary(mixed.lmer4)
print(s4)

mixed.lmer5 <- lmer(AUC ~ age*region +  (1 |id) +  (1 |sample) , data = mydata )
qqnorm(residuals(mixed.lmer5))
qqline(residuals(mixed.lmer5) , col = 2,lwd=2,lty=2)
s5 <- summary(mixed.lmer5)
print(s5)

mixed.lmer6 <- lmer(durations ~ age*region +  (1 |id) +  (1 |sample) , data = mydata )
qqnorm(residuals(mixed.lmer6))
qqline(residuals(mixed.lmer6) , col = 2,lwd=2,lty=2)
s6 <- summary(mixed.lmer6)
print(s6)

## Plot effect sizes to file
plotreg(list(mixed.lmer1,mixed.lmer2,mixed.lmer3,mixed.lmer4,mixed.lmer5,mixed.lmer6) , file = "BolusLoad.pdf" ,
        lwd.vbars = 0 , custom.coef.names = c("Intercept" , "Age", "S1" , "AL" , "RL" , "S1 : Age" , "AL : Age" , "RL : Age"), 
        custom.model.names = c("amps","rates","jitter","IEI","AUC","durations"),
        override.se = list(s1$coefficients[ , 2] , s2$coefficients[ , 2] , s3$coefficients[ , 2] , s4$coefficients[ , 2] , s5$coefficients[ , 2] , s6$coefficients[ , 2]),
        override.pval = list(s1$coefficients[ , 5] , s2$coefficients[ , 4] , s3$coefficients[ , 5] , s4$coefficients[ , 5] , s5$coefficients[ , 5] , s6$coefficients[ , 5]))
## Output table with effects
screenreg(list(mixed.lmer1,mixed.lmer2,mixed.lmer3,mixed.lmer4,mixed.lmer5,mixed.lmer6), digits = 3, leading.zero = TRUE , dcolumn = FALSE , sideways = TRUE ,
       override.pvalues = list(s1$coefficients[ , 5] , s2$coefficients[ , 4] , s3$coefficients[ , 5] , s4$coefficients[ , 5] , s5$coefficients[ , 5] , s6$coefficients[ , 5]),
       #override.se = list(s1$coefficients[ , 5] , s2$coefficients[ , 4] , s3$coefficients[ , 5] , s4$coefficients[ , 5] , s5$coefficients[ , 5] , s6$coefficients[ , 5]),
       override.se = list(s1$coefficients[ , 2] , s2$coefficients[ , 2] , s3$coefficients[ , 2] , s4$coefficients[ , 2] , s5$coefficients[ , 2] , s6$coefficients[ , 2]),
       custom.model.names = c("amps","rates","jitter","IEI","AUC","durations"))


