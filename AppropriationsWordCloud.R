# wordcloud For Alex Reports
# Arica Schuett
# July 28, 2021

install.packages("wordcloud")
library(wordcloud)
install.packages("RColorBrewer")
library(RColorBrewer)
install.packages("wordcloud2")
library(wordcloud2)
install.packages("tm")
library(tm)#Create a vector containing only the text
install.packages("qdapRegex")
library(qdapRegex) #removing URLS
install.packages("webshot")
library(tidyverse)
library(csv)

BillRaw <- read_lines("/Users/aricaschuett/Documents/Alex/f1.txt") example


text <- BillRaw# Create a corpus  

# continue cleaning the text
text <- 
  text %>%
  str_remove("\\n") %>%                   # remove linebreaks
  #removeWords(stopwords("english")) %>%   # Remove common words (a, the, it etc.)
  #removeNumbers() %>%
  tolower() %>%
  stripWhitespace() %>%
  removeWords(c("amp")) 

text <- removeWords(text, c(stopwords("en"), "shall", "section",
                            "program", "u.s.", "may", "made", "secretary", "year",
                            "current", "including", "program", "necessaary",
                            "provided,", "remain", "funds", "necessary", "authorized", 
                            "expenses", "provided,", "provided", "act", "office", "fiscal", 
                            "appropriations", "service", "amount", "pursuant", "42", 
                            "appropriated", "used", "exceed", "carry", "30,", "related", 
                            "sec.", "expended,", "agriculture,", "notwithstanding", "subject"))

# Convert the data into a summary table
textCorpus <- 
  Corpus(VectorSource(text)) %>%
  TermDocumentMatrix() %>%
  as.matrix()

textCorpus <- sort(rowSums(textCorpus), decreasing=TRUE)
#textCorpus <- filter(freq >= 3)
textCorpus <- data.frame(word = names(textCorpus), freq=textCorpus, row.names = NULL)


# build wordcloud 
wordcloud <- wordcloud2(data = textCorpus, minRotation = 0, maxRotation = 0, ellipticity = 0.6)
wordcloud
