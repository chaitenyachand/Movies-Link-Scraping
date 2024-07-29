from imdb import IMDb  # type: ignore
import csv
import time

ia = IMDb()

def fetch_movie_details(start_id, end_id, batch_size):
    movies = []
    for movie_id in range(start_id, end_id, batch_size):
        batch_end = min(movie_id + batch_size, end_id)
        for mid in range(movie_id, batch_end):
            try:
                movie = ia.get_movie(mid)
                if 'title' in movie.keys():
                    movie_name = movie.get('title', 'N/A')
                    cover_photo = movie.get('cover url', 'N/A')
                    if not cover_photo:
                        cover_photo = movie.get('full-size cover url', 'N/A')
                    source_link = f"https://www.imdb.com/title/tt{mid:07d}/"
                    rating = movie.get('rating', 'N/A')
                    trailer_link = f"https://www.imdb.com/title/tt{mid:07d}/videogallery"
                    categories = ', '.join(movie.get('genres', []))
                    
                    movies.append([movie_name, cover_photo, source_link, rating, trailer_link, categories])
            except Exception as e:
                print(f"Error fetching movie ID {mid}: {e}")
            time.sleep(1)  # Sleep to avoid rate limits after each request
    return movies

start_id = 54110
end_id = 54111
 # Adjust this range based on requirements
batch_size = 100  # Adjust the batch size if necessary
movie_details = fetch_movie_details(start_id, end_id, batch_size)

with open('imdb_movies.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Movie Name', 'Cover Photo', 'Source Link', 'Rating', 'Trailer Link', 'Categories'])
    for details in movie_details:
        writer.writerow(details)

print("Movie details have been successfully fetched and saved to imdb_movies.csv")
