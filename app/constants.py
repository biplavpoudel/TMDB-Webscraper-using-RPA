browser_lib = [r"https://www.themoviedb.org/",False, True]
path = r"D://tmdb_webscraper/files/movies.xlsx"

movie_card_path = '//*[@id="main"]//div[@class="search_results movie "]/div/'
second_part_path = '/div[@class="title"]/div/a/'

single_movie_link = movie_card_path + '/a[@data-media-type="movie"]'
full_remaining_movie_link = '/div[@class="title"]/div/a'

certification_link = '//*[@class="certification"]'
genre_link = '//*[@class="genres"]'
storyline_link = '//*[@class="header_info"]'

review_into_view_link = '//*[@class="white_column"]/section[3]/div/h3'
actual_review_link = '//*[@class="inner_content"]/p/a'

count_of_reviews = '//*[@class="panel review"]'
single_review_link = count_of_reviews + '/div[@class="review_container"]'