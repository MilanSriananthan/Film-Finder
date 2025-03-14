import NavBar from "../components/NavBar";
import { useEffect, useState } from "react";
import api from "../api";
import { Movie } from "../types/Movie";
import MovieGrid from "../components/MovieGrid";

export default function ListWatch() {
  const [movies, setMovies] = useState<Movie[]>([]);

  useEffect(() => {
    api
      .get("/api/movies/details/?preference=watch_later")
      .then((response) => {
        setMovies(response.data); // Axios response data is stored in response.data
      })
      .catch((err) => {
        console.error("Error fetching watchlist movies:", err);
      });
  }, []);

  return (
    <>
      <NavBar />
      <div className="max-w-7xl mx-auto p-4">
        <h1 className="text-2xl font-bold text-black mb-4">
          Watch Later Movies
        </h1>
        <MovieGrid movies={movies} />
      </div>
    </>
  );
}
