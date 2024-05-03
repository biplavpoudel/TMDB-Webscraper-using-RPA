browser_lib = [r"https://www.themoviedb.org/",False, True]
path = r"D://tmdb_webscraper/files/movies.xlsx"

movie_card_path = '//*[@id="main"]//div[@class="search_results movie "]/div/'
second_part_path = 'div/div[2]/div[1]/div/div/a/'

single_movie_link = movie_card_path + '/a[@data-media-type="movie"]'
full_remaining_movie_link = 'div/div[2]/div[1]/div/div/a[@data-media-type="movie"]'

certification_link = '//*[@class="certification"]'
genre_link = '//*[@class="genres"]'
storyline_link = '//*[@class="header_info"]'

review_into_view_link = '//*[@id="media_v4"]/div/div/div[1]/div/section[3]/div/h3'
actual_review_link = '//*[@id="media_v4"]/div/div/div[1]/div/section[2]/section/div[2]/div/div/div/div/p/a'

count_of_reviews = '//*[@id="media_v4"]/div/div/div[2]/div/section'
single_review_link = count_of_reviews + '/div[@class="review_container"]'