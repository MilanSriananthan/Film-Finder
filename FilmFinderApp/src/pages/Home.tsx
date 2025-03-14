import ButtonRow from "../components/ButtonRow";
import NavBar from "../components/NavBar";
import { useState, useEffect } from "react";
import api from "../api";
import MovieCard from "../components/MovieCard";
import { Movie } from "../types/Movie";

export default function Home() {
  const [movies, setMovies] = useState<Movie[]>([]);
  const [currentMovieIndex, setCurrentMovieIndex] = useState(0);

  useEffect(() => {
    const fetchMovies = async () => {
      try {
        // Fetch top-rated movies
        const response = await api.get(`/api/movies-details/`);
        const data = response.data;
        const filteredMovies: Movie[] = data.movies;
        setMovies(filteredMovies);
        setCurrentMovieIndex(0);
      } catch (error) {
        console.error("Error fetching movies:", error);
      }
    };

    fetchMovies();
  }, []);

  const triggerRadarrRequest = async () => {
    console.log("🎯 Sending movie to Radarr...");
    try {
      await api.post("/api/add-movie/", {
        tmdbId: movies[currentMovieIndex].tmdb_id,
      });
    } catch (error) {
      console.error("Error sending movie to Radarr:", error);
    }
  };

  const nextMovie = () => {
    if (currentMovieIndex < movies.length - 1) {
      setCurrentMovieIndex(currentMovieIndex + 1);
    } else {
      console.log("🎯 End of movies reached, fetching next set...");
      setMovies([]);
    }
  };

  const saveMovieInteraction = (
    preferences: "liked" | "disliked" | "watch_later" | "not_watched"
  ) => {
    if (movies.length === 0) return;
    const movie: Movie = movies[currentMovieIndex];
    api
      .post("/api/movies/", {
        movie_details: movie.movie_id,
        preferences,
      })
      .then((res) => {
        if (res.status !== 201) alert("Failed to interact with movie.");
        else {
          if (preferences === "watch_later") {
            triggerRadarrRequest();
          }
        }
      })
      .catch((err) => alert(err));
    nextMovie();
  };

  return (
    <>
      <NavBar />
      <main className="flex min-h-screen flex-col items-center justify-center p-16 relative">
        <div className="relative w-full flex justify-center">
          <div className="max-w-md">
            <MovieCard movie={movies[currentMovieIndex]} />
          </div>
        </div>
        <div className="flex w-full max-w-lg justify-between mt-4">
          <ButtonRow interactionHandler={saveMovieInteraction} />
        </div>
      </main>
    </>
  );
}
