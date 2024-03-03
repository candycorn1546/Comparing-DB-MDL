# OVERVIEW

- #### This is a personal project I have been working on for around three months. The reason behind this project is my love for watching Chinese and Korean dramas; I have never been a fan of the rating system for the most popular international rating pages (MDL) as they are too biased toward famous actors.
- #### Using all previously collected data from scraping Douban and Mydramalist. I build graphs and tables from Plotly to analyze the difference between Western and Eastern audiences.
- #### MDL is known as a "fandom" website, meaning ratings are more biased toward their favourite actors' shows without a fair representation of the good/bad the shows are.
- #### The average age group for MDL will be around 15-30. On the other hand, DB is used by a much more diverse group of people; therefore, their ratings will be more objective when compared to MDL.


  ## Process
  - Use DBscrapping to scrape popular shows from DB with at least 20k reviewers.
  - Use MDLscraping to scrape the 250 most popular show pages from MDL.
  - Took the DB and MDL CSV files with all the scraped data and combined them into the same sheets if the 'English Title' or 'Native Title' matches.
  - After combining the CSV and creating a final CSV file, use the CSV file to build graphs using Plotly and Dash.
  <br><br>

  ## Pictures
  ### 1. Table
  <img width="1512" alt="Screenshot 2024-03-03 at 10 00 36 AM" src="https://github.com/candycorn1546/Comparing-DB-MDL/assets/157404986/4a3937b5-1c95-4065-ae29-89f0f52c66bd">
    <br>
    
  The table shows all the information about the shows, such as DB rating, DB number of raters, MDL rating, and MDL number of raters. The table can be sorted by ascending or descending in any way the user would like. Furthermore, the user can also search for specific titles or countries based on their choice. An example: <br>
  
  <img width="1512" alt="Screenshot 2024-03-03 at 10 00 55 AM" src="https://github.com/candycorn1546/Comparing-DB-MDL/assets/157404986/d0f271b0-3f3b-4961-918b-0a7f0a150997">
   <br> <br><br> 
   
  ### 2. ScatterPlot
  <img width="1512" alt="Screenshot 2024-03-03 at 10 01 04 AM" src="https://github.com/candycorn1546/Comparing-DB-MDL/assets/157404986/7236ea33-e5d1-4dc2-893e-ca5c940efb5c"> <br>
    The scatterplot represents the rating when compared to the number of raters. The points on the plot are colour-orientated by a website, with orange being Douban and blue being MDL. If you click on an orange dot, it will redirect to the website URL with Douban or MDL, depending on the user's selection.
   <br> <br><br> 

  ### 3. Line Plot
  <img width="1507" alt="Screenshot 2024-03-03 at 10 01 12 AM" src="https://github.com/candycorn1546/Comparing-DB-MDL/assets/157404986/63b0ace6-e94d-40fc-b98a-e0f110af1b9e"> <br>
    The line plot is used for data analysis to visualize the changes in rating depending on the year. This graph also tells the story, which is already expected. MDL raters are a lot more lenient than Douban raters, who are more critical of shows.



