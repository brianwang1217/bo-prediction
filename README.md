# Box Office Prediction
Using linear regression to predict the box office success (domestic and worldwide grosses) of movies using budget as the predictive factor.

## Data Acquisition
Used BeautifulSoup to web scrape [boxofficemojo](https://www.boxofficemojo.com/) to acquire dataset. From the first ten pages of the top domestic grosses of all time, visited individual movie links to scrape relevant data and saved to .csv file. Such categorical data includes title, distributor, release date, genre, runtime, MPAA rating, budget, domestic gross, and worldwide gross. The data was then cleared of movies that were unfit for analysis (no reported budget, no worldwide release, etc.).

Unused categories (such as distributor, seasonal release, genre, etc.) can be implemented in the future for multiple linear regression in order to improve overall accuracy of box office prediction. Additional factors from other sites (critic ratings, number of reviews, etc.) may be possible as well, though linking movie information from different sites may be troublesome.

## Analysis
Used Linear Regression and Gradient Descent to predict box office grosses with budget as input. The untransformed data took on an exponential shape, leading a large MSE, even after training, so we applied a y^.125 transformation to linearize the data we were working with. After transformation, we ended up with an error of **.98** on the training data set and **.887** on the test set (scraped data from .csv file was split 80/20).

## Future Considerations
* multiple linear regression with different factors
* scrape review sites (imdb, RT) for additional data
* detect and remove outliers from dataset 
